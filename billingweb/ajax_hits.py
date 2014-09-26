from collections import defaultdict
import dateutil.parser
import json
import datetime
from flask import Response, request
from billing.models import Hits
from billingweb import flask_app
import sqla


@flask_app.route("/ajax/hits/new/<uid>")
def new_hits(uid):
    s = sqla.db()
    u = Hits(hits=1, user_id=uid)
    s.add(u)
    s.commit()
    return "Done"


@flask_app.route("/ajax/hits_test/<uid>")
def hits_test(uid):
    ret = [
        {
            "hits": 2,
            "app_id": 2,
            "ts": "2014-09-19T15:36:54.583331"
        },
        {
            "hits": 4,
            "app_id": 2,
            "ts": "2014-09-20T15:36:54.583331"
        },
        {
            "hits": 12,
            "app_id": 2,
            "ts": "2014-09-22T15:36:54.583331"
        }
    ]

    return Response(json.dumps(ret), mimetype="application/json")


def accumulate_hits(hits, granularity):
    """
    Accumulates the specified hits according to the specified granularity.

    @param hits: List of hits, with any time.
    @param granularity: yearly, monthly, weekly, daily or hourly

    Returns a simple dictionary of (accumulated) Hits, linked to the rounded timestamps.
    """

    # Dictionary to store the hits organized by their granularity.
    hits_by_granularity = defaultdict(list)

    # Define the adaptors for each granularity
    if granularity == "yearly":
        adapt = lambda t: datetime.datetime(year=t.year, month=1, day=1)
    elif granularity == "monthly":
        adapt = lambda t: datetime.datetime(year=t.year, month=t.month, day=1)
    elif granularity == "weekly":
        # NOT YET SUPPORTED. TODO.
        adapt = None
        pass
    elif granularity == "daily":
        adapt = lambda t: datetime.datetime(year=t.year, month=t.month, day=t.day)
    elif granularity == "hourly":
        adapt = lambda t: datetime.datetime(year=t.year, month=t.month, day=t.day, hour=t.hour)
    else:
        raise Exception("Unknown granularity specified")

    for h in hits:
        # Round the detailed ts to the granularity, so that no matter what
        # the sub-granularity unit, they compare equally.
        ts = adapt(h.ts)

        # Add the rounded hit to the dictionary, using the rounded ts as the key.
        hits_by_granularity[ts].append({"hits": h.hits, "uid": h.app_id})


    # Add up all the hits within the same granular date, to form a new simple dictionary.
    accumulated_hits = {}

    for ts, hits_list in hits_by_granularity.iteritems():
        hits_number = 0
        for h in hits_list:
            hits_number += h["hits"]
        appid = hits_list[0]["uid"]  # Just get the app_id of one of them.

        hits = Hits(hits=hits_number, ts=ts, app_id=appid)
        accumulated_hits[ts] = hits

    return accumulated_hits


@flask_app.route("/ajax/hits/<uid>")
def hits(uid):
    from_dt = request.values.get("from")
    to_dt = request.values.get("to")

    # The granularity can be: daily, yearly, monthly, weekly, hourly
    granularity = request.values.get("granularity")

    if from_dt is not None:
        from_dt = dateutil.parser.parse(from_dt)
    else:
        from_dt = datetime.datetime.utcfromtimestamp(0)

    if to_dt is not None:
        to_dt = dateutil.parser.parse(to_dt)
    else:
        to_dt = datetime.datetime.utcnow()


    # Retrieve hits from DB but filtering by the from and to dates.
    s = sqla.db()
    hits = s.query(Hits).filter(Hits.app_id == uid, Hits.ts <= to_dt, Hits.ts >= from_dt).all()

    hits_md = defaultdict(list)

    # Consider accumulating the hits for a period.
    if request.values.get("daily") == "true":
        for h in hits:
            hits_n = h.hits
            uid = h.app_id
            ts = h.ts
            ts = datetime.datetime(year=ts.year, month=ts.month, day=ts.day)
            hits_md[ts].append({"hits": hits_n, "uid": uid})
    else:
        for h in hits:
            hits_n = h.hits
            uid = h.app_id
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