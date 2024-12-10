# tests/test_api_client.py
from dotenv import load_dotenv
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Data_Collector'))
from data_pipeline_movies_collection_TMDB_API.data_collection_pipeline_JSON_4_Endpoints import TMDBApiClient

# variables setup
load_dotenv()
api_key = os.getenv('TMDB_BEARER_TOKEN')
client = TMDBApiClient(api_key)
movie_id = 27205  # Inception
    
def test_intialization():
    assert client.base_url == "https://api.themoviedb.org/3"
    assert client.headers["accept"] == "application/json"
    assert client.headers["Authorization"].startswith("Bearer")

def test_movie_request():
    response = client.make_request(f"/movie/{movie_id}")
    assert response.get('title') == "Inception"
    assert response.get('id') == movie_id

def testing_15_endpoints():
    endpoints = client.get_endpoints(movie_id)
    for name, endpoint in endpoints.items():
        response = client.make_request(endpoint)
        assert response != {}

if __name__ == "__main__":
    test_intialization()
    test_movie_request()
    testing_15_endpoints()
    print("All tests passed!")