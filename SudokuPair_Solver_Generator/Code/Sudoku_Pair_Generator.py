import pysat
import itertools
import pandas as pd
import numpy as np
import random
from pysat.solvers import Solver
import datetime
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

def encode(s, i, j, k, num):
    if s==1:
        return i*(k**4) + j*(k**2) + num
    else:
        return k**6 + i*(k**4) + j*(k**2) + num
    
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
    sudoku1 = np.zeros((rows, cols)).astype(int)
    sudoku2 = np.zeros((rows, cols)).astype(int)
    if(g.solve()):
        output = g.get_model()
        for i in output:
            if(i>0 and i<=2*k**6):
                if(i<=(k**6)):
                    r, c, num = decode(i, k)
                    sudoku1[r][c]=num
                else:
                    r, c, num = decode(i , k)
                    sudoku2[r][c]=num        
    return g, sudoku1, sudoku2

def solve_pair(g, sudoku1,sudoku2):
    g = eachCellUniqueNumber(g, sudoku1, sudoku2)
    g = eachRowUniqueNumber(g, sudoku1, sudoku2)
    g = eachColumnUniqueNumber(g, sudoku1, sudoku2)
    g = eachBlockUniqueNumber(g, sudoku1, sudoku2)
    g = pairConstraints(g, sudoku1, sudoku2)
    g = alreadyFilled(g,sudoku1,sudoku2)
    g, output1, output2 = getOutputs(g)
    return g, output1, output2

def randomCells(k, mid):
    i=0
    j=0
    n=0
    cells=[]
    while n<mid:
        cells.append([randr[i],randr[j]])
        if len(cells)%len(randr) == 0:
            i+=1
            j=0
        else:
            j+=1
        n+=1
    return cells

def generateEmptyPairs(k):
    mat1 = [[0 for j in range(k**2)] for i in range(k**2)]
    mat2 = [[0 for j in range(k**2)] for i in range(k**2)]
    return mat1, mat2

def removeEntries(out1, out2, cells):
    i = 0
    out_h1 = out1.copy()
    out_h2 = out2.copy()
    while i<len(cells):
        if i%2 == 0:
            out_h1[cells[i][0]-1][cells[i][1]-1] = 0
        else:
            out_h2[cells[i][0]-1][cells[i][1]-1] = 0
        i+=1
    return out_h1, out_h2 

def solve_uniquely(g2,cells, out_re1, out_re2):
    out_temp1, out_temp2 = removeEntries(out_re1, out_re2, cells)
    lis1 = []
    lis2 = []
    
    g2.add_clause([-int(encode(1, cells[i][0]-1, cells[i][1]-1, k, out_re1[cells[i][0]-1][cells[i][1]-1])) for i in np.arange(0,len(cells),2)])
    g2.add_clause([-int(encode(2, cells[i][0]-1, cells[i][1]-1, k, out_re2[cells[i][0]-1][cells[i][1]-1])) for i in np.arange(1,len(cells),2)])
    g2, out1, out2 = solve_pair(g2, out_temp1, out_temp2)
    return g2, out1, out2

def generatePairLinear(k, out1, out2):
    l = k
    h = 2*(k**4)-2
    steps = 0
    cells = []
    while l<=h:
        steps+=1
        if l==k:
            out_hold1, out_hold2 = out1.copy(), out2.copy()
        ans1, ans2 = out_hold1.copy(), out_hold2.copy()
        r = random.randint(1, k**2)
        c = random.randint(1, k**2)
        if l%2 == 0:
            while out_hold1[r-1][c-1] == 0:
                r = random.randint(1, k**2)
                c = random.randint(1, k**2)
            out_hold1[r-1][c-1] = 0
        else:
            while out_hold2[r-1][c-1] == 0:
                r = random.randint(1, k**2)
                c = random.randint(1, k**2)
            out_hold2[r-1][c-1] = 0
        cells.append([r,c])

        
        g1 = Solver()
        g1, out_re1, out_re2 = solve_pair(g1, out_hold1, out_hold2) 
        g2 = Solver()
        g2, out_dp1, out_dp2 = solve_uniquely(g2, cells, out_re1, out_re2)
        
        result = ""
        if (out_dp1[0][0] == 0 and out_dp2[0][0]==0) or (out_dp1 == out_re1).all():
            result = "unique"
        else:           
            result = "multiple"     
        if result == "multiple":
            break
        else:
            l+=1
        del g1
        del g2
           
    return (l-1), ans1, ans2


k = int(input("Enter the value of k : "))
rows = k**2 
cols = rows

in1, in2 = generateEmptyPairs(k)


randr = random.randint(0, k**2-1)
randc = random.randint(0, k**2-1)
rnum = random.randint(1, k**2)
in1[randr][randc] = rnum



randr = random.randint(0, k**2-1)
randc = random.randint(0, k**2-1)
rnum = random.randint(1, k**2)
while in1[randr][randc] == rnum:
    randr = random.randint(0, k**2-1)
    randc = random.randint(0, k**2-1)
    rnum = random.randint(1, k**2)
in2[randr][randc] = rnum

a = datetime.datetime.now()
g = Solver()
g, out1, out2 = solve_pair(g, in1, in2)

ans, ans1, ans2 = generatePairLinear(k, out1, out2)

print(ans1)
print(ans2)
np.savetxt("puzzlepair.csv", np.concatenate((ans1,ans2),axis=0), fmt='%d',delimiter=",")

g_ans = Solver()
g_ans, out_ans1, out_ans2 = solve_pair(g_ans, ans1, ans2)
