from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_403_FORBIDDEN

class ChamaException(HTTPException):
    """Base exception for the application"""
    pass

class InsufficientBalance(ChamaException):
    def __init__(self, detail: str = "Insufficient balance"):
        super().__init__(status_code=HTTP_400_BAD_REQUEST, detail=detail)

class NotEligibleForLoan(ChamaException):
    def __init__(self, detail: str = "You are not eligible for this loan"):
        super().__init__(status_code=HTTP_400_BAD_REQUEST, detail=detail)

class BookingConflict(ChamaException):
    def __init__(self, detail: str = "Equipment booking conflict"):
        super().__init__(status_code=HTTP_400_BAD_REQUEST, detail=detail)

class InvalidMpesaTransaction(ChamaException):
    def __init__(self, detail: str = "Invalid M-Pesa transaction"):
        super().__init__(status_code=HTTP_400_BAD_REQUEST, detail=detail)

class ResourceNotFound(ChamaException):
    def __init__(self, resource: str = "Resource"):
        super().__init__(status_code=HTTP_404_NOT_FOUND, detail=f"{resource} not found")

class PermissionDenied(ChamaException):
    def __init__(self, detail: str = "Permission denied"):
        super().__init__(status_code=HTTP_403_FORBIDDEN, detail=detail)