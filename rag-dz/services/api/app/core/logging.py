"""
Structured Logging System with Correlation IDs
Provides distributed tracing and JSON logging for production
"""
import json
import logging
import sys
import time
import uuid
from contextvars import ContextVar
from datetime import datetime
from typing import Any, Dict, Optional
from functools import wraps

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

# Context variables for request tracking
correlation_id_var: ContextVar[str] = ContextVar("correlation_id", default="")
user_id_var: ContextVar[str] = ContextVar("user_id", default="")
tenant_id_var: ContextVar[str] = ContextVar("tenant_id", default="")
request_path_var: ContextVar[str] = ContextVar("request_path", default="")


class StructuredLogFormatter(logging.Formatter):
    """
    JSON formatter for structured logging
    Includes correlation ID, user context, and metadata
    """

    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "correlation_id": correlation_id_var.get() or None,
            "user_id": user_id_var.get() or None,
            "tenant_id": tenant_id_var.get() or None,
            "request_path": request_path_var.get() or None,
        }

        # Add location info
        if record.pathname:
            log_data["location"] = {
                "file": record.pathname.split("/")[-1],
                "line": record.lineno,
                "function": record.funcName
            }

        # Add exception info
        if record.exc_info:
            log_data["exception"] = {
                "type": record.exc_info[0].__name__ if record.exc_info[0] else None,
                "message": str(record.exc_info[1]) if record.exc_info[1] else None,
                "traceback": self.formatException(record.exc_info) if record.exc_info else None
            }

        # Add extra fields
        if hasattr(record, "extra_data"):
            log_data["extra"] = record.extra_data

        return json.dumps(log_data, ensure_ascii=False, default=str)


class HumanReadableFormatter(logging.Formatter):
    """
    Human-readable formatter for development
    """
    COLORS = {
        "DEBUG": "\033[36m",     # Cyan
        "INFO": "\033[32m",      # Green
        "WARNING": "\033[33m",   # Yellow
        "ERROR": "\033[31m",     # Red
        "CRITICAL": "\033[35m",  # Magenta
        "RESET": "\033[0m"
    }

    def format(self, record: logging.LogRecord) -> str:
        correlation_id = correlation_id_var.get()
        user_id = user_id_var.get()

        color = self.COLORS.get(record.levelname, self.COLORS["RESET"])
        reset = self.COLORS["RESET"]

        # Build context string
        context_parts = []
        if correlation_id:
            context_parts.append(f"cid={correlation_id[:8]}")
        if user_id:
            context_parts.append(f"uid={user_id[:8]}")
        context = f"[{' '.join(context_parts)}] " if context_parts else ""

        timestamp = datetime.utcnow().strftime("%H:%M:%S.%f")[:-3]

        return (
            f"{color}{timestamp} {record.levelname:8}{reset} "
            f"{context}{record.name}: {record.getMessage()}"
        )


class StructuredLogger(logging.Logger):
    """
    Extended logger with structured logging support
    """

    def _log_with_extra(self, level: int, msg: str, extra_data: Dict[str, Any] = None, **kwargs):
        """Log with extra structured data"""
        if extra_data:
            # Create a LogRecord with extra_data attribute
            extra = kwargs.get("extra", {})
            extra["extra_data"] = extra_data
            kwargs["extra"] = extra
        super()._log(level, msg, (), **kwargs)

    def debug_with_data(self, msg: str, data: Dict[str, Any] = None, **kwargs):
        self._log_with_extra(logging.DEBUG, msg, data, **kwargs)

    def info_with_data(self, msg: str, data: Dict[str, Any] = None, **kwargs):
        self._log_with_extra(logging.INFO, msg, data, **kwargs)

    def warning_with_data(self, msg: str, data: Dict[str, Any] = None, **kwargs):
        self._log_with_extra(logging.WARNING, msg, data, **kwargs)

    def error_with_data(self, msg: str, data: Dict[str, Any] = None, **kwargs):
        self._log_with_extra(logging.ERROR, msg, data, **kwargs)


