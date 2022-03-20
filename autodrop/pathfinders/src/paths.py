# Pathfinding
#	Filename: paths.py
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

from search import search
from PIL import Image
import random
import os


# The width and height of the .bmp input image file
# These values are initialized by default to 50
# but the program gets the actual width and height of the input image file
width = 50
height = 50

# For the .bmp input image file (opening, getting pixels, etc)
terrain_img = None

# These are the coordinates of a blue pixel in the input image file
# This values are given as an argument to the search function
init_x = None
init_y = None

# These are the coordinates of a green pixel in the input image file
goal_x = None
goal_y = None


# Decrease the grayscale after each path
#decrease_grayscale = 1

# The locations of blue pixels in the .bmp input image file
possible_initial_states = []

# The locations of green pixels in the .bmp input image file
possible_goal_states = []

# The locations of red pixels in the .bmp input image file
# Our path cannot walk through red pixels, it should go around them when necessary
terrain_impassible = [] # cache of impassible locations

# An array containing the cost of each pixel in the .bmp input image file
terrain_cost = {}   

# Don't know
# ******************************************
terrain_cost_factor = 500.0
# ******************************************



# ****************************************************************
#                     Needed functions
# ****************************************************************
# This function will extract information from the input image file
# It will find the location of the pixels that are possible initial states, possible goal states
# and that are impassable (we cannot walk through them)
# It will fill in a terrain cost depending on how dark or white a pixel is (grayscale)
# This terrain cost array will be a 2D array representing the cost of each pixel
# from the input image
def establish_terrain(img_filename):
    #print("\n***\t Inside establish_terrain, img_filename: ", img_filename) ############################
    
    global terrain_img, terrain_cost, terrain_impassible, width, height, possible_initial_states, possible_goal_states
    
    possible_initial_states = []    # When we found a blue pixel, we add it here to know the location
    
    # The x,y location of a green pixel in the .bmp image
    possible_goal_states = []   # When we found a green pixel, we add it here to know the location
    terrain_cost = {}

    # Get the location of input image
    script_dir = os.path.dirname(__file__)  # Absolute directory of this script
    relative_path = "../input_files/" + img_filename
    abs_file_path = os.path.join(script_dir, relative_path)

    terrain_img = Image.open(abs_file_path)  # Open the image file
    terrain_impassible = [] # When we find a red pixel, we add it here to know the location
    
    # This will have the width and height of the .bmp input image file
    # By default, width and height are initialized to 50
    (width, height) = terrain_img.size  # This returns the size of the img_filename
    
    # Allocates the storage for the image and loads the pixel data
    # Closes the file associated with the image
    pixels = terrain_img.load()
    
    # Looping through each pixel in the picture
    # Loops from 0 width to max height
    # so it analyzes pixels vertically
    #print("***\t\t image width: ", width) ############################
    #print("***\t\t image height: ", height) ############################
    for x in range(0, width):
        for y in range(0, height):
            # For the current pixel (x,y)
            # get the red, green, blue color components
            (r,g,b) = pixels[x,y]
            #print("***\t\t r:",r,",g:",g,"b:", b) ############################
            
            # If the amount of red equals the amount of green
            # and the amount of green equals the amount of blue
            # then we have a grayscale
            if r == g and g == b: # grayscale, terrain cost
                # we can use either r, g or b to save as terrain_cost as they have the same value
                # the terrain_cost of pixel (x,y) = r
                terrain_cost[(x,y)] = r
                #print("***\t\t pixel(",x,",",y,") is grayscale") ############################
                #print("***\t\t terrain_cost[(",x,",",y,")] =", terrain_cost[(x,y)]) ############################
            #elif r >= 220 and g == 0 and b == 0: # red, impassible
            elif r >= 220: # red, impassible
                # we have a red pixel, represented by -1 in the terrain_cost array
                terrain_cost[(x,y)] = -1
                # add the pixel location to the terrain_impassible array
                terrain_impassible.append((x,y))
                #print("***\t\t pixel(",x,",",y,") is red") ############################
                #print("***\t\t terrain_cost[(",x,",",y,")] =", terrain_cost[(x,y)]) ############################
                #print("***\t\t pixel added to terrain_impassible") ############################
            elif r == 0 and g == 255 and b == 0: # green, goal point
                # we have a green pixel, represents a goal point, add it to possible_goal_states array
                possible_goal_states.append((x,y))
                # The cost of a goal point is 0
                terrain_cost[(x,y)] = 0
                #print("***\t\t pixel(",x,",",y,") is green") ############################
                #print("***\t\t terrain_cost[(",x,",",y,")] =", terrain_cost[(x,y)]) ############################
                #print("***\t\t pixel added to possible_goal_states") ############################
            elif r == 0 and g == 0 and b == 255: # blue, starting point
                # we have a blue pixel, represents a possible initial state
                possible_initial_states.append((x,y))
                # The terrain_cost is set to -1, same as a red pixel
                terrain_cost[(x,y)] = -1
                #print("***\t\t pixel(",x,",",y,") is blue") ############################
                #print("***\t\t terrain_cost[(",x,",",y,")] =", terrain_cost[(x,y)]) ############################
                #print("***\t\t pixel added to possible_intial_states") ############################
                
