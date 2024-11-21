from dotenv import load_dotenv
import os
import requests
import time
from typing import Dict, Optional

load_dotenv()
api_key = os.getenv('TMDB_BEARER_TOKEN')

class TMDBApiClient:
    """ Managing TMDB API interactions and requests """
    
    def __init__(self, api_key: str):
        self.base_url = "https://api.themoviedb.org/3"
        self.headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        self.rate_limit_wait = 0.25

    def make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """ Making API requests with rate limiting and error handling """
        url = f"{self.base_url}{endpoint}"
        try:
            time.sleep(self.rate_limit_wait)
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching {endpoint}: {str(e)}")
            return {}
    
    def get_endpoints(self, movie_id: int) -> Dict[str, str]:
        """ TMDB endpoints for a movie data """
        
        return {
            "details": f"/movie/{movie_id}",
            "credits": f"/movie/{movie_id}/credits",
            "keywords": f"/movie/{movie_id}/keywords",
            "reviews": f"/movie/{movie_id}/reviews",
            "similar": f"/movie/{movie_id}/similar",
            "recommendations": f"/movie/{movie_id}/recommendations"
        }

client = TMDBApiClient(api_key)