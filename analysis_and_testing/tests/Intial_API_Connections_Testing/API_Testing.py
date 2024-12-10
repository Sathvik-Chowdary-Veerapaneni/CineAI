import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Fetch the Bearer token from environment variables
bearer_token = os.getenv('TMDB_BEARER_TOKEN')

# Debug print to check what is being loaded from the environment
print("Loaded Bearer token from env:", bearer_token)

# URL for fetching popular movies
url = "https://api.themoviedb.org/3/movie/popular?language=en-US&page=1"

# Configure headers with the Bearer token
headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {bearer_token}"
}

# Make the request
response = requests.get(url, headers=headers)

# Print the status code and response text to check if access is working
print("Status Code:", response.status_code)
print("Response Content:", response.text)
