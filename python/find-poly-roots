# Programmer: Rohan Kosalge
# Date: October 29th, 2018
# Purpose: find all roots of any polynomial

from rutils import *
from ralgebra import *

# lol back when I totally forgot about ASCII
letters  = ['a', 'b', 'c', 'd', 'e', 'f',
           'g', 'h', 'i', 'j', 'k', 'l', 'm',
           'n', 'o', 'p', 'q', 'r', 's',
           't', 'u', 'v', 'w', 'x', 'y', 'z']

# I should really make this program compact

def editFindList(alist, key): # special one I really needed for NR
    keyFound = False
    keyNum = 0
    blist = []
    for x in range(len(alist)):
        element = alist[len(alist)-(x+1)]
        num = element[len(element)-1]
        for y in range(len(element)):
            if element[y] == key and keyFound == False:
                keyFound = True
                keyNum = num
                break
            if keyFound == True and num == keyNum-1:
                for x in range(len(element[:len(element)-1])):
                    blist.append(element[x])
                break

    return blist

def editEx(expression):
    syms = ['+', '-']
    lim = 0
    for x in range(len(expression)-1):
        if expression[x] == 'x' and (x!= len(expression)-1 and expression[x+1] not in syms):
            lim+=1
    for x in range(len(expression)-1+lim):
        if expression[x] == 'x' and (x!= len(expression)-1 and expression[x+1] not in syms):
            expressionList = list(expression)
            expressionList.insert(x+1, '^')
            expression = combine(expressionList)
            
    expression = expression.replace('^', '**')
    
    newx = "(x)"
    expression = expression.replace("x", newx)

    lim = 0
    for x in range(len(expression)):
        if expression[x] == '(' and (expression[x-1] not in syms and x!=0):
            lim+=1
            
    for x in range(len(expression)+lim):
        if expression[x] == '(' and (expression[x-1] not in syms and x!=0):
            expressionList = list(expression)
            expressionList.insert(x+1, '*')
            expression = combine(expressionList)

    expression = expression.replace("(*", "*(")
    return expression


def findDerivative(terms):
    syms = ['+', '-']
    newterms = []
    for x in range(len(terms)):
        term = terms[x]
        newterm = ''

        for y in range(len(term)):
            if term[y] == 'x':              # assuming that variable is 'x' for now...
                coefficient = term[:y]
                exponent = term[y+1:]

        termfound = True
        addx = True
        addplus = False
        if 'x' not in term:  
            coefficient = '0'
            exponent = '0'
            termfound = False
        
        if (coefficient in syms) or (coefficient == ''):
            coefficient += '1'

        if exponent == '':
            exponent = '1'

        coefficient = float(coefficient)
        exponent = float(exponent)

        coefficient*=exponent
        exponent-=1

        if coefficient.is_integer() == True:
            coefficient = int(coefficient)
        if exponent.is_integer() == True:
            exponent = int(exponent)

        if coefficient > 0 and len(newterms)!=0:
            addplus = True
        newcoefficient = str(coefficient)
        newexponent = str(exponent)
        if newexponent == '1':
            newexponent = ''
        if newexponent == '0':
            newexponent = ''
            addx = False
            
        if termfound == False:
            newterm = ''
        else:
            if addx == False:
                if addplus == True:
                    newterm = '+' + str(newcoefficient)
                else:
                    newterm = str(newcoefficient)
            else:
                if addplus == True:
                    newterm = '+' + str(newcoefficient) + 'x' + str(newexponent)
                else:
                    newterm = str(newcoefficient) + 'x' + str(newexponent)
            
        newterms.append(newterm)

    derivative = combine(newterms)
    return derivative

def combine(terms):
    finalstr = ''
    for x in range(len(terms)):
        finalstr += terms[x]
    return finalstr

def revCombine(terms):
    finalstr = ''
    for x in range(len(terms)):
        finalstr += terms[len(terms)-(x+1)]
    return finalstr

def reverse(alist):
    revlist = []
    for x in range(len(alist)):
        revlist.append(alist[len(alist)-(x+1)])
    return revlist

def getTerms(expression):
    syms = ['+', '-']
    terms = []
    tmin = 0
    for x in range(len(expression)):
        if expression[x] in syms:
            term = expression[tmin:x]
            terms.append(term)
            tmin = x
        if x == len(expression)-1:
            term = expression[tmin:]
            terms.append(term)

    return terms

def findMinDegree(terms):
    term = terms[0]
    degree = ""
    for x in range(len(term)):
        if term[x] in letters:
            degree = term[x+1:]
    if degree == "":
        degree = 1
    degree = int(degree)
    return degree

def findMaxDegree(terms):
    terms.sort()
    terms = reverse(terms)
    #print(terms)
    degree = ""
    degreeList = []
    for x in range(len(terms)):
        term = terms[x]
        for y in range(len(term)):
            if term[y] in letters:
                degree = term[y+1:]
                degreeList.append(degree)
                
    for x in range(len(degreeList)):
        if degreeList[x] == "":
            degreeList[x] = 1
        else:
            degreeList[x] = int(degreeList[x])

    #print(degreeList)    
    maxDegree = max(degreeList)
    return maxDegree

