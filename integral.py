#!/usr/bin/env python3
import sys
from scipy import integrate
import numpy as np
import math
import re

def mathToPython(mathFunc):
    mathFunc=re.sub(r"(?<=[\*\+/-])([\d\w]+)(?=\()",r"math.\1",mathFunc);
    mathFunc=re.sub(r"^([\d\w]+)(?=\()",r"math.\1",mathFunc);
    mathFunc=re.sub(r"(^|(?<=[\*\+/-]))e((?=[\*\+/-])|$)",r"math.e",mathFunc);
    mathFunc=re.sub(r"(^|(?<=[\*\+/-]))pi((?=[\*\+/-])|$)",r"math.pi",mathFunc);
    return mathFunc

def getIntegralNumber():
    if(len(sys.argv)!=2):
        print("Error: require 1 argument, the number of integrals.")
        sys.exit(1);
    try: 
        num=int(sys.argv[1])
    except:
        print("Error: require a number parameter, the number of integrals.")
        sys.exit(1);
    if(num<1):
            print("Error: minimum integral number is 1.")
            sys.exit();
    return num;

def getBounds(num):
    print("Enter bounds from left to right. For each bound, \
enter the lower then the upper, separated by a single space.")
    bounds=[]
    for i in range(0,num):
        print("Bound ",i+1,": ",sep="",end="")
        bound=input().split(' ')
        if(len(bound)!=2):
            print("Error: require lower bound then upper bound, separated by a space.")
            print("Recieved: ",bound)
            sys.exit(1)
        bound[0]=mathToPython(bound[0])
        bound[1]=mathToPython(bound[1])
        bounds.append(bound);
    return bounds

def getBoundStr(bounds,var):
    boundStr=[]
    for i in range (0,len(bounds)):
        myVars="(";
        for j in range (len(bounds)-i, len(bounds)):
            if(j==len(bounds)-1):
                myVars+=var[j]
            else:
                myVars+=var[j]+','
        myVars+=")"
        boundStr.append("def Bound"+str(i+1)+myVars+":\n\treturn ["+bounds[i][0]+", "+bounds[i][1]+"]\n")
    return boundStr

def getFunc():
    print("Enter the function: ",end="")
    func=mathToPython(input())
    return func

def getFuncStr(func, var):
    funcStr="def funct("+','.join(var)+"):\n\treturn "+func+"\n"
    return funcStr

def getVars(num):
    print("Differentials in order separated by spaces: ",end="")
    vars=input().split(' ')
    if(len(vars)!=num):
        print("Error: require",num,"differentials separated by single spaces.")
        print("Recieved: ",vars)
        sys.exit(1)
    return vars

def run():
    print("Common calls: x**y, pi, e, log(x[, base]), abs(x), acos(rad), tan(rad)")
    num=getIntegralNumber()
    strs=""
    for i in range (0, num):
        if(i==num-1):
            strs+="Bound"+str(num-i)
        else:
            strs+="Bound"+str(num-i)+", "
    bounds=getBounds(num)
    func=getFunc()
    var=getVars(num)
    boundStrs=getBoundStr(bounds,var)
    funcStr=getFuncStr(func,var)
    inteStr="integrate.nquad(funct,["+strs+"])"
    for i in range (0, num):
        try:
            exec(boundStrs[i])
        except:
            print("Error: bound",i,"not recognized.")
            print("Tried to process", bounds[i])
            sys.exit(1)
    try:
        exec(funcStr)
    except:
        print("Error: function not recognized")
        print("Tried to process ", func)
        sys.exit(1)
    try:
        ans=eval(inteStr)
    except:
        print("Evaluation failed!")
        print("Attempted... ")
        print(boundStrs)
        print(funcStr)
        print(inteStr)
        sys.exit(1)
    print("Answer:",ans[0])





def main():
    run();
    


    
if __name__ == "__main__":
    main()
