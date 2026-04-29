import time
import logging
from typing import Callable, Any

logger = logging.getLogger(__name__)

def retry_with_backoff(
    func: Callable[..., Any], 
    retries: int = 3, 
    backoff_factor: float = 1.5,
    initial_delay: float = 1.0,
    *args, **kwargs
) -> Any:
    """
    Executes a function with retries and exponential backoff.
    Useful for search providers or external requests.
    """
    delay = initial_delay
    for attempt in range(retries + 1):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if attempt == retries:
                logger.error(f"Failed after {retries} attempts. Last error: {str(e)}")
                raise e
            logger.warning(f"Attempt {attempt + 1} failed: {str(e)}. Retrying in {delay} seconds...")
            time.sleep(delay)
            delay *= backoff_factor
