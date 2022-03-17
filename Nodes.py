import itertools
import random
from typing import Tuple

import matplotlib.pyplot as plt
import networkx as nx

MAX = 600
ITERATION_LIMIT = 30


class NodesList:

    nodes_list: list["Node"]

    def __init__(self, filename: str = None):
        if filename is not None:
            self.readNodes(filename)

    def __repr__(self):
        return list(map(str, self.nodes_list))

    def readNodes(self, filename: str):
        """
        Read data from file,generate nodes and assign it to self.nodes_list

        Args:
            filename (str): path to datafile
        Raises:
            Exception: length of Nodes unequal to number declared in data file

        """

        with open(filename, "r") as f:
            count = int(f.readline())
            l = f.readlines()
            if len(l) != count:
                raise Exception("Error in data")
            obj_list = []
            for el in l:
                a, b, c = map(int, el[:-1].split())
                obj_list.append(Node(a - 1, b, c))
        self.nodes_list = obj_list

    def setRandomData(self, n: int):
        """
        Sets self.nodes_list to list of randomly genrated nodes

        Args:
            n (int): Number of nodes to generate
        """
        self.nodes_list = Node.randomNodesList(n)

    def greedy(self, plot=False) -> Tuple[list[int], float]:
        """
        Greedy approach to TSP problem

        Args:
            plot (bool, optional): if set to true, shows plotted path with edges weights. Defaults to False.

        Returns:
            Tuple[list[int],float]: Tuple with list of nodes on path and total distance
        """
        path = [self.nodes_list[0]]  # first node as start
        nodesToVisit = self.nodes_list[1:]
        distance = 0
        while nodesToVisit != []:
            next, delta = path[-1].getclosest(nodesToVisit)
            distance += delta
            path.append(next)
            nodesToVisit.pop(nodesToVisit.index(next))

        distance += path[0].getdistance(path[-1])  # go back to first node
        path.append(path[0])
        path = [node.id for node in path]

        if plot:
            self.plot(path)

        return path, distance

    def Ants(
        self,
        plot=False,
        iteration_limit: int = ITERATION_LIMIT,
        evaporation_rate: float = 0.2,
        alpha: int = 6,
        beta: int = 61,
        ants_count: int = 30,
    ) -> Tuple[list[int], float]:
        """
        Ant colony optimization algorithm to solve TSP problem

        Args:
            plot (bool, optional): if set to true,plots path. Defaults to False.
            iteration_limit (int, optional): number of iterations for algorithm. Defaults to ITERATION_LIMIT.
            evaporation_rate (float, optional): pheromone loss over iterations. Defaults to 0.2.
            alpha (int, optional): weight of pheromones for heuristics. Defaults to 6.
            beta (int, optional): weight of distance for heuristics. Defaults to 61.
            ants_count (int, optional): number of ants in single iterations. Defaults to 30.

        Returns:
            Tuple[list[int],float]: Tuple with list of nodes on path and total distance

        """
        # Theory -> https://www.youtube.com/watch?v=783ZtAF4j5g
        distance_matrix: list[float] = []
        pheromones_matrix: list[float] = []

        for p1 in self.nodes_list:
            costs_row = []
            pheromones_row = []
            for p2 in self.nodes_list:
                if p1 == p2:
                    costs_row.append(0)
                    pheromones_row.append(0)
                else:
                    dist = p1.getdistance(p2)
                    costs_row.append(dist)
                    try:
                        pheromones_row.append(1 / dist)
                    except ZeroDivisionError:  # well, it shouldn't be possible
                        print(p1, p2)
                        break
            distance_matrix.append(costs_row)
            pheromones_matrix.append(pheromones_row)
        res = []
        iteration = 0
        while iteration < iteration_limit:
            iteration += 1
            resant = []
            for _ in range(ants_count):
                current = random.randint(0, len(self.nodes_list) - 1)
                visited = [0 for _ in range(len(distance_matrix))]
                path = [current]
                dist = 0
                while len(path) < len(distance_matrix):
                    visited[current] = 1
                    numerators = []
                    denominator = 0
                    for ph, d, v in zip(
                        pheromones_matrix[current], distance_matrix[current], visited
                    ):
                        if v == 1 or d == 0:
                            val = 0
                        else:  # not visited and not (x,x) pair
                            val = ph**alpha + (1 / d) ** beta
                        numerators.append(val)
                        denominator += val
                    probabilities = list(
                        map(lambda numerator: numerator / denominator, numerators)
                    )

                    # roulette wheel
                    choice_num = random.random()  # <0,1)
                    probabilities_sum = 0
                    for V, P in enumerate(probabilities):
                        probabilities_sum += P
                        if choice_num <= probabilities_sum and P != 0:
                            dist += distance_matrix[current][V]
                            path.append(V)
                            current = V
                            break
                path.append(path[0])
                dist += distance_matrix[current][path[-1]]
                resant.append((path, dist))

            # update pheromones
            for i in range(len(distance_matrix)):  # evaporation
                for j in range(len(distance_matrix)):
                    pheromones_matrix[i][j] *= 1 - evaporation_rate

            for path, length in res:  # add pheromones after iteration
                # local ph update
                for i in range(len(path) - 1):
                    v1 = path[i]
                    v2 = path[i + 1]
                    pheromones_matrix[v1][v2] += 1 / length
                    pheromones_matrix[v2][v1] += 1 / length

            res += resant

        best = min(res, key=lambda x: x[1])
        if plot:
            self.plot(best[0])

        return best

    def plot(self, path: list[int]):
        """
        Method that plots path

        Args:
            path (list[int]): list of nodes on path
        """

        G = nx.DiGraph(directed=True)
        for p in self.nodes_list:
            G.add_node(p.id, pos=(p.x, p.y))

        for id, p in enumerate(path[:-1]):
            G.add_edges_from(
                [(p, path[id + 1])],
                weight=round(
                    self.nodes_list[p].getdistance(self.nodes_list[path[id + 1]]), 2
                ),
                color="r",
            )

        pos = nx.get_node_attributes(G, "pos")
        _, colors = zip(*nx.get_edge_attributes(G, "color").items())
        nx.draw(
            G,
            pos,
            with_labels=True,
            edge_color=colors,
            node_color="#93ccfa",
            node_size=500,
        )
        labels = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        plt.show()


