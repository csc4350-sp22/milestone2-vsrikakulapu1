import flask
from flask import jsonify
import requests
import os
from dotenv import find_dotenv, load_dotenv
import json

app = flask.Flask(__name__)
@app.route('/')
def index():
    return "Hello World!"

@app.route('/trendingAPI')
def trendingAPI():
    load_dotenv(find_dotenv())

    BASE_URL = "https://api.nytimes.com/svc/search/v2/articlesearch.json"
    API_KEY = os.getenv("API_KEY")
    BASE_URL = "https://api.themoviedb.org/3/trending/all/day?api_key=" + API_KEY
    params = {
    }

    response = requests.get(
        BASE_URL,
        params=params,
    )

    response_json = response.json()

    try:
        results = response_json['results']
        trending_movies = []
        counter = 0

        for result in results:
            if(counter <10):
                if result['media_type'] == 'movie':
                    print(str(counter + 1) + " : " + result['title'])
                    trending_movies.append(result['title'])
                    counter +=1
        print(trending_movies)
        return jsonify(trending_movies)
    except KeyError:
        print("Couldn't fetch movies!")

app.run(debug=True)
