''' This file generates a movie application'''
import os
import random
from dotenv import find_dotenv, load_dotenv
import flask
import requests

#load_dotenv(find_dotenv())

app = flask.Flask(__name__)

@app.route('/')
def trendset():
    ''' This function is called on landing page to output movie details'''
    movie_ids = [767, 460458, 634649, 566525]
    movie_id = str(random.choice(movie_ids))
    load_dotenv(find_dotenv())
    api_key = os.getenv("API_KEY")
    base_url = "https://api.themoviedb.org/3/movie/"+\
        movie_id+"?api_key="+ api_key +"&language=en-US"
    config_url = "https://api.themoviedb.org/3/configuration?api_key="+ api_key
    params = {}

    response = requests.get(
        base_url,
        params=params,
    )
    response_config = requests.get(
        config_url,
        params=params,
    )
    response_config = response_config.json()
    img_url = response_config['images']['base_url']+ response_config['images']['poster_sizes'][6]
    response_json = response.json()

    try:
        genres_str = ""
        for genre in response_json['genres']:
            genres_str = genre["name"] + ", " +genres_str
        movie_vals = {'title': response_json['title'],
                      'tagline': response_json['tagline'],
                      'genres': genres_str,
                      'poster_image': img_url + response_json['poster_path'],
                       'wiki_url' : get_wikipage(response_json['title'])}
        return flask.render_template("index.html", movie_vals = movie_vals)
    except KeyError:
        return "Couldn't fetch movies!"

def get_wikipage(name):
    ''' This function is used to get the wikipedia link
    relating to a specific name given as argument'''
    wiki_url = "https://en.wikipedia.org/?curid="
    session = requests.Session()
    url = "https://en.wikipedia.org/w/api.php"
    page_id = 0

    params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": name
    }

    response = session.get(url=url, params=params)
    data = response.json()

    for val in data['query']['search']:
        if val['title'] == name:
            page_id = val['pageid']
    wiki_url = wiki_url + str(page_id)
    return wiki_url
app.run(
    host=os.getenv('IP', '0.0.0.0'),
    port=int(os.getenv('PORT', '8080')),
    debug=True
)
