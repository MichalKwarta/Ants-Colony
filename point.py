import itertools
import random
import time
import networkx as nx
from typing import Tuple
import matplotlib.pyplot as plt

MAX = 600
ITERATION_LIMIT = 30


class PointsList:
    points_list:list["Point"]

    def __init__(self, filename: str):
        if filename is not None:
            self.readPoints(filename)

    def __repr__(self):
        return list(map(str,self.points_list))

    def readPoints(self,filename):
        with open(filename, "r") as f:
            count = int(f.readline())
            l = f.readlines()
            if len(l) != count:
                raise ("Error in data")
            obj_list = []
            for el in l:
                a, b, c = map(int, el[:-1].split())
                obj_list.append(Point(a-1, b, c))

        self.points_list = obj_list

    def randomPoints(self, n):
        self.points_list = Point.randomPointsList(n)

    def greedy(self,plot=False):
        path = [self.points_list[0]]  # first node as start
        self.points_list = self.points_list[1::]
        distance = 0

        while self.points_list != []:
            next, delta = path[-1].getclosest(self.points_list)
            distance += delta
            path.append(next)
            self.points_list.pop(self.points_list.index(next))

        distance += path[0].getdistance(path[-1])  # go back to first node
        path.append(path[0])
        path = [point.id for point in path]
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
    ):
        # Theory -> https://www.youtube.com/watch?v=783ZtAF4j5g
        distance_matrix: list[float] = []
        pheromones_matrix: list[float] = []

        for p1 in self.points_list:
            costs_row = []
            pheromones_row = []
            for p2 in self.points_list:
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
        start = time.time()
        iteration = 0
        while iteration < iteration_limit:  # TODO: Mieli 50 sekund
            iteration += 1
            # print(i, end=" ")
            resant = []
            for _ in range(ants_count):
                current = random.randint(0, len(self.points_list) - 1)
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

        # print()
        best = min(res, key=lambda x: x[1])
        if plot:
            self.plot(best[0])

        return best
    def plot(self,path):
        G = nx.DiGraph(directed=True)
        for p in self.points_list:
            G.add_node(p.id,pos=(p.x,p.y))

        for id, p in enumerate(path[:-1]):
            G.add_edges_from(
                [(p, path[id + 1])], weight=round(self.points_list[p].getdistance(self.points_list[path[id + 1]]),2),color='r'
            )
        edge_labels = dict(
            [
                (
                    (
                        u,
                        v,
                    ),
                    d["weight"],
                )
                for u, v, d in G.edges(data=True)
            ]
        )
        pos=nx.get_node_attributes(G,'pos')
        _,colors = zip(*nx.get_edge_attributes(G,'color').items())
        nx.draw(G,pos,with_labels=True,edge_color=colors,node_color='#93ccfa',node_size=500)
        labels = nx.get_edge_attributes(G,'weight')
        nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
        plt.show()


class Point:
    cords: list[Tuple[int, int]] = []  # check if coordinates were already used

    def __init__(self, id: int, X: int, Y: int):

        if (X, Y) in Point.cords:
            raise (f"Point {X} {Y} already exists")

        Point.cords.append((X, Y))
        self.x: int = X
        self.y: int = Y
        self.id = id
        id += 1

    def __del__(self):
        Point.cords.remove((self.x, self.y))

    @classmethod
    def randomPointsList(cls, n: int):
        possibleCords = list(itertools.product(range(MAX), range(MAX)))
        return [cls(X, Y) for (X, Y) in random.sample(possibleCords, n)]

    def getdistance(self, p2: "Point"):
        return ((self.x - p2.x) ** 2 + (self.y - p2.y) ** 2) ** 0.5

    def getclosest(self, l: list["Point"]):  # assumption that node is not in the list
        closest: "Point" = l[0]
        for point in l[1:]:
            if self.getdistance(point) < self.getdistance(closest):
                closest = point

        delta_distance: float = self.getdistance(closest)

        return closest, delta_distance

    def __repr__(self):
        return f"{self.id} {self.x} {self.y}"


