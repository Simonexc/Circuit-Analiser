import sympy as sp


def define_symbols_from_graph(grid, labels):
    # R L C E I
    keys = "RLCEI"
    count = [0]*5
    for i, l in enumerate(grid):
        for j, cell in enumerate(l):
            count[keys.find(labels[grid[i][j][0]])] += 1

    zr = [sp.Symbol(f'Z_r{i+1}') for i in range(count[0])]

    il = [sp.Symbol(f'i_l{i+1}') for i in range(count[1])]
    ul = [sp.Symbol(f'u_l{i+1}') for i in range(count[1])]
    zl = [sp.Symbol(f'Z_l{i+1}') for i in range(count[1])]
    l_symbols = [sp.Symbol(f'L_{i+1}') for i in range(count[1])]
    l_dot = [sp.Symbol('\\dot{i_{l'+str(i+1)+'}}') for i in range(count[1])]
    Ls = [f'L{i}' for i in range(count[1])]

    ic = [sp.Symbol(f'i_c{i + 1}') for i in range(count[2])]
    uc = [sp.Symbol(f'u_c{i + 1}') for i in range(count[2])]
    zc = [sp.Symbol(f'Z_c{i + 1}') for i in range(count[2])]
    c_symbols = [sp.Symbol(f'C_{i + 1}') for i in range(count[2])]
    c_dot = [sp.Symbol('\\dot{u_{c' + str(i + 1) + '}}') for i in range(count[2])]
    Cs = [f'C{i}' for i in range(count[2])]

    Es = [sp.Symbol(f'e_{i+1}') for i in range(count[3])]
    Is = [sp.Symbol(f'I_{i+1}') for i in range(count[4])]

    return zr, il, zl, Ls, uc, zc, Cs, Es, Is, ul, ic, l_symbols, c_symbols, l_dot, c_dot


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
    current_sources = [sp.Symbol(element[0]+'_'+str(int(element[1:])+1))
                       for element in circuit_elements if element[0] == 'I']
    currents_n = 0
    circles = []
    Is = []
    currents_equations = []
    while connection_points != dict():
        starting_point = list(connection_points.keys())[0]
        last_point = starting_point
        act_connection_points = {element: circuit[element].copy() for element in circuit_elements if element[0] == 'P'}
        next_point, connection_points = get_point(starting_point, connection_points)

        act_connection_points[starting_point].remove(next_point)
        previous_point = last_point
        points_history = [last_point]
        point_currents[starting_point][next_point] = [currents_n, last_point]
        Is.append(sp.Symbol('i_'+str(currents_n+1)))
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
                    if last_point == next_point:
                        last_point = "Q"
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
                    Is.append(sp.Symbol('i_' + str(currents_n+1)))
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
                        currents_equations.append(current_sources[int(next_point[1:])] - Is[currents[next_point][0]])
                    else:
                        currents_equations.append(current_sources[int(next_point[1:])] + Is[currents[next_point][0]])
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

    return circles, Is, currents, point_currents, currents_equations


def find_equations(circles, Is, currents, point_currents, currents_equations, il, uc, zl, zc, zr, Es, Ls, Cs, ul, ic,
                   omega, state, l_symbols, c_symbols, l_dot, c_dot):
    equations = currents_equations.copy()
    null_subs = []
    print(ic)

    for l in Ls:
        if l not in currents:
            equations.append(il[int(l[1:])])
            equations.append(ul[int(l[1:])])
        else:
            equations.append(il[int(l[1:])] - Is[currents[l][0]])
            if state != 2:
                equations.append(ul[int(l[1:])] - zl[int(l[1:])]*il[int(l[1:])])

    for c in Cs:
        if c not in currents:
            if state == 2:
                equations.append(c_symbols[int(c[1:])]*c_dot[int(c[1:])])
            else:
                equations.append(ic[int(c[1:])])
            equations.append(uc[int(c[1:])])
        elif omega != 0:
            if state != 2:
                equations.append(ic[int(c[1:])] - Is[currents[c][0]])
                equations.append(uc[int(c[1:])] - ic[int(c[1:])] * zc[int(c[1:])])
            else:
                equations.append(c_symbols[int(c[1:])] * c_dot[int(c[1:])] - Is[currents[c][0]])

    for circle in circles:
        equation = sp.sympify(0)
        for element, direction in circle:
            if element[0] == 'L':
                if state == 2:
                    print(element, l_symbols, l_dot, l_dot[int(element[1:])], l_symbols[int(element[1:])])
                    equation += direction*l_symbols[int(element[1:])]*l_dot[int(element[1:])]
                else:
                    equation += direction*ul[int(element[1:])]

            elif element[0] == 'C':
                equation += direction * uc[int(element[1:])]
                if omega == 0:
                    if Is[currents[element][0]] not in null_subs:
                        null_subs.append(Is[currents[element][0]])

            elif element[0] == 'R':
                equation += direction*Is[currents[element][0]] * zr[int(element[1:])]
            elif element[0] == 'E':
                equation += direction*Es[int(element[1:])]

        equations.append(equation)

    for sub in null_subs:
        equations.append(sub)

    for point in list(point_currents.keys())[:-1]:
        equation = sp.sympify(0)
        for current, p in point_currents[point].values():
            if p == point:
                equation -= Is[current]
            else:
                equation += Is[current]
        equations.append(equation)

    return equations


