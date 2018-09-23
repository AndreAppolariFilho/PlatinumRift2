import sys
import math
import random
#
from scipy.sparse.csgraph import minimum_spanning_tree
id_enemy = 0
id_friendly = 0
#G = nx.Graph()
# player_count: the amount of players (always 2)
# my_id: my player ID (0 or 1)
# zone_count: the amount of zones on the map
# link_count: the amount of links between all zones
def dijsktra(graph, initial, graph_properties):
    # shortest paths is a dict of nodes
    # whose value is a tuple of (previous node, weight)
    shortest_paths = {initial: (None, 0)}
    current_node = initial
    visited = set()
    
    while True:
        for v in graph[current_node]:
            if graph_properties[v]['owner_id'] == -1 or graph_properties[v]['owner_id'] == 1:
                break
        visited.add(current_node)
        destinations = graph[current_node]
        weight_to_current_node = shortest_paths[current_node][1]

        for next_node in destinations:
            weight = 1 + weight_to_current_node
            if next_node not in shortest_paths:
                shortest_paths[next_node] = (current_node, weight)
            else:
                current_shortest_weight = shortest_paths[next_node][1]
                if current_shortest_weight > weight:
                    shortest_paths[next_node] = (current_node, weight)
        
        next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited}
        if not next_destinations:
            return "Route Not Possible"
        # next node is the destination with the lowest weight
        current_node = min(next_destinations, key=lambda k: next_destinations[k][1])
    
    # Work back through destinations in shortest path
    path = []
    while current_node is not None:
        path.append(current_node)
        next_node = shortest_paths[current_node][0]
        current_node = next_node
    # Reverse path
    path = path[::-1]
    return path
    
def find_path(graph, start_vertex, graph_properties, path=None):
    if path == None:
        path = []
    #graph = self.__graph_dict
    path = path + [start_vertex]
    for v in graph[start_vertex]:
        if graph_properties[v]['owner_id'] == -1 or graph_properties[v]['owner_id'] == 1:
            return path
    if start_vertex not in graph:
        return None
    for vertex in graph[start_vertex]:
        if vertex not in path:
            extended_path = find_path(graph,vertex, 
                                            graph_properties, 
                                             path)
            if extended_path: 
                return extended_path
    return None
def dfs_iterative(graph, start, graph_properties):
    stack, path = [start], []

    while stack:
        vertex = stack.pop()
        if vertex in path:
            continue
        path.append(vertex)
        if vertex!=start:
            for v in graph[vertex]:
                if graph_properties[v]['owner_id'] == -1 or graph_properties[v]['owner_id'] == 1:
                    return path
        for neighbor in graph[vertex]:
            stack.append(neighbor)

    return path
    
def dfs(graph, start, graph_properties, visited):
    #visited, stack = list(), [start]
    if start not in visited:
        visited.append(start)
        
        for n in graph[start]:
            dfs(graph,n, graph_properties, visited)
    return visited
    '''
    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            #visited.add(vertex)
            visited.append(vertex)
            stack.extend( visited)
    '''
    return visited
    
def prim(G,start):
    pq = PriorityQueue()
    for v in G:
        v.setDistance(sys.maxsize)
        v.setPred(None)
    start.setDistance(0)
    pq.buildHeap([(v.getDistance(),v) for v in G])
    while not pq.isEmpty():
        currentVert = pq.delMin()
        for nextVert in currentVert.getConnections():
          newCost = currentVert.getWeight(nextVert)
          if nextVert in pq and newCost<nextVert.getDistance():
              nextVert.setPred(currentVert)
              nextVert.setDistance(newCost)
              pq.decreaseKey(nextVert,newCost)
              
