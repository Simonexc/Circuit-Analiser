from flask import Flask, render_template, request
import json
from convert_graph import *
from give_equations import *


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
x, y = 10, 5
counters = [0 for f in files]
labels = ["", "", "R", "C", "L", "E", "I", "P"]
rotation_modes = [0, 0, 2, 2, 2, 1, 1, 0]
sources_direction = {"I": "O", "E": "U"}


@app.route("/", methods=["GET", "POST"])
def home_func():
    if request.method == 'POST':
        grid = json.loads(request.data)
        grid = find_intersections(grid, labels)
        #print(grid)
        graph = convert_to_graph(grid, labels, rotation_modes, sources_direction)
        print(graph)
        zr, il, zl, Ls, uc, zc, Cs, Es = define_symbols_from_graph(graph)
        equations = find_equations(*analise_circuit(graph), il, uc, zl, zc, zr, Es, Ls, Cs)
        equations = [sp.latex(equation) for equation in equations]
        response = app.response_class(response=json.dumps(equations),
                                      status=200,
                                      mimetype='application/json')
        return response
    return render_template("layout.html", files=files, x=x, y=y, counters=counters, labels=labels,
                           rotation_modes=rotation_modes)


if __name__ == "__main__":
    app.run()
