# %%
import pandas as pd
import json
import os

# %%
root_dir='/Users/HVMS/Desktop/GitHub/CineAI/src/data'

# %%
for sub_dir in sorted(os.listdir(root_dir)):
    print(sub_dir)  # Print each subdirectory in order

# %%
for sub_dir in sorted(os.listdir(root_dir+ '/2000/')):
    print(sub_dir)

# %%
batch_1_2000 = root_dir+ '/2000/batch_001.json'
with open(batch_1_2000, 'r') as file_1:
    data_1 = json.load(file_1)

# %%
len(data_1)

# %%
#To get movie ID
for movie_id in data_1:
    for keys,values in movie_id.items():
        print(keys)

# %%
# To get movie individual keys columns such as(endpoints) - expecting 15 endpoints

first_movie = data_1[0]
movie_id = list(first_movie.keys())[0]
endpoints = first_movie[movie_id].keys()

print(f"Endpoints for movie ID {movie_id}:")
for endpoint in endpoints:
    print(f"- {endpoint}")

# %%
# Getting keys from 'details' endpoint for first movie
first_movie = data_1[0]  # Get first movie
movie_id = list(first_movie.keys())[0]  # Get movie ID


details_keys = first_movie[movie_id]['details'].keys()

print(f"\nKeys in 'details' for movie {movie_id}:")
for key in sorted(details_keys):
    print(f"- {key}")

# %%



