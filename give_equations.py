import sympy as sp


def define_symbols_from_graph(graph):
    # R L C E
    keys = "RLCE"
    count = [0]*4
    for key in graph:
        if key[0] in keys:
            count[keys.find(key[0])] += 1

    zr = [sp.Symbol(f'Z_r{i+1}') for i in range(count[0])]

    il = [sp.Symbol(f'i_l{i+1}') for i in range(count[1])]
    zl = [sp.Symbol(f'Z_l{i+1}') for i in range(count[1])]
    Ls = [f'L{i}' for i in range(count[1])]

    uc = [sp.Symbol(f'u_c{i + 1}') for i in range(count[2])]
    zc = [sp.Symbol(f'Z_c{i + 1}') for i in range(count[2])]
    Cs = [f'C{i}' for i in range(count[2])]

    Es = [sp.Symbol(f'E{i}') for i in range(count[3])]

    return zr, il, zl, Ls, uc, zc, Cs, Es


def get_point(point, connection_points):
    next_point = connection_points[point].pop(0)
    if connection_points[point] == list():
        del connection_points[point]

    return next_point, connection_points


def analise_circuit(input_circuit):
    circuit = input_circuit.copy()
    circuit_elements = circuit.keys()
    connection_points = {element: circuit[element].copy() for element in circuit_elements if element[0] == 'P'}
    currents = {element: [-1, ''] for element in circuit_elements if element[0] not in 'P'}
    point_currents = {element: {component: [-1, ''] for component in connection_points[element]}
                      for element in circuit_elements if element[0] == 'P'}
    current_sources = [sp.Symbol(element[0]+'_'+element[1:]) for element in circuit_elements if element[0] == 'I']
    currents_n = 0
    circles = []
    Is = []

    while connection_points != dict():
        starting_point = list(connection_points.keys())[0]
        last_point = starting_point
        act_connection_points = {element: circuit[element].copy() for element in circuit_elements if element[0] == 'P'}
        next_point, connection_points = get_point(starting_point, connection_points)

        act_connection_points[starting_point].remove(next_point)
        previous_point = last_point
        points_history = [last_point]
        point_currents[starting_point][next_point] = [currents_n, last_point]
        Is.append(sp.Symbol('i_'+str(currents_n)))
        currents_n += 1
        circle = []
        circle_history = [[]]
        force_current = None
        found_source = False

        while True:
            if next_point[0] == 'P':
                if point_currents[next_point][previous_point][0] == -1:
                    connection_points[next_point].remove(previous_point)
                    if connection_points[next_point] == list():
                        del connection_points[next_point]
                    point_currents[next_point][previous_point] = [currents_n-1, last_point]

                if next_point == starting_point:
                    if force_current:
                        circle = []
                    break

                act_connection_points[next_point].remove(previous_point)
                if act_connection_points[next_point] == list():  # found dead end
                    del act_connection_points[next_point]
                    circle = []
                    break

                if force_current:
                    force_current = None
                    stop = False
                    while circle_history != list():
                        circle = circle_history.pop()
                        next_point = points_history.pop()
                        if next_point in act_connection_points:
                            stop = True
                            break
                    if not stop:
                        break

                circle_history.append(circle.copy())

                last_point = next_point
                points_history.append(last_point)
                next_point, act_connection_points = get_point(next_point, act_connection_points)

                previous_point = last_point
                if point_currents[last_point][next_point][0] == -1:
                    Is.append(sp.Symbol('i_' + str(currents_n)))
                    connection_points[last_point].remove(next_point)
                    if connection_points[last_point] == list():
                        del connection_points[last_point]
                    point_currents[last_point][next_point] = [currents_n, last_point]
                    currents_n += 1
            else:
                if next_point[0] == 'E':
                    circle.append([next_point, -1 + 2 * int(found_source)])
                    found_source = not found_source
                if next_point[0] in 'UO':
                    found_source = not found_source

                if currents[next_point][0] == -1:
                    currents[next_point] = [currents_n-1, last_point]

                if next_point[0] == 'I':
                    if found_source and currents[next_point][1] == last_point:
                        Is[currents[next_point][0]] = current_sources[int(next_point[1:])]
                    else:
                        Is[currents[next_point][0]] = -current_sources[int(next_point[1:])]
                    force_current = next_point
                    found_source = not found_source

                if next_point[0] not in 'IOEUP':
                    circle.append([next_point, -1 + 2*int(last_point != currents[next_point][1])])

                if circuit[next_point][0] == previous_point:
                    previous_point, next_point = next_point, circuit[next_point][1]
                else:
                    previous_point, next_point = next_point, circuit[next_point][0]
        if circle != list():
            circles.append(circle)

    return circles, Is, currents, point_currents


def find_equations(circles, Is, currents, point_currents, il, uc, zl, zc, zr, Es, Ls, Cs):
    equations = []

    for l in Ls:
        equations.append(il[int(l[1:])] - Is[currents[l][0]])
    for c in Cs:
        equations.append(uc[int(c[1:])] - Is[currents[c][0]] * zc[int(c[1:])])

    for circle in circles:
        equation = sp.sympify(0)
        for element, direction in circle:
            if element[0] == 'L':
                equation += direction*Is[currents[element][0]] * zl[int(element[1:])]

            elif element[0] == 'C':
                equation += direction * Is[currents[element][0]] * zc[int(element[1:])]

            elif element[0] == 'R':
                equation += direction*Is[currents[element][0]] * zr[int(element[1:])]
            elif element[0] == 'E':
                equation += direction*Es[int(element[1:])]

        equations.append(equation)

    for point in list(point_currents.keys())[:-1]:
        equation = sp.sympify(0)
        for current, p in point_currents[point].values():
            if p == point:
                equation -= Is[current]
            else:
                equation += Is[current]
        equations.append(equation)

    return equations
