import os
import logging
import requests
import time

from requests.exceptions import HTTPError, JSONDecodeError
from .custom_exceptions import JSONParseError, MaxRetriesExceeded, ResourceNotFound

from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class GitHubClient:
    """A resilient client for interacting with the GitHub API."""

    def __init__(self) -> None:
        """Initializes the client, loading the API key from environment variables."""
        self.api_key: str = os.getenv("GITHUB_API_KEY")
      

    def _get_headers(self) -> dict[str, str]:
        """Constructs the headers for API requests."""
        headers = {
            "Authorization": f"token {self.api_key}",       
            "Accept": "application/vnd.github+json", 
            "User-Agent": "github_connector/1.0",         
            "Content-Type": "application/json",      
            "Cache-Control": "no-cache"              
        }
        
        return headers

    def _make_request(self, method: str, endpoint: str) -> requests.Response:
        """Makes an API request with automatic retries for rate limits."""
        MAX_RETRIES = 3
        backoff_factor = 2
        
        logger.info(f"Commencing API call to {endpoint}")
        for attempt in range(MAX_RETRIES):
            logger.info(f"Attempt {attempt} initialized...")
            try:
                response = requests.request(method=method, 
                                            url=endpoint, 
                                            headers=self._get_headers())
                response.raise_for_status()
                return response
            except HTTPError as err:
                logger.warning({
                    "status": f"{err.response.status_code}",
                    "message": f"{err}. Retrying..."
                })

                if err.response.status_code in (429, 403):
                    retry_after = err.response.headers.get("Retry-After")
                    if retry_after:
                        wait = int(retry_after)
                        logger.warning(f"[GitHub] Rate limited. Waiting {wait}s ...")
                        time.sleep(wait)
                        continue
        
                    # Otherwise fall back to X-RateLimit-Reset
                    reset_at = err.response.headers.get("X-RateLimit-Reset")
                    if reset_at:
                        now = int(time.time())
                        wait = max(0, int(reset_at) - now)
                        logger.warning(f"[GitHub] Rate limit reset at {reset_at}. Waiting {wait}s ...")
                        time.sleep(wait)
                        continue 
                       
                elif err.response.status_code == 404:
                    raise ResourceNotFound(str(err))
      
                elif 500 <= err.response.status_code < 600:
                    sleep_time = backoff_factor * (2 ** attempt)
                    logger.warning(f"[GitHub] Server error {err.response.status_code}. Retrying in {sleep_time:.1f}s ...")
                    time.sleep(sleep_time)
                    continue
                        
                else:
                    sleep_time = backoff_factor * (2 ** attempt)
                    logger.warning(f"{err}. Retrying in {sleep_time:.1f}s ...")
                    time.sleep(sleep_time)
                    continue
 
                    
                        
            except requests.ConnectionError:
                sleep_time = backoff_factor * (2 ** attempt)
                logger.warning(f"Could not connect to [GitHub] Server. Retrying in {sleep_time:.1f}s ...")
                time.sleep(sleep_time)
                continue

        logger.error({
            "message": "Max retries exceeded"
        })
        
        raise MaxRetriesExceeded("An error occurred. Retry failed. Max retries exceeded.")
            

                    
    def get_repo(self, owner: str, repo: str) -> dict:
        endpoint = f"https://api.github.com/repos/{owner}/{repo}"
        
        result = self._make_request("GET", endpoint)
        
        logger.info("Converting JSON to python dict")
        try:
            data = result.json()
        except JSONDecodeError as err:
            logger.error({
                "message": str(err)
            })
            raise JSONParseError(str(err))
            
        return data

            
        
        
        
    def get_latest_release(self, owner: str, repo: str) -> dict:
        endpoint = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
        
        result = self._make_request("GET", endpoint)
        
        logger.info("Converting JSON to python dict")
        try:
            data = result.json()
        except JSONDecodeError as err:
            logger.error({
                "message": str(err)
            })
            raise JSONParseError(str(err))
            
        return data
        
        