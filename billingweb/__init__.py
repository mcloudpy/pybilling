from flask import render_template

from billingweb.flask_app_builder import build_flask_app
from billing.models import Application, Hits
from sqla import db

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
    s = db()
    u = Application(name=name)
    s.add(u)
    s.commit()
    return "New user: %s" % u.id


def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)

@flask_app.route("/test/fill")
def fill():

    start_date = datetime.datetime(year=2014, month=1, day=1)
    end_date = datetime.datetime(year=2015, month=1, day=1)
    for single_date in daterange(start_date, end_date):
        hits = random.randint(0, 15)
        s = db()
        u = Hits(hits=hits, user_id=2, ts=single_date)
        s.add(u)
        s.commit()

    return "Ok"

@flask_app.route("/test/addhits")
def addhits():
    return render_template("add_hits.html")

@flask_app.route("/test")
def test():
    return render_template("hits_chart.html")
