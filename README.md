# Autodrop 
<i>Autonomous delivery services</i>
<p align="center">
<img src="https://user-images.githubusercontent.com/54982599/159121289-e77ab694-41bb-4516-9603-417fd9280779.jpg" width="400">
</p>
<p align="center">
  <img src="https://img.shields.io/badge/Maintained%3F-Yes-green?style=for-the-badge">
  <img src="https://img.shields.io/github/license/GauravKakoti/Autodrop?style=for-the-badge">
  <img src="https://img.shields.io/github/stars/GauravKakoti/Autodrop?style=for-the-badge">
  <img src="https://img.shields.io/github/forks/GauravKakoti/Autodrop?color=teal&style=for-the-badge">
  <img src="https://img.shields.io/github/issues/GauravKakoti/Autodrop?color=violet&style=for-the-badge">
</p>

## Who are we ?
Autodrop aims to be a self-contained shipping solution for cooperations and individials alike.

We wish to provide full ecosystem for autonomous vehicles/drones which can deliver

cargo from your warehouses (or doorsteps) to anywhere in the world ASAP

<img src="https://user-images.githubusercontent.com/54982599/159128616-1b5e688e-f01a-4d27-aaa6-b64b289580a4.gif" width="200">

## How the magic happens :

Autodrop uses state of the art algorithims to find the shortest routes from just a picture of a map and ensures high-speed delivery of goods with the lowest carbon footprint possible.

In addition, we also outfit our drones with our in-house self-driving technologies to detect obstacles and weather to deliver your package to you safely .

<img src="https://user-images.githubusercontent.com/54982599/159148510-8995e0f9-5f5b-4f29-a8c8-33d6a12a2d7e.gif" width="200">
 
 ## 1) Path finding Algorithims :
 
 __To find a shortest route , we have utilized heuristic search algorithims. Namely :__
 
a. Greedy Best First Search

b. Beam search

c. A* Search

Our project takes bmp image files as input map data then applies the above algorithims 🤖
It then outputs the route according to the selected algorithim in an image file, and also provides a .csv file comparing the various algorithims
To learn more about how it works and how we make it 
[Click Here !](https://drive.google.com/file/d/1KgdXWOM8oL3-y5NxNYvEBrM6x-kgsRth/view?usp=sharing)

<img src="https://media.giphy.com/media/47EtjlHYFREM5Rznaf/giphy.gif" width="400">

## 2) Self navigation technologies :
   
Our project also uses realtime object detection using haar features to detect obstacles,lanes and the weather to reduce accidents due to human error
and optimally follow the route determined by the pathfinding component .
