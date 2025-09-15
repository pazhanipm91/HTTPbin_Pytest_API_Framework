import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

class Config:
    # Base URL for the API
    BASE_URL = "https://httpbin.org"

    # Retry configs
    RETRY_ATTEMPTS = 3
    RETRY_DELAY_SECONDS = 2
