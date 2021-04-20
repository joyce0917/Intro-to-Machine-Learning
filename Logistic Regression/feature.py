import sys
import math
import csv
import copy
import numpy as np


def readFile(path):
    with open(path) as f:
        csvlst=list(csv.reader(f,delimiter='\t'))
        return csvlst

def readtxtFile(path):
    with open(path, "rt") as f:
        return f.read()

def writeFile(path, contents):
    with open(path, "w") as f:
        f.write(contents)

def setDict(dict):
    dict=dict.split("\n")
    dict=[x.split() for x in dict]
    return dict[:-1]

def strtolst(lst,dict):
    dictlst=[word[0] for word in dict]
    cleanlst=[]
    for i in range(0, len(lst)):
        lst[i][1]=lst[i][1].split()
        lst[i][1]=[dictlst.index(word) for word in lst[i][1] if word in dictlst]
        uniqueword=np.unique(lst[i][1])
        freqlst=[(word,lst[i][1].count(word)) for word in uniqueword]
        cleanlst.append([lst[i][0],freqlst])
    return cleanlst


def model1(lst,dict):
    dictlst=[word[0] for word in dict]
    cleanlst=[]
    for i in range(0, len(lst)):
        lst[i][1]=lst[i][1].split()
        lst[i][1]=[dictlst.index(word) for word in lst[i][1] if word in dictlst]
        uniqueword=np.unique(lst[i][1])
        freqlst=[word for word in uniqueword]
        cleanlst.append([lst[i][0],freqlst])
    return cleanlst


def model2(lst,dict):
    dictlst=[word[0] for word in dict]
    cleanlst=[]
    for i in range(0, len(lst)):
        lst[i][1]=lst[i][1].split()
        lst[i][1]=[dictlst.index(word) for word in lst[i][1] if word in dictlst]
        uniqueword=np.unique(lst[i][1])
        uniquelst=[]
        for word in uniqueword:
            if lst[i][1].count(word)<4:
                uniquelst.append(word)
        cleanlst.append([lst[i][0],uniquelst])
    return cleanlst


def outstring(lst):
    outstr=""
    for line in lst:
        outstr+=str(line[0])
        for word in line[1]:
            outstr=outstr+"\t"+str(word)+":1"
        outstr+="\n"
    return outstr


if __name__ == '__main__':
    traininput = sys.argv[1]
    validationinput = sys.argv[2]
    testinput = sys.argv[3]
    dictinput = sys.argv[4]
    formattedtrainout = sys.argv[5]
    formattedvalidationout = sys.argv[6]
    formattedtestout = sys.argv[7]
    featureflag = sys.argv[8]

    traindata=readFile(traininput)
    validationdata=readFile(validationinput)
    testdata=readFile(testinput)
    dictdata=readtxtFile(dictinput)
    dictdata=setDict(dictdata)

    if featureflag == "1":
        traindata=model1(traindata,dictdata)
        validationdata=model1(validationdata,dictdata)
        testdata=model1(testdata,dictdata)
    if featureflag == "2":
        traindata=model2(traindata,dictdata)
        validationdata=model2(validationdata,dictdata)
        testdata=model2(testdata,dictdata)

    trainout=outstring(traindata)
    validationout=outstring(validationdata)
    testout=outstring(testdata)
    writeFile(formattedtrainout,trainout)
    writeFile(formattedvalidationout,validationout)
    writeFile(formattedtestout,testout)
    
