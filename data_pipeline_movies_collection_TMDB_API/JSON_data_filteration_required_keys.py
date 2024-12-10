import os
import json
from typing import Dict, Any
from tqdm import tqdm

class DataFilter:
    def __init__(self, input_dir: str, output_dir: str):
        self.input_dir = input_dir
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def get_fields_to_retain(self, endpoint_name: str) -> Any:
        # Fields to retain
        fields_to_retain = {
            "details": {
                "id", "title", "release_date", "genres", "runtime",
                "original_language", "popularity", "overview"
            },
            "credits": {
                "cast": [
                    {"id", "name", "character", "credit_id"}
                ],
                "crew": [
                    {"id", "name", "department", "job", "credit_id"}
                ]
            },
            "recommendations": {
                "results": [
                    {"id", "title", "popularity", "genre_ids"}
                ]
            },
            "watch_providers": {
                "results": {
                    "US": {}  # Include all data under 'US'
                }
            }
        }
        return fields_to_retain.get(endpoint_name)

    def filter_fields(self, data: Any, fields: Any) -> Any:
        if fields is None:
            return data
        elif isinstance(fields, set) and isinstance(data, dict):
            return {key: data[key] for key in fields if key in data}
        elif isinstance(fields, dict) and isinstance(data, dict):
            if not fields:  # Include all data if fields dict is empty
                return data
            return {
                key: self.filter_fields(data.get(key, {}), sub_fields)
                for key, sub_fields in fields.items() if key in data
            }
        elif isinstance(fields, list) and isinstance(data, list):
            if not fields:  # Include all items if fields list is empty
                return data
            return [
                self.filter_fields(item, fields[0]) for item in data
            ]
        else:
            return data

    def filter_movie_data(self, movie_data: Dict[str, Any]) -> Dict[str, Any]:
        filtered_movie_data = {}
        for endpoint_name, endpoint_data in movie_data.items():
            fields = self.get_fields_to_retain(endpoint_name)
            if fields is not None:
                filtered_data = self.filter_fields(endpoint_data, fields)
                filtered_movie_data[endpoint_name] = filtered_data
            else:
                filtered_movie_data[endpoint_name] = endpoint_data
        return filtered_movie_data

    def process_batch_file(self, batch_file_name: str):
        input_file_path = os.path.join(self.input_dir, batch_file_name)
        output_file_path = os.path.join(self.output_dir, batch_file_name)

        with open(input_file_path, 'r', encoding='utf-8') as f:
            batch_data = json.load(f)

        filtered_batch_data = []
        for movie_entry in batch_data:
            movie_id, movie_data = next(iter(movie_entry.items()))
            filtered_movie_data = self.filter_movie_data(movie_data)
            filtered_batch_data.append({movie_id: filtered_movie_data})

        with open(output_file_path, 'w', encoding='utf-8') as f:
            json.dump(filtered_batch_data, f, indent=2, ensure_ascii=False)

    def process_batch_files(self, batch_file_names):
        for batch_file_name in tqdm(batch_file_names, desc="Filtering batches", ncols=80, dynamic_ncols=True):
            self.process_batch_file(batch_file_name)
            # Use tqdm.write to indicate progress
            tqdm.write(f"Filtered {batch_file_name}")

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python filter_movie_data.py batch_file1.json batch_file2.json ...")
        sys.exit(1)

    input_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "movie_data", "2023")
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "filtered_data", "2023")
    batch_file_names = sys.argv[1:]

    data_filter = DataFilter(input_dir, output_dir)
    data_filter.process_batch_files(batch_file_names)
