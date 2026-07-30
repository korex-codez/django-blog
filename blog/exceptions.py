class BlogException(Exception):
    """Base exception for blog app"""
    pass

class PostNotFoundError(BlogException):
    """Raised when a post is not found"""
    pass

class CommentNotFoundError(BlogException):
    """Raised when a comment is not found"""
    pass

class UserNotAuthorizedError(BlogException):
    """Raised when a user is not authorized"""
    pass

class InvalidRequestError(BlogException):
    """Raised when a request is invalid"""
    pass

class EmailSendingError(BlogException):
    """Raised when email sending fails"""
    pass

class ImageProcessingError(BlogException):
    """Raised when image processing fails"""
    pass

class NewsletterSubscriptionError(BlogException):
    """Raised when newsletter subscription fails"""
    pass