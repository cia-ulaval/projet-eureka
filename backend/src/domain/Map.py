import numpy as np
import json
import os


class Map:
    def __init__(self):
        self.traffic_probability: float = 0.3
        self.map: list[list[list[float]]] = self.__generate_map()
        self.width: int = np.shape(self.map)[1]
        self.height: int = np.shape(self.map)[2]
        self.obstacle_list: list[(int, int)] = self.__generate_obstacle_list()

        no_traffic = [[0 for j in range(self.height)] for i in range(self.width)]
        self.map.insert(3, no_traffic)

    def get_map(self) -> list[list[list[float]]]:
        return self.map

    def get_obstacle_list(self) -> list[[int, int]]:
        return self.obstacle_list

    def generate_traffic(self) -> list[list[float]]:
        traffic = [[0 for j in range(self.height)] for i in range(self.width)]
        for i in range(self.width):
            for j in range(self.height):
                if self.map[0][i][j] == 1:
                    s = np.random.sample()
                    if s <= self.traffic_probability:
                        t = np.random.sample()
                        traffic[i][j] = round(t, 3)
                    else:
                        traffic[i][j] = 0

        self.__set_traffic(traffic)
        return traffic

    def __generate_map(self):
        with open('./data/map.json') as file:
            map_loaded = json.load(file)
        return map_loaded

    def __set_traffic(self, traffic: list[list[float]]):
        try:
            self.map[3] = traffic
        except IndexError:
            self.map.insert(3, traffic)

    def __generate_obstacle_list(self) -> list[(int, int)]:
        obstacle_list = []
        for i in range(np.shape(self.map)[1]):
            for j in range(np.shape(self.map)[2]):
                if self.map[0][i][j] == 0:
                    obstacle_list.append([i, j])
        return obstacle_list