# x1_y1 and x2_y2 are tuples
# then the function breaks up the tuple into x,y coordinates for two points
# and finds the distance between the two points
def dist(x1_y1, x2_y2):
    #print("\n***\t Inside dist") ############################
    # Get the first point
    x1,y1 = x1_y1
    # Get the second point
    x2,y2 = x2_y2
    
    # Calculate the distance between point 1 and point 2
    distance = ((x2-x1)**2 + (y2-y1)**2)**0.5
    #print("***\t\t The distance from (% .2f, % .2f) to (% .2f, % .2f) is % .4f" %(x1, y1, x2, y2, distance))
    return distance



# Using the global variable possible_initial_states
# that contains all the pixels(x,y) coordinates of all blue pixels
# from the input image,
# initializes the x and y coordinate to one of these blue pixels location
def make_initial_state():
    #print("\n***\t Inside make_initial_state") ############################
    global possible_initial_states, init_x, init_y
    
    # Pick a random blue pixel (x,y) from the possible initial states array
    (init_x, init_y) = random.choice(possible_initial_states)
    #print("***\t\t init_x:", init_x, ", init_y:", init_y) ############################
    
# This function will pick a goal location from the possible goal states
# These states are the x,y coordinates of green pixels in the input image
# This function also checks that the initial state and the goal state are at least
# 10 pixels from each other, otherwise, it will pick a new goal state
def make_goal_state():
    #print("\n***\t Inside make_goal_state") ############################
    global possible_goal_states, goal_x, goal_y, init_x, init_y
    
    # Pick a random green pixel (x,y) from the possible goal states
    (goal_x, goal_y) = random.choice(possible_goal_states)
    
#     # This loops checks that the starting position and the goal position
#     # are at least 10 pixels away from each other
#     while dist((init_x, init_y), (goal_x, goal_y)) < 10:
#         # The goal is too close to the starting position, get a new random goal x,y location
#         (goal_x, goal_y) = random.choice(possible_goal_states)
    
    
    #print("***\t\t goal_x:", goal_x, ", goal_y:", goal_y) ############################



# Takes in a tuple x_y that contains the coordinates of a point
# Breaks up the tuple into x and y and compares this point to th
# x and y coordinates of the goal
# if the given point is the goal, then it returns true
# This function is given as an argument to the search function
def is_goal_state(x_y):
    #print("\n***\t Inside is_goal_state") ############################
    # Break the tuple into x and y
    x,y = x_y
    # Compare the point with the goal point
    # If equal return True
    result = x == goal_x and y == goal_y
    #print("***\t\t Comparing",x_y,"with",(goal_x,goal_y),"has the result:",result) ############################
    return result



