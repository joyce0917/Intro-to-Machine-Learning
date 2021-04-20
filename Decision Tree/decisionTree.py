import sys
import math
import csv
import copy


def readFile(path):
    with open(path) as f:
        csvlst=list(csv.reader(f,delimiter='\t'))
        return csvlst

def writeFile(path, contents):
    with open(path, "w") as f:
        f.write(contents)


def entropy(i1,i2):
    if i1==0 or i2==0:
        return 0
    p1=float(i1)/float(i1+i2)
    p2=float(i2)/float(i1+i2)
    return -(p1*math.log2(p1)+p2*math.log2(p2))


def mutualinfo(lst, index):
    Atext=""
    Acount=0
    AYcount=0
    AnotYcount=0
    Btext=""
    Bcount=0
    BYcount=0
    BnotYcount=0
    Y=lst[0][-1]


    for i in range(0,len(lst)):
        choice=lst[i][index]
        if Atext=="" or Atext==choice:
            Atext=choice
            Acount+=1
            if Y==lst[i][-1]:
                AYcount+=1
            else:
                AnotYcount+=1
        else:
            Btext=choice
            Bcount+=1
            if Y==lst[i][-1]:
                BYcount+=1
            else:
                BnotYcount+=1

    H_y=entropy(AYcount+BYcount,AnotYcount+BnotYcount)
    H_ya1=Acount/(Acount+Bcount)*entropy(AYcount,AnotYcount)
    H_ya2=Bcount/(Acount+Bcount)*entropy(BYcount,BnotYcount)
    H_ya=H_ya1+H_ya2
    I_ya=H_y-H_ya

    return I_ya

import numpy

def mutualinfo_order(lst):
    mutualinfolst=[0 for x in range(len(lst[0])-1)]
    for i in range(0,len(mutualinfolst)):
        mutualinfolst[i]=mutualinfo(lst,i)
    mutualinfoorder = numpy.argsort(mutualinfolst)[::-1]
    mutualinfoorder = list(mutualinfoorder)
    return [mutualinfolst,mutualinfoorder]


class Node:
    def __init__(self,depth,splitval,splitindex,lst,pastsplit):
        self.left=None
        self.right=None
        self.depth=depth
        self.splitval=splitval
        self.splitindex=splitindex
        self.decision=None
        self.lst=lst
        self.pastsplit=pastsplit
 



def tree(lst,currentnode, depth, maxdepth,splitorder):
    # print("\n\n\n")
    # print("depth="+str(depth)+", splitindex="+str(currentnode.splitindex)+ ", splitval="+str(currentnode.splitval))
    # print("list     ")
    
    # for i in lst:
    #     print (i[3],i[-1])
    # print(lst)
    # print("MI")
    # print(splitorder)
    # print(currentnode.pastsplit)
    if depth==maxdepth:

        decisiona=currentnode.lst[0][-1]
        decisiona_count=0
        decisionb=None
        decisionb_count=0
        for i in range (0,len(currentnode.lst)):
            currentdecision=currentnode.lst[i][-1]
            if currentdecision==decisiona:
                decisiona_count+=1
            else:
                decisionb=currentdecision
                decisionb_count+=1
        if decisiona_count>=decisionb_count:
            currentnode.decision=decisiona
        else:
            currentnode.decision=decisionb
        return
    # elif splitorder[0][splitorder[1][0]]<=0:
    #     decisiona=currentnode.lst[0][-1]
    #     decisiona_count=0
    #     decisionb=None
    #     decisionb_count=0
    #     for i in range (0,len(currentnode.lst)):
    #         currentdecision=decisioncurrentnode.lst[i][-1]
    #         if currentdecision==decisiona:
    #             decisiona_count+=1
    #         elif currentdecision!=decisiona & decisionb==None:
    #             decisionb=currentdecision
    #             decisionb_count+=1
    #         else:
    #             decisionb_count+=1
    #     if decisiona_count>=decisionb_count:
    #         currentnode.decision=decisiona
    #     else:
    #         currentnode.decision=decisionb
    #     return
    else:
        # splitorder=mutualinfo_order(lst)
        # # print("     "+str(depth))
        # # print(splitorder)
        # print(depth)
        # print(alreadysplitlst,splitorder[1])
        # for a in alreadysplitlst:
        #     splitorder[1].remove(a)
        # print("\n\n\n")
        # print("depth="+str(depth)+", splitindex="+str(currentnode.splitindex)+ ", splitval="+str(currentnode.splitval))
        # print("list     ")
        # print(lst)
        # print("MI")
        # print(splitorder)
        # print(currentnode.pastsplit)

        if splitorder[0][splitorder[1][0]]<=0:
            decisiona=currentnode.lst[0][-1]
            decisiona_count=0
            decisionb=""
            decisionb_count=0
            for i in range (0,len(currentnode.lst)):
                currentdecision=currentnode.lst[i][-1]
                if currentdecision==decisiona:
                    decisiona_count+=1
                elif currentdecision!=decisiona and decisionb=="":
                    decisionb=currentdecision
                    decisionb_count+=1
                else:
                    decisionb_count+=1
            if decisiona_count>=decisionb_count:
                currentnode.decision=decisiona
            else:
                currentnode.decision=decisionb
            return


        for a in currentnode.pastsplit:
            splitorder[1].remove(a)
        splitindex=splitorder[1][0]


        leftval=lst[0][splitindex]
        rightval=None
        j=1

        while j<len(lst):
            if leftval!=lst[j][splitindex]:
                rightval=lst[j][splitindex]
            j+=1

        leftlst=[]
        rightlst=[]
        for i in range(0,len(lst)):
            if lst[i][splitindex]==leftval:
                leftlst.append(lst[i])
            else:
                rightlst.append(lst[i])





        pastsplit_copy1 = copy.deepcopy(currentnode.pastsplit)
        pastsplit_copy2 = copy.deepcopy(currentnode.pastsplit)

        currentnode.left= Node(depth+1,leftval,splitindex,leftlst,pastsplit_copy1)
        currentnode.right= Node(depth+1,rightval,splitindex,rightlst,pastsplit_copy2)
        currentnode.left.pastsplit.append(splitindex)
        currentnode.right.pastsplit.append(splitindex)


        
        splitorder_left=mutualinfo_order(leftlst)
        splitorder_right=mutualinfo_order(rightlst)

        tree(leftlst,currentnode.left,depth+1,maxdepth,splitorder_left)
        tree(rightlst,currentnode.right,depth+1,maxdepth,splitorder_right)

        # tree(leftlst,currentnode.left,depth+1,maxdepth,alreadysplitlst)
        # tree(rightlst,currentnode.right,depth+1,maxdepth,alreadysplitlst)




