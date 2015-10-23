"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/', methods=["POST", "GET"])
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route('/login')
def show_login_form():
    """Shows login form."""
    return render_template("login.html")


@app.route('/process_login', methods=["POST"])
def process_login():
    """Checks if the user exists in the User table. If not, creates a new user."""
    username = request.form.get("username")
    password = request.form.get("password")

    user_object = User.query.filter(User.email == username).first()

    if not user_object:
        new_user = User(email=username, password=password)
        db.session.add(new_user)
        db.session.commit()
    else:
        user_email= user_object.email
        user_password = user_object.password
        if user_password != password:
            return redirect("/login")
        else:
            while user_email not in session.values():
                session['user_name'] = user_email
    return redirect("/")


@app.route('/users')
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)


@app.route('/users/<int:user_id>')
def user_details(user_id):
    """Shows detail;s about a user clicked on, including age, zipcode, the list 
    of movies that they reviewed, and their ratings for those movies."""

    user = User.query.get(user_id) #gets the object associated with the user
    user_age = user.age
    user_zipcode = user.zipcode
    user_ratings = user.ratings

    movie_titles_and_scores = {}
    for rating in user_ratings:
        movie = Movie.query.get(rating.movie_id)
        movie_score = rating.score
        movie_name = movie.title
        movie_titles_and_scores[movie_name] = movie_score

    return render_template("user_details.html", 
                            user_age=user_age, 
                            user_zipcode=user_zipcode, 
                            movie_titles_and_scores=movie_titles_and_scores)


@app.route('/movies')
def show_movies():
    movies = Movie.query.order_by(Movie.title).all()

    return render_template("movies.html", movies=movies)


@app.route('/movies/<int:movie_id>')
def movie_details(movie_id):
    rating_objects_list = Rating.query.filter(Rating.movie_id == movie_id).all()

    movie_ratings_dictionary = {}
    for rating_object in rating_objects_list:
        rating_score = rating_object.score
        rating_user = rating_object.user_id
        movie_ratings_dictionary[rating_user] = rating_score

    movie = Movie.query.get(movie_id)

    return render_template("movie_ratings.html", 
                            movie_ratings_dictionary = movie_ratings_dictionary, 
                            movie = movie)


@app.route('/rating_form/<int:movie_id>')
def rate_movie(movie_id):
    if session['user_name']: # or if user_name in session
        username = session.values()
        print username
        username = username[0]
        return render_template("rating_form.html", 
                                movie_id = movie_id, 
                                username = username)
    else:
        return redirect("/login")


@app.route('/rating_updated', methods=["POST"])
def update_rating():
    score = request.form.get("score")
    movie_id = request.form.get("movie_id")
    user_id_object = User.query.filter(User.email == session["user_name"]).first()
    user_id = user_id_object.user_id
    print session["user_name"]
    print movie_id
    print score
    print user_id
    # Rating.insert().values(score = score, movie_id = movie_id, user_id = user_id)
    rating = Rating.query.filter(Rating.user_id == user_id, Rating.movie_id == movie_id).first()
    print rating
    if rating:
        rating.score = score
    else:
        rating = Rating(score = score, movie_id = movie_id, user_id = user_id)
        db.session.add(rating)
    db.session.commit()
    return redirect("/movies")


def get_common_movies():
    """This function gets the movies that 2 users have both rated"""

    user_ratings = {}
    common_ratings = []

    movie = Movie.query.filter_by(title="Toy Story").one()
    user = User.query.get(1)    # someone we know who hasn't rated TS
    ratings = user.ratings
    other_ratings = Rating.query.filter_by(movie_id=m.movie_id).all()
    other_users = [r.user for r in other_ratings]

    for y in other_ratings:
        if 

    
    

    for x in ratings:
        user_ratings[x.movie_id] = x








if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()