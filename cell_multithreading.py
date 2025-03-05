'''
Project 3 code Rewritten for optimization
'''
#test speed
import time
#allows the program to read command line inputs and check files
import sys
import os
#for rounding calculations
import math
#allows multiple thread to be run during calculations
import threading

'''
Calculate living cells after 100 cycles
Neighbor calculations must be done manually and no library can be used

Modified version of Conway's Game of Life using these rules
rules for dead cell:
    num live neighbors is EVEN then it lives

rules for live cells:
    num live neighbors is PRIME then it lives
'''
#list of prime numbers and even numbers
primes = {2, 3, 5, 7}
evens = {2, 4, 6, 8}
#length of the column and row
c, r = 0, 0
#temp matrix to store new values while calculating
matrix2 = []
def main():
    #Default value for number of processes, input file, output file
    numProcesses = 1
    sourceFile = ""
    outFile = ""
    #global variable call
    global c, r, size, matrix2 

    #gets the command arguments after the program call
    commandList = sys.argv[1:]
    print(commandList)
    #assigns each argument to a variable for use later (might remove to improve time/memory)
    try:
        for i in range(len(commandList)):
            if commandList[i] == "-i":
                sourceFile = commandList[i + 1]
                i += 1
            elif commandList[i] == "-o":
                outFile = commandList[i + 1]
                i += 1
            elif commandList[i] == "-p":
                numProcesses = int(commandList[i + 1])
                i += 1
        #ensures the outfile exists
        f = open(outFile, "w")
        f.close()
    except:
        print("There was an error with your arguments")
    
    #confirms that input & output files exist and that processes are at least 1 (returns error otherwise)
    if not os.path.exists(sourceFile):
        return print("Error: source file does not exist!!")
    elif not os.path.exists(outFile):
        return print("Error: output file does not exist!")
    elif numProcesses <= 0:
        return print("Error: Can't run negative processes!")
    #prints for testing
    print(sourceFile, outFile, str(numProcesses))
    print('')

    #matrix for storing the cells
    matrix = []
    #reads the file and returns the matrix and the number of columns and rows
    #matrix, c, r = readFile(sourceFile, matrix, c, r)
    matrix = readFile(sourceFile, matrix)
    #updates the matrix size
    size = c * r
    #print("size: ", str(size))
    start = time.time()
    #iterates for 100 cell time steps (101)
    for j in range(1,101):
        #updates the temporary matrix to store the new live values
        matrix2 = [[0 for l in range(c)] for m in range(r)] #updated for 2d list
        #print(matrix2)
        #calculates the number of cells each process will calculate (rounded up)
        cellsPerProcess = math.ceil(size / numProcesses)
        #creates the threads list for storing threads
        threads = list()
        #creates a thread and tells it what to do (target is function, args is the arguments needed)
        for i in range(numProcesses):
            #start and end positions for each thread (accounts for numProcesses not being a square root of matrix size)
            if(i == numProcesses - 1):
                pos1 = i * cellsPerProcess
                pos2 = size
            else:
                pos1 = i * cellsPerProcess
                pos2 = (i + 1) * cellsPerProcess
            cellThread = threading.Thread(target = nextLiveCell, args = (matrix, pos1, pos2))
            #adds the thread to the list
            threads.append(cellThread)
            #runs the thread
            cellThread.start()
        #ensure each thread is complete
        for thread in threads:
            thread.join()
        #print("Matrix Before:" + str(matrix))
        #updates matrix with the new values
        p1 = 0
        p2 = 0
        for mR in matrix2:
            for mC in mR:
                matrix[p1][p2] = mC
                p2 += 1
            p1 += 1
            p2 = 0
        #print("Matrix After:" + str(matrix))
        if (j % 10 == 0):
            print("Percent complete: ", j)
    
    #writes the final matrix to the output file
    writeFile(outFile, matrix, c, r)
    end = time.time()
    print("time elapsed: ", end - start)

#reads the file to record each cell value
def readFile(file, matrix):
    global c, r
    #opens the file as read only
    f = open(file, "r")
    #goes throught the file and stores the values in a list for evaluation
    for i in f:
        if(i[0] == '.' or i[0] == 'O'):
            row = []
            for j in i:
                if j != '\n':
                    #assigns the value 0 for dead cells and 1 for living cells
                    if(j == '.'):
                        row.append(0)
                    else:
                        row.append(1)
            matrix.append(row)
            #caluclates the number of columns and rows
            if r == 0:
                #number of columns is the length of array after row 1 because it is a rectangle
                c = len(row)
        r += 1
    
    #prints the matrix and the number of rows and columns to ensure it's correct
    #sprint(matrix)
    print("Number rows: " + str(r) + "\nNumber columns: " + str(c) + "\nSize of matrix: " + str(c*r))
    
    #closes the file after it is read and stored
    f.close()
    return matrix

#creates a new file to store the matrix after each step
def writeFile(file, matrix, c, r):
    #opens the file that the matrix will be printed in (cReates if it does not exist)
    f = open(file, "w")
    #iterates through the matrix printing each element in a matrix form
    for i in matrix:
        for j in i:
            #writes the corresponding character (. or O) for the cell
            if j == 0:
                f.write('.')
            else:
                f.write('O')
            #f.write(str(matrix[pos]))
        #line break for the next row
        f.write("\n")
    #closes the file 
    f.close()

#calculates which cells will be alive next iteration and which will be dead
def nextLiveCell(matrix, startP, endP):
    global c, r, primes, evens, matrix2
    #convert start and end position to 2d array access values
    for i in range(startP, endP):
        cr = int(i / c)
        cc = int(i % c)
        #print(f"Matrix [{cr}] [{cc}] ")
        nr1, nr2 = cr - 1, cr + 1 #neighboring rows
        nc1, nc2 = cc - 1, cc + 1 #neighboring columns
        '''
        Wrap around conditions

        if row is 0 then previous row is last row in matrix
        if row is last row in matrix then next row is first row in matrix
        if column is 0 then previous column is last column in matrix
        if column is last column in matrix then next column is first column in matrix
        '''
        #Adjusts the neighbor values for wrapping around
        if nr1 == -1:
            nr1 = r - 1
        if nr2 == r:
            nr2 = 0
        if nc1 == -1:
            nc1 = c - 1
        if nc2 == c:
            nc2 = 0
        #rules for cells
        '''
        rules for dead cell:
            num live neighbors is EVEN then it lives

        rules for live cells:
            num live neighbors is PRIME then it lives
        '''
        #print(f"N1 [{nr1}] [{nc1}] ")
        #print(f"N2 [{nr2}] [{nc2}] ")
        #get total number of living neighbor cells
        total = matrix[nr1][nc1] + matrix[nr1][cc] + matrix[nr1][nc2] + matrix[cr][nc1] + matrix[cr][nc2] + matrix[nr2][nc1] + matrix[nr2][cc] + matrix[nr2][nc2]
        #print(f"Total: {total}")
        if (matrix[cr][cc] and total in primes) or ((not matrix[cr][cc]) and total in evens):
            matrix2[cr][cc] = 1

#ensures that main runs first
if __name__ == "__main__":
    main()
