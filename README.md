# Concepts-Final-project
Final project from Concepts of Programming Languages.

Modified version of Conway's Game of Life where a dead cell will live if the number of living neighbors is even (2,4,6,8) and living cells will continue to live if the number of living neighbors is prime (2,3,5,7).
This project required all neighbor cells to be calculated manually and we could not use a library such as numpy to perform 2d array calculations.

When I first wrote this program it generated a long 1d array that held all the information but it was extremely slow. 
After I graduated I rewrote the code with the knowledge and experience I gained from other classes and used a 2d array instead. This significantly decreased the time required to run the program especially on large matrices such as 10000x10000.
