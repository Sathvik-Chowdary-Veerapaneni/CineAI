from dotenv import load_dotenv
import os
import requests
import time
import json
from typing import Dict, Optional
import threading
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
import sys

# Set up logging to a file to avoid interfering with tqdm
logging.basicConfig(
    level=logging.INFO,
    filename='data_collection.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

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
        self.session = requests.Session()
        from urllib3.util.retry import Retry  # Import Retry here

        retries = Retry(
            total=5,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"]
        )
        adapter = requests.adapters.HTTPAdapter(max_retries=retries)
        self.session.mount('https://', adapter)
        self.session.mount('http://', adapter)

    def make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """Makes API requests with rate limiting and error handling."""
        url = f"{self.base_url}{endpoint}"
        try:
            time.sleep(self.rate_limit_wait)
            response = self.session.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            # Log errors to the log file
            logger.error(f"Error fetching {endpoint}: {e}")
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
        # Fetch the first page to get total_pages
        params = {
            "language": "en-US",
            "primary_release_year": self.year,
            "page": 1,
            "sort_by": "popularity.desc"
        }
        data = self.api_client.make_request("/discover/movie", params)
        total_pages = data.get('total_pages', 1)
        page = 1
        batch_number = 1
        batch_data = []
        batches_to_filter = []

        # Use tqdm for the progress bar
        with tqdm(total=total_pages, desc="Fetching movies", ncols=80, dynamic_ncols=True) as pbar:
            while page <= total_pages:
                params['page'] = page
                data = self.api_client.make_request("/discover/movie", params)
                results = data.get('results', [])
                if not results:
                    break

                # Use ThreadPoolExecutor to fetch movie data concurrently
                with ThreadPoolExecutor(max_workers=10) as executor:
                    future_to_movie = {
                        executor.submit(self.fetch_movie_data, movie): movie for movie in results
                    }
                    for future in as_completed(future_to_movie):
                        movie_data = future.result()
                        if movie_data:
                            batch_data.append(movie_data)
                            if len(batch_data) >= batch_size:
                                batch_file_name = self.save_batch_data(batch_number, batch_data)
                                batches_to_filter.append(batch_file_name)
                                batch_data = []
                                batch_number += 1

                                # Trigger filtering after every 2 batches
                                if len(batches_to_filter) >= 2:
                                    self.trigger_filtering(batches_to_filter.copy())
                                    batches_to_filter.clear()

                page += 1
                pbar.update(1)  # Update progress bar

        # Save any remaining movies
        if batch_data:
            batch_file_name = self.save_batch_data(batch_number, batch_data)
            batches_to_filter.append(batch_file_name)

        # Trigger filtering for any remaining batches
        if batches_to_filter:
            self.trigger_filtering(batches_to_filter.copy())

    def fetch_movie_data(self, movie):
        movie_id = movie.get('id')
        if not movie_id:
            return None
        endpoints = self.api_client.get_endpoints(movie_id)
        movie_data = {}
        for endpoint_name, endpoint in endpoints.items():
            endpoint_data = self.api_client.make_request(endpoint)
            movie_data[endpoint_name] = endpoint_data
        return {movie_id: movie_data}

    def save_batch_data(self, batch_number: int, batch_data: list) -> str:
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
        # Use tqdm.write to print without disrupting the progress bar
        tqdm.write(f"Saved batch {batch_number} with {len(batch_data)} movies.")
        # Also log the event
        logger.info(f"Saved batch {batch_number} with {len(batch_data)} movies.")
        return output_file_name  # Return the file name for filtering

    def trigger_filtering(self, batch_file_names):
        filter_thread = threading.Thread(target=run_filtering, args=(batch_file_names,))
        filter_thread.start()

def run_filtering(batch_file_names):
    from filter_movie_data import DataFilter  # Import the filtering module

    input_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "movie_data", str(2023))
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "filtered_data", str(2023))

    data_filter = DataFilter(input_dir, output_dir)
    data_filter.process_batch_files(batch_file_names)

if __name__ == "__main__":
    # Instantiate the API client and data collector
    api_client = TMDBApiClient(api_key)
    collector = MovieDataCollector(api_client, year=2023)

    try:
        # Collect and save movie data
        collector.get_movies_by_year_batch(batch_size=1000)
    except Exception as e:
        logger.error(f"An error occurred during data collection: {e}")
        # Use tqdm.write to print the error without disrupting the progress bar
        tqdm.write(f"An error occurred during data collection: {e}")
