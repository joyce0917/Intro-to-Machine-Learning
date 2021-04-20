import sys
import math
import csv
import copy
import numpy as np




def readFile(path):
    with open(path) as f:
        csvlst=list(csv.reader(f))
        return csvlst


def writeFile(path, contents):
    with open(path, "w") as f:
        f.write(contents)


def generateWeight(row,col,initflag):
    if initflag ==1 :
        M=np.random.uniform(low=-0.1, high=0.1, size=(row,col))
    else:
        M=np.zeros((row,col))
    return M


def linearForward(a,b):
    return np.dot(b,a)


def sigmoid(x):
    return 1 / (1 + math.exp(-x))


def sigmoidForward(a):
    return np.vectorize(sigmoid)(a)


def softmaxForward(b):
    denominator=np.sum(np.exp(b))
    y_hat=np.exp(b)/denominator
    return y_hat


def crossentropyForward(y,y_hat):
    y_hat=np.log(y_hat)
    loss=np.sum(np.multiply(y,y_hat))
    return -loss


class O:
    def __init__(self,x,a,z,b,y_hat,J):
        self.x=x
        self.a=a
        self.z=z
        self.b=b
        self.y_hat=y_hat
        self.J=J


def object(x,a,z,b,y_hat,J):
    o=O(x,a,z,b,y_hat,J)
    return o


def NNForward(x,y,alpha,beta):
    a=linearForward(x,alpha)    # hiddenunits x 1
    z=sigmoidForward(a)         # hiddenunits x 1
    z=np.insert(z,0,1,axis=0)   # (hiddenunits+1) x 1
    b=linearForward(z,beta)     # 10 x 1
    y_hat=softmaxForward(b)     # 10 x 1
    J=crossentropyForward(y,y_hat)
    o=object(x,a,z,b,y_hat,J) #struct
    # print(y)
    # print(a)
    # print(z)
    # print(b)
    # print(y_hat)
    # print(J)
    return o


def softmaxBackward(y,y_hat):
    return np.subtract(y_hat,y)


def sigmoidBackward(z,g_z):
    g_a=np.multiply(g_z,z)
    g_a=np.multiply(g_a,(1-z))
    # z2=np.subtract(1,z)
    # dot=np.matmul(z.transpose(),z2)
    # g_a=np.multiply(dot,g_z)
    return g_a


def NNBackward(x,y,alpha,beta,o):
    a=o.a
    z=o.z
    b=o.b
    y_hat=o.y_hat
    J=o.J

    #y 10x1 y_hat 10x1         
    g_b=softmaxBackward(y,y_hat)            # 10 x 1
    # print(g_b)
    #g_b 10x1 z 5x1
    g_beta=np.matmul(g_b,z.transpose())     # 10x5
    print(g_beta)
    betastar=np.delete(beta,0,1)
    g_z=np.matmul(betastar.transpose(),g_b) #
    z=z[1:]
    g_a=sigmoidBackward(z,g_z)              # hiddenunits x 1
    g_alpha=np.matmul(g_a,x.transpose())
    
    return (g_alpha,g_beta)



