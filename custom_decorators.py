import time
import functools
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def retry(max_attempts, delay_seconds):
    """
    A custom decorator to retry a function up to a maximum number of attempts
    with a specified delay between attempts.

    :param max_attempts: The maximum number of times to attempt the function call.
    :param delay_seconds: The delay in seconds between each retry attempt.
    """
    def decorator_retry(func):
        @functools.wraps(func)
        def wrapper_retry(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    logging.info(f"Attempt {attempt}/{max_attempts}: Executing '{func.__name__}'")
                  
                    return func(*args, **kwargs)
                except AssertionError as e:
                    logging.warning(f"Attempt {attempt}/{max_attempts} failed: {e}")
                    if attempt < max_attempts:
                        logging.info(f"Retrying in {delay_seconds} seconds...")
                        time.sleep(delay_seconds)
                    else:
                        logging.error(f"All {max_attempts} attempts failed for '{func.__name__}'.")
                        raise
                except Exception as e:
                    logging.error(f"An unexpected error occurred during '{func.__name__}': {e}")
                    raise

        return wrapper_retry
    return decorator_retry