# This function returns the cost of moving from point 1 to point 2
# Equivalent to g(n)
# action cost from point 1 to point 2 is terrain cost on point 2
def action_cost_true(x1_y1, action, x2_y2):
    #print("\n***\t Inside action_cost_true") ############################
    #x1,y1 = x1_y1
    x2,y2 = x2_y2
    global terrain_cost, terrain_cost_factor
    action_cost = 1.0 + terrain_cost[(x2, y2)] / terrain_cost_factor
    #print("\n***\t The action cost",x1_y1,"to",x2_y2,"is:",action_cost) ############################
    return action_cost


# This function is given as an argument to the search function
# From the given point x_y we break it up into x, y
# Then we check whether we can move up,down, left, right or diagonally
# We add all possible moves to transitions[] and return it
def possible_transitions(x_y):
    #print("\n***\t Inside possible_transitions") ############################
    # Break up x_y into x,y
    x,y = x_y
    
    # width and height of the input image
    # terrain_cost is the array containing the cost of each position (pixel)
    # in the input image
    global terrain_cost, width, height
    
    # An array containing the possible moves we can make from the given point
    transitions = []
    
    if x > 0 and terrain_cost[(x-1,y)] >= 0:
        # If the given point x > 0 that means we can move left (west)
        # on the 2d terrain_cost array
        # Append this possible move to transitions
        transitions.append(('west', (x-1, y)))
    if x < (width-1) and terrain_cost[(x+1,y)] >= 0:
        # If x isn't at the right corner (top or bot)
        # and the terrain cost of the pixel to the right of x is >= 0
        # then this means we can move east
        # Remember that if terrain_cost = 0, then the pixel is a goal
        # if terrain_cost = -1, then the pixel is an initial state pixel
        # otherwise, terrain_cost = r, and it's a grayscale pixel
        transitions.append(('east', (x+1, y)))
    if y > 0 and terrain_cost[(x,y-1)] >= 0:
        # We can move up
        transitions.append(('north', (x, y-1)))
    if y < (height-1) and terrain_cost[(x,y+1)] >= 0:
        # We can move down
        transitions.append(('south', (x, y+1)))
    if x < (width-1) and y < (height-1) and terrain_cost[(x+1,y+1)] >= 0:
        # Same as above examples but for diagonals
        transitions.append(('southeast', (x+1, y+1)))
    if x > 0 and y < (height-1) and terrain_cost[(x-1,y+1)] >= 0:
        transitions.append(('soutwest', (x-1, y+1)))
    if x > 0 and y > 0 and terrain_cost[(x-1,y-1)] >= 0:
        transitions.append(('northwest', (x-1, y-1)))
    if x < (width-1) and y > 0 and terrain_cost[(x+1,y-1)] >= 0:
        transitions.append(('northeast', (x+1, y-1)))
        
    return transitions


# This function updates the terrain_cost array
# so that the changes made by creating a path from the 
# initial state to the end state are reflected for the 
# next time we are making a path
def update_terrain_costs(path, decrease_grayscale):
    #print("\n***\t Inside update_terrain_costs") ############################
    # The array with the cost of each pixel
    global terrain_cost

    #print("***\t\t path:",path) ############################
    # for each point in path
    for (x, y) in path:
        # if the cost of the point (pixel) is greater than 0
        #print("***\t\t (x,y)",(x,y)) ############################
        if terrain_cost[(x,y)] > 0:
            # Don't know
            # ******************************************
            # Decrease the grayscale of the current pixel
            # this will make it darker
            # If you change -1 to a bigger number, the path lines will be darker with less iterations
            minimum = min(256, terrain_cost[(x,y)] - decrease_grayscale)
            #print("***\t\t min(256, terrain_cost[(x,y)] - 1):",minimum) ############################
            terrain_cost[(x,y)] = max(1, minimum)
            # the max() makes it so that it so that we don't go into negative (0 is black)
            #print("***\t\t terrain_cost[(x,y)] = max(1, minimum):",terrain_cost[(x,y)]) ############################
            # ******************************************