def bfs(graph, start, graph_properties):
    queue = [[start]]
    visited = set()
    while queue:
        path = queue.pop(0)
        vertex = path[-1]    
        '''
        if vertex!=start:
            for v in graph[vertex]:
                if graph_properties[v]['owner_id'] == -1 or graph_properties[v]['owner_id'] == 1:
                    return path
        '''
        if vertex == id_enemy:
            return path
        elif vertex not in visited:
            for current_neighbour in graph[vertex]:
                new_path = list(path)
                new_path.append(current_neighbour)
                queue.append(new_path)
            visited.add(vertex)
    return path
    
def bfs_path(graph, start, end, graph_properties):
    queue = [[start]]
    visited = set()
    while queue:
        path = queue.pop(0)
        vertex = path[-1]    
        if vertex == end:
            return path
        elif vertex not in visited:
            for current_neighbour in graph[vertex]:
                new_path = list(path)
                new_path.append(current_neighbour)
                queue.append(new_path)
            visited.add(vertex)
    return path

def bfs_deviate(graph, start, end, graph_properties):
    queue = [[start]]
    visited = set()
    while queue:
        path = queue.pop(0)
        vertex = path[-1]    
        if not graph_properties[vertex]['is_leaf_path']:
            return path
        elif vertex not in visited:
            for current_neighbour in graph[vertex]:
                new_path = list(path)
                new_path.append(current_neighbour)
                queue.append(new_path)
            visited.add(vertex)
    return path
    
def dfs_path(graph, start, end, graph_properties):
    stack, path = [start], []

    while stack:
        vertex = stack.pop()
        if vertex in path:
            continue
        path.append(vertex)
        if vertex!=start:
            for v in graph[vertex]:
                if graph_properties[v]['owner_id'] == -1 or graph_properties[v]['owner_id'] == 1:
                    return path
        for neighbor in graph[vertex]:
            stack.append(neighbor)

    return path
    
graph = {}
map_properties = {}
player_count, my_id, zone_count, link_count = [int(i) for i in input().split()]

for i in range(zone_count):
    # zone_id: this zone's ID (between 0 and zoneCount-1)
    # platinum_source: Because of the fog, will always be 0
    zone_id, platinum_source = [int(j) for j in input().split()]
    
for i in range(link_count):
    zone_1, zone_2 = [int(j) for j in input().split()]
    
    try:
        graph[zone_1].append(zone_2)
    except:
        graph[zone_1] = []
        graph[zone_1].append(zone_2)
        
    try:
        graph[zone_2].append(zone_1)
    except:
        graph[zone_2] = []
        graph[zone_2].append(zone_1)
    try:
        map_properties[zone_1]    
    except:
          map_properties[zone_1]={
            'owner_id':-1,
            'quantity':[0, 0],
            'is_visible':0,
            'd_base':999999,
            'weight':0,
            'is_leaf_path':False,
            'd_base_enemy':999999,
            'last_seen':0
        }
    try:
        map_properties[zone_2]    
    except:
          map_properties[zone_2]={
            'owner_id':-1,
            'quantity':[0, 0],
            'is_visible':0,
            'd_base':99999,
            'weight':0,
            'is_leaf_path':False,
            'd_base_enemy':99999,
            'last_seen':0
        }

