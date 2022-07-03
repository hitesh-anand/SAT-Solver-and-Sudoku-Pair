import copy

a = input("Enter the path of the file: ")
f = open(a, "r")

content = f.readlines()[7:]

f.close()

desc = content[0].split(" ")

sample_clause = content[-1].split(" ")

num_vars = int(desc[2])
num_clauses = int(desc[4])
print('Number of literals = ', num_vars)
print('Number of clauses = ', num_clauses)

clauses = []*num_clauses
for i in range(num_clauses):
    str_clause = content[i+1].split(" ")[:-1]
    clause_len = len(str_clause)
    clauses.append([int(str_clause[j]) for j in range(clause_len)])

# print("The clauses are:")
# print(clauses)


def unitPropagation(formula):
    clauses_temp = copy.deepcopy(formula)
    for i, clause in enumerate(formula):
        if len(clause) == 1:
            num = clause[0]
            for j, others in enumerate(formula):
                if j != i and num in others and others in clauses_temp:
                    clauses_temp.remove(others)
            negnum = num* -1            
            for j, others in enumerate(clauses_temp):
                if len(others) == 1:
                    continue
                if negnum in others:
                    clauses_temp[j].remove(negnum)

    return clauses_temp

def polarityDict(clauses):
    polarity = {i+1:'none' for i in range(num_vars)}
    counts = [0 for i in range(num_vars)]
    for clause in clauses:
        for literal in clause:
            if polarity[abs(literal)] == "none":
                polarity[abs(literal)] = "pos" if literal>0 else "neg"
            elif polarity[abs(literal)] == "pos":
                polarity[abs(literal)] = "both" if literal<0 else "pos"
            elif polarity[abs(literal)] == "neg":
                polarity[abs(literal)] = "both" if literal>0 else "neg"
            else:
                continue
            
            counts[abs(literal)-1]+=1
                
    return polarity, counts

def pureLiterals(polarity):
    pureLits = []
    for literal in polarity.keys():
        if polarity[literal] == "neg" or polarity[literal] == "pos":
            pureLits.append([literal, polarity[literal]])
    return pureLits

def pureElimination(pureLits, rem_clauses):
    clauses_temp = rem_clauses.copy()
    for i in pureLits:
        num = i[0] if i[1] == "pos" else -i[0]
        for clause in clauses_temp:
            if num in clause:
                clauses_temp.remove(clause)
        clauses_temp.append([num])
    return clauses_temp

def consistent(formula):
    for i in range(len(formula)):
        if len(formula[i]) != 1:
            continue
        for j in range(len(formula)):
            if len(formula[j]) != 1:
                continue
            if formula[i][0] + formula[j][0] == 0:
                return "unsat",0
    if len(formula) != num_vars:
        return "continue",0
    found = [0 for i in range(num_vars)]
    for clause in formula:
        if len(clause) != 1:
            return "continue",0
        found[abs(clause[0])-1] = 1
    
    for i in range(num_vars):
        if found[i] == 0:
            return "continue",0

    return "consistent",1 

def removeEmptyClauses(formula):
    for clause in formula:
        if len(clause) == 0:
            formula.remove(clause)
    return formula

def solve(clauses):
    first_clauses = unitPropagation(clauses)
    polarity, counts = polarityDict(first_clauses)
    pureLits = pureLiterals(polarity)
    rem_clauses = pureElimination(pureLits, first_clauses)
    rem_clauses = removeEmptyClauses(rem_clauses)
    if len(rem_clauses) == 0:
        return "unsat", rem_clauses
    remark, valid = consistent(rem_clauses)
    if(remark == "consistent"):
        return "sat", rem_clauses
    elif(remark == "unsat"):
        return "unsat", rem_clauses
    if 0 in counts:
        var = counts.index(0)
    else:
        var = counts.index(max(counts))
    counts[var] = 0
    rem_clauses.append([var+1])
    result, solution = solve(rem_clauses)
    if result == "sat":
        return result, solution
    else:
        rem_clauses.remove([var+1])
        rem_clauses.append([-(var+1)])
        return solve(rem_clauses)

result, model = solve(clauses)

if result == "unsat":
    print("The formula is unsatisfiable!")
    text_file = open("./outfile.txt", "w")
    text_file.write("UNSAT")
    text_file.close()
else:
    print("The formula is satisfiable!")
    print("The following model satisfies the formula:")
    print(model)
    text_file = open("./outfile.txt", "w")
    text_file.write(str(model))
    text_file.close()

