import itertools
import pandas as pd
import numpy as np
import time
from pysat.solvers import Solver

def encode(s, i, j, k, num):
    if s==1:
        return i*(k**4) + j*(k**2) + num
    else:
        return k**6 + i*(k**4) + j*(k**2) + num
    
def decode(i,k):
    if i<=k**6:
        if i%(k**4) == 0:
            r = i//(k**4) - 1
        else:
            r = (i)//(k**4)
            
        if (i - r*k**4)%(k**2) == 0:
            c = (i-r*k**4)//(k**2)-1
        else:
            c = ((i)%(k**4))//(k**2)
        num = (i) - r*(k**4) - c*(k**2)
    else:
        i = i - k**6
        if i%(k**4) == 0:
            r = i//(k**4) - 1
        else:
            r = (i)//(k**4)
            
        if (i - r*k**4)%(k**2) == 0:
            c = (i-r*k**4)//(k**2)-1
        else:
            c = ((i)%(k**4))//(k**2)
        num = (i) - r*(k**4) - c*(k**2)
    return r, c, num

def eachCellUniqueNumber(g, sudoku1, sudoku2):
    for i, j in itertools.product(range(k**2), repeat=2):
        g.add_clause([encode(1, i, j, k, num) for num in range(1, k**2 + 1)])
        g.add_clause([encode(2, i, j, k, num) for num in range(1, k**2 + 1)])
        for num1, num2 in itertools.combinations(range(1, k**2 + 1), 2):
            g.add_clause([-encode(1, i, j, k, num1), -encode(1, i, j, k, num2)])
            g.add_clause([-encode(2, i, j, k, num1), -encode(2, i, j, k, num2)])
    
    return g
def eachBlockUniqueNumber(g, sudoku1, sudoku2):
    lis1 = []
    n = 0
    while(n < k):
        lis1.append(n*k)
        n+=1
    arr = []
    for i in range(k):
        arr.append(i)
    for row_st, col_st in itertools.product(lis1, repeat=2):
        for n in range(1, k**2 + 1):
            g.add_clause([encode(1, row_st+row_ch, col_st+col_ch, k, n) for row_ch, col_ch in itertools.product(arr, repeat=2)])
            g.add_clause([encode(2, row_st+row_ch, col_st+col_ch, k, n) for row_ch, col_ch in itertools.product(arr, repeat=2)])
    return g

def eachRowUniqueNumber(g, sudoku1, sudoku2):
    for i in range(k**2):
        for num in range(1, k**2 + 1):
            g.add_clause([encode(1,i,j,k,num) for j in range(k**2)])
            g.add_clause([encode(2,i,j,k,num) for j in range(k**2)])
            
    for i in range(k**2):
        for num in range(1, k**2 + 1):
            for j1, j2 in itertools.combinations(range(k**2), 2):
                g.add_clause([-encode(1, i, j1, k, num), -encode(1, i, j2, k, num)])
                g.add_clause([-encode(2, i, j1, k, num), -encode(2, i, j2, k, num)])
    return g

def eachColumnUniqueNumber(g, sudoku1, sudoku2):
    for j in range(k**2):
        for num in range(1, k**2 + 1):
            g.add_clause([encode(1,i,j,k,num) for i in range(k**2)])
            g.add_clause([encode(2,i,j,k,num) for i in range(k**2)])

    for j in range(k**2):
        for num in range(1, k**2 + 1):
            for i1, i2 in itertools.combinations(range(k**2), 2):
                g.add_clause([-encode(1, i1, j, k, num), -encode(1, i2, j, k, num)])
                g.add_clause([-encode(2, i1, j, k, num), -encode(2, i2, j, k, num)])
    return g

    return g

def pairConstraints(g, sudoku1, sudoku2):
    for i,j in itertools.product(range(k**2), repeat=2):
        for num in range(1, k**2 + 1):
            g.add_clause([-encode(1,i,j,k,num), -encode(2,i,j,k,num)])
    return g

def alreadyFilled(g,sudoku1,sudoku2):
    for i in range(k**2):
        for j in range(k**2):
            if(sudoku1[i][j]>0):
                g.add_clause([int("%d" % encode(1, i, j, k, sudoku1[i][j]))])
            if(sudoku2[i][j]>0):
                g.add_clause([int("%d" % encode(2, i, j, k, sudoku2[i][j]))])
    return g

def getOutputs(g):
    sudoku1 = np.zeros((rows, cols))
    sudoku2 = np.zeros((rows, cols))
    if(g.solve()):
        print("Solution Exists!")
        output = g.get_model()
        for i in output:
            if(i>0 and i<=2*k**6):
#                 print("For i:", i)
                if(i<=(k**6)):
                    r, c, num = decode(i, k)
                    sudoku1[c][r]=num
                else:
                    r, c, num = decode(i , k)
                    sudoku2[c][r]=num        
    else:
        print("Solution was not found!")
    return g, sudoku1, sudoku2

def solve_pair(sudoku1,sudoku2):
    g = Solver()
    g = eachCellUniqueNumber(g, sudoku1, sudoku2)
    print("Checked cells")
    if type(g.get_model()) == "list":
        print(len(g.get_model()))
    g = eachRowUniqueNumber(g, sudoku1, sudoku2)
    if type(g.get_model()) == "list":
        print(len(g.get_model()))
    print("Checked rows")
    g = eachColumnUniqueNumber(g, sudoku1, sudoku2)
    if type(g.get_model()) == "list":
        print(len(g.get_model()))
    print("Checked columns")
    g = eachBlockUniqueNumber(g, sudoku1, sudoku2)
    if type(g.get_model()) == "list":
        print(len(g.get_model()))
    print("Checked Blocks")
    g = pairConstraints(g, sudoku1, sudoku2)
    if type(g.get_model()) == "list":
        print(len(g.get_model()))
    print("Checked pair constraints")
    g = alreadyFilled(g,sudoku1,sudoku2)
    if type(g.get_model()) == "list":
        print(len(g.get_model()))
    print("Checked already filled values")
    g, output1, output2 = getOutputs(g)
    if type(g.get_model()) == "list":
        print(len(g.get_model()))
    return g, output1, output2

k = int(input("Enter k : "))
rows = k**2 
cols = rows
a = input("Enter path : ")
input_sudoku1 = pd.read_csv(a,header=None,nrows=rows)
input_sudoku2 = pd.read_csv(a,header=None,skiprows=rows)
print(np.matrix(input_sudoku1))
print(np.matrix(input_sudoku2))
np.set_printoptions(threshold=np.inf)

start = time.time()
g = Solver()
g, output_sudoku1, output_sudoku2 = solve_pair(input_sudoku1, input_sudoku2)
end = time.time()
print("Time taken : ",end-start, "sec")

output_sudoku1 = output_sudoku1.astype(int)
output_sudoku2 = output_sudoku2.astype(int)
if(output_sudoku1[0][0]!=0):
    print(output_sudoku1,end='\n\n')
    print(output_sudoku2)
np.savetxt("solvedsudoku.csv", np.concatenate((output_sudoku1,output_sudoku2),axis=0), fmt='%d',delimiter=",")