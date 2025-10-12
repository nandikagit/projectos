import requests
from dotenv import load_dotenv
import os

def omdb_request():

    # Load the .env file in the current directory
    load_dotenv()

    api_key = os.getenv('API_KEY')
    movie_title = 'Inception'

    url = f'http://www.omdbapi.com/?t={movie_title}&apikey={api_key}'

    response = requests.get(url)
    data = response.json()

    if data['Response'] == 'True':
        print(f"Title: {data['Title']}")
        print(f"Year: {data['Year']}")
        print(f"Director: {data['Director']}")
        print(f"Plot: {data['Plot']}")
    else:
        print("Movie not found!")

if __name__ == "__main__":
    omdb_request()