"""Custom error classes for backend error handling"""

class NetworkError(Exception):
    """Raised when network-related operations fail"""
    def __init__(self, message="Network operation failed"):
        self.message = message
        super().__init__(self.message)

class ValidationError(Exception):
    """Raised when input validation fails"""
    def __init__(self, message="Validation failed"):
        self.message = message
        super().__init__(self.message)

class TimeoutError(Exception):
    """Raised when an operation times out"""
    def __init__(self, message="Operation timed out"):
        self.message = message
        super().__init__(self.message)