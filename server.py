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


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route('/users')
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)

@app.route('/users/<int: user.user_id')
def user_details():
    """Shows detail;s about a user clicked on, including age, zipcode, the list 
    of movies that they reviewed, and their ratings for those movies."""

    user = User.query.get(user.user_id).first() #gets the object associated with the user
    user_age = user.age
    user_zipcode = user.zipcode
    user_ratings = user.ratings
    print user_ratings

    return redirect("/")


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
            session['user_name'] = user_email
    return redirect("/")





if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()