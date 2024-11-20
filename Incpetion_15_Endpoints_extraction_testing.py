import os
import requests
from dotenv import load_dotenv
from pprint import pprint
import time
import sys
from datetime import datetime

# Creating filename with timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_file = f"inception_data_{timestamp}.txt"

# stdout to file
sys.stdout = open(output_file, "w", encoding='utf-8')

# Load environment variables
load_dotenv()

# Setup
bearer_token = os.getenv('TMDB_BEARER_TOKEN')
headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {bearer_token}"
}
movie_id = 27205  # Inception's ID

# List of all endpoints we'll query
endpoints = {
    "details": f"/movie/{movie_id}",
    "credits": f"/movie/{movie_id}/credits",
    "keywords": f"/movie/{movie_id}/keywords",
    "reviews": f"/movie/{movie_id}/reviews",
    "similar": f"/movie/{movie_id}/similar",
    "recommendations": f"/movie/{movie_id}/recommendations",
    "videos": f"/movie/{movie_id}/videos",
    "images": f"/movie/{movie_id}/images",
    "watch_providers": f"/movie/{movie_id}/watch/providers",
    "release_dates": f"/movie/{movie_id}/release_dates",
    "translations": f"/movie/{movie_id}/translations",
    "alternative_titles": f"/movie/{movie_id}/alternative_titles",
    "lists": f"/movie/{movie_id}/lists",
    "external_ids": f"/movie/{movie_id}/external_ids",
    "changes": f"/movie/{movie_id}/changes"
}

# Function to make API calls
def get_movie_data(endpoint: str):
    url = f"https://api.themoviedb.org/3{endpoint}"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        time.sleep(0.25)  # Rate limiting
        return response.json()
    except Exception as e:
        print(f"Error fetching {endpoint}: {str(e)}")
        return None

# Collect all data
inception_data = {}
print("Fetching data from all endpoints...")
for key, endpoint in endpoints.items():
    print(f"Fetching {key}...")
    data = get_movie_data(endpoint)
    if data:
        inception_data[key] = data

# Print results by category
for category, data in inception_data.items():
    print(f"\n{'='*50}")
    print(f"\n{category.upper()}:")
    print(f"{'='*50}\n")
    pprint(data)

# Some useful summaries
print("\nKEY INFORMATION SUMMARY:")
print("="*50)

if 'details' in inception_data:
    details = inception_data['details']
    print(f"\nBasic Info:")
    print(f"- Title: {details.get('title')}")
    print(f"- Release Date: {details.get('release_date')}")
    print(f"- Runtime: {details.get('runtime')} minutes")
    print(f"- Budget: ${details.get('budget'):,}")
    print(f"- Revenue: ${details.get('revenue'):,}")
    print(f"- Rating: {details.get('vote_average')} ({details.get('vote_count')} votes)")

if 'credits' in inception_data:
    credits = inception_data['credits']
    print("\nKey People:")
    # Main cast
    print("Main Cast:")
    for actor in credits.get('cast', [])[:5]:
        print(f"- {actor['name']} as {actor['character']}")
    # Key crew
    print("\nKey Crew:")
    key_positions = ['Director', 'Producer', 'Writer', 'Director of Photography', 'Editor']
    for crew in credits.get('crew', []):
        if crew['job'] in key_positions:
            print(f"- {crew['name']} ({crew['job']})")

if 'videos' in inception_data:
    videos = inception_data['videos']
    print("\nVideos:")
    for video in videos.get('results', [])[:3]:
        print(f"- {video.get('type')}: {video.get('name')} ({video.get('site')})")

if 'reviews' in inception_data:
    reviews = inception_data['reviews']
    print("\nSample Reviews:")
    for review in reviews.get('results', [])[:2]:
        print(f"- Author: {review.get('author')}")
        print(f"  Rating: {review.get('author_details', {}).get('rating')}")
        print(f"  Excerpt: {review.get('content')[:100]}...")

if 'watch_providers' in inception_data:
    providers = inception_data['watch_providers']
    if 'results' in providers and 'US' in providers['results']:
        us_providers = providers['results']['US']
        print("\nWatch Providers (US):")
        for provider_type in ['flatrate', 'rent', 'buy']:
            if provider_type in us_providers:
                print(f"\n{provider_type.title()}:")
                for provider in us_providers[provider_type]:
                    print(f"- {provider.get('provider_name')}")