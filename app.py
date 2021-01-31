import os
from flask import Flask, render_template


app = Flask(__name__)


files = [
    "/static/images/dot.svg",
    "/static/images/intersection.svg",
    "/static/images/resistor.svg",
    "/static/images/capacitor.svg",
    "/static/images/inductor.svg",
    "/static/images/v_source.svg",
    "/static/images/i_source.svg"
]
x, y = 30, 20


@app.route("/")
def home_func():
    return render_template("layout.html", files=files, x=x, y=y)


if __name__ == "__main__":
    app.run()