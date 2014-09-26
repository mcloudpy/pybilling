import dateutil.parser
from flask import render_template, request, flash, session, redirect, url_for

from billingweb.flask_app_builder import build_flask_app
from billing.models import Application, Hits
import sqla

flask_app = build_flask_app()
flask_app.config.from_pyfile("../config.py")

# Import the different flask_views. This needs to be exactly here because
# otherwise the @flask_app notation wouldn't work.
import view_index
import view_install
import ajax_hits



# From here: BillingWeb code which should probably be moved to a specific sub-module.


import random
import datetime


@flask_app.route("/ajax/users/new/<name>")
def create_new_user(name):
    s = sqla.db()
    u = Application(name=name)
    s.add(u)
    s.commit()
    return "New user: %s" % u.id


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)


@flask_app.route("/test/fill")
def fill():
    start_date = datetime.datetime(year=2014, month=1, day=1)
    end_date = datetime.datetime(year=2015, month=1, day=1)
    for single_date in daterange(start_date, end_date):
        hits = random.randint(0, 15)
        s = sqla.db()
        u = Hits(hits=hits, user_id=2, ts=single_date)
        s.add(u)
        s.commit()

    return "Ok"


@flask_app.route("/test/addapp", methods=["GET", "POST"])
def addapp():

    # Retrieve the list of existing applications.
    s = sqla.db()
    applications = s.query(Application).all()

    if request.method == "POST":

        # Read the input.

        name = request.values.get("name")
        if name is None:
            flash("Please, provide an application name", "error")
            return render_template("add_app.html", applications=applications)

        description = request.values.get("description")
        if description is None:
            flash("Please, provide an application description", "error")
            return render_template("add_app.html", applications=applications)

        # Add the specified app itself.

        app = Application(name=name, description=description)
        s.add(app)
        s.commit()

        appid = app.id

        flash("The specified app has been added with ID: %r" % appid, "success")

        return redirect(url_for("addapp"))

    return render_template("add_app.html", applications=applications)


@flask_app.route("/test/addhits", methods=["GET", "POST"])
def addhits():
    if request.method == "POST":

        # Read the input.

        isodate = request.values.get("datetime")
        if isodate is None:
            flash("Please, provide a date and time", "error")
            return render_template("add_hits.html")
        try:
            session["last_datetime"] = isodate
            isodate = dateutil.parser.parse(isodate)
        except:
            flash("Could not parse the date you provided", "error")
            return render_template("add_hits.html")

        hits = request.values.get("hits")
        if hits is None:
            flash("Please, provide the number of hits", "error")
            return render_template("add_hits.html")
        try:
            hits = int(hits)
        except:
            flash("The number of hits must be a valid integer")
            return render_template("add_hits.html")

        appid = request.values.get("appid")
        if appid is None:
            flash("Please, provide an application ID", "error")
            return render_template("add_hits.html")
        try:
            session["last_appid"] = appid
            appid = int(appid)
        except:
            flash("The Application ID must be a valid integer")
            return render_template("add_hits.html")


        # Add the specified hits themselves.
        hits = Hits(ts=isodate, hits=hits, app_id=appid)

        # WARNING: Doing db() only results in issues from the tests when we
        # modify the DB. TODO: A better method for testing.
        s = sqla.db()
        s.add(hits)
        s.commit()

        flash("The specified hits have been added", "success")
        return redirect(url_for("addhits"))

    return render_template("add_hits.html")


@flask_app.route("/test")
def test():
    return render_template("hits_chart.html")