class CorrelationIDMiddleware(BaseHTTPMiddleware):
    """
    Middleware to handle correlation IDs for request tracing
    """

    CORRELATION_ID_HEADER = "X-Correlation-ID"
    REQUEST_ID_HEADER = "X-Request-ID"

    async def dispatch(self, request: Request, call_next) -> Response:
        # Get or generate correlation ID
        correlation_id = (
            request.headers.get(self.CORRELATION_ID_HEADER) or
            request.headers.get(self.REQUEST_ID_HEADER) or
            str(uuid.uuid4())
        )

        # Set context variables
        correlation_id_token = correlation_id_var.set(correlation_id)
        request_path_token = request_path_var.set(f"{request.method} {request.url.path}")

        # Extract user/tenant from request state if available
        user_id_token = None
        tenant_id_token = None

        if hasattr(request.state, "user_id"):
            user_id_token = user_id_var.set(request.state.user_id)
        if hasattr(request.state, "tenant_id"):
            tenant_id_token = tenant_id_var.set(request.state.tenant_id)

        # Log request start
        start_time = time.time()
        logger = logging.getLogger("http")
        logger.info(f"Request started: {request.method} {request.url.path}")

        try:
            response = await call_next(request)

            # Log request completion
            duration_ms = (time.time() - start_time) * 1000
            logger.info(
                f"Request completed: {request.method} {request.url.path} "
                f"status={response.status_code} duration={duration_ms:.2f}ms"
            )

            # Add correlation ID to response headers
            response.headers[self.CORRELATION_ID_HEADER] = correlation_id

            return response

        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            logger.error(
                f"Request failed: {request.method} {request.url.path} "
                f"error={str(e)} duration={duration_ms:.2f}ms",
                exc_info=True
            )
            raise

        finally:
            # Reset context variables
            correlation_id_var.reset(correlation_id_token)
            request_path_var.reset(request_path_token)
            if user_id_token:
                user_id_var.reset(user_id_token)
            if tenant_id_token:
                tenant_id_var.reset(tenant_id_token)


def setup_logging(
    level: str = "INFO",
    json_format: bool = True,
    log_file: Optional[str] = None
):
    """
    Configure structured logging for the application

    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        json_format: Use JSON format (True for production, False for development)
        log_file: Optional file path for logging
    """
    # Set custom logger class
    logging.setLoggerClass(StructuredLogger)

    # Get root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, level.upper()))

    # Remove existing handlers
    root_logger.handlers.clear()

    # Create formatter
    if json_format:
        formatter = StructuredLogFormatter()
    else:
        formatter = HumanReadableFormatter()

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # File handler (if specified)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(StructuredLogFormatter())  # Always JSON for files
        root_logger.addHandler(file_handler)

    # Set levels for noisy libraries
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)

    return root_logger


def log_function_call(logger_name: str = None):
    """
    Decorator to log function calls with arguments and return values

    Usage:
        @log_function_call("my_service")
        async def my_function(arg1, arg2):
            ...
    """
    def decorator(func):
        _logger = logging.getLogger(logger_name or func.__module__)

        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            func_name = func.__name__
            _logger.debug(f"Calling {func_name} with args={args[:3]}, kwargs={list(kwargs.keys())}")

            start_time = time.time()
            try:
                result = await func(*args, **kwargs)
                duration = (time.time() - start_time) * 1000
                _logger.debug(f"{func_name} completed in {duration:.2f}ms")
                return result
            except Exception as e:
                duration = (time.time() - start_time) * 1000
                _logger.error(f"{func_name} failed after {duration:.2f}ms: {e}", exc_info=True)
                raise

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            func_name = func.__name__
            _logger.debug(f"Calling {func_name}")

            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                duration = (time.time() - start_time) * 1000
                _logger.debug(f"{func_name} completed in {duration:.2f}ms")
                return result
            except Exception as e:
                duration = (time.time() - start_time) * 1000
                _logger.error(f"{func_name} failed after {duration:.2f}ms: {e}", exc_info=True)
                raise

        import asyncio
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper

    return decorator


# Utility functions for context access
def get_correlation_id() -> str:
    """Get current correlation ID"""
    return correlation_id_var.get() or str(uuid.uuid4())


def set_user_context(user_id: str, tenant_id: str = None):
    """Set user context for logging"""
    user_id_var.set(user_id)
    if tenant_id:
        tenant_id_var.set(tenant_id)
