from flask import Flask, render_template, request
import json
import copy
from convert_graph import *
from give_equations import *
from initial_conditions import *
import sympy as sp


app = Flask(__name__)


files = [
    "/static/images/dot.svg",
    "/static/images/wire.svg",
    "/static/images/resistor.svg",
    "/static/images/capacitor.svg",
    "/static/images/inductor.svg",
    "/static/images/v_source.svg",
    "/static/images/i_source.svg",
    "/static/images/switch.svg",
    "/static/images/intersection.svg"
]
x, y = 20, 10
counters = [0 for f in files]
labels = ["", "", "R", "C", "L", "E", "I", "S", "P"]
rotation_modes = [0, 0, 2, 2, 2, 1, 1, 2, 0]
sources_direction = {"I": "O", "E": "U"}


@app.route("/", methods=["GET", "POST"])
def home_func():

    if request.method == 'POST':
        grid = json.loads(request.data)
        print(grid)
        grid_mod = find_intersections(copy.deepcopy(grid), labels)
        print(grid_mod)
        grid_switch = find_switches(copy.deepcopy(grid_mod), labels, 0)
        graph = convert_to_graph(copy.deepcopy(grid_switch), labels, rotation_modes, sources_direction)
        print(graph)
        graph_mod = filter_graph(copy.deepcopy(graph))
        print(graph_mod)
        intersections = find_neighbours(grid_switch, graph_mod, labels, sources_direction)
        print(intersections)

        zr, il, zl, Ls, uc, zc, Cs, Es = define_symbols_from_graph(grid, labels)
        circles, Is, currents, point_currents, currents_equations = analise_circuit(graph_mod)
        print(point_currents)
        equations = find_equations(circles, Is, currents, point_currents, currents_equations,
                                   il, uc, zl, zc, zr, Es, Ls, Cs)
        equations_latex = [sp.latex(equation) for equation in equations]

        solved_equations = solve_initial_conditions(equations, il, uc, Is, sp.Symbol("w"))
        solved_for = [sp.latex(i) for i in list(il+uc+Is)]
        solved_equations_latex = [sp.latex(sp.simplify(eq)) for eq in solved_equations]
        print(solved_equations_latex)
        response = app.response_class(response=json.dumps([intersections, point_currents, equations_latex,
                                                           grid_switch, solved_equations_latex, solved_for]),
                                      status=200,
                                      mimetype='application/json')
        return response
    return render_template("layout.html", files=files, x=x, y=y, counters=counters, labels=labels,
                           rotation_modes=rotation_modes)


if __name__ == "__main__":
    app.run()