def countY(currentnode):
    if currentnode.depth==0:
        global Y1
        global Y2
        Y1=currentnode.lst[0][-1]
        for i in range (0,len(currentnode.lst)):
            currentdecision=currentnode.lst[i][-1]
            if currentdecision!=Y1:
                Y2=currentdecision
    Y1_count=0
    Y2_count=0
    for i in range (0,len(currentnode.lst)):
        currentdecision=currentnode.lst[i][-1]
        if currentdecision==Y1:
            Y1_count+=1
        else:
            Y2_count+=1
    return "["+str(Y1_count)+" "+Y1+" / "+str(Y2_count)+" "+Y2+"]"


def printTree(root):
    if root:
        if root.depth==0:
            print(countY(root))
            printTree(root.left)
            printTree(root.right)
        else:
            print("| "*root.depth+traindata[0][root.splitindex]+" = "+str(root.splitval)+" : "+countY(root))
            # if root.decision!=None:
            #     print(root.decision)
            printTree(root.left)
            printTree(root.right)


def predict(node,lst):
    if node.decision!=None:
        return node.decision
    elif node.left.splitval==lst[node.left.splitindex]:
        # print("left")
        return predict(node.left,lst)
    else:
        # print("right")
        return predict(node.right,lst)


def trainoutfunc(root,lst):
    result=""
    for i in range(0,len(lst)):
        # print(predict(root,lst[i]))
        result=result+predict(root,lst[i])+"\n"
    return result





def error(root,lst):
    correct=0
    total=0
    for i in lst:
        prediction=predict(root,i)
        if prediction==i[-1]:
            correct+=1
        total+=1
    return (1-correct/total)



if __name__ == '__main__':
    traininput = sys.argv[1]
    testinput = sys.argv[2]
    maxdepth = sys.argv[3]
    trainout = sys.argv[4]
    testout = sys.argv[5]
    metricsout = sys.argv[6] 


    traindata=readFile(traininput)
    testdata=readFile(testinput)
    splitorder=mutualinfo_order(traindata[1:]) #[mutualinfolst,mutualinfoorder]
    maxdepth=int(maxdepth)

    if maxdepth>len(splitorder[0]):
        maxdepth = len(splitorder[0])

    root=Node(0,None,None,traindata[1:],[]) #depth,splitval,splitindex,lst

    tree(traindata[1:], root, 0, maxdepth,splitorder)


    printTree(root)


    writeFile(trainout,trainoutfunc(root,traindata[1:]))
    writeFile(testout,trainoutfunc(root,testdata[1:]))

    trainerror=round(error(root,traindata[1:]),6)
    testerror=round(error(root,testdata[1:]),6)
    
    metrics_string="error(train): "+str(trainerror)+"\nerror(test): "+str(testerror)
    writeFile(metricsout,metrics_string)





















