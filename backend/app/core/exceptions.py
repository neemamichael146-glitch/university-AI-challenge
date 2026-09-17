class ChuoAIException(Exception):
    def __init__(self, message: str, status_code: int = 500, error_code: str = "INTERNAL_ERROR"):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        super().__init__(self.message)


class NotFoundException(ChuoAIException):
    def __init__(self, resource: str, identifier: str = ""):
        message = f"{resource} not found"
        if identifier:
            message += f": {identifier}"
        super().__init__(message, status_code=404, error_code="NOT_FOUND")


class ValidationException(ChuoAIException):
    def __init__(self, message: str, details: dict = None):
        super().__init__(message, status_code=422, error_code="VALIDATION_ERROR")
        self.details = details or {}


class UnauthorizedException(ChuoAIException):
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(message, status_code=401, error_code="UNAUTHORIZED")


class ForbiddenException(ChuoAIException):
    def __init__(self, message: str = "Forbidden"):
        super().__init__(message, status_code=403, error_code="FORBIDDEN")


class ConflictException(ChuoAIException):
    def __init__(self, message: str):
        super().__init__(message, status_code=409, error_code="CONFLICT")


class RateLimitException(ChuoAIException):
    def __init__(self, message: str = "Rate limit exceeded"):
        super().__init__(message, status_code=429, error_code="RATE_LIMIT")


class AIProviderException(ChuoAIException):
    def __init__(self, message: str, provider: str = ""):
        full_message = f"AI Provider error"
        if provider:
            full_message += f" ({provider})"
        full_message += f": {message}"
        super().__init__(full_message, status_code=503, error_code="AI_PROVIDER_ERROR")


class DatabaseException(ChuoAIException):
    def __init__(self, message: str):
        super().__init__(message, status_code=500, error_code="DATABASE_ERROR")