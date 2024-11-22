import os
import json
import pytest
from typing import Any

def test_filter_details_from_batch():
    # Define the path to your batch file
    batch_file_path = os.path.join('2023', 'batch_001.json')

    # Load the batch data
    with open(batch_file_path, 'r', encoding='utf-8') as f:
        batch_data = json.load(f)

    # Extract the "details" endpoint data
    movies_details = []

    for movie_data in batch_data:
        for movie_id, endpoints_data in movie_data.items():
            details_data = endpoints_data.get('details')
            if details_data:
                movies_details.append({
                    'movie_id': movie_id,
                    'details': details_data
                })
            else:
                print(f"Details data not found for movie ID {movie_id}")

def test_filter_credits_from_batch():
    # Define the path to your batch file
    batch_file_path = os.path.join('2023', 'batch_001.json')

    # Load the batch data
    with open(batch_file_path, 'r', encoding='utf-8') as f:
        batch_data = json.load(f)

    # Extract the "credits" endpoint data
    movies_credits = []

    for movie_data in batch_data:
        for movie_id, endpoints_data in movie_data.items():
            credits_data = endpoints_data.get('credits')
            if credits_data:
                movies_credits.append({
                    'movie_id': movie_id,
                    'credits': credits_data
                })
            else:
                print(f"Credits data not found for movie ID {movie_id}")

    # Define the fields to retain
    FIELDS_TO_RETAIN_CREDITS = {
        "cast": [
            {
                "name": None,
                "character": None
            }
        ],
        "crew": [
            {
                "name": None,
                "job": None
            }
        ]
    }

    # Define the filter_fields function (or import it if it's in your module)
    def filter_fields(data: Any, fields: Any) -> Any:
        """Recursively filter the data to retain only specified fields."""
        if isinstance(data, dict) and isinstance(fields, dict):
            filtered_data = {}
            for key, value in fields.items():
                if key in data:
                    if isinstance(value, (dict, list)):
                        filtered_data[key] = filter_fields(data[key], value)
                    else:
                        filtered_data[key] = data[key]
            return filtered_data
        elif isinstance(data, list) and isinstance(fields, list):
            item_fields = fields[0] if fields else None
            return [filter_fields(item, item_fields) for item in data if isinstance(item, dict)]
        else:
            return data

    # Create test_output directory if it doesn't exist
    output_dir = os.path.join(os.path.dirname(__file__), 'test_output')
    os.makedirs(output_dir, exist_ok=True)

    # Apply the filter_fields function and save filtered data
    for movie in movies_credits:
        movie_id = movie['movie_id']
        credits_data = movie['credits']
        filtered_credits = filter_fields(credits_data, FIELDS_TO_RETAIN_CREDITS)

        # Process to retain only directors from crew
        directors = [member for member in filtered_credits.get('crew', []) if member.get('job') == 'Director']
        directors = [{'name': director['name']} for director in directors if 'name' in director]

        # Update the filtered credits data
        filtered_credits['director'] = directors
        # Remove the 'crew' key as we have extracted the directors
        filtered_credits.pop('crew', None)

        # Save the filtered data to the specified directory
        output_file_name = f"{movie_id}_credits.json"
        output_file_path = os.path.join(output_dir, output_file_name)
        with open(output_file_path, 'w', encoding='utf-8') as f:
            json.dump(filtered_credits, f, indent=2, ensure_ascii=False)

        # Verify that the filtered data contains 'cast' and 'director' keys
        actual_keys = set(filtered_credits.keys())
        expected_keys = {'cast', 'director'}
        assert actual_keys == expected_keys, f"Mismatch in keys for movie ID {movie_id}: expected {expected_keys}, got {actual_keys}"

        # Verify that cast members contain only 'name' and 'character' keys
        for cast_member in filtered_credits.get('cast', []):
            cast_keys = set(cast_member.keys())
            assert cast_keys == {'name', 'character'}, f"Cast member keys mismatch for movie ID {movie_id}: expected {{'name', 'character'}}, got {cast_keys}"

        # Verify that directors contain only 'name' key
        for director in filtered_credits.get('director', []):
            director_keys = set(director.keys())
            assert director_keys == {'name'}, f"Director keys mismatch for movie ID {movie_id}: expected {{'name'}}, got {director_keys}"

    print("All tests passed for filtering credits from batch.")

