import sympy as sp
import numpy as np


t = sp.Symbol('t')


def mag_phase(com):
    magnitude = sp.sqrt(sp.re(com)**2+sp.im(com)**2)
    phase = 0
    if com != 0:
        phase = sp.arg(com)*180/sp.pi
    return sp.sympify(magnitude), sp.sympify(phase)


def find_omega(graph, i_val, e_val):
    omega = -1
    for key in graph:
        if key[0] == "E":
            omega = e_val[int(key[1:])][2]
        elif key[0] == "I":
            omega = i_val[int(key[1:])][2]

    return omega


def substitute_sources(es, symbols, equations):
    for i, source in enumerate(es):
        sub = source[0]*sp.exp(sp.I*source[1]/180*sp.pi)
        if source[2] != 0:
            sub /= sp.sqrt(2)
        for j in range(len(equations)):
            equations[j] = equations[j].subs(symbols[i], sub)

    return equations


def solve_initial_conditions(equations, i_l, u_c, custom_symbols):
    print("-----")
    print(equations)
    equations = sp.Matrix(equations)
    vars = tuple(list(i_l) + list(u_c) + list(custom_symbols))
    print(vars)
    print(sp.solve(equations, vars))
    print(sp.linsolve(equations, vars))
    result = sp.solve(equations, vars)
    result = [result[i] if i in result else sp.sympify(0) for i in i_l+u_c]

    return result


def convert_to_exponential(val):
    magnitude, phase = mag_phase(val)
    return sp.latex(magnitude.evalf(5))+'e^{'+sp.latex(phase.evalf(5))+'^\\circ j}'
'''

            display(Math(sp.latex(u) + "(t)=" + sp.latex(magnitude.evalf(5)) + 'sin(' +
                         str(omega) + 't + (' + sp.latex(phase.evalf(5)) + '^\\circ ))'))
'''


def init_conditions(vars, equations, omega):
    initial_conditions = []
    time_equations = []

    for i, u in enumerate(vars):
        magnitude, phase = mag_phase(equations[i])

        initial = magnitude
        if omega != 0:
            magnitude *= sp.sqrt(2)
            magnitude = magnitude.evalf()
            time_equations.append(magnitude.evalf(5)*sp.sin(omega*t+phase.evalf(5)*sp.Symbol('^\\circ')))
            initial = magnitude * sp.sin(phase / 180 * sp.pi)
        else:
            time_equations.append(magnitude.evalf(5))

        initial_conditions.append(initial.evalf())

    return time_equations, initial_conditions


def give_A(equations, l_dot, c_dot, u_c, i_l):
    A = np.ndarray((len(l_dot) + len(c_dot), len(l_dot) + len(c_dot)))
    for i, u in enumerate(l_dot):
        for j, k in enumerate(i_l):
            print(equations)
            A[i][j] = equations[i].coeff(k, 1)

        for j, k in enumerate(u_c):
            A[i][j + len(l_dot)] = equations[i].coeff(k, 1)

    for i, u in enumerate(c_dot):
        for j, k in enumerate(i_l):
            A[i + len(l_dot)][j] = equations[i + len(l_dot)].coeff(k, 1)
        for j, k in enumerate(u_c):
            A[i + len(l_dot)][j + len(l_dot)] = equations[i + len(l_dot)].coeff(k, 1)

    A = sp.Matrix(A)
    return A

