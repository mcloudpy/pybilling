from flask import request, render_template
from sqlalchemy import create_engine
from billing.models import Base
from billingweb import flask_app

from sqlalchemy.orm import sessionmaker

@flask_app.route("/install", methods=["GET", "POST"])
def install():
    """
    View to install the Web, creating and initializing the database.
    """
    if request.method == "GET":
        return render_template("install.html")

    elif request.method == "POST":
        database_uri = flask_app.config["DATABASE_URI"]

        engine = create_engine(database_uri)
        Base.metadata.create_all(engine)
        Session = sessionmaker(engine)

        return render_template("install_success.html")