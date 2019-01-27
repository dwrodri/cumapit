import itertools
import math
import heapq
import sys
import numpy
from copy import deepcopy



def traveling_salesman(goal_list, robot_pose):  #  returns list of goals sorted in order they should be visited

    def calculate_total_distance(poses):  #  get total distance for list of locations
        total_distance = 0.0
        pose1 = poses.pop()
        while poses:
            pose2 = poses.pop()
            total_distance += math.sqrt(sum(map(lambda diff: diff**2, [x-y for x,y in zip(pose1, pose2)])))
            pose1 = pose2

        return total_distance

    possibilities = map(list, list(itertools.permutations(goal_list))) #  generate every possible ordering of locations
    distances = []  #  parallel array for distances
    for i in range(len(possibilities)):
        possibilities[i].insert(0, robot_pose)  # tack on the robot's original position because I suck at using lambdas properly
        distances.append(calculate_total_distance(deepcopy(possibilities[i])))  # get distance for that arrangement
    return possibilities[distances.index(min(distances))][1:] # return config with shortest distance


def a_star(start_index, end_index, lqtld):

    def cost_function(index, other_index):  # get cost of travel to center of cell
        if lqtld.tree[other_index][2] == 'B':  # don't allow travel in to obstacles
            return sys.maxsize
        row, col = lqtld.get_center_pixel_from_index(index)
        other_row, other_col = lqtld.get_center_pixel_from_index(other_index)
        return 0.5 * math.sqrt((other_row-row)**2 + (other_col-col)**2)

    def heuristic(index):
        return cost_function(index, end_index)  # scaled down for uncertainty

    print 'Going from {} to {}'.format(lqtld.binary_to_quaternary_string(lqtld.tree[start_index][0]), lqtld.binary_to_quaternary_string(lqtld.tree[end_index][0]))
    visited_pile = []  # heap of visited nodes
    shit_heap = [[0, None, start_index]]  # this is the priority queue, it keeps net distance from start to that node, previous node, and index in tree


    while (1<2):
        tracer = heapq.heappop(shit_heap)  # get most nearest known cell
        unvisited_neighbors = filter(lambda x: lqtld.tree[x][1] != 10, numpy.setdiff1d(lqtld.get_all_neighbor_indices(tracer[-1]), visited_pile))  # get univisted neighbors
        if tracer[-1] == end_index:
            print 'Found Goal! Breaking'
            visited_pile.append(tracer)   # put end_goal on tip of visited nodes
            break
        for cell_index in unvisited_neighbors:  # for the index of every neighboring cell in the LQT...
            if filter(lambda x: x[-1] == cell_index, shit_heap):  # if neighbor cell has already been added to shit_heap...
                heap_index = [i for i, j in enumerate(shit_heap) if j[-1]==cell_index].pop()  # get index of cell index in heap,
                new_cost = tracer[0] + cost_function(tracer[-1], cell_index) + heuristic(cell_index)  # calculate cost to travel to that cell
                if new_cost < shit_heap[heap_index][0]:  # if route from traced cell to neighboring cell is shorter than current known path, update
                    shit_heap[heap_index][0] = new_cost
                    shit_heap[heap_index][1] = tracer[-1]
                    heapq.heapify(shit_heap)  # re-sort cells based on update
            else:  # if neighbor cell is being examined for the first time, add it into the shit_heap
                heapq.heappush(shit_heap, [cost_function(tracer[-1], cell_index)+heuristic(cell_index), tracer[-1], cell_index])  # add the cell to the shit_heap
        visited_pile.append(tracer)  # push tracer onto visited_pile

    # generate shortest path from visited nodes
    print 'Amount of cells visited: {}'.format(len(visited_pile))
    visited_pile = visited_pile[::-1]
    backtrace = visited_pile.pop(0)
    shortest_path = []  # answer goes here
    arrived = False
    while (1<2):
        shortest_path.append(backtrace)  # put answer onto list
        if backtrace[1] is None:
            break
        prev_index = backtrace[1]  #tree index of cell used to get to backtrace
        backtrace = next((x for x in visited_pile if x[-1] == prev_index), None)
    return [x[-1] for x in shortest_path[::-1]]  # flip it for convenience
