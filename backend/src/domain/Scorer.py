import numpy as np
from backend.src.domain.AStar import AStar


class Scorer:
    def __init__(self):
        self.CO2_value = 18 # g/km
    def get_score(self, map_id: int, path: list[tuple[float, float]]) -> float:
        return 0.5

    # Get stats from the AStar path (they have special properties)
    def get_stats_from_AStar(self, path, end, add_last=True):
        """
              input
                  path : list des coordonnées (x,y) des noeuds visités
                  end : position finale
                  add_last : Ajouter manuellement la fin du trajet dans la liste finale
              output
                  solution_path : liste du trajet emprunté
                  co2_total : total co2 sur le trajet (g/km)
                  waiting_time_total : temps d'attente total (secondes)
        """
        # Total co2, total waiting time and final path in a list
        co2_total = 0
        solution_path = []
        waiting_time_total = 0

        for p in path[::-1]:  # reverse from start to end
            solution_path.append((p.x, p.y))

            co2_total += p.co2
            waiting_time_total += p.waiting_time

            # print(p.co2, p.waiting_time)
        if add_last:
            x, y = end
            solution_path.append((x, y))  # add end state

        return co2_total, waiting_time_total, solution_path

    # Get stats from any path
    def get_stats_from_path(self, path, ecolo):
        """
          inputs
            path : list of (x,y) coordinates that show the path taken ((x,y) must match with the grid map)
            ecolo : tenseur des informations relatives à la carte
          output
            total co2 (en g/km) and waiting time (en secondes) on this path
        """
        co2_total = 0
        wait_total = 0

        for x, y in path:
            # Dimension du traffic : 3 (temps de retard de traffic entre 0 et 1. 0 : pas de traffic, 1 plein de traffic)
            traffic = float(ecolo[3][x][y])

            # Dimension de la vitesse : 1 (vitesse (30, 50 70, 100))
            vitesse = float(ecolo[1][x][y]) * (1 - traffic)

            # Dimension lumière/stop : 2
            lum_stop = ecolo[2][x][y]
            # Stop
            if lum_stop == 1:
                lum_stop = 0.1
            # feu de circulation
            elif lum_stop == 2:
                lum_stop = 0.75

                # co2 total
            c = self.CO2_value * (lum_stop + 1 / vitesse)
            # print(lum_stop, vitesse, 1/vitesse, traffic, c)

            # wait total
            w = 100 * (lum_stop + traffic)

            co2_total += c
            wait_total += w

        return co2_total, wait_total

    # -------------- Shortest path trough particular nodes ----------------------

    # Get shortest cost path going throush particular nodes (hard coded way)
    def path_through_specific_nodes(self, must_visit, obstacle_list, ecolo):
        """
          Assuming we go to the physically closest node first,
          We compute the least cost path between each must visit node
          input
            must_visit : list of nodes to go through in the path
          output
            path : final path that goes through all must visit nodes
            total_c02 : total co2 cost of the path
            total_wait : total wait time during the path
        """
        # Order the must visit by closest to start point
        start = must_visit[0]
        end = must_visit[-1]
        distances = []

        for x, y in must_visit[1:-1]:
            distances.append(np.sqrt((x - start[0]) ** 2 + (y - start[1]) ** 2))
        inds = np.argsort(distances)

        tmp = must_visit[1:-1]

        must_visit = [tmp[i] for i in inds]
        must_visit.append(end)
        must_visit = [start] + must_visit

        # initialisation
        path = []
        total_co2 = 0
        total_wait = 0

        # Find smallest cost path between each must visit node
        for v, u in zip(must_visit, must_visit[1:]):
            x, y = v
            end_x, end_y = u
            # print(x,y,end_x,end_y)
            astar = AStar(25, 25, [x, y], [end_x, end_y])
            p = astar.run_AStar(obstacle_list, ecolo)

            c, w, s = self.get_stats_from_AStar(p, u, add_last=False)
            total_co2 += c
            total_wait += w

            # Add to final path
            for e in s:
                path.append(e)

        return total_co2, total_wait, path