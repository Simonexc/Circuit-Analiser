import sympy as sp
import numpy as np


t = sp.Symbol('t')

def eigen(M):
    eigen_val = M.eigenvects()
    print(eigen_val)
    eigen_values = sp.Matrix([val[0] for val in eigen_val])
    print(np.array([val[2][0] for val in eigen_val]))
    eigen_vectors = [val[2][0].evalf(5) for val in eigen_val]
    eigen_vectors = sp.Matrix([eigen_vectors[:2], eigen_vectors[2:]])
    return eigen_values, eigen_vectors


def hamilton(M):
    text = "Metoda Cayleya-Hamiltona<br>"
    eigen_values, eigen_vectors = eigen(M)
    text += 'Eigenvalues: $' + sp.latex(eigen_values) + ' = ' + sp.latex(eigen_values.evalf(5)) + '$<br>'
    eigen_values = eigen_values.evalf(5)

    x = sp.symbols(str(['a'+str(i) for i in range(len(eigen_values))])[1:-1].replace("'", ""))
    if len(eigen_values) == 1:
        x = [x]

    A = sp.ones(len(x), 1)

    for i in range(1, len(x)):
        A = sp.Matrix(sp.BlockMatrix([A, sp.HadamardPower(eigen_values, i)]))

    b = sp.Matrix(sp.HadamardPower(sp.E, eigen_values*t))
    result = sp.Matrix(list(sp.linsolve((A, b), *x))[0])
    text += "$"+sp.latex(b)+' = '+sp.latex(A)+'\\bullet'+sp.latex(sp.Matrix(x))+'\\implies' + \
            sp.latex(sp.Matrix(x))+' = '+sp.latex(result) + "$<br>"

    s = sp.diag(*tuple([1]*len(x)))*result[0, 0]
    for i in range(1, len(x)):
        s += M*result[i, 0]

    text += "$e^{\\mathbb{A}t} = "+sp.latex(sp.simplify(s))+"$<br><br>"

    return s, text


def lagrange(M):
    text = "Metoda Lagrange'a-Sylvestera<br>"

    eigen_values, eigen_vectors = eigen(M)
    if len(eigen_values) != 2:
        text += "Macierz nie spełnia wymogów<br>"
        return text
    if eigen_values[0] == eigen_values[1]:
        text += "Macierz nie spełnia wymogów<br>"
        return text

    text += 'Eigenvalues: $' + sp.latex(eigen_values) + ' = ' + sp.latex(eigen_values.evalf(5)) + '$<br>'

    eigen_values = eigen_values.evalf(5)
    s_1, s_2 = eigen_values

    diag1 = sp.diag(*tuple([1]*2))
    s = sp.exp(s_1*t)/(s_2-s_1)*(s_2*diag1-M)+sp.exp(s_2*t)/(s_1-s_2)*(s_1*diag1-M)
    text += "$e^{\\mathbb{A}t} = e^{s_1t}\\bullet \\frac{s_2\\mathbb{1}-\\mathbb{A}}{s_2-s_1}+e^{s_2t}\\bullet \\frac{s_1\\mathbb{1}-\\mathbb{A}}{s_1-s_2} = "+sp.latex(s)+"$<br><br>"

    return text


def vectors(M):
    text = "Metoda wektorów własnych<br>"

    eigen_values, eigen_vectors = eigen(M)
    text += 'Eigenvalues: $' + sp.latex(eigen_values.evalf(5)) + "$<br>"
    text += '$\\mathbb{P} \\text{(kolejne kolumny to kolejne eigenwektory)}: ' + sp.latex(eigen_vectors.evalf(5)) + "$<br>"

    eigen_values = eigen_values.evalf(5)
    eigen_vectors = eigen_vectors.evalf(5)
    print(eigen_vectors)
    p_inv = eigen_vectors.inv()
    text += "$\\mathbb{P}^{-1} = " + sp.latex(p_inv) + "$<br>"

    D = sp.diag(*tuple(sp.Matrix(sp.HadamardPower(sp.E, eigen_values*t))))
    text += "$\\mathbb{D} = " + sp.latex(D) + "$<br>"

    s = eigen_vectors*D*p_inv
    text += "$e^{\\mathbb{A}t} = \\mathbb{P}\\bullet\\mathbb{D}\\bullet\\mathbb{P}^{-1}=" + sp.latex(s) + "$<br><br>"

    return text


def final_x(eA, initial_conditions, final_conditions):
    xp = eA*initial_conditions
    x = xp + final_conditions
    text = "Stan Przejściowy<br><br>"
    text += "$\\mathbb{x}_p(t) = e^{\\mathbb{A}t}\\bullet\\mathbb{x}_p(0^+) = "+sp.latex(eA.evalf(5))+'\\bullet' + \
            sp.latex(initial_conditions.evalf(5)) + ' = ' + sp.latex(xp.evalf(5))+"$<br><br><br>"
    text += "$\\mathbb{x}(t) = \\mathbb{x}_p(t) + \\mathbb{x}_u(t) = "+ sp.latex(sp.simplify(xp.evalf(5))) +\
            ' + ' + sp.latex(final_conditions.evalf(5)) + ' = ' + sp.latex(sp.simplify(x.evalf(5))) + "$<br><br>"

    return text
