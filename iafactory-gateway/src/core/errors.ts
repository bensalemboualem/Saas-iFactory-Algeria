import { FastifyError, FastifyRequest, FastifyReply } from 'fastify';

export class GatewayError extends Error {
  constructor(
    public code: string,
    message: string,
    public statusCode: number = 400,
    public details?: any
  ) {
    super(message);
    this.name = 'GatewayError';
  }
}

export const errorHandler = async (
  error: FastifyError | GatewayError,
  request: FastifyRequest,
  reply: FastifyReply
) => {
  request.log.error(error);

  if (error instanceof GatewayError) {
    return reply.status(error.statusCode).send({
      error: {
        code: error.code,
        message: error.message,
        details: error.details,
      },
    });
  }

  // Map common error codes
  const statusCode = error.statusCode || 500;
  const errorCode = mapErrorCode(error);

  return reply.status(statusCode).send({
    error: {
      code: errorCode,
      message: error.message || 'Internal server error',
    },
  });
};

function mapErrorCode(error: any): string {
  if (error.code === 'FST_JWT_AUTHORIZATION_TOKEN_INVALID') return 'UNAUTHORIZED';
  if (error.code === 'FST_ERR_VALIDATION') return 'INVALID_REQUEST';
  if (error.statusCode === 429) return 'RATE_LIMIT_EXCEEDED';
  return 'INTERNAL_ERROR';
}