def train(traindata,testdata,numepoch,learningrate,initflag,hiddenunits):

    # alpha=np.matrix([[1,1,2,-3,0,1,-3],[1,3,1,2,1,0,2],[1,2,2,2,2,2,1],[1,1,0,2,1,-2,2]])
    # beta=np.matrix([[1,1,2,-2,1],[1,1,-1,1,2],[1,3,1,-1,1]])


    # alpha hiddenunits x 128
    alpha=generateWeight(hiddenunits,128,initflag)
    alpha=np.insert(alpha,[0],0,axis=1)


    # beta 10 x hiddenunits
    beta=generateWeight(10,hiddenunits,initflag)
    beta=np.insert(beta,[0],0,axis=1)



    avg_train=[]
    avg_test=[]
    for epoch in range(numepoch):
        avg_cross_entropy=0
        for row in traindata:
            x=row[1:]
            x=np.insert(x,0,1)
            x=np.asmatrix(x).transpose()
            y=row[0]

            yvector=np.zeros(10)
            yvector[y]=1
            yvector=np.asmatrix(yvector).transpose()
            y=yvector

            o=NNForward(x,y,alpha,beta)
            (g_alpha,g_beta)=NNBackward(x,y,alpha,beta,o)
            alpha=np.subtract(alpha,np.multiply(learningrate,g_alpha))
            beta=np.subtract(beta,np.multiply(learningrate,g_beta))
        

        for row in traindata:
            x=row[1:]
            x=np.insert(x,0,1)
            x=np.asmatrix(x).transpose()
            y=row[0]
            yvector=np.zeros(10)
            yvector[y]=1
            yvector=np.asmatrix(yvector).transpose()
            y=yvector
            o=NNForward(x,y,alpha,beta)
            avg_cross_entropy+=o.J
        avg_cross_entropy=avg_cross_entropy/len(traindata)
        avg_train.append(avg_cross_entropy)

        test_cross_entropy=0
        for row in testdata:
            x=row[1:]
            x=np.insert(x,0,1)
            x=np.asmatrix(x).transpose()
            y=row[0]
            yvector=np.zeros(10)
            yvector[y]=1
            yvector=np.asmatrix(yvector).transpose()
            y=yvector
            o=NNForward(x,y,alpha,beta)
            test_cross_entropy+=crossentropyForward(y,o.y_hat)
        test_cross_entropy=test_cross_entropy/len(testdata)
        avg_test.append(test_cross_entropy)

    return (alpha,beta,avg_train,avg_test)



def error(lst,predict):
    correct=0
    total=0
    for i in range (len(lst)):
        if predict[i]==lst[i]:
            correct+=1
        total+=1
    return (1-correct/total)



def predict(data,alpha,beta):
    out=[]
    for row in data:
        x=row[1:]
        x=np.insert(x,0,1)
        x=np.asmatrix(x).transpose()
        y=row[0]
        yvector=np.zeros(10)
        yvector[y]=1
        yvector=np.asmatrix(yvector).transpose()
        y=yvector
        o=NNForward(x,y,alpha,beta)
        predicted=np.argmax(o.y_hat)
        out.append(predicted)
    return out


def lsttostring(lst):
    out=""
    for i in range(len(lst)):
        out=out+str(lst[i])+"\n"
    return out

if __name__ == '__main__':
    # traindata=[[1,1,1,0,0,1,1]]
    # testdata=[]
    # train(traindata,testdata,1,1,1,4)
    traininput = sys.argv[1]
    testinput = sys.argv[2]
    trainout = sys.argv[3]
    testout = sys.argv[4]
    metricsout = sys.argv[5]
    numepoch = sys.argv[6]
    hiddenunits = sys.argv[7]
    initflag = sys.argv[8]  # 1:random / 2:all 0
    learningrate = sys.argv[9]

    traindata=readFile(traininput)
    testdata=readFile(testinput)
    traindata=np.array(traindata)
    traindata=traindata.astype(int)
    testdata=np.array(testdata)
    testdata=testdata.astype(int)

    numepoch=int(numepoch)
    hiddenunits=int(hiddenunits)
    initflag=int(initflag)
    learningrate=float(learningrate)


    (alpha,beta,avg_train,avg_test)=train(traindata,testdata,numepoch,learningrate,initflag,hiddenunits)

    trainlabel=predict(traindata,alpha,beta)
    testlabel=predict(testdata,alpha,beta)

    traindata_y=traindata[:,:1]
    testdata_y=testdata[:,:1]
    trainerror=error(trainlabel,traindata_y)
    testerror=error(testlabel,testdata_y)


    metrics=""
    for i in range(numepoch):
        metrics=metrics+"epoch="+str(i)+" crossentropy(train): "+str(avg_train[i])+"\n"
        metrics=metrics+"epoch="+str(i)+" crossentropy(test): "+str(avg_test[i])+"\n"
    metrics=metrics+"error(train): "+str(round(trainerror,2))+"\n"
    metrics=metrics+"error(test): "+str(round(testerror,2))+"\n"
    print(metrics)
    writeFile(metricsout,metrics)
    writeFile(trainout,lsttostring(trainlabel))
    writeFile(testout,lsttostring(testlabel))

