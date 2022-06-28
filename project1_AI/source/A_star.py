##############################################################################

# import packages

##############################################################################


from queue import PriorityQueue as pq

import numpy as np

import make_obstacle as mo

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

# check if neighbor is in frontier without popping it
def check_in_frontier(neighbor, frontier):
    for i in range(frontier.qsize()):
        if (frontier.queue[i][1] == neighbor):
            return 1
    return 0   


# A* function

def astar(array, start, goal):
    # all place can be move in matrix 
    move = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]

    explored_set = set() # inial a set

    came_from = {}

    g_value = {start:0} # initial g value ( the real cost)

    h_value = {start:heuristic(start, goal)} # initial h value (the heuristic function)

    #create a frontier by PriorityQueue 
    frontier = pq()
    
    frontier.put((h_value[start], start))

    # while frontier is not empty do:
    while not frontier.empty():
       
        #take the first element in frontier anbd check it
        current = frontier.get()[1]
        # if find the goal then create the path
        if current == goal:
            path = []

            while current in came_from: # take the path from the goal came from
                path.append(current) # add vertex to path
                current = came_from[current]

            return path

        explored_set.add(current) # if current state is not goal state then add to explored_set

        #move all valid move
        for i, j in move:
            #move to neighbor
            neighbor = current[0] + i, current[1] + j

            #calc the f value of the current state
            f_value = g_value[current] + heuristic(current, neighbor)

            #ignore invalid place
            if (valid_place(array, neighbor) == 0):
                continue

            #ignore if the neighbor has in explored_set and it has f value larger than ....
            if neighbor in explored_set and f_value >= g_value.get(neighbor, 0):
                continue
 
            #if .. or neighbor is not in frontier than:
            if  f_value < g_value.get(neighbor, 0) or check_in_frontier(neighbor, frontier) == 0:
                
                came_from[neighbor] = current
                g_value[neighbor] = f_value
                h_value[neighbor] = f_value + heuristic(neighbor, goal)

                #add both neighbor and the h value to the frontier
                frontier.put((h_value[neighbor], neighbor))
 

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