# This function creates the output picture file as .png
def draw_terrain(out_filename):
    #print("\n***\t Inside draw_terrain") ############################
    # terrain_img is used to load the input image
    # modify it, and then save it as the output .png
    # terrain_cost is the array with the cost of each pixel
    global terrain_img, terrain_cost
    
    # load the input picture once again
    # Note that we don't open the image again
    # since we opened it in establish_terrain()
    pixels = terrain_img.load()
    
    # loop through each pixel
    for x in range(0, width):
        for y in range(0, height):
            # Don't know
            # ******************************************
            c = int(terrain_cost[(x, y)])
            # ******************************************
            
            if c > 0:
                pixels[x, y] = (c, c, c)
    
    img = terrain_img.resize((width * 5, height * 5))
    
    # Save the modifications to the new image file
    script_dir = os.path.dirname(__file__)  # Absolute directory of this script
    relative_path = "../output_files/" + out_filename
    abs_file_path = os.path.join(script_dir, relative_path)
    img.save(abs_file_path)
    #img.show()
    
    
    
# ****************************************************************
#                     Extra functions
# ****************************************************************
# This function finds the distance to the nearest object from a given point
def dist_to_nearest_obstacle(x_y):
    #print("\n***\t Inside dist_to_nearest_obstacle") ############################
    # The point we are at
    x,y = x_y
    
    # The array containing the location of red pixels in the input image
    # Each red pixel is saved as -1 in this array
    global terrain_impassible
    
    # We assume the nearest object is the max between the width and height boarder
    min_dist = max(width, height)
    
    # loop through each point in the terrain_impassible array
    for (x2, y2) in terrain_impassible:
        if x != x2 or y != y2:
            # If the point from terrain_impassible isn't the given point then
            # find the distance from the impassible point to the given point
            d = dist((x, y), (x2, y2))
            if d < min_dist:
                # if the distance is less than the current min_dist then
                # set min_dist to this value
                min_dist = d
                
    # Return the distance to the nearest object from the given point
    return min_dist



#### A01: Modify some of the defintions below the TODOs.
####      Consider using some functions provided above.


# ****************************************************************
#                     Best first Heuristic
# ****************************************************************
# TODO
def heuristic_best_first(x_y, time, parents, action):
    #print("\n***\t Inside heuristic_best_first") ############################
    #print("***\t\t Calculating heuristic_value, call dist()") ############################
    heuristic_value = dist(x_y, (goal_x,goal_y))
    #print("***\t Inside heuristic_best_first, Heuristic from", x_y, "to", (goal_x,goal_y),"is:",heuristic_value)
    return heuristic_value

# TODO
def action_cost_best_first(x1_y1, action, x2_y2):
    #print("\n***\t Inside action_cost_best_first") ############################
    result = 0
    #print("***\t\t The cost from",x1_y1,"to",x2_y2,"with the action",action,":",result) ############################
    return result

# TODO
beam_size_best_first = None



# ****************************************************************
#                     A* Heuristic
# ****************************************************************
# TODO
def heuristic_astar(x_y, time, parents, action):
    #print("\n***\t heuristic_astar") ############################
    heuristic_value = dist(x_y, (goal_x,goal_y))
    
    return heuristic_value

# TODO
def action_cost_astar(x1_y1, action, x2_y2):
    #print("\n***\t Inside action_cost_astar") ############################
    x1,y1 = x1_y1
    x2,y2 = x2_y2
    return action_cost_true((x1,y1), action, (x2,y2))

# TODO
beam_size_astar = None



# ****************************************************************
#                     Beam Heuristic
# ****************************************************************
# TODO
def heuristic_beam(x_y, time, parents, action):
    #print("\n***\t Inside heuristic_beam") ############################
    heuristic_value = dist(x_y, (goal_x,goal_y))
    return heuristic_value

# TODO
def action_cost_beam(x1_y1, action, x2_y2):
    #print("\n***\t Inside action_cost_beam") ############################
    x1,y1 = x1_y1
    x2,y2 = x2_y2
    return action_cost_true((x1,y1), action, (x2,y2))

# TODO
beam_size_beam = 10



