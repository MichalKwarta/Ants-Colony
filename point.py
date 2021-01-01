from os import stat
from random import randint, random
MAX = 50


class Point:
    count = 0
    cords = []  # check if coordinates were already used

    def __init__(self, id, X, Y):
        Point.count += 1
        self.id = id
        if (X, Y) in Point.cords:
            raise("Już jest taki punkt")
        Point.cords.append((X, Y))
        self.x = X
        self.y = Y

    def __del__(self):
        Point.count -= 1
        Point.cords.remove((self.x, self.y))

    @classmethod
    def random(cls):
        X, Y = randint(0, MAX), randint(0, MAX)
        while (X, Y) in Point.cords:
            X, Y = randint(0, MAX), randint(0, MAX)
        return cls(Point.count+1, X, Y)

    def getdistance(self, p2):
        return ((self.x-p2.x)**2+(self.y-p2.y)**2)**0.5

    def getclosest(self, l: list):  # zakładam, że nie znajduje sie na liście
        closest = l[0]
        delta_distance = self.getdistance(closest)
        for point in l[1::]:
            if self.getdistance(point) < self.getdistance(closest):
                closest = point
                delta_distance = self.getdistance(closest)
        return closest, delta_distance

    def __str__(self):
        return f"{self.id} {self.x} {self.y}"

    @staticmethod
    def Ants(points_list,evaporation_rate = 0.1,
        alpha = 15,
        beta = 200,
        ants_count = 100,
        iterations_count = 10):
        # Theory -> https://www.youtube.com/watch?v=783ZtAF4j5g
        distance_matrix = []
        pheromones_matrix = []
        

        for p1 in points_list:
            costs_row = []
            pheromones_row = []
            for p2 in points_list:
                if p1 == p2:
                    costs_row.append(0)
                    pheromones_row.append(0)
                else:
                    dist = ((p1[1]-p2[1])**2+(p1[2]-p2[2])**2)**0.5
                    costs_row.append(dist)
                    pheromones_row.append(1/dist)
            distance_matrix.append(costs_row)
            pheromones_matrix.append(pheromones_row)
        res = []
        for i in range(iterations_count):  # progress output
            #print(i, end=" ")
            res = []
            for _ in range(ants_count):
                current = 0
                visited = [0 for _ in range(len(distance_matrix))]
                path = [current]
                dist = 0
                while(len(path) < len(distance_matrix)):
                    visited[current] = 1
                    numerators = []
                    denominator = 0
                    for ph, d, v in zip(pheromones_matrix[current], distance_matrix[current], visited):
                        if v or d == 0:
                            val = 0
                        else:  # not visited and not (x,x) pair
                            val = ph**alpha+(1/d)**beta
                        numerators.append(val)
                        denominator += val
                    probabilities = list(
                        map(lambda numerator: numerator / denominator, numerators))

                    # roulette wheel
                    choice_num = random()  # <0,1)
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
                res.append((path, dist))

            # update pheromones
            for i in range(len(distance_matrix)):  # evaporation
                for j in range(len(distance_matrix)):
                    pheromones_matrix[i][j] *= (1-evaporation_rate)
            for path, length in res:  # add pheromones after iteration
                for i in range(len(path)-1):
                    v1 = path[i]
                    v2 = path[i+1]
                    pheromones_matrix[v1][v2] += 1/length
                    pheromones_matrix[v2][v1] += 1/length
        #print()
        best = min(res, key=lambda x: x[1])
        return list(map(lambda x: x + 1, best[0])),evaporation_rate,alpha,beta,ants_count,iterations_count, best[1]

    @staticmethod
    def greedy(listofinstances):
        path = [listofinstances[0]]  # biore pierwszy wierzcholek jako poczatek
        listofinstances = listofinstances[1::]
        distance = 0

        while listofinstances != []:
            next, delta = path[-1].getclosest(listofinstances)
            distance += delta
            path.append(next)
            listofinstances.pop(listofinstances.index(next))

        distance += path[0].getdistance(path[-1])  # zamykam cykl
        path.append(path[0])
        return path, distance

    @staticmethod
    def write(filename, list, distance=None):
        f = open(filename, 'w+')
        print(Point.count, file=f)
        for object in list:
            print(object, file=f)
        print(distance, file=f)

    @staticmethod
    def read(filename):
        f = open(filename, 'r')
        count = int(f.readline())
        l = f.readlines()
        if len(l) != count:
            raise('błąd danych')
        obj_list = []
        for el in l:
            a, b, c = map(int, el[:-1].split())
            obj_list.append((a, b, c))
        return obj_list
    @staticmethod
    def readPoints(filename):
        f = open(filename, 'r')
        count = int(f.readline())
        l = f.readlines()
        if len(l) != count:
            raise('błąd danych')
        obj_list = []
        for el in l:
            a, b, c = map(int, el[:-1].split())
            obj_list.append(Point(a, b, c))
        return obj_list


def generatelistofinstances(n: int):
    l = []
    for k in range(n):
        l.append(Point.random())
    return l


def generatematrix(l: list):
    matrix = []
    for p1 in l:
        row = []
        for p2 in l:
            if p2 == p1:
                row.append(-1)
            else:
                # FIXME: TO TYLKO POGLĄDOWE BO JEST ZAOKRĄGLANIE
                row.append(round(p1.getdistance(p2)))
        matrix.append(row)
    return matrix
