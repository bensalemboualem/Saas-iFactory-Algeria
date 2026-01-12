"""
User Repository - Database operations
"""
from typing import Optional
from datetime import datetime
import logging

from app.db import get_db_connection
from app.models.user import UserCreate, UserInDB
from app.services.auth_service import auth_service

logger = logging.getLogger(__name__)


class UserRepository:
    """Repository for user database operations"""

    def create_user(self, user: UserCreate) -> UserInDB:
        """
        Create a new user in the database

        Args:
            user: User creation data

        Returns:
            Created user with ID

        Raises:
            Exception: If user already exists or creation fails
        """
        # Hash password
        hashed_password = auth_service.get_password_hash(user.password)

        query = """
            INSERT INTO users (email, full_name, hashed_password, is_active, is_superuser, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id, email, full_name, hashed_password, is_active, is_superuser, created_at, updated_at
        """

        now = datetime.utcnow()

        try:
            with get_db_connection() as conn, conn.cursor() as cur:
                cur.execute(
                    query,
                    (user.email,
                    user.full_name,
                    hashed_password,
                    user.is_active,
                    user.is_superuser,
                    now,
                    now)
                )

                row = cur.fetchone()

                logger.info(f"User created: {user.email}")

                return UserInDB(
                    id=row[0],
                    email=row[1],
                    full_name=row[2],
                    hashed_password=row[3],
                    is_active=row[4],
                    is_superuser=row[5],
                    created_at=row[6],
                    updated_at=row[7]
                )

        except Exception as e:
            if "duplicate key" in str(e).lower() or "unique" in str(e).lower():
                logger.error(f"User already exists: {user.email}")
                raise Exception("User with this email already exists")
            raise

    def get_user_by_email(self, email: str) -> Optional[UserInDB]:
        """
        Get user by email

        Args:
            email: User email address

        Returns:
            User if found, None otherwise
        """
        query = """
            SELECT id, email, full_name, hashed_password, is_active, is_superuser, created_at, updated_at
            FROM users
            WHERE email = %s
        """

        with get_db_connection() as conn, conn.cursor() as cur:
            cur.execute(query, (email,))
            row = cur.fetchone()

            if not row:
                return None

            return UserInDB(
                id=row[0],
                email=row[1],
                full_name=row[2],
                hashed_password=row[3],
                is_active=row[4],
                is_superuser=row[5],
                created_at=row[6],
                updated_at=row[7]
            )

    def get_user_by_id(self, user_id: int) -> Optional[UserInDB]:
        """
        Get user by ID

        Args:
            user_id: User ID

        Returns:
            User if found, None otherwise
        """
        query = """
            SELECT id, email, full_name, hashed_password, is_active, is_superuser, created_at, updated_at
            FROM users
            WHERE id = %s
        """

        with get_db_connection() as conn, conn.cursor() as cur:
            cur.execute(query, (user_id,))
            row = cur.fetchone()

            if not row:
                return None

            return UserInDB(
                id=row[0],
                email=row[1],
                full_name=row[2],
                hashed_password=row[3],
                is_active=row[4],
                is_superuser=row[5],
                created_at=row[6],
                updated_at=row[7]
            )

    def authenticate_user(self, email: str, password: str) -> Optional[UserInDB]:
        """
        Authenticate user with email and password

        Args:
            email: User email
            password: Plain text password

        Returns:
            User if authentication succeeds, None otherwise
        """
        user = self.get_user_by_email(email)

        if not user:
            logger.warning(f"Authentication failed - user not found: {email}")
            return None

        if not auth_service.verify_password(password, user.hashed_password):
            logger.warning(f"Authentication failed - wrong password: {email}")
            return None

        if not user.is_active:
            logger.warning(f"Authentication failed - user inactive: {email}")
            return None

        logger.info(f"User authenticated successfully: {email}")
        return user


# Global instance
user_repository = UserRepository()