# ****************************************************************
#                     Human Heuristic
# ****************************************************************
# TODO
def heuristic_human(x_y, time, parents, action):
    #print("\n***\t Inside heuristic_human") ############################
    
    #print("***\t Inside heuristic_human, parents:",parents)
    
    #dis_to_object = dist_to_nearest_obstacle(x_y)
    dis_to_goal = dist(x_y, (goal_x,goal_y))
    
    heuristic_value = 0
    
    #if(len(parents) >= 1):
        
        # Getting the parent
        #(parent,action,cost) = parents[x_y,action,time]
        
        # Calculating distances
        #dis_to_parent = dist(x_y, parent)
        
        #print("***\t Inside heuristic_human, the parent of:",x_y,"is:",parent)
        #print("***\t Inside heuristic_human, dis_to_parent:",dis_to_parent)
        #print("***\t Inside heuristic_human, dis_to_object:",dis_to_object)
        #print("***\t Inside heuristic_human, dis_to_goal:",dis_to_goal)
        
        #if(dis_to_parent > dis_to_object):
        #    heuristic_value = dis_to_goal + 16 * dis_to_object
        #else:
        
    heuristic_value = dis_to_goal
    
    #print("***\t Inside heuristic_human, heuristic_value:",heuristic_value)    
    return heuristic_value

# TODO
def action_cost_human(x1_y1, action, x2_y2):
    #print("\n***\t Inside action_cost_human") ############################
    x1,y1 = x1_y1
    x2,y2 = x2_y2
    dis_to_object = dist_to_nearest_obstacle(x2_y2)
    
    result = action_cost_true((x1,y1), action, (x2,y2))
    
    #print("dis_to_object:",dis_to_object)
    
    if (dis_to_object < 4):
        result += 10
    
    return result 

# TODO
beam_size_human = 10



