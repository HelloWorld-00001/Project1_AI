##############################################################################

# import packages

##############################################################################


import queue as qe

import numpy as np

import make_obstacle as mo

import heapq

import matplotlib.pyplot as plt

from matplotlib.pyplot import figure

 


# initial map ( matrix)
rows = 20
cols = 20
grid = np.zeros((rows, cols))
vt = np.array([11, 1, 11, 6, 14, 6, 14, 1])
vt2 = np.array([4, 4, 5, 9, 8, 10, 9, 5])
vt3 = np.array([8, 12, 8, 17, 13, 12])
mo.make_obstacle(grid, vt)
mo.make_obstacle(grid, vt2)
mo.make_obstacle(grid, vt3)

# create start point and goal

start = (0,0)

goal = (8,19)


 
# the heuristic function
def heuristic(a, b):
    # a[x, y], b[x, y] calc mahatan distance by pytago
    return np.linalg.norm(np.array(a)-np.array(b))

 
def valid_place(matrix, neighbor):
    if 0 <= neighbor[0] < matrix.shape[0]:
        if 0 <= neighbor[1] < matrix.shape[1]:                
            if matrix[neighbor[0]][neighbor[1]] == 1:
                return 0
        else:
            return 0
    else:
        return 0
    return 1

# A* function

def astar(array, start, goal):
    # all place can be move in matrix 
    neighbors = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]

    explored_set = set() # inial a set

    came_from = {}

    g_value = {start:0}

    h_value = {start:heuristic(start, goal)}

    oheap = []

    heapq.heappush(oheap, (h_value[start], start))
 

    while oheap:

        current = heapq.heappop(oheap)[1]
        # check if current sate is goal state
        if current == goal:
            #make the path from start to goal
            path = []
            
            while current in came_from:

                path.append(current)

                current = came_from[current]

            return path

        explored_set.add(current)

        for i, j in neighbors:

            neighbor = current[0] + i, current[1] + j

            f_value = g_value[current] + heuristic(current, neighbor)

            #ignore invalid place
            if (valid_place(array, neighbor) == 0):
                continue


            if neighbor in explored_set and f_value >= g_value.get(neighbor, 0):

                continue
 
            print(neighbor)
            if  f_value < g_value.get(neighbor, 0) or neighbor not in [i[1]for i in oheap]:

                came_from[neighbor] = current

                g_value[neighbor] = f_value

                h_value[neighbor] = f_value + heuristic(neighbor, goal)

                heapq.heappush(oheap, (h_value[neighbor], neighbor))
 

    return False

route = astar(grid, start, goal)

route = route + [start]

route = route[::-1]

print(route)


##############################################################################

# plot the path

##############################################################################

 

#extract x and y coordinates from route list

x_coords = []

y_coords = []

for i in (range(0,len(route))):

    x = route[i][0]

    y = route[i][1]

    x_coords.append(x)

    y_coords.append(y)

# plot map and path

fig, ax = plt.subplots(figsize=(20,20))

ax.imshow(grid, cmap=plt.cm.Dark2)

ax.scatter(start[1],start[0], marker = "*", color = "yellow", s = 200)

ax.scatter(goal[1],goal[0], marker = "*", color = "red", s = 200)

ax.plot(y_coords,x_coords, color = "black")
plt.axis([0, 20, 0, 20])

plt.show()