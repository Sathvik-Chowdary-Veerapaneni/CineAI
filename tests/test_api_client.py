# tests/test_api_client.py
from dotenv import load_dotenv
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Data_Collector'))
from Movie_Data_Collection_by_Year_Pipeline import TMDBApiClient

def test_api_client():
    # Setup
    load_dotenv()
    api_key = os.getenv('TMDB_BEARER_TOKEN')
    client = TMDBApiClient(api_key)
    movie_id = 27205  # Inception

    # Test 1: Initialization
    assert client.base_url == "https://api.themoviedb.org/3"
    assert client.headers["accept"] == "application/json"
    assert client.headers["Authorization"].startswith("Bearer")

    # Test 2: Basic movie request
    response = client.make_request(f"/movie/{movie_id}")
    assert response.get('title') == "Inception"
    assert response.get('id') == movie_id

    # Test 3: Multiple endpoints
    endpoints = client.get_endpoints(movie_id)
    for name, endpoint in endpoints.items():
        response = client.make_request(endpoint)
        assert response != {}

    print("All tests passed!")

if __name__ == "__main__":
    test_api_client()