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



if __name__ == '__main__':
    #app.run()
    from billingweb import flask_app
    flask_app.run()
