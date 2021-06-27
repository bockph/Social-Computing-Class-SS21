import random

import matplotlib.pyplot as plt
import networkx as nx


# TODO: Calculates the sum of the weights of all edges incident in node i
def calc_ki(g, i):
    return g.degree(nbunch=i, weight='weight')


# TODO: Calculates the sum of the weights of all edges in the graph
def calc_m(g):
    result = 0
    for (u, v, weight) in g.edges.data('weight', default=0):
        result += weight
    return 1 / 2 * result


# TODO: Calculates the sum of the weights of all edges to nodes in com
def calc_tot(g, com):
    result = 0
    for (u, v, weight) in g.edges.data('weight', default=0):
        if v in com or u in com:
            result += weight
    return result


# TODO: Calculates the sum of the weights of edges from node i to nodes in com
def calc_ki_in(g, i, com):
    result = 0
    for (u, v, weight) in g.edges.data('weight', default=0):
        if u == i:
            if v in com:
                result += weight
    return result


# TODO: Calculates the delta Modularity with the formula given above
def calc_deltaMm(g, i, com, m):
    m = calc_m(g)
    ki = calc_ki(g, i)
    kic = calc_ki_in(g, i, com)
    tot = calc_tot(g, com)
    result = kic - (tot * ki / 2 / m)
    return result


# TODO: Calculates the sum of the weights of all intra-community edges in com
def calc_lc(g, com):
    result = 0
    for (u, v, weight) in g.edges.data('weight', default=0):
        if u in com and v in com:
            result += weight
    return result


# TODO: Calculates the sum of degrees of the nodes in com
def calc_kc(g, com):
    result = 0
    for (u, v, weight) in g.edges.data('weight', default=0):
        if u in com or v in com:
            result += weight
    return result



# TODO: Calculates the modularity with the formula given above
def calc_mod(g, M_com, m):
    result = 0
    for com in M_com.values():
        # print(type(calc_lc(g,com)))
        # print(type(calc_kc(g,com)))
        # print(type(m))
        result += calc_lc(g, com) / m - (calc_kc(g, com) / (2 * m)) ** 2
    return result


def plotGraph(g):
    # Create positions of all nodes and save them
    pos = nx.spring_layout(g)

    # Draw the graph according to node positions
    nx.draw(g, pos, with_labels=True)

    label_pos = {}

    for k, v in pos.items():
        label_pos[k] = (v[0], v[1] + 0.1)

    nx.draw_networkx_labels(g, label_pos, labels=nx.get_node_attributes(g, 'name'))

    # Create edge labels
    labels = {e: str(g.get_edge_data(*e)) for e in g.edges}

    # Draw edge labels according to node positions
    nx.draw_networkx_edge_labels(g, pos, edge_labels=labels)

    plt.show()


def mergeCommunities(g, M_com):
    g_new = nx.Graph()
    for key, com in M_com.items():
        if com:
            name = ''.join(str(e) for e in com)
            print(name)
            g_new.add_node(key, name=name)

    for a in g_new.nodes:
        for b in g_new.nodes:
            weight = 0
            if a == b:
                weight = calc_lc(g, M_com[a])
            else:
                for (u, v, w) in g.edges.data('weight', default=0):
                    if (u in M_com[a] and v in M_com[b]) or (u in M_com[b] and v in M_com[a]):
                        weight += w
            g_new.add_edge(a, b, weight=weight)

    return g_new


# Krackhardt Kite Graph with assigned weight=1
def krackhardt_graph():
    g = nx.krackhardt_kite_graph()
    for e in g.edges():
        g[e[0]][e[1]]["weight"] = 1
    return g


# Test graph from linked website
def test_graph():
    g = nx.Graph()
    g.add_node("A")
    g.add_node("B")
    g.add_node("C")
    g.add_node("D")
    g.add_node("E")
    g.add_node("F")
    g.add_edge("A", "B", weight=5)
    g.add_edge("A", "C", weight=4)
    g.add_edge("A", "E", weight=1)
    g.add_edge("B", "C", weight=2)
    g.add_edge("C", "D", weight=7)
    g.add_edge("D", "F", weight=3)
    g.add_edge("E", "F", weight=8)
    return g


g = test_graph()
# Can be used for testing
g = krackhardt_graph()
plotGraph(g)
m = calc_m(g)  # TODO
print(type(m))
print(m)
k = 0  # iteration number

# Loop until no improvement can be made through merging
while True:
    V = g.nodes
    M_com = {}  # M_com is explained in sub task b)
    nodes_dict = {}  # A dictionary that contains all nodes as keys and tracks their respective community

    M_com = {i: [i] for i in V}
    mod_new = calc_mod(g, M_com, m)

    # PhaseI: Loop until no node movement/improvement can be made
    while True:

        mod = mod_new

        M_com_old = copy.deepcopy(M_com)
        v_random = random.sample(V, k=len(V))

        vertex_movement = False
        for i in V:
            improvement = False

            best_community = M_com[i]
            best_increase = 0
            print(M_com.items())
            for (key, com) in M_com.items():
                removed = False
                if i in com:
                    com.remove(i)
                    best_community = key
                    removed = True

                q_delta = calc_deltaMm(g, i, com, m)
                if q_delta > best_increase:
                    best_increase = q_delta
                    best_community = key
                    improvement = True

            M_com[best_community].append(i)

            if M_com != M_com_old:
                vertex_movement = True

        mod_new = calc_mod(g, M_com, m)
        if mod_new - mod < 0 or M_com == M_com_old:
            M_com = M_com_old
            break



    g = mergeCommunities(g, M_com)
    break

print("End result")
print("Modularity: " + str(mod))
plotGraph(g)
