

# Mostly for debugging purposes, this snippet will print the site-map so that we can check
# which methods we are routing.
from flask import render_template, redirect, url_for
from billingweb import flask_app

import os


@flask_app.route("/site-map")
def site_map():
    lines = []
    for rule in flask_app.url_map.iter_rules():
        line = str((repr(rule)))
        lines.append(line)

    ret = "<br>".join(lines)
    return ret


@flask_app.route("/")
def index():
    """
    Index page.
    """

    # Check if the Web has been installed.

    # TODO: THIS CHECK IS TEMPORARY. UPDATE IT TO SUPPORT MORE DBS ETC.
    if not os.path.isfile(flask_app.config["DATABASE_URI"].split(":///", 1)[1]):
        return redirect(url_for("install"))

    return render_template("index.html")



