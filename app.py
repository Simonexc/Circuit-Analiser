from flask import Flask, render_template


app = Flask(__name__)


files = [
    "/static/images/dot.svg",
    "/static/images/resistor.svg",
    "/static/images/capacitor.svg",
    "/static/images/inductor.svg",
    "/static/images/v_source.svg",
    "/static/images/i_source.svg",
    "/static/images/intersection.svg"
]
x, y = 10, 5
counters = [0 for f in files]
labels = ["", "R", "C", "L", "E", "I", ""]


@app.route("/")
def home_func():
    return render_template("layout.html", files=files, x=x, y=y, counters=counters, labels=labels)


if __name__ == "__main__":
    app.run()
