

# Mostly for debugging purposes, this snippet will print the site-map so that we can check
# which methods we are routing.
from flask import render_template
from markupsafe._speedups import escape
from billingweb import flask_app


@flask_app.route("/site-map")
def site_map():
    lines = []
    for rule in flask_app.url_map.iter_rules():
        line = str(escape(repr(rule)))
        lines.append(line)

    ret = "<br>".join(lines)
    return ret


@flask_app.route("/")
def index():
    return render_template("index.html")
