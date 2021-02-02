import sympy as sp


t = sp.Symbol('t')


def mag_phase(com):
    magnitude = sp.sqrt(sp.re(com)**2+sp.im(com)**2)
    phase = 0
    if com != 0:
        phase = sp.arg(com)*180/sp.pi
    return magnitude, phase


def solve_initial_conditions(equations, i_l, u_c, custom_symbols, omega):
    equations = sp.Matrix(equations)
    vars = tuple(list(i_l) + list(u_c) + list(custom_symbols))

    result = list(sp.linsolve(equations, vars))[0]

    return result

'''
i_l = []
u_c = [sp.Symbol('u_c1')]
custom_symbols = [sp.Symbol('i_1')]
z_c = sp.Symbol('z_c1')
e = sp.Symbol('e_1')
equations = [u_c[0]-z_c*custom_symbols[0], e-z_c*custom_symbols[0]]
solve_initial_conditions(equations, i_l, u_c, custom_symbols, sp.Symbol("\\omega"))
'''
'''
initial_conditions = []
for u in u_c:
    magnitude, phase = mag_phase(result[u])
    display(Math(sp.latex(u)+"="+sp.latex(magnitude.evalf(5))+'e^{'+sp.latex(phase.evalf(5))+'^\\circ j}'))
    initial = magnitude
    if omega != 0:
        magnitude *= sp.sqrt(2)
        magnitude = magnitude.evalf()
        display(Math(sp.latex(u) + "(t)=" + sp.latex(magnitude.evalf(5)) + 'sin('+
                     str(omega)+'t + (' + sp.latex(phase.evalf(5)) + '^\\circ ))'))
        initial = magnitude*sp.sin(phase/180*sp.pi)
    else:
        display(Math(sp.latex(u) + "(t)=" + sp.latex(magnitude.evalf(5))))
    initial_conditions.append(initial.evalf())
    display(Math(sp.latex(u) + "(0^-)=" + sp.latex(initial.evalf(5))))
    print()

return sp.Matrix(initial_conditions)
'''