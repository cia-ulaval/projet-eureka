from astar import *
import json  

#Get map
with open('map.json') as file:
    ecolo = json.load(file) #22 x 19
#print(len(ecolo[1]))

#Get obstacle_list
obstacle_list = get_obstacle_list(ecolo)

#Generate traffic
traffic = generate_traffic(ecolo,0.3) #this is random, do this once and save it
ecolo.append(traffic)

#Run the AI - AStar (start to end)
rows = 22
cols = 19
start = [4,9]
end = [21,18]
astar = AStar(rows,cols,start,end)
path = astar.run_AStar(obstacle_list, ecolo)
print(get_stats_from_AStar(path,end))


#Testing diejkstra
"""
dijsktra = Dijsktra(25,25,[0,0],[24,24])
path = dijsktra.run_Dijsktra(obstacle_list, ecolo) #this one is optimal (actually called Dijsktra's algo)
print(get_stats_from_AStar(path))
"""

#Testing must visit path
#Based on the closest must visit node next, and on getting shortest path between each node
#must_visit = [[0,0],[3,3],[5,4],[8,8],[10,11],[24,24]] #must contain start and end
#must_visit = [[0,0],[8,8],[5,4],[3,3],[10,11],[24,24]]

#print(path_through_specific_nodes(must_visit, obstacle_list, ecolo))