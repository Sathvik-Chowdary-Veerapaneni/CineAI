import os
import json
import requests
from dotenv import load_dotenv
import time

# Setting up environment and authentication
load_dotenv()
bearer_token = os.getenv('TMDB_BEARER_TOKEN')
headers = {
   "accept": "application/json",
   "Authorization": f"Bearer {bearer_token}"
}

# Using Inception movie ID for data collection
movie_id = 27205  # Inception

# Defining endpoints for complete movie information
endpoints = {
   "details": f"/movie/{movie_id}",          # Basic movie information
   "credits": f"/movie/{movie_id}/credits",   # Cast and crew details
   "keywords": f"/movie/{movie_id}/keywords", # Movie themes and topics
   "reviews": f"/movie/{movie_id}/reviews",   # User and critic reviews
   "similar": f"/movie/{movie_id}/similar",   # Similar movie suggestions
   "recommendations": f"/movie/{movie_id}/recommendations", # Movie recommendations
   "videos": f"/movie/{movie_id}/videos",     # Trailers and video content
   "images": f"/movie/{movie_id}/images",     # Movie posters and backdrops
   "watch_providers": f"/movie/{movie_id}/watch/providers", # Streaming availability
   "release_dates": f"/movie/{movie_id}/release_dates",    # Global release dates
   "translations": f"/movie/{movie_id}/translations",       # Language versions
   "alternative_titles": f"/movie/{movie_id}/alternative_titles", # Regional titles
   "lists": f"/movie/{movie_id}/lists",       # Featured movie lists
   "external_ids": f"/movie/{movie_id}/external_ids",      # Platform identifiers
   "changes": f"/movie/{movie_id}/changes"    # Data update history
}

# Collecting data from all endpoints
inception_data = {}
for key, endpoint in endpoints.items():
   print(f"Fetching {key} data...")
   url = f"https://api.themoviedb.org/3{endpoint}"
   response = requests.get(url, headers=headers)
   if response.status_code == 200:
       inception_data[key] = response.json()
   time.sleep(0.25)  # Adding delay for rate limit compliance

# Saving collected data to JSON format
output_file = f"inception_{movie_id}_Json_File.json"
with open(output_file, 'w', encoding='utf-8') as f:
   json.dump(inception_data, f, ensure_ascii=False, indent=2)

print(f"Successfully saved complete data to {output_file}")