# game loop
paths = {}
inibidors_friendly = True
inibidors_enemy = True
paths_calculated = {}
distances = {}
paths_calculated = []
last_respawn = 10
first_iteration = True
while True:
    my_platinum = int(input())  # your available Platinum
    possible_route = []
    players_owners = []
    last_play = []
    remove = False
    num_computations = 0
    in_attack = []
    for i in range(zone_count):
        # z_id: this zone's ID
        # owner_id: the player who owns this zone (-1 otherwise)
        # pods_p0: player 0's PODs on this zone
        # pods_p1: player 1's PODs on this zone
        # visible: 1 if one of your units can see this tile, else 0
        # platinum: the amount of Platinum this zone can provide (0 if hidden by fog)
        dests_ids = []
        z_id, owner_id, pods_p0, pods_p1, visible, platinum = [int(j) for j in input().split()]
        if my_id == 1 :
            pods_p0, pods_p1 = pods_p1, pods_p0
        dest_id = 0
        map_properties[z_id]['last_seen']+=1
        map_properties[z_id]['owner_id'] = owner_id
        if my_id == 1 and owner_id == 0:
            map_properties[z_id]['owner_id'] = 1
        if my_id == 1 and owner_id == 1:
            map_properties[z_id]['owner_id'] = 0
        if inibidors_friendly and pods_p0 > 0:
            id_friendly = z_id
            inibidors_friendly = False
        if inibidors_enemy and pods_p1 > 0:
            id_enemy = z_id
            inibidors_enemy = False
        map_properties[z_id]['quantity'] = [pods_p0, pods_p1]
        map_properties[z_id]['is_visible'] = visible
        if map_properties[z_id]['last_seen'] >=10:
            map_properties[z_id]['is_visible'] = False
            #map_properties[z_id]['owner_id'] = -1
           # print('LAST SEEN', file=sys.stderr)
        if z_id != id_friendly or (z_id == id_friendly and (last_respawn>=2 or map_properties[z_id]['quantity'][0]>=5)):
            
            if map_properties[z_id]['quantity'][0] > 0 and\
                map_properties[z_id]['quantity'][1] > 0:
                    if map_properties[z_id]['quantity'][0] < map_properties[z_id]['quantity'][1] > 0:
                        in_attack.append(z_id)
            else:
                if map_properties[z_id]['quantity'][0] > 0:
                    
                    dists = []
                    if z_id != id_friendly:
                        for adjacent in graph[z_id]:
                            #map_properties[z_id]['quantity'][0] = 0
                            if map_properties[adjacent]['owner_id']==1 or map_properties[adjacent]['owner_id']==-1 and not map_properties[adjacent]['is_leaf_path']:  
                                dests_ids.append(adjacent)
                                map_properties[adjacent]['weight'] = map_properties[z_id]['weight'] + 1
                                print('dest_id0 ', adjacent, file=sys.stderr)
                    else:
                        for adjacent in graph[z_id]:
                            dests_ids.append(adjacent)
                            #map_properties[z_id]['quantity'][0] = 0
                            if not map_properties[adjacent]['is_leaf_path']:
                                map_properties[adjacent]['weight'] = map_properties[z_id]['weight'] + 1
                                paths_calculated.append([{z_id:adjacent}])
                                first_iteration = False
                                print('dest_id1 ', adjacent, file=sys.stderr)
                    #print('dests_ids ',dests_ids, file=sys.stderr)        
                    if dests_ids == []:
                        dists = []
                        for adjacent in graph[z_id]:
                            if map_properties[adjacent]['owner_id'] == 0 or map_properties[adjacent]['owner_id'] == 1 or map_properties[adjacent]['owner_id'] == -1:
                                
                                try:
                                    dist_future = distances[adjacent]
                                    dist_now = distances[z_id]
                                except:
                                    dist_future = {
                                        'to_enemy' : len(bfs_path(graph, adjacent, id_enemy,map_properties)),
                                        'to_base' : len(bfs_path(graph, adjacent, id_friendly,map_properties))
                                        
                                    }
                                    dist_now = {
                                        'to_enemy' : len(bfs_path(graph, z_id, id_enemy,map_properties)),
                                        'to_base' : len(bfs_path(graph, z_id, id_friendly,map_properties))
                                    }
                                    distances[adjacent] = dist_future
                                    distances[z_id] = dist_now
                                num_computations+=1
                                #print(adjacent,'->',dist_future['to_base'], ' ',z_id,'->',dist_now['to_base'], file=sys.stderr)
                                
                                
                                if dist_future['to_enemy']<dist_now['to_enemy']  and dist_future['to_base']>dist_now['to_base'] and not map_properties[adjacent]['is_leaf_path']:
                                    dests_ids.append(adjacent)
                                    print('dest_id2 ', adjacent, file=sys.stderr)
                                    map_properties[adjacent]['weight'] = map_properties[z_id]['weight'] + 1
                                    #dists.append({'id':adjacent, 'dist':dist_future['to_enemy']})
                                
                    if dests_ids == []:
                        for adjacent in graph[z_id]:
                            if map_properties[adjacent]['owner_id'] == 0 or map_properties[adjacent]['owner_id'] == 1 or map_properties[adjacent]['owner_id'] == -1:
                                    
                                try:
                                    dist_future = distances[adjacent]
                                    dist_now = distances[z_id]
                                except:
                                    dist_future = {
                                        'to_enemy' : len(bfs_path(graph, adjacent, id_enemy,map_properties)),
                                        'to_base' : len(bfs_path(graph, adjacent, id_friendly,map_properties))
                                            
                                    }
                                    dist_now = {
                                        'to_enemy' : len(bfs_path(graph, z_id, id_enemy,map_properties)),
                                        'to_base' : len(bfs_path(graph, z_id, id_friendly,map_properties))
                                    }
                                    distances[adjacent] = dist_future
                                    distances[z_id] = dist_now
                                num_computations+=1
                                    
                                    
                                if dist_future['to_base']>dist_now['to_base'] and not map_properties[adjacent]['is_leaf_path']:
                                    dests_ids.append(adjacent)
                                    map_properties[adjacent]['weight'] = map_properties[z_id]['weight'] + 1
                                    print('dest_id3 ', adjacent, file=sys.stderr)
                                    #dists.append({'id':adjacent, 'dist':dist_future['to_enemy']})
                                    
                    if dests_ids == []:
                        map_properties[z_id]['is_leaf_path'] = True
                        dests_ids.append(bfs_deviate(graph, z_id, 0, map_properties)[1])
                        print('is_leaf_path ', z_id, file=sys.stderr)
                        '''
                        if dests_ids==[]:
                            dest_id = graph[z_id][random.randint(0, len(graph[z_id])-1)]
                            dests_ids.append(dest_id)
                            #path = bfs_path(graph, z_id, id_friendly, map_properties)
                            #map_properties[dest_id]['weight'] = -99999999+1*map_properties[dest_id]['weight']
                        
                            #for i in path[1:len(path)-1]:
                               
                            #    count -= 1
                            #    print(i, ' ',map_properties[i], file=sys.stderr)
                        '''    
        else:
            last_respawn += 1
        if map_properties[z_id]['quantity'][0]>0:
            for d_id in dests_ids:
                #print('pods ',math.ceil(pods_p0/len(dests_ids)), file=sys.stderr)
                
                if map_properties[z_id]['quantity'][0] > 0 and not map_properties[d_id]['is_leaf_path']:
                    if z_id == id_friendly:
                        last_respawn = 0
                    print(z_id, ' ' , d_id, file=sys.stderr)
                    map_properties[d_id]['last_seen'] = 0
                    #map_properties[z_id]['quantity'][0] = 0
                    map_properties[z_id]['quantity'][0] -= math.ceil(pods_p0/len(dests_ids))
                    possible_route.append([z_id, d_id, math.ceil(pods_p0/len(dests_ids))])
            #print(possible_route, file=sys.stderr)
    #print(possible_route, file=sys.stderr)
    
    for in_attack_id in in_attack:
        count = 0
        for route in possible_route:
            if count == 10:
                break
            if route[0] != in_attack_id:
                #print('attacking', file=sys.stderr)
                path = bfs_path(graph, route[0], in_attack_id,map_properties)
                dist = len(path)
                if dist < 30:
                    route[1] = path[1]
                    count+=1
    '''
    for node in map_properties:
        dests_ids = []
    '''    
    str_result = ''
    for possible in possible_route:
        str_result+=str(possible[2])+" "+str(possible[0])+" "+str(possible[1])
        str_result+=" "
    print(str_result[:len(str_result)-1])
    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)
    # first line for movement commands, second line no longer used (see the protocol in the statement for details)
    #print("WAIT")
    print("WAIT")
