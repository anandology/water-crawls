from flask import Flask, render_template, abort
import web
from db import STP

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/stps")
def stps():
    stps = STP.all()
    return render_template("stps/index.html", stps=stps)

@app.route("/stps/<name>")
def stp(name):
    stp = STP.find(name=name)
    if not stp:
        abort(404)
    return render_template("stps/view.html", stp=stp)


if __name__ == "__main__":
    app.run()