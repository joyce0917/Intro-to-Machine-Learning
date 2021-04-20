import sys
import math
import csv
import copy



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

def strtolst(lst):
    ylst=[]
    xlst=[]
    for i in range(0, len(lst)):
        ylst.append(int(lst[i][0]))
        tempxdict=dict()
        for j in range (1,len(lst[i])):
            tempxdict[int(lst[i][j][:-2])]=1
        xlst.append(tempxdict)
    return (ylst,xlst)

def dotproduct(xdict,thetadict):
    result=0
    for x in xdict:
        if x in thetadict:
            result=result+xdict[x]*thetadict[x]
    return result

def vectormultiple(a,xdict):
    for x in xdict:
        xdict[x]=xdict[x]*a
    return xdict

def vectorsubtract(dict1,dict2):
    for x in dict2:
        if x in dict1:
            dict1[x]-=dict2[x]
        else:
            dict1[x]=-dict2[x]
    return dict1


def sigmoid(v):
    return 1/(1+math.exp(-1*v))


def sgd(y,xdict,theta):
    # print("sgd")
    rate=0.1
    R=-(y-sigmoid(dotproduct(xdict,theta)))
    J=vectormultiple(R,xdict)
    theta=vectorsubtract(theta,vectormultiple(rate,J))
    return theta


def logisticregression(ylst,xlst,numepoch,dictdata):
    # print("logisticregression")
    n=len(xlst)
    m=len(dictdata)
    theta={m:0}
    for k in range (n):
        xlst[k][m]=1
    for i in range (numepoch):
        for j in range (n):
            ylst_j=copy.deepcopy(ylst[j])
            xlst_j=copy.deepcopy(xlst[j])
            theta=sgd(ylst_j,xlst_j,theta)
    return theta


def label(xdict,thetadict):
    # print("label")
    out = dotproduct(xdict,thetadict)
    out = sigmoid(out)
    if out>=0.5:
        out=1
    else:
        out=0
    return out


def predict(xlst,theta):
    # print("predict")
    out=[]
    for i in range(len(xlst)):
        # print(xlst[i])
        out.append(label(xlst[i],theta))
    return out

def error(lst,predict):
    correct=0
    total=0
    for i in range (len(lst)):
        if predict[i]==lst[i]:
            correct+=1
        total+=1
    return (1-correct/total)

def lsttostring(lst):
    out=""
    for i in range(len(lst)):
        out=out+str(lst[i])+"\n"
    return out

if __name__ == '__main__':
    formattedtraininput = sys.argv[1]
    formattedvalidationinput = sys.argv[2]
    formattedtestinput = sys.argv[3]
    dictinput = sys.argv[4]
    trainout = sys.argv[5]
    testout = sys.argv[6]
    metricsout = sys.argv[7]
    numepoch = sys.argv[8]

    traindata=readFile(formattedtraininput)
    validationdata=readFile(formattedvalidationinput)
    testdata=readFile(formattedtestinput)
    dictdata=readtxtFile(dictinput)
    dictdata=setDict(dictdata)


    traindata=strtolst(traindata)
    testdata=strtolst(testdata)
    theta=logisticregression(traindata[0],traindata[1],int(numepoch),dictdata)
    trainlabel=predict(traindata[1],theta)
    testlabel=predict(testdata[1],theta)


    trainerror=round(error(traindata[0],trainlabel),6) 
    testerror=round(error(testdata[0],testlabel),6)
    metrics_string="error(train): "+str(trainerror)+"\nerror(test): "+str(testerror)
   

    print(trainlabel)
    print("\n\n")
    print(testlabel)
    print("\n\n")
    print(metrics_string)
    

    writeFile(metricsout,metrics_string)
    writeFile(trainout,lsttostring(trainlabel))
    writeFile(testout,lsttostring(testlabel))


    # initialtheta=[0 for x in range(len(dictdata))]

    # print(sgd(traindata[0],initialtheta))
    # print(traindata[0])
    # print(traindata[0])

