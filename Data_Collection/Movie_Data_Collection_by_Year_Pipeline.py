#Importing Required Librarires
from dotenv import load_dotenv
import os

load_dotenv()
api_key=os.getenv('TMDB_BEARER_TOKEN')


class TMDB_API_Client:
    ''' Managing TMDB API Interactions and requests '''

    def __init__(self, API_KEY:str):
        self.base_url = "https://api.themoviedb.org/3"
        self.headers = {
            "accept": "applicaiton/json",
            "Authorization": f"Bearer {API_KEY}"
        }

client = TMDB_API_Client(api_key)
