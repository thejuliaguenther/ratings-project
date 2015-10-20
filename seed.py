"""Utility file to seed ratings database from MovieLens data in seed_data/"""


from model import User
from model import Rating
from model import Movie

from model import connect_to_db, db
from server import app
import datetime


def load_users():
    """Load users from u.user into database."""

    print "Users"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    User.query.delete()

    # Read u.user file and insert data
    for row in open("seed_data/u.user"):
        row = row.rstrip()
        user_id, age, gender, occupation, zipcode = row.split("|")

        user = User(user_id=user_id,
                    age=age,
                    zipcode=zipcode)

        # We need to add to the session or it won't ever be stored
        db.session.add(user)

    # Once we're done, we should commit our work
    db.session.commit()


def load_movies():
    """Load movies from u.item into database."""

    for row in open("seed_data/u.item"):
        row = row.rstrip()
        row = row.split('|')

        released_at = row[2]
        if released_at:
            released_at = datetime.datetime.strptime(released_at, "%d-%b-%Y")
        else:
            released_at = None

        movie_title_split = row[1].split(" ")
        title = (" ").join(movie_title_split[:-1])
        print title 

        movie = Movie(movie_id=row[0],
                      title=title,
                      released_at=released_at,
                      imdb_url=row[4])

        db.session.add(movie)

    db.session.commit()


def load_ratings():
    """Load ratings from u.data into database."""

    for row in open("seed_data/u.data"):
        row = row.rstrip()
        row = row.split('\t')

        rating = Rating(movie_id=row[1],
                        user_id=row[0],
                        score=row[2])

        db.session.add(rating)

    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_users()
    load_movies()
    load_ratings()
