from collections import defaultdict
import dateutil.parser
import json
import datetime
from flask import Response, request
from billing.models import Hits
from billingweb import flask_app, db


@flask_app.route("/ajax/hits/new/<uid>")
def new_hits(uid):
    s = db()
    u = Hits(hits=1, user_id=uid)
    s.add(u)
    s.commit()
    return "Done"


@flask_app.route("/ajax/hits_test/<uid>")
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


@flask_app.route("/ajax/hits/<uid>")
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

        #print "MERGED HITS %d ON %r %r" % (h, mts.day, mts.month)

        data.append({"hits": h, "user_id": uid, "ts": mts.isoformat()})

    hits_str = json.dumps(data)

    return Response(hits_str, mimetype="application/json")