def find_neighbours(grid, graph, labels, sources_direction):
    intersections = {}
    y, x = len(grid), len(grid[0])
    for i, l in enumerate(grid):
        for j, cell in enumerate(l):
            if cell[0] == len(labels) - 1:
                act_label = "P"+str(cell[1])
                if act_label not in graph:
                    continue

                neighbours = ['']*4
                cases = [i > 0, j < x - 1, i < y - 1, j > 0]
                positions = [(i - 1, j), (i, j + 1), (i + 1, j), (i, j - 1)]
                orientations = [(0, 180), (270, 90), (0, 180), (270, 90)]
                for k, (case, pos, ori) in enumerate(zip(cases, positions, orientations)):
                    past_previous = (i, j)
                    previous = pos
                    if not case:
                        continue
                    if grid[previous[0]][previous[1]][0] == 0:
                        continue
                    if grid[previous[0]][previous[1]][0] != 1:
                        if ori[0] != grid[previous[0]][previous[1]][2] and ori[1] != grid[previous[0]][previous[1]][2] \
                           and grid[previous[0]][previous[1]][0] != len(labels) - 1:
                            continue
                        new_label = labels[grid[previous[0]][previous[1]][0]] + str(grid[previous[0]][previous[1]][1])

                        if new_label in graph[act_label]:
                            neighbours[k] = new_label
                        elif new_label[0] in list(sources_direction.keys()):
                            new_label = sources_direction[new_label[0]] + str(grid[previous[0]][previous[1]][1])
                            if new_label in graph[act_label]:
                                neighbours[k] = new_label
                        continue

                    end = False

                    while not end:
                        end = True
                        new_cases = [previous[0] > 0, previous[0] < y - 1, previous[1] > 0, previous[1] < x - 1]
                        new_positions = [(previous[0] - 1, previous[1]), (previous[0] + 1, previous[1]),
                                         (previous[0], previous[1] - 1), (previous[0], previous[1] + 1)]
                        new_orientations = [(0, 180), (0, 180), (270, 90), (270, 90)]
                        for q, (c, p, o) in enumerate(zip(new_cases, new_positions, new_orientations)):
                            if not c or p == past_previous:
                                continue
                            if grid[p[0]][p[1]][0] == 0:
                                continue
                            if grid[p[0]][p[1]][0] != 1:
                                if o[0] != grid[p[0]][p[1]][2] and o[1] != grid[p[0]][p[1]][2] and \
                                   grid[p[0]][p[1]][0] != len(labels) - 1:
                                    continue
                                new_label = labels[grid[p[0]][p[1]][0]] + str(grid[p[0]][p[1]][1])

                                if new_label in graph[act_label]:
                                    neighbours[k] = new_label
                                elif new_label[0] in list(sources_direction.keys()):
                                    new_label = sources_direction[new_label[0]] + str(grid[p[0]][p[1]][1])
                                    if new_label in graph[act_label]:
                                        neighbours[k] = new_label
                                break
                            else:
                                past_previous = previous
                                previous = p
                                end = False
                                break

                intersections[i*100+j] = neighbours

    return intersections


def filter_graph(graph):
    removed = True
    count_p = 0
    while removed:
        removed = False
        count_p = 0
        for key in list(graph.keys()):
            if key[0] == "P":
                count_p += 1
            if len(graph[key]) <= 1:
                for node in graph[key]:
                    graph[node].remove(key)
                del graph[key]
                removed = True

    if count_p > 1:
        removed = True
        while removed:
            removed = False
            for key in list(graph.keys()):
                if key[0] == "P" and len(graph[key]) == 2:
                    nodes = graph[key]
                    print(graph, nodes, key)
                    graph[nodes[0]].remove(key)
                    if nodes[1] not in graph[nodes[0]]:
                        graph[nodes[0]].append(nodes[1])
                    graph[nodes[1]].remove(key)
                    if nodes[0] not in graph[nodes[1]]:
                        graph[nodes[1]].append(nodes[0])
                    del graph[key]
                    count_p -= 1
                    if count_p == 1:
                        removed = False
                        break
                    removed = True

    return graph

