from dotenv import load_dotenv
import os
import requests
import time
import json
from typing import Dict, Optional, Any

load_dotenv()
api_key = os.getenv('TMDB_BEARER_TOKEN')

if not api_key:
    raise ValueError("TMDB_BEARER_TOKEN is not set in the environment variables.")

class TMDBApiClient:
    """Manages TMDB API interactions and requests."""

    def __init__(self, api_key: str):
        self.base_url = "https://api.themoviedb.org/3"
        self.headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        self.rate_limit_wait = 0.26  # Adjust according to API's rate limits

    def make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """Makes API requests with rate limiting and error handling."""
        url = f"{self.base_url}{endpoint}"
        try:
            time.sleep(self.rate_limit_wait)
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {endpoint}: {e}")
            return {}

    def get_endpoints(self, movie_id: int) -> Dict[str, str]:
        """Defines the TMDB endpoints for movie data."""
        return {
            "details": f"/movie/{movie_id}",
            "credits": f"/movie/{movie_id}/credits",
            "recommendations": f"/movie/{movie_id}/recommendations",
            "watch_providers": f"/movie/{movie_id}/watch/providers"
        }

class MovieDataCollector:
    """Collects movie data using TMDBApiClient."""

    def __init__(self, api_client: TMDBApiClient, year: int = 2023, output_dir: Optional[str] = None):
        """
        Initializes the MovieDataCollector.

        Args:
            api_client (TMDBApiClient): Instance of TMDBApiClient.
            year (int): Year of movie releases to collect. Defaults to 2023.
            output_dir (Optional[str]): Directory to save collected data.
        """
        self.api_client = api_client
        self.year = year
        self.output_dir = output_dir or os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "movie_data", str(self.year)
        )
        os.makedirs(self.output_dir, exist_ok=True)

    def get_movies_by_year_batch(self, batch_size: int = 1000):
        """
        Collects all movies released in the specified year and saves them in batches.

        Args:
            batch_size (int): Number of movies per batch file. Defaults to 1000.
        """
        page = 1
        batch_number = 1
        batch_data = []

        while True:
            params = {
                "language": "en-US",
                "primary_release_year": self.year,
                "page": page,
                "sort_by": "popularity.desc"
            }
            data = self.api_client.make_request("/discover/movie", params)
            results = data.get('results', [])
            if not results:
                break
            for movie in results:
                movie_id = movie.get('id')
                if not movie_id:
                    continue
                endpoints = self.api_client.get_endpoints(movie_id)
                movie_data = {}
                for endpoint_name, endpoint in endpoints.items():
                    endpoint_data = self.api_client.make_request(endpoint)
                    movie_data[endpoint_name] = endpoint_data
                batch_data.append({movie_id: movie_data})
                if len(batch_data) >= batch_size:
                    self.save_batch_data(batch_number, batch_data)
                    batch_data = []
                    batch_number += 1
            page += 1

        # Save any remaining movies in the last batch
        if batch_data:
            self.save_batch_data(batch_number, batch_data)

    def save_batch_data(self, batch_number: int, batch_data: list):
        """
        Saves a batch of movie data to a JSON file named batch_{batch_number:03d}.json.

        Args:
            batch_number (int): The batch number for naming the file.
            batch_data (list): The list of movie data to save.
        """
        output_file_name = f"batch_{batch_number:03d}.json"
        output_file_path = os.path.join(self.output_dir, output_file_name)
        with open(output_file_path, 'w', encoding='utf-8') as f:
            json.dump(batch_data, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    # Instantiate the API client and data collector
    api_client = TMDBApiClient(api_key)
    collector = MovieDataCollector(api_client, year=2023)

    try:
        # Collect and save movie data
        collector.get_sample_movies_by_year(limit=1000)
    except Exception as e:
        print(f"An error occurred during data collection: {e}")