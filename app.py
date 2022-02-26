""" This file generates a movie application"""
# pylint: disable=too-few-public-methods
# pylint: disable=too-many-locals
# pylint: disable=no-member
import os
import random
import json
from dotenv import find_dotenv, load_dotenv
import flask
import requests
from flask_login import LoginManager, UserMixin
from flask_login import login_user, login_required, logout_user
from flask_sqlalchemy import SQLAlchemy
from flask import session

load_dotenv(find_dotenv())

app = flask.Flask(__name__)

app.config["SECRET_KEY"] = "a safe and secure secret key is used here"
# Point SQLAlchemy to your Heroku database
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
# Gets rid of a warning
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = "app.login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    """This function is used to load user"""
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    """This class is used to create User database"""

    __tablename__ = "users"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100))
    username = db.Column(db.String(50), nullable=False, unique=True)


class Reviews(db.Model):
    """This class is used to create Reviews database"""

    __tablename__ = "reviews"
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, unique=False)
    rating = db.Column(db.Integer())
    review = db.Column(db.String(300))
    movie_id = db.Column(db.Integer())


db.create_all()


@app.route("/")
def start():
    """This function is called on landing page to sign up"""
    value = 0
    page = 0
    if "page" in session:
        page = session["page"]
    if "user_exists" in session:
        if session["user_exists"]:
            value = 1
    return flask.render_template("sign.html", value=value, page=page)


@app.route("/signUpPage", methods=["GET", "POST"])
def sign():
    """This function is called on signUpPage to store the form data"""
    # code to validate and add user to database goes here
    name = flask.request.form.get("name")
    username = flask.request.form.get("username")
    # if this returns a user, then the username already exists in database
    user = User.query.filter_by(username=username).first()

    if user:
        # if a user is found, we want to redirect back to signup page so user can try again
        session["user_exists"] = True
        session["page"] = 1
        return flask.redirect(flask.url_for("start"))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(username=username, name=name)

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    return flask.render_template("login.html")


@app.route("/loginPage", methods=["GET", "POST"])
def login():
    """This function is called on loginPage to store the form data"""
    if flask.request.method == "GET":
        return flask.render_template("login.html")

    username = flask.request.form.get("username")
    user = User.query.filter_by(username=username).first()

    # check if the user actually exists
    if not user:
        session["user_exists"] = False
        session["page"] = 2
        # if the user doesn't exist, go to / page
        return flask.redirect(flask.url_for("start"))

    login_user(user)
    messages = json.dumps({"username": username})
    session["username"] = username
    return flask.redirect(flask.url_for("trendset", messages=messages))


@app.route("/other_page")
def trendset():
    """This function is called on landing page to output movie details"""
    username = session["username"]
    print(username)
    movie_ids = [767, 460458, 634649, 566525]
    movie_id = str(random.choice(movie_ids))
    api_key = os.getenv("API_KEY")
    base_url = (
        "https://api.themoviedb.org/3/movie/"
        + movie_id
        + "?api_key="
        + api_key
        + "&language=en-US"
    )
    config_url = "https://api.themoviedb.org/3/configuration?api_key=" + api_key
    params = {}

    movie_reviews = Reviews.query.filter_by(movie_id=movie_id).all()
    reviews = []
    for class_instance in movie_reviews:
        review = vars(class_instance)
        this_user = 1 if session["username"] == review["username"] else 0
        review = {
            "rating": review["rating"],
            "movie_id": review["movie_id"],
            "username": review["username"],
            "review": review["review"],
            "id": review["id"],
            "this_user": this_user,
        }
        reviews.append(review)

    response = requests.get(
        base_url,
        params=params,
    )
    response_config = requests.get(
        config_url,
        params=params,
    )
    response_config = response_config.json()
    img_url = (
        response_config["images"]["base_url"]
        + response_config["images"]["poster_sizes"][6]
    )
    response_json = response.json()

    try:
        genres_str = ""
        for genre in response_json["genres"]:
            genres_str = genre["name"] + ", " + genres_str
        movie_vals = {
            "title": response_json["title"],
            "tagline": response_json["tagline"],
            "genres": genres_str,
            "poster_image": img_url + response_json["poster_path"],
            "wiki_url": get_wikipage(response_json["title"]),
        }
        return flask.render_template(
            "index.html",
            movie_vals=movie_vals,
            movie_id=movie_id,
            username=username,
            reviews=reviews,
        )
    except KeyError:
        return "Couldn't fetch movies!"


def get_wikipage(name):
    """This function is used to get the wikipedia link
    relating to a specific name given as argument"""
    wiki_url = "https://en.wikipedia.org/?curid="
    session_val = requests.Session()
    url = "https://en.wikipedia.org/w/api.php"
    page_id = 0

    params = {"action": "query", "format": "json", "list": "search", "srsearch": name}

    response = session_val.get(url=url, params=params)
    data = response.json()

    for val in data["query"]["search"]:
        if val["title"] == name:
            page_id = val["pageid"]
    wiki_url = wiki_url + str(page_id)
    return wiki_url


@app.route("/save_reviews", methods=["GET", "POST"])
def mv_reviews():
    """This function is used to store the reviews in database"""
    # code to validate and add user to database goes here
    rating = flask.request.form.get("rating")
    review = flask.request.form.get("review")
    username = session["username"]
    movie_id = flask.request.form.get("movieid")
    # create a new review_user with the form data.
    reviewed_user = Reviews(
        username=username, rating=rating, review=review, movie_id=movie_id
    )
    # add the new review_user to the database
    db.session.add(reviewed_user)
    db.session.commit()
    return flask.redirect(flask.url_for("trendset"))


@app.route("/logout")
@login_required
def logout():
    """This function is used to logout"""
    logout_user()
    return flask.redirect(flask.url_for("login"))


app.run(host=os.getenv('IP','0.0.0.0'), port=int(os.getenv("PORT", "8080")), debug=True)
