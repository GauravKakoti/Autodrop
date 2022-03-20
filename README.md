# Autodrop 
<i>Autonomous delivery services</i>
<p align="center">
<img src="https://user-images.githubusercontent.com/54982599/159121289-e77ab694-41bb-4516-9603-417fd9280779.jpg" width="400">
</p>

## Who are we ?
Autodrop aims to be a self-contained shipping solution for cooperations and individials alike.

We wish to provide full ecosystem for autonomous vehicles/drones which can deliver

cargo from your warehouses (or doorsteps) to anywhere in the world ASAP


<img src="https://user-images.githubusercontent.com/54982599/159128616-1b5e688e-f01a-4d27-aaa6-b64b289580a4.gif" width="200">


## How the magic happens :

Autodrop uses state of the art algorithims to find the shortest routes from just a picture of a map and ensures high-speed delivery of goods with the lowest carbon footprint possible.

In addition, we also outfit our drones with our in-house self-driving technologies to detect obstacles and weather to deliver your package to you safely .
 
 ## Work example:
 
 ### 1) Path finding Algorithims :
 
 __To find a shortest route , we have utilized heuristic search algorithims. Namely :__
 
a. Greedy Best First Search

b. Beam search

c. A* Search

#### Input map image : 

![image](https://user-images.githubusercontent.com/54982599/159146742-4c489513-3f44-497f-aad9-43ad98c8eee2.png)

The program allows the user to select one or more input image files for the program to use. The input image files are .bmp format.

It must contain the following:
● A blue pixel representing the starting
pixel

● A green pixel representing the goal
pixel

● Red pixels to outline obstacles

There could be multiple blue and green pixels present in an image file. The program randomly chooses one starting point and one
ending goal if they are available. The default image files can be selected from the GUI, but the user can use the menu/upload option
to select any input image.

1.A* algorithim :
![road-config-tree-sidewalks-astar](https://user-images.githubusercontent.com/54982599/159147005-a0ce6484-d59f-4923-b075-6245e5715a85.png)
1.Best-First algorithim
![road-config-tree-best-first](https://user-images.githubusercontent.com/54982599/159147279-c2d5123e-f4ab-4beb-a5ff-ee05d65fe1ad.png)




   ### 2) Self navigation technologies :
