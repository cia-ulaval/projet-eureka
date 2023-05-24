import numpy as np
from random import randint
from backend.src.domain.Node import Node

class AStar:

    def __init__(self, cols, rows):
        self.cols: int = cols
        self.rows: int = rows

    @staticmethod
    def clean_open_set(open_set, current_node):

        for i in range(len(open_set)):
            if open_set[i] == current_node:
                open_set.pop(i)
                break

        return open_set

    @staticmethod
    def h_score(current_node, end):

        # distance =  abs(current_node.x - end.x) + abs(current_node.y - end.y)
        distance = np.sqrt(abs(current_node.x - end.x) ** 2 + abs(current_node.y - end.y) ** 2)
        # print(f"d : {distance}")
        return distance

    @staticmethod
    def g_score(node, ecolo):  # Adapt this to the tensor values

        # Dimension du co2 : 0 (valeur de co2)
        co2 = 18.0  # centaines de g co2 par km en moyenne -- ADJUST

        # Dimension du traffic : 3 (temps de retard de traffic entre 0 et 1 : 0 pas de traffic, 1 plein de traffic)
        traffic = float(ecolo[3][node.x][node.y])

        # Dimension de la vitesse : 1 (vitesse (30, 50 70, 100))
        vitesse = float(ecolo[1][node.x][node.y]) * (1 - traffic)
        if vitesse == 0: vitesse = 1

        # Dimension lumière/stop : 2 (1 : arrêt, 2 : feu de circulation)
        lum_stop = ecolo[2][node.x][node.y]

        # tps moyen à un arrêt (10 secondes)
        if lum_stop == 1:
            lum_stop = 0.1
        # feu de circulation
        # tps moyen à un feu de circulation est 75 secondes
        elif lum_stop == 2:
            lum_stop = 0.75

        g = co2 * lum_stop + co2 * 1 / vitesse
        # print(g, co2, lum_stop, vitesse)

        node.co2 = g
        node.waiting_time = traffic * 100 + lum_stop * 100  # en secondes
        # vitesse moyenne

        # print(f"g :{g}")
        return g + 1

    @staticmethod
    def create_grid(cols, rows):  # don't need this

        grid = []
        for _ in range(cols):
            grid.append([])
            for _ in range(rows):
                grid[-1].append(0)

        return grid

    @staticmethod
    def fill_grids(grid, cols, rows, obstacle_ratio=False, obstacle_list=False):

        for i in range(cols):
            for j in range(rows):
                grid[i][j] = Node(i, j)
                if obstacle_ratio == False:
                    pass
                else:
                    n = randint(0, 100)
                    if n < obstacle_ratio: grid[i][j].obstacle = True
        if obstacle_list == False:
            pass
        else:
            for i in range(len(obstacle_list)):  # populate the grid elements that are not streets
                grid[obstacle_list[i][0]][obstacle_list[i][1]].obstacle = True

        return grid

    @staticmethod
    def get_neighbors(grid, cols, rows):
        for i in range(cols):
            for j in range(rows):
                grid[i][j].add_neighbors(grid, cols, rows)
        return grid

    @staticmethod
    def start_path(open_set, closed_set, current_node, end, ecolo):

        best_way = 0
        for i in range(len(open_set)):
            # print(open_set[i].f, open_set[best_way].f)
            # Break ties according to H (be closest to the goal)
            if open_set[i].f <= open_set[best_way].f:
                if open_set[i].f == open_set[best_way].f:
                    # print(f"h : {open_set[i].h, open_set[best_way].h}")
                    if open_set[i].h < open_set[best_way].h:
                        best_way = i
                        # print(f"new best {open_set[best_way].f}")
                        # print(open_set[best_way].x,open_set[best_way].y)
                else:
                    best_way = i
                    # print(f"new best {open_set[best_way].f}")
                    # print(open_set[best_way].x,open_set[best_way].y)

        current_node = open_set[best_way]  # select lowest f value to continue
        final_path = []
        if current_node == end:
            temp = current_node
            while temp.previous:
                final_path.append(temp)
                temp = temp.previous

        open_set = AStar.clean_open_set(open_set, current_node)
        closed_set.append(current_node)
        neighbors = current_node.neighbors
        # current_node.g = AStar.g_score(current_node, ecolo)

        for neighbor in neighbors:
            if (neighbor in closed_set) or (neighbor.obstacle == True):
                continue
            else:
                # print(current_node.g, AStar.g_score(neighbor, ecolo))
                temp_g = current_node.g + AStar.g_score(neighbor, ecolo)
                # temp_g = current_node.g + 1
                control_flag = 0
                for k in range(len(open_set)):
                    if neighbor.x == open_set[k].x and neighbor.y == open_set[k].y:
                        # print(neighbor.x, neighbor.y, temp_g, open_set[k].g)
                        if temp_g < open_set[k].g:
                            open_set[k].g = temp_g
                            open_set[k].h = AStar.h_score(open_set[k], end)
                            open_set[k].f = open_set[k].g + open_set[k].h
                            open_set[k].previous = current_node
                        else:
                            pass
                        control_flag = 1
                if control_flag == 1:
                    pass
                else:
                    neighbor.g = temp_g
                    neighbor.h = AStar.h_score(neighbor, end)
                    neighbor.f = neighbor.g + neighbor.h
                    neighbor.previous = current_node
                    open_set.append(neighbor)

        return open_set, closed_set, current_node, final_path

    def run_AStar(self, obstacle_list, ecolo, start: [int, int], end: [int, int]):

        grid = AStar.create_grid(self.cols, self.rows)
        grid = AStar.fill_grids(grid, self.cols, self.rows, obstacle_list=obstacle_list)
        grid = AStar.get_neighbors(grid, self.cols, self.rows)
        open_set = []
        closed_set = []
        current_node = None
        final_path = []
        open_set.append(grid[start[0]][start[1]])
        end = grid[end[0]][end[1]]
        while len(open_set) > 0:
            open_set, closed_set, current_node, final_path = AStar.start_path(open_set, closed_set, current_node,
                                                                              end, ecolo)

            if len(final_path) > 0:
                break

        return final_path
