import os
import requests
from dotenv import load_dotenv
from pprint import pprint  # for better formatted output

# Load environment variables
load_dotenv()

# Fetch the Bearer token from environment variables
bearer_token = os.getenv('TMDB_BEARER_TOKEN')

# Configure headers with the Bearer token
headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {bearer_token}"
}

# Method 1: Search for Inception
search_url = "https://api.themoviedb.org/3/search/movie"
search_params = {
    "query": "Inception",
    "language": "en-US"
}

search_response = requests.get(search_url, headers=headers, params=search_params)
search_results = search_response.json()

# Get Inception's ID from search results
inception_id = None
for movie in search_results.get('results', []):
    if movie['title'] == "Inception":
        inception_id = movie['id']
        break

# Method 2: Use known ID directly
inception_id = 27205  # This is Inception's actual TMDB ID

# Get detailed movie information
movie_url = f"https://api.themoviedb.org/3/movie/{inception_id}"
movie_response = requests.get(movie_url, headers=headers)
movie_details = movie_response.json()

# Get credits (cast and crew)
credits_url = f"https://api.themoviedb.org/3/movie/{inception_id}/credits"
credits_response = requests.get(credits_url, headers=headers)
credits = credits_response.json()

# Get keywords
keywords_url = f"https://api.themoviedb.org/3/movie/{inception_id}/keywords"
keywords_response = requests.get(keywords_url, headers=headers)
keywords = keywords_response.json()

# Print all information
print("\nMovie Details:")
pprint(movie_details)

print("\nCast (first 5):")
for actor in credits['cast'][:5]:
    print(f"- {actor['name']} as {actor['character']}")

print("\nKey Crew Members:")
for crew in credits['crew']:
    if crew['job'] in ['Director', 'Producer', 'Writer']:
        print(f"- {crew['name']} ({crew['job']})")

print("\nKeywords:")
for keyword in keywords['keywords']:
    print(f"- {keyword['name']}")