def findDerivatives(polynomial):
    dList = [polynomial]
    maxD = findMaxDegree(getTerms(polynomial))
    #print(maxD)
    while True:
        derivative = findDerivative(getTerms(polynomial))
        dTerms = getTerms(derivative)
        deg = findMinDegree(dTerms)
        if deg==1:
            break
        else:
            polynomial = combine(dTerms)
            dList.append(polynomial)
            
    finalDerivative = combine(dTerms)
    dList.append(finalDerivative)

    # get the int d for linear sol
    # we only need it if degree>1 though
    lastD = findDerivative(getTerms(finalDerivative))
    
    if maxD>1:
        dList.append(lastD)    
    return dList

def evaluate(val, func):
    func = editEx(func)
    func = func.replace("x", str(val))
    #print(func)
    sol = float(eval(func))
    return sol
        
def newtonRaphson(x0, polynomial, derivative):
    #print("Input: " + str(x0))
    #print("Derivative: " + str(derivative) + ", and polynomial: " + polynomial)
    fx0 = evaluate(x0, polynomial)
    dfx0 = evaluate(x0, derivative)
    if dfx0 ==0:
        x1 = x0
    else:
        x1 = x0 - (fx0/dfx0)
    #print("Output: " + str(x1))
    #print()
    return x1

def betweenVals(vals, avals):
    #print("VALS: " + str(vals))
    # important function because it will return
    # list of inputs where each input fits certain range
    # of the vals passed in this function.
    # *really important for NR-Method*!

    vals.sort()
    
    bVals = []
    bVals.append(vals[0]-1)
    for x in range(len(vals)-1):
        val1 = vals[x]                          
        val2 = vals[x+1]
        avgVal = (val1+val2)/2
        if avgVal in avals:
            avgVal+=0.001
        bVals.append(avgVal)
        
    bVals.append(vals[len(vals)-1]+1)

    #print(len(bVals))
    return bVals
    

def findRoots(dList):
    # initial guess for NR-Method.
    # No wrong answer for a linear equation!
    # loop goes as follows: linear, square, cubic, etc.
    x0 = 1
    vertexX = 1       # not needed in first loop (linear)
    archivevertices = []
    lastvertices = [] # keep track of the vertices before
    useLast = False
    vertices = []     # needed above square graphs
    x0s = [x0]
    for x in range(len(dList)-1):
        for a in range(len(vertices)):
            archivevertices.append([vertices[a], x])
        #print("A: " + str(archivevertices))
        if len(vertices)>0:
            if useLast == True:
                #print("lv: " + str(lastvertices))
                #print("V:  " + str(vertices))
                #print("A: " + str(archivevertices))
                lastvertices = editFindList(archivevertices, "NO SOLUTIONS")
                #print("lv: " + str(lastvertices))
                x0s = betweenVals(lastvertices, archivevertices)
            else:
                x0s = betweenVals(vertices, archivevertices)
        useLast = False
        #print()
        #print("Vertices: " + str(vertices))
        #print("X0s: " + str(x0s))
        #print()
        lastvertices = vertices
        vertices.clear()
        derivative = dList[x]
        polynomial = dList[x+1]
        for y in range(len(x0s)):
            x0 = x0s[y]
            x1List = []
            done_checking = False
            weirdcounter = 0
            weirdcounterlimit = 10
            while done_checking==False:
                x0 = newtonRaphson(x0, polynomial, derivative)
                x0 = round(x0, 5)
                x1List.append(x0)

                for i in range(len(x1List)-1):
                    if x1List[i-1] < x1List[i] and x1List[i] > x1List[i+1] and weirdcounter == weirdcounterlimit:
                        vertices.append("NO SOLUTIONS")
                        useLast = True
                        #print(useLast)
                        done_checking = True
                        break
                    if x1List[i] == x1List[i+1]:
                        vertexX = x1List[i+1]
                        vertices.append(vertexX)
                        done_checking = True
                        break
                    if x1List[i-1] < x1List[i] and x1List[i] > x1List[i+1]:
                        weirdcounter +=1
 
        #print("AA: " + str(archivevertices))
    return vertices

            
def getSolutions(polynomial):    
    dList = findDerivatives(polynomial)
    dList = reverse(dList)
    roots = findRoots(dList)
    return roots

print(getSolutions("2x2+5x-7"))
# EQUATION IS PASSED HERE
# THE PROGRAM WILL PASS THE SOLUTIONS IN AN ARRAY FORMAT
# THE ARRAY MAY CONTAIN DUPLICATES.
# THIS IS A BASIC PROGRAM AND CANNOT SOLVE ALL TYPES OF PROBLEMS.
# POLYNOMIALS ARE PREFERRED. 
