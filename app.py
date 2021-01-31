from flask import Flask, render_template, request
import json


app = Flask(__name__)


files = [
    "/static/images/dot.svg",
    "/static/images/wire.svg",
    "/static/images/resistor.svg",
    "/static/images/capacitor.svg",
    "/static/images/inductor.svg",
    "/static/images/v_source.svg",
    "/static/images/i_source.svg",
    "/static/images/intersection.svg"
]
x, y = 5, 4
counters = [0 for f in files]
labels = ["", "", "R", "C", "L", "E", "I", ""]
rotation_modes = [0, 0, 2, 2, 2, 1, 1, 0]


@app.route("/", methods=["GET", "POST"])
def home_func():
    if request.method == 'POST':
        grid = request.data
        print(grid)
        response = app.response_class(response=json.dumps(['aa', 2]),
                                      status=200,
                                      mimetype='application/json')
        return response
    return render_template("layout.html", files=files, x=x, y=y, counters=counters, labels=labels,
                           rotation_modes=rotation_modes)


if __name__ == "__main__":
    app.run()
