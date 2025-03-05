# Concepts-Final-project
Final project from Concepts of Programming Languages.

Modified version of Conway's Game of Life where a dead cell will live if the number of living neighbors is even (2,4,6,8) and living cells will continue to live if the number of living neighbors is prime (2,3,5,7).
This project required all neighbor cells to be calculated manually and we could not use a library such as numpy to perform 2d array calculations.

When I first wrote this program I used a 1d array to store the matrix due to its simplicity and I didn't fully understand 2d arrays in python at the time. 
After I learning more python and using it everyday in an internship I rewrote the code to run with a 2d array instead. This significantly decreased the time required to run the program especially on large matrices such as 10000x10000.

### Running the code
The code takes command line arguments following this format
-i {input_file} -o {output_file} -p {number_threads}

Input txt files must contain 'O' and '.' exclusivley for the code to run correctly. 