def test_filter_recommendations_from_batch():
    # Define the path to your batch file
    batch_file_path = os.path.join('2023', 'batch_001.json')

    # Load the batch data
    with open(batch_file_path, 'r', encoding='utf-8') as f:
        batch_data = json.load(f)

    # Extract the "recommendations" endpoint data
    movies_recommendations = []

    for movie_data in batch_data:
        for movie_id, endpoints_data in movie_data.items():
            recommendations_data = endpoints_data.get('recommendations')
            if recommendations_data:
                movies_recommendations.append({
                    'movie_id': movie_id,
                    'recommendations': recommendations_data
                })
            else:
                print(f"Recommendations data not found for movie ID {movie_id}")

    # Define the fields to retain
    FIELDS_TO_RETAIN_RECOMMENDATIONS = {
        "results": [
            {
                "id": None,
                "title": None,
                "popularity": None,
                "genre_ids": None
            }
        ]
    }

    # Define the filter_fields function (or import it if it's in your module)
    def filter_fields(data: Any, fields: Any) -> Any:
        """Recursively filter the data to retain only specified fields."""
        if isinstance(data, dict) and isinstance(fields, dict):
            filtered_data = {}
            for key, value in fields.items():
                if key in data:
                    if isinstance(value, (dict, list)):
                        filtered_data[key] = filter_fields(data[key], value)
                    else:
                        filtered_data[key] = data[key]
            return filtered_data
        elif isinstance(data, list) and isinstance(fields, list):
            item_fields = fields[0] if fields else None
            return [filter_fields(item, item_fields) for item in data if isinstance(item, dict)]
        else:
            return data

    # Create test_output directory if it doesn't exist
    output_dir = os.path.join(os.path.dirname(__file__), 'test_output')
    os.makedirs(output_dir, exist_ok=True)

    # Apply the filter_fields function and save filtered data
    for movie in movies_recommendations:
        movie_id = movie['movie_id']
        recommendations_data = movie['recommendations']
        filtered_recommendations = filter_fields(recommendations_data, FIELDS_TO_RETAIN_RECOMMENDATIONS)

        # Save the filtered data to the specified directory
        output_file_name = f"{movie_id}_recommendations.json"
        output_file_path = os.path.join(output_dir, output_file_name)
        with open(output_file_path, 'w', encoding='utf-8') as f:
            json.dump(filtered_recommendations, f, indent=2, ensure_ascii=False)

        # Verify that the filtered data contains only 'results' key
        actual_keys = set(filtered_recommendations.keys())
        expected_keys = {'results'}
        assert actual_keys == expected_keys, f"Mismatch in keys for movie ID {movie_id}: expected {expected_keys}, got {actual_keys}"

        # Verify that each recommendation contains only the specified keys
        for result in filtered_recommendations.get('results', []):
            result_keys = set(result.keys())
            expected_result_keys = {'id', 'title', 'popularity', 'genre_ids'}
            assert result_keys == expected_result_keys, f"Recommendation keys mismatch for movie ID {movie_id}: expected {expected_result_keys}, got {result_keys}"

    print("All tests passed for filtering recommendations from batch.")

def test_filter_watch_providers_from_batch():
    # Define the path to your batch file
    batch_file_path = os.path.join('2023', 'batch_001.json')

    # Load the batch data
    with open(batch_file_path, 'r', encoding='utf-8') as f:
        batch_data = json.load(f)

    # Extract the "watch_providers" endpoint data
    movies_watch_providers = []

    for movie_data in batch_data:
        for movie_id, endpoints_data in movie_data.items():
            watch_providers_data = endpoints_data.get('watch_providers')
            if watch_providers_data:
                movies_watch_providers.append({
                    'movie_id': movie_id,
                    'watch_providers': watch_providers_data
                })
            else:
                print(f"Watch providers data not found for movie ID {movie_id}")

    # Define the fields to retain
    FIELDS_TO_RETAIN_WATCH_PROVIDERS = {
        "results": {
            "US": {
                "flatrate": [
                    {
                        "provider_name": None
                    }
                ]
            }
        }
    }

    # Define the filter_fields function (or import it if it's in your module)
    def filter_fields(data: Any, fields: Any) -> Any:
        """Recursively filter the data to retain only specified fields."""
        if isinstance(data, dict) and isinstance(fields, dict):
            filtered_data = {}
            for key, value in fields.items():
                if key in data:
                    if isinstance(value, (dict, list)):
                        filtered_data[key] = filter_fields(data[key], value)
                    else:
                        filtered_data[key] = data[key]
            return filtered_data
        elif isinstance(data, list) and isinstance(fields, list):
            item_fields = fields[0] if fields else None
            return [filter_fields(item, item_fields) for item in data if isinstance(item, dict)]
        else:
            return data

    # Create test_output directory if it doesn't exist
    output_dir = os.path.join(os.path.dirname(__file__), 'test_output')
    os.makedirs(output_dir, exist_ok=True)

    # Apply the filter_fields function and save filtered data
    for movie in movies_watch_providers:
        movie_id = movie['movie_id']
        watch_providers_data = movie['watch_providers']
        filtered_watch_providers = filter_fields(watch_providers_data, FIELDS_TO_RETAIN_WATCH_PROVIDERS)

        # Extract provider names
        us_providers = filtered_watch_providers.get('results', {}).get('US', {}).get('flatrate', [])
        provider_names = [provider.get('provider_name') for provider in us_providers if 'provider_name' in provider]

        # Prepare the final data structure
        final_data = {
            'provider_names': provider_names
        }

        # Save the filtered data to the specified directory
        output_file_name = f"{movie_id}_watch_providers.json"
        output_file_path = os.path.join(output_dir, output_file_name)
        with open(output_file_path, 'w', encoding='utf-8') as f:
            json.dump(final_data, f, indent=2, ensure_ascii=False)

        # Verify that provider_names is a list
        assert isinstance(provider_names, list), f"provider_names should be a list for movie ID {movie_id}"

    print("All tests passed for filtering watch providers from batch.")
