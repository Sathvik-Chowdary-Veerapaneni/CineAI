from Data_Collection.Movie_Data_Collection_by_Year_Pipeline import TMDB_API_Client
from dotenv import load_dotenv
import os

load_dotenv()
test_api_key=os.getenv('TMDB_BEARER_TOKEN')


def test_api_client(test_api_key):
    client = TMDB_API_Client(test_api_key)

       # Test base URL
    assert client.base_url == "https://api.themoviedb.org/3"
   
    # Test headers
    assert client.headers["accept"] == "application/json"
    assert client.headers["Authorization"] == f"Bearer {test_api_key}"

    print("All initialization tests passed!")


if __name__ == "__main__":
    test_api_client(test_api_key)