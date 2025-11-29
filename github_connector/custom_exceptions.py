# github_connector/custom_exceptions.py
class GitHubAPIError(Exception):
    """Base exception for GitHub API errors."""
    pass

class ResourceNotFound(GitHubAPIError):
    """Raised when a repository or resource is not found (404)."""
    pass

class MaxRetriesExceeded(GitHubAPIError):
    """Raised after max retries is reached."""
    pass
    

class JSONParseError(Exception):
    """Raised when JSON decoding fails."""
    pass


# ... add more exceptions as needed