# graph = {'P0': ['C0', 'P1', 'I0'], 'C0': ['P0', 'P3'], 'P3': ['C0', 'P5', 'O0'], 'P5': ['P3', 'R0', 'P4'], 'R0': ['P5', 'L0'], 'L0': ['R0', 'P1'], 'P1': ['L0', 'P0', 'P2'], 'I0': ['P0', 'O0'], 'O0': ['I0', 'P3'], 'P2': ['P1', 'C1', 'E0'], 'C1': ['P2', 'P4'], 'P4': ['C1', 'P5', 'U0'], 'U0': ['P4', 'E0'], 'E0': ['U0', 'P2']}
# grid = [[[0, 1, 0], [0, 2, 0], [0, 3, 0], [0, 4, 0], [0, 5, 0], [0, 6, 0], [0, 7, 0], [0, 8, 0], [0, 9, 0], [0, 10, 0], [0, 11, 0], [0, 12, 0], [0, 13, 0], [0, 14, 0], [0, 15, 0], [0, 16, 0], [0, 17, 0], [0, 18, 0], [0, 19, 0], [0, 20, 0]], [[0, 21, 0], [0, 22, 0], [0, 23, 0], [0, 24, 0], [0, 25, 0], [0, 26, 0], [0, 27, 0], [0, 28, 0], [0, 29, 0], [0, 30, 0], [0, 31, 0], [0, 32, 0], [0, 33, 0], [0, 34, 0], [0, 35, 0], [0, 36, 0], [0, 37, 0], [0, 38, 0], [0, 39, 0], [0, 40, 0]], [[0, 41, 0], [0, 42, 0], [0, 43, 0], [0, 44, 0], [0, 45, 0], [0, 46, 0], [0, 47, 0], [0, 48, 0], [0, 49, 0], [0, 50, 0], [0, 51, 0], [0, 52, 0], [0, 53, 0], [0, 54, 0], [0, 55, 0], [0, 56, 0], [0, 57, 0], [0, 58, 0], [0, 59, 0], [0, 60, 0]], [[0, 61, 0], [0, 62, 0], [0, 63, 0], [0, 64, 0], [0, 65, 0], [0, 66, 0], [0, 67, 0], [0, 68, 0], [0, 69, 0], [0, 70, 0], [0, 71, 0], [0, 72, 0], [0, 73, 0], [0, 74, 0], [0, 75, 0], [0, 76, 0], [0, 77, 0], [0, 78, 0], [0, 79, 0], [0, 80, 0]], [[0, 81, 0], [0, 82, 0], [0, 83, 0], [1, 0, 0], [8, 0, 360], [8, 1, 360], [8, 2, 360], [1, 4, 0], [0, 84, 0], [0, 85, 0], [0, 86, 0], [0, 87, 0], [0, 88, 0], [0, 89, 0], [0, 90, 0], [0, 91, 0], [0, 92, 0], [0, 93, 0], [0, 94, 0], [0, 95, 0]], [[0, 96, 0], [0, 97, 0], [0, 98, 0], [6, 0, 0], [3, 0, 0], [4, 0, 0], [3, 1, 0], [5, 0, 0], [0, 99, 0], [0, 100, 0], [0, 101, 0], [0, 102, 0], [0, 103, 0], [0, 104, 0], [0, 105, 0], [0, 106, 0], [0, 107, 0], [0, 108, 0], [0, 109, 0], [0, 110, 0]], [[0, 111, 0], [0, 112, 0], [0, 113, 0], [1, 11, 0], [8, 3, 360], [2, 0, 0], [8, 4, 360], [1, 5, 0], [0, 114, 0], [0, 115, 0], [0, 116, 0], [0, 117, 0], [0, 118, 0], [0, 119, 0], [0, 120, 0], [0, 121, 0], [0, 122, 0], [0, 123, 0], [0, 124, 0], [0, 125, 0]], [[0, 126, 0], [0, 127, 0], [0, 128, 0], [0, 129, 0], [1, 9, 0], [8, 5, 360], [1, 7, 0], [0, 130, 0], [0, 131, 0], [0, 132, 0], [0, 133, 0], [0, 134, 0], [0, 135, 0], [0, 136, 0], [0, 137, 0], [0, 138, 0], [0, 139, 0], [0, 140, 0], [0, 141, 0], [0, 142, 0]], [[0, 143, 0], [0, 144, 0], [0, 145, 0], [0, 146, 0], [0, 147, 0], [0, 148, 0], [0, 149, 0], [0, 150, 0], [0, 151, 0], [0, 152, 0], [0, 153, 0], [0, 154, 0], [0, 155, 0], [0, 156, 0], [0, 157, 0], [0, 158, 0], [0, 159, 0], [0, 160, 0], [0, 161, 0], [0, 162, 0]], [[0, 163, 0], [0, 164, 0], [0, 165, 0], [0, 166, 0], [0, 167, 0], [0, 168, 0], [0, 169, 0], [0, 170, 0], [0, 171, 0], [0, 172, 0], [0, 173, 0], [0, 174, 0], [0, 175, 0], [0, 176, 0], [0, 177, 0], [0, 178, 0], [0, 179, 0], [0, 180, 0], [0, 181, 0], [0, 182, 0]]]

