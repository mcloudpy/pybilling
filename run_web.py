from collections import defaultdict
import json
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
from time import strftime
from flask import Flask, render_template, request, Response, url_for
from billing.models import Base, User, Hits

import config

import dateutil.parser

from markupsafe._speedups import escape

# Initialize Flask
app = Flask(__name__)
app.config["DEBUG"] = True
app.config.from_object(__name__)

# Initialize SQLA
_db_eng = create_engine(config.DATABASE_URI)
Base.metadata.bind = _db_eng
db = sessionmaker(bind=_db_eng)


@app.route("/ajax/users/new/<name>")
def create_new_user(name):
    s = db()
    u = User(name=name)
    s.add(u)
    s.commit()
    return "New user: %s" % u.id


@app.route("/ajax/hits/new/<uid>")
def new_hits(uid):
    s = db()
    u = Hits(hits=1, user_id=uid)
    s.add(u)
    s.commit()
    return "Done"


@app.route("/ajax/hits_test/<uid>")
def hits_test(uid):
    ret = [
        {
            "hits": 2,
            "user_id": 2,
            "ts": "2014-09-19T15:36:54.583331"
        },
        {
            "hits": 4,
            "user_id": 2,
            "ts": "2014-09-20T15:36:54.583331"
        },
        {
            "hits": 12,
            "user_id": 2,
            "ts": "2014-09-22T15:36:54.583331"
        }
    ]

    return Response(json.dumps(ret), mimetype="application/json")


@app.route("/ajax/hits/<uid>")
def hits(uid):
    from_dt = request.values.get("from")
    to_dt = request.values.get("to")

    if from_dt is not None:
        from_dt = dateutil.parser.parse(from_dt)
    else:
        from_dt = datetime.datetime.utcfromtimestamp(0)

    if to_dt is not None:
        to_dt = dateutil.parser.parse(to_dt)
    else:
        to_dt = datetime.datetime.utcnow()


    # Retrieve hits from DB but filtering by the from and to dates.
    s = db()
    hits = s.query(Hits).filter(Hits.user_id == uid, Hits.ts <= to_dt, Hits.ts >= from_dt).all()

    hits_md = defaultdict(list)

    # Consider accumulating the hits for a period.
    if request.values.get("daily") == "true":
        for h in hits:
            hits_n = h.hits
            uid = h.user_id
            ts = h.ts
            ts = datetime.datetime(year=ts.year, month=ts.month, day=ts.day)
            hits_md[ts].append({"hits": hits_n, "uid": uid})
    else:
        for h in hits:
            hits_n = h.hits
            uid = h.user_id
            ts = h.ts
            hits_md[ts].append({"hits": hits_n, "uid": uid})

    data = []
    for mts in sorted(hits_md):
        h = 0
        for hits in hits_md[mts]:
            h += hits["hits"]

        print "MERGED HITS %d ON %r %r" % (h, mts.day, mts.month)

        data.append({"hits": h, "user_id": uid, "ts": mts.isoformat()})

    hits_str = json.dumps(data)

    return Response(hits_str, mimetype="application/json")


def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)

@app.route("/test/fill")
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

@app.route("/test")
def test():
    return render_template("hits_chart.html")


if __name__ == '__main__':
    #app.run()
    from billingweb import flask_app
    flask_app.run()