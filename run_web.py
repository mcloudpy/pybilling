from flask import Flask, render_template

app = Flask(__name__)
app.config.from_object(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/ajax/hits/<uid>")
def hits(uid):
    return ""


if __name__ == '__main__':
    app.run()