# ****************************************************************
#                     PROGRAM STARTS HERE
# ****************************************************************
def main_backend(strategies, road_configs, new_iterations, new_decrease_grayscale ):
    # Put here the name of the input images (.bmp) without the extension
    #road_configs = ["road-config-tree-sidewalks", "road-config-garden", "road-config-aldrich-park", "road-config-tree"]
    #road_configs = ["road-config-garden"]
    #road_configs = ["map_wlu_t7"]
    #road_configs = ["basic_v2"]

    # Put here the search algorithms to be used
    #strategies = ["best-first", "astar", "beam","human"]
    #strategies = ["human"]
    # The higher this number, the more time the program will take
    # but the output image will have a darker path

    #global decrease_grayscale

    iterations = new_iterations
    decrease_grayscale = new_decrease_grayscale

    # Don't know
    # ******************************************
    # generate random seeds, so we can be sure terrain and initial/goal positions
    # are reused when strategies are switched
    terrain_seeds = []
    for i in range(0, len(strategies)):
        ran_num = random.random()
        terrain_seeds.append(ran_num)
        #print("***\t Inside main, terrain_seeds ", i, ": ", ran_num) ############################
    state_seeds = []
    for i in range(0, iterations):
        ran_num = random.random()
        state_seeds.append(ran_num)
        #print("***\t Inside main, state_seeds ", i, ": ", ran_num) ############################
    # ******************************************



    # This file is used to output the collection of paths
    # found for each strategy and road configuration
    # Each line will have the iteration number and the length of the path found
    script_dir = os.path.dirname(__file__)  # Absolute directory of this script
    relative_path = "../output_files/path_lengths.csv"
    abs_file_path = os.path.join(script_dir, relative_path)

    path_lengths_csv = open(abs_file_path, "w")
    path_lengths_csv.write("road_config,strategy,iteration,path_length\n")

    print("***\t Inside main, iterations: ", iterations) ############################
    print("***\t Inside main, decrease_grayscale: ", decrease_grayscale ) ############################
    print("***\t Inside main, road_configs: ", road_configs ) ############################
    print("***\t Inside main, strategies: ", strategies ) ############################    
    # Loop through all the input images (.bmp)
    for road_config in road_configs:
        
        #print("***\t Inside main, road_config: ", road_config) ############################
        
        for i in range(0, len(strategies)):
        
            strategy = strategies[i]
            
            #print("***\t Inside main, strategy: ", strategy) ############################
    
    
            # Don't know
            # ******************************************            
            random.seed(terrain_seeds[i])
            # ******************************************
            
            # This passes the name of the input file to establish_terrain()
            # what else?
            # Loads the pixels of the .bmp image file
            # and fills in the following arrays:
            # possible_initial_states, possible_goal_states, terrain_impassible, terrain_cost
            establish_terrain("%s.bmp" % road_config)
        
    
    
            for j in range(0, iterations):
                # Don't know
                # ******************************************
                random.seed(state_seeds[j])
                # ******************************************
    #              
                # For each iteration
                # it will pick a random starting point (a blue pixel in the input image)
                # This starting position could be repeated
                make_initial_state()
            
                # It picks a random goal point (a green pixel in the input image)
                # The goal must be at least 10 pixels away from the initial state
                # hence why it needs to come after make_initial_state()
                make_goal_state() # must come second
        
                #print("\n***\t Inside main, iteration:",j+1,"init_x:", init_x, ", init_y:", init_y) ############################
                #print("***\t Inside main, iteration:",j+1,"goal_x:", goal_x, ", goal_y:", goal_y) ############################
                
                path = None
                
                if strategy == "best-first":
                    # Call search
                    # Return a path to the goal
                    # Search arguments
                    #    (init_x, init_y) - coordinates of the starting point
                    #    None - Depth limit to use in IDDFS (set to None if IDDFS isn't implemented)
                    #    heuristic_best_first - the heuristic function to use
                    #    action_cost_best_first -
                    #    beam_size_best_first -
                    #    is_goal_state - a function used to check if the given point is the goal
                    #    possible_transitions - a function used to collect all possible moves from a given point into an array
                    #    make_graphviz_mode - 
                    (path, _, _) = search((init_x, init_y), None,
                                        heuristic_best_first, action_cost_best_first, beam_size_best_first,
                                        is_goal_state, possible_transitions)
                    #print("***\t Inside main, best-first path:",(path, _, _))
        
                elif strategy == "astar":
                    (path, _, _) = search((init_x, init_y), None,
                                        heuristic_astar, action_cost_astar, beam_size_astar,
                                        is_goal_state, possible_transitions)
        
                elif strategy == "beam":
                    (path, _, _) = search((init_x, init_y), None,
                                        heuristic_beam, action_cost_beam, beam_size_beam,
                                        is_goal_state, possible_transitions)
        
                elif strategy == "human":
                    (path, _, _) = search((init_x, init_y), None,
                                        heuristic_human, action_cost_human, beam_size_human,
                                        is_goal_state, possible_transitions)
        
        
                # Don't know
                # ******************************************
                if path is None:
                    # If we didn't find a path from the initial state to the goal
                    # Then just print the coordinates
                    #print ("No path found to goal: (",goal_x, ",", goal_y,") from initial: (", init_x, ",", init_y, ")")
                    exit(-1)
                # ******************************************
        
                # Output to the console the image file used, the strategy used, iterations and path length
                print (road_config, strategy, (j+1), "path length", len(path), "path cost")
                # Output the same to the csv file
                path_lengths_csv.write("%s,%s,%d,%d\n" % (road_config, strategy, (j+1), len(path)))
        
        
                #print("***\t Inside main, before update_terrain_costs:",terrain_cost)
                # Don't know
                # ******************************************
                update_terrain_costs(path, decrease_grayscale)
                # ******************************************
                #print("***\t Inside main, after update_terrain_costs:",terrain_cost)
                
            # This function makes an output picture file with the paths found
            draw_terrain("%s-%s.png" % (road_config, strategy))
        
    # Closing the csv file
    path_lengths_csv.close()

    print("Done...")
    # ****************************************************************
    #                     PROGRAM ENDS HERE
    # ****************************************************************