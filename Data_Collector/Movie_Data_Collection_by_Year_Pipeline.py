from dotenv import load_dotenv
import os
import requests
import time
from typing import Dict, Optional

load_dotenv()
api_key = os.getenv('TMDB_BEARER_TOKEN')

class TMDBApiClient:
    """Managing TMDB API interactions and request handling"""
    
    def __init__(self, api_key: str):
        self.base_url = "https://api.themoviedb.org/3"
        self.headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        self.rate_limit_wait = 0.25

    def make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """Making API requests with rate limiting and error handling"""
        url = f"{self.base_url}{endpoint}"
        try:
            time.sleep(self.rate_limit_wait)
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching {endpoint}: {str(e)}")
            return {}

client = TMDBApiClient(api_key)

# Testing the client
if __name__ == "__main__":
    # Test initialization
    print("Base URL:", client.base_url)
    print("Headers:", client.headers)
    
    # Test API call with Inception movie ID
    response = client.make_request("/movie/27205")
    print("\nTest movie title:", response.get('title'))