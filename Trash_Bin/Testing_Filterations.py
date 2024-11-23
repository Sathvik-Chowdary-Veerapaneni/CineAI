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
            "keywords": f"/movie/{movie_id}/keywords",
            "reviews": f"/movie/{movie_id}/reviews",
            "similar": f"/movie/{movie_id}/similar",
            "recommendations": f"/movie/{movie_id}/recommendations",
            # "videos": f"/movie/{movie_id}/videos",
            # "images": f"/movie/{movie_id}/images",
            "watch_providers": f"/movie/{movie_id}/watch/providers",
            "release_dates": f"/movie/{movie_id}/release_dates",
            "translations": f"/movie/{movie_id}/translations",
            # "alternative_titles": f"/movie/{movie_id}/alternative_titles",
            "lists": f"/movie/{movie_id}/lists",
            # "external_ids": f"/movie/{movie_id}/external_ids",
            "changes": f"/movie/{movie_id}/changes"
        }

class MovieDataCollector:
    """Collects movie data using TMDBApiClient."""

    def __init__(self, api_client: TMDBApiClient, year: int = 2023, output_dir: Optional[str] = None):
        """
        Initializes the MovieDataCollector.

        Args:
            api_client (TMDBApiClient): Instance of TMDBApiClient.
            year (int): Year of movie releases to collect. Defaults to 2023.
            output_dir (Optional[str]): Directory to save collected data. Defaults to 'movie_data/<year>/'.
        """
        self.api_client = api_client
        self.year = year
        self.output_dir = output_dir or os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "movie_data", str(self.year)
        )
        os.makedirs(self.output_dir, exist_ok=True)

    def get_sample_movies_by_year(self, limit: int = 50, batch_size: int = 10):
        """
        Gets a sample of movies released in the specified year and saves them in batches.

        Args:
            limit (int): Total number of movies to fetch. Defaults to 50.
            batch_size (int): Number of movies per batch. Defaults to 10.
        """
        movies = []
        page = 1
        collected = 0
        batch_number = 1

        while collected < limit:
            params = {
                "primary_release_year": self.year,
                "sort_by": "popularity.desc",
                "page": page
            }
            response = self.api_client.make_request("/discover/movie", params=params)
            if not response.get('results'):
                print(f"No results returned for page {page}.")
                break

            results = response['results']
            total_pages = response.get('total_pages', page)

            for movie in results:
                if collected >= limit:
                    break
                movie_id = movie.get('id')
                if not movie_id:
                    print("A movie without 'id' encountered. Skipping.")
                    continue

                # Collect data for the movie
                batch_data = {}
                print(f"Collecting data for movie ID {movie_id}")
                endpoints = self.api_client.get_endpoints(movie_id)
                batch_data[movie_id] = {}
                for name, endpoint in endpoints.items():
                    data = self.api_client.make_request(endpoint)
                    if not data:
                        print(f"No data returned for endpoint {endpoint}.")
                        continue
                    batch_data[movie_id][name] = data

                movies.append(batch_data)
                collected += 1

                # When batch is full, save it and reset
                if len(movies) % batch_size == 0 or collected == limit:
                    self.save_batch(movies, batch_number)
                    batch_number += 1
                    movies = []

            if page >= total_pages:
                break
            page += 1

        # Save any remaining movies as the last batch
        if movies:
            self.save_batch(movies, batch_number)

    def save_batch(self, batch_data: list, batch_number: int):
        """
        Saves a batch of movie data to a JSON file.

        Args:
            batch_data (list): A list of movie data dictionaries.
            batch_number (int): The batch number for naming the file.
        """
        filename = f"batch_{batch_number:03d}.json"
        file_path = os.path.join(self.output_dir, filename)

        try:
            with open(file_path, 'w') as f:
                json.dump(batch_data, f, indent=2)
            print(f"Batch {batch_number} saved to {file_path}")
        except IOError as e:
            print(f"Failed to write batch {batch_number} to {file_path}: {e}")

if __name__ == "__main__":
    # Instantiate the API client and data collector
    api_client = TMDBApiClient(api_key)
    collector = MovieDataCollector(api_client, year=2023)

    try:
        # Collect and save movie data in batches
        collector.get_sample_movies_by_year(limit=10, batch_size=5)
    except Exception as e:
        print(f"An error occurred during data collection: {e}")