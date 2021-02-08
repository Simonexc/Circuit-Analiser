def find_intersections(grid, labels):
    first_wire = None
    count = 0

    for i, l in enumerate(grid):
        for j, cell in enumerate(l):
            if cell[0] == 1 and cell[2] == 360:
                grid[i][j][0] = len(labels) - 1
                grid[i][j][1] = count
                count += 1
            elif cell[0] == 1 and not first_wire:
                first_wire = (i, j)
    if count == 0:
        grid[first_wire[0]][first_wire[1]][0] = len(labels) - 1
        grid[first_wire[0]][first_wire[1]][1] = 0
    return grid


def find_switches(grid, labels, state):
    for i, l in enumerate(grid):
        for j, cell in enumerate(l):
            if labels[cell[0]] == "S":
                cell[2] = (cell[2] + 90*state)%360
                if cell[2] == 0 or cell[2] == 180:
                    grid[i][j-1][0] = 0
                    grid[i][j+1][0] = 0
                else:
                    grid[i-1][j][0] = 0
                    grid[i+1][j][0] = 0
                grid[i][j][0] = 1

    return grid


def delete_sources(graph, sources_direction):
    for key in list(graph.keys()):
        nodes = graph[key]
        if key[0] == "E" or key[0] == sources_direction["E"]:
            graph[nodes[0]].remove(key)
            if nodes[1] not in graph[nodes[0]]:
                graph[nodes[0]].append(nodes[1])
            graph[nodes[1]].remove(key)
            if nodes[0] not in graph[nodes[1]]:
                graph[nodes[1]].append(nodes[0])
            del graph[key]

        elif key[0] == "I" or key[0] == sources_direction["I"]:
            for node in graph[key]:
                graph[node].remove(key)
            del graph[key]

    return graph


def convert_to_graph(grid, labels, rotation_modes, sources_direction):
    starting_point = None
    for i, l in enumerate(grid):
        for j, cell in enumerate(l):
            if cell[0] == len(labels) - 1:
                starting_point = (i, j)
                break
        if starting_point:
            break

    y, x = len(grid), len(grid[0])
    point = grid[starting_point[0]][starting_point[1]]
    label = labels[point[0]] + str(point[1])
    start_points = [[starting_point, label, []]]
    last_name = label
    graph = {label: []}

    while start_points:
        act_point, name, vis = start_points[-1]
        remove = True
        if name != "W":
            last_name = name

        cases = [act_point[0] > 0, act_point[0] < y-1, act_point[1] > 0, act_point[1] < x-1]
        positions = [(act_point[0]-1, act_point[1]), (act_point[0]+1, act_point[1]), (act_point[0], act_point[1]-1),
                     (act_point[0], act_point[1]+1)]
        orientations = [(0, 180), (0, 180), (270, 90), (270, 90)]
        if rotation_modes[grid[act_point[0]][act_point[1]][0]] > 0:
            if grid[act_point[0]][act_point[1]][2] == 90 or grid[act_point[0]][act_point[1]][2] == 270:
                cases = cases[2:]
                positions = positions[2:]
                orientations = orientations[2:]
            else:
                cases = cases[:2]
                positions = positions[:2]
                orientations = orientations[:2]

        for i, (case, pos, orient) in enumerate(zip(cases, positions, orientations)):
            if case:
                p = grid[pos[0]][pos[1]]
                if p[0] != 0 and (rotation_modes[p[0]] == 0 or p[2] == orient[0] or p[2] == orient[1]):

                    if p[0] == 1:
                        names_visited = []
                        if name[0] == labels[-1]:
                            names_visited.append(name)
                        start_points.append([pos, "W", names_visited])
                        remove = False
                    else:
                        label = labels[p[0]] + str(p[1])
                        act_label = label
                        if label in vis:
                            continue

                        if rotation_modes[p[0]] == 1:
                            act_label = sources_direction[labels[p[0]]] + str(p[1])
                            if orient[i % 2] != p[2]:
                                act_label, label = label, act_label
                        print(start_points)
                        if label[0] == labels[-1]:
                            print(start_points)
                            start_points[-1][2].append(label)

                        names_visited = []
                        if name[0] == labels[-1]:
                            names_visited.append(name)

                        start_points.append([pos, label, names_visited])
                        remove = False

                        if act_label not in graph[last_name]:
                            graph[last_name].append(act_label)
                        if act_label not in graph:
                            graph[act_label] = []
                        if last_name not in graph[act_label]:
                            graph[act_label].append(last_name)

                        if label != act_label:
                            if label not in graph:
                                graph[label] = []
                            graph[label].append(act_label)
                            graph[act_label].append(label)

                    break

        if remove:
            start_points.pop()
            grid[act_point[0]][act_point[1]][0] = 0
        elif name[0] != labels[-1]:
            start_points.pop(-2)
            grid[act_point[0]][act_point[1]][0] = 0

    return graph
