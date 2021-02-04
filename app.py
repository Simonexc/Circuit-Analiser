from flask import Flask, render_template, request
import json
import copy
from convert_graph import *
from give_equations import *
from initial_conditions import *
from methods import *
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
passing = None
stable_state = None


@app.route("/", methods=["GET", "POST"])
def home_func():
    global passing
    global stable_state
    if request.method == 'POST':
        grid, (r_val, l_val, c_val, e_val, i_val), state = json.loads(request.data)
        grid_mod = find_intersections(copy.deepcopy(grid), labels)

        grid_switch = find_switches(copy.deepcopy(grid_mod), labels, min(1,state))
        graph = convert_to_graph(copy.deepcopy(grid_switch), labels, rotation_modes, sources_direction)

        if state == 2:
            graph = delete_sources(graph, sources_direction)

        graph_mod = filter_graph(copy.deepcopy(graph))
        intersections = find_neighbours(grid_switch, graph_mod, labels, sources_direction)

        zr, il, zl, Ls, uc, zc, Cs, Es, I_power, ul, ic, l_symbols, c_symbols, l_dot, c_dot = define_symbols_from_graph(grid, labels)
        print(ul, ic)

        circles, Is, currents, point_currents, currents_equations = analise_circuit(graph_mod)
        if state == 2:
            omega = 1
        else:
            omega = find_omega(graph_mod, i_val, e_val)
        equations = find_equations(circles, Is, currents, point_currents, currents_equations,
                                   il, uc, zl, zc, zr, Es, Ls, Cs, ul, ic, omega, state, l_symbols, c_symbols, l_dot, c_dot)
        equations_latex = [sp.latex(equation) for equation in equations]

        if state == 2:
            solved_equations = solve_initial_conditions(equations, l_dot, c_dot, Is)
            print(solved_equations)
        else:
            solved_equations = solve_initial_conditions(equations, il, uc, ul+ic+Is)

        time_equations_latex, initial_conditions_latex, variables_latex = "", "", ""
        calc_equations = list(copy.deepcopy(solved_equations))
        for i, element in enumerate(r_val):
            sub = element
            for j in range(len(calc_equations)):
                calc_equations[j] = calc_equations[j].subs(zr[i], sub)

        if state < 2:
            calc_equations = substitute_sources(e_val, Es, calc_equations)
            calc_equations = substitute_sources(i_val, I_power, calc_equations)
            for i, element in enumerate(l_val):
                sub = sp.I*omega*element
                for j in range(len(calc_equations)):
                    calc_equations[j] = calc_equations[j].subs(zl[i], sub)
            for i, element in enumerate(c_val):
                sub = -sp.I/(omega*element)
                for j in range(len(calc_equations)):
                    calc_equations[j] = calc_equations[j].subs(zc[i], sub)

            time_equations, initial_conditions = init_conditions(il+uc, calc_equations, omega)
            print(state)
            if state == 0:
                passing = sp.Matrix(initial_conditions)
            elif state == 1:
                stable_state = sp.Matrix(time_equations)
                passing -= sp.Matrix(initial_conditions)
            time_equations_latex = sp.latex(sp.Matrix(time_equations))
            initial_conditions_latex = sp.latex(sp.Matrix(initial_conditions))
            variables_latex = [sp.latex(v) for v in il+uc]
            calc_equations_latex = [convert_to_exponential(eq) for eq in calc_equations]
        else:
            for i, element in enumerate(l_val):
                sub = element
                for j in range(len(calc_equations)):
                    calc_equations[j] = calc_equations[j].subs(l_symbols[i], sub)
            for i, element in enumerate(c_val):
                sub = element
                for j in range(len(calc_equations)):
                    calc_equations[j] = calc_equations[j].subs(c_symbols[i], sub)

            calc_equations_latex = [sp.latex(eq) for eq in calc_equations]

        if state == 2:
            solved_for = [sp.latex(i) for i in list(l_dot+c_dot)]
        else:
            solved_for = [sp.latex(i) for i in list(il+uc)]
        solved_equations_latex = [sp.latex(sp.simplify(eq)) for eq in solved_equations]

        send_more = ""
        if state == 2:
            A = give_A(calc_equations, l_dot, c_dot, uc, il)
            send_more = "$A="+sp.latex(A)+"$<br><br>"
            eA, text = hamilton(A)
            send_more += text
            send_more += lagrange(A)
            send_more += vectors(A)
            send_more += final_x(eA, passing,stable_state)

            #equations = find_equations(circles, Is, currents, point_currents, currents_equations,
            #                           il, uc, zl, zc, zr, Es, Ls, Cs, ul, ic, omega, 3, l_symbols, c_symbols,
            #                           l_dot, c_dot)
            # send_more += operatorowa(equations, ul, il, uc, ic, Is, l_val, c_val, passing, stable_state)

        response = app.response_class(response=json.dumps([intersections, point_currents, equations_latex,
                                                           grid_switch, solved_equations_latex, solved_for,
                                                           calc_equations_latex, time_equations_latex,
                                                           initial_conditions_latex, variables_latex,
                                                           sp.latex(passing), send_more]),
                                      status=200,
                                      mimetype='application/json')
        return response
    return render_template("layout.html", files=files, x=x, y=y, counters=counters, labels=labels,
                           rotation_modes=rotation_modes)


if __name__ == "__main__":
    app.run()