class Node:
    cords: list[Tuple[int, int]] = []  # check if coordinates were already used
    def __init__(self, id: int, X: int, Y: int):

        if (X, Y) in Node.cords:
            raise (f"Node {X} {Y} already exists")

        Node.cords.append((X, Y))
        self.x: int = X
        self.y: int = Y
        self.id = id

    def __del__(self):
        Node.cords.remove((self.x, self.y))

    @classmethod
    def randomNodesList(cls, n: int) -> list["Node"]:
        """Classmethod, generates list of random Nodes with cords in range <0;MAX>
        MAX is defined in class,default 600

        Returns:
            list[Node]: List of Nodes
        """
        possibleCords = list(itertools.product(range(MAX), range(MAX)))

        return [
            cls(id, X, Y) for (id, (X, Y)) in enumerate(random.sample(possibleCords, n))
        ]

    def getdistance(self, p2: "Node") -> float:
        """calculate distance betweend two nodes

        Args:
            p2 (Node): Another Node to get distance to

        Returns:
            float: distance
        """
        return ((self.x - p2.x) ** 2 + (self.y - p2.y) ** 2) ** 0.5

    def getclosest(self, l: list["Node"]) -> Tuple["Node", float]:
        """
        Method to find closest Node and calculate distance to it

        Args:
            l(list["Node"]): List of remaining Nodes to visit
        Returns:
            Tuple["Node",float]: Closest Node and distance to it
        """
        closest: "Node" = l[0]
        for node in l[1:]:
            if self.getdistance(node) < self.getdistance(closest):
                closest = node

        delta_distance: float = self.getdistance(closest)

        return closest, delta_distance

    def __repr__(self):
        return f"{self.id} {self.x} {self.y}"
