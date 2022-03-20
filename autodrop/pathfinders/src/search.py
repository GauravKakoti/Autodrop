# Pathfinding
#	Filename: search.py
#	Authors:
#		Abdirahman Yassin 	- 154160030
#		Gaymer Barrios 		- 171898540
#	Description:
#		Implements heuristics to find paths
#	Reference:
#		http://modelai.gettysburg.edu/2017/pathfinding/index.html
# NOTES:
#    Print lines that end with #s are for debugging purposes
#        print("\n***\t road_config: ", road_config) ############################
#    The pieces of code we don't understand are surrounding by
#        # Don't know
#        # ******************************************
#            -code-
#        # ******************************************

from sys import stdout
from subprocess import Popen, PIPE
import random
import re
from heapq import heappop, heappush

def reconstruct_path(parents, current_state_action_time):
    #print("\n***\t Inside reconstruct_path") ############################    
    current_state,action,time = current_state_action_time
    path = [(current_state, action, time)]
    while path[-1] in parents:
        path.append(parents[path[-1]])
    path.reverse()
    return [current_state_action_time[0] for current_state_action_time in path]

# Generic search algorithm
# TODO: rewrite IDDFS so it continues where it left off (yield? or return state?)
# TODO: use make_graphviz_node
# TODO: make sure (using graphviz) that iddfs works
def search(start_state, depth_limit, heuristic, action_cost, openset_limit, is_goal_state,
           possible_transitions):
    #print("\n***\t Inside search") ############################    
    # states already checked
    closedset = []

    # a map of (state, action, time) => parent
    parents = {}

    # map of actual+estimated costs of going from every known state to goal state;
    # initialize with start state (F-score is simply the heuristic, no path cost)
    f_scores = {start_state: heuristic(start_state, 0, parents, None)}

    #print("\n***\t Inside search, initializing f_scores:",f_scores)
    #for x, y in f_scores.items():
    #    print("***\t",x, y)

    # map of actual costs of going from start state to every known state
    # initialize with start state (path cost = 0)
    g_scores = {start_state: 0}
    #print("\n***\t Inside search, initializing g_scores:",g_scores)
    
    # states that we know exist but have not checked;
    # need both openset and openheap because heaps won't let us check if a state is a member
    openset = [start_state]
    openheap = [(f_scores[start_state], (start_state, None, 0))]
    #print("\n***\t Inside search, initialize openset:", openset) ############################ 
    #print("\n***\t Inside search, initialize openheap:", openheap) ############################ 

    # keep track of the largest openset we ever had to maintain
    max_openset_size = 1
    #print("\n***\t Inside search, initialize max_openset_size:", max_openset_size) ############################ 
    
    #print("\n***\t Inside search, loop") ############################ 
    
    # while we still have a state to visit, and haven't found the goal
    while len(openset) > 0:
        #print("\n***\t Inside search, len(openset):", len(openset)) ############################ 
        
        # keep track of max_openset_size (just for benchmarking purposes)
        if max_openset_size < len(openset):
            max_openset_size = len(openset)

        #print("\n***\t Inside search, max_openset_size):", max_openset_size) ############################  
           
        # pick best state, make it the current state
        (val, (current_state, current_action, time)) = heappop(openheap)
        #print("\n***\t Inside search, (val, (current_state, current_action, time))):", (val, (current_state, current_action, time))) ############################ 
        
        # if next-best state is just as good, we'll need to randomly choose
        equally_good = [(val, (current_state, current_action, time))]
        #print("\n***\t Inside search, equally_good:", equally_good) ############################
        
        while len(openheap) > 0 and openheap[0][0] == val:
            (val2, (current_state2, current_action2, time2)) = heappop(openheap)
            #print("\n***\t Inside search, (val2, (current_state2, current_action2, time2)):", (val2, (current_state2, current_action2, time2))) ############################
            equally_good.append((val2, (current_state2, current_action2, time2)))
        random.shuffle(equally_good)
        (val, (current_state, current_action, time)) = equally_good[0]
        #print("\n***\t Inside search, equally_good:", equally_good) ############################
        
        # push all equally-good states not used
        for i in range(1, len(equally_good)):
            heappush(openheap, equally_good[i])

        openset.remove(current_state)

        #print("\n***\t Inside search, openset:", openset) ############################ 
        #print("\n***\t Inside search, openheap:", openheap) ############################ 
    
        # if we found the goal, we're done
        if is_goal_state(current_state):
            path = reconstruct_path(parents, (current_state, current_action, time))
            return (path, len(closedset), max_openset_size)

        # append current state to closed set so we don't visit it again
        closedset.append(current_state)
        #print("\n***\t Inside search, closedset:", closedset) ############################ 
        
        # for each possible next state from current state
        transitions = possible_transitions(current_state)
        #print("\n***\t Inside search, transitions (action, next_state):", transitions) ############################
        
        for (action, next_state) in transitions:

            # determine path cost to this next state
            tentative_g_score = g_scores[current_state] + action_cost(current_state, action, next_state)
            #print("\n***\t Inside search, tentative_g_score = g_scores + action_cost:", tentative_g_score) ############################

            # skip next states that we've already visited if this path isn't cheaper
            if next_state in closedset and \
               (next_state not in g_scores or g_scores[next_state] <= tentative_g_score):
                #print("\n***\t Inside search, Skipping:", next_state) ############################
                continue

            # skip if we have a depth limit and this node is too deep
            if depth_limit is not None and time > depth_limit:
                #print("\n***\t Inside search, depth_limit:", depth_limit,",adding node to closedset since is too deep, node:",next_state) ############################
                closedset.append(next_state)
                #print("\n***\t Inside search, closedset:", closedset) ############################ 
                continue

            # if this next state is new, or we found a cheaper way to get there, put it in the openset
            if next_state not in openset or tentative_g_score < g_scores[next_state]:

                # save the parentage and calculated scores for next state
                parents[(next_state, action, time+1)] = (current_state, current_action, time)
                #print("\n***\t Inside search, parents[(next_state, action, time+1)]:", parents) ############################ 
                g_scores[next_state] = tentative_g_score
                f_scores[next_state] = g_scores[next_state] + heuristic(next_state, time+1, parents, action)
                heappush(openheap, (f_scores[next_state], (next_state, action, time+1)))
                openset.append(next_state)
                #print("\n***\t Inside search, openset:", openset) ############################ 
                #print("\n***\t Inside search, openheap:", openheap) ############################ 

        # keep only best states if we have a limit (beam search / hillclimbing)
        if openset_limit is not None:
            new_openset = []
            new_openheap = []
            while len(new_openheap) < openset_limit and len(openheap) > 0:
                (val, (state, action, time)) = heappop(openheap)
                heappush(new_openheap, (val, (state, action, time)))
                new_openset.append(state)
            openset = new_openset
            openheap = new_openheap
            if len(openheap) == 1:
                #closedset = closedset[-openset_limit:] # keep only last N history
                closedset = closedset[-1:] # only one possible state to visit, may run out; so clear the history, allow covering old ground

        time += 1

    # if we made it here, we ran out of states to visit and never found the goal
    return (None, len(closedset), max_openset_size)