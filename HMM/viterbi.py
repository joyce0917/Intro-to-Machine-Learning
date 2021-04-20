import sys
import numpy as np




def writeFile(path, contents):
    with open(path, "w") as f:
        f.write(contents)


def read_train(train_input):
    with open(train_input) as f:
        lines=f.readlines()
        linelst=[]
        for line in lines:
            words=line.split()
            wordslst=[]
            for word in words:
                sep=word.strip().split("_")
                wordslst.append(sep[0])
            linelst.append(wordslst)
    return linelst


def read_index(index_to_word):
    word_dict={}
    with open(index_to_word) as f:
        lines=f.readlines()
        for i in range (len(lines)):
            word_dict[lines[i].strip()]=i
    return word_dict

def read_index2(index_to_word):
    wordlst=[]
    with open(index_to_word) as f:
        lines=f.readlines()
        for i in range (len(lines)):
            wordlst.append(lines[i].strip())
    return wordlst

def read_pi(pi):
    pilst=[]
    with open(pi) as f:
        lines=f.readlines()
        for word in lines:
            pilst.append(np.float(word.strip()))
    return pilst

def read_AB(AB):
    ABlst=[]
    with open(AB) as f:
        lines=f.readlines()
        for line in lines:
            wordlst=[]
            line=line.strip().split(" ")
            for word in line:
                wordlst.append(np.float(word))
            ABlst.append(wordlst)
    return ABlst    


def lw_func(t,j,lw,A,B,J,i):
    lst=np.zeros(J)
    for k in range(J):
        lst[k]=np.log(B[j][word_dict.get(test_data[i][t])])+np.log(A[k][j])+lw[t-1][k]
    return (np.max(lst),np.argmax(lst))



def viterbi(test_data,tag_dict,pi,A,B,word_dict):
    ylst=[0 for i in range(len(test_data))]
    # print(pi)
    # print(A)
    # print(B)
    for i in range(len(test_data)):
    # for i in range(1,2):
        T=len(test_data[i])     #word1 word2 ... word t
        J=len(tag_dict)         #A B
        lw=np.zeros((T,J))     
        p=np.zeros((T,J))

        for t in range(T):
            for j in range(J):
                if t==0:
                    firstword=word_dict.get(test_data[i][0])
                    lw[t][j]=np.log(pi[j])+np.log(B[j][firstword])
                    p[t][j]=np.int(j)
                else:
                    lw[t][j]=lw_func(t,j,lw,A,B,J,i)[0]
                    p[t][j]=np.int(lw_func(t,j,lw,A,B,J,i)[1])
        
        ylst2=[0 for i in range(T)]
        ylst2[T-1]=np.int(np.argmax(lw[T-1]))
        for t in range (T-1,0,-1):
            ylst2[t-1]=p[t][np.int(ylst2[t])]
        ylst[i]=ylst2
    return ylst




def predict(test_data,ylst,taglst):
    out=""
    for i in range(len(test_data)):
        for j in range(len(test_data[i])):
            out=out+test_data[i][j]+"_"+taglst[np.int(ylst[i][j])]+" "
        out=out[:-1]
        out=out+"\n"
    return out


def read_train2(train_input,tag_dict):
    with open(train_input) as f:
        lines=f.readlines()
        linelst=[]
        for line in lines:
            words=line.split()
            wordslst=[]
            for word in words:
                sep=word.strip().split("_")
                wordslst.append(tag_dict.get(sep[1]))
            linelst.append(wordslst)
    return linelst


def accuracy(test_data2,ylst):
    count=0
    total=0
    for i in range(len(ylst)):
        for j in range(len(ylst[i])):
            total+=1
            if test_data2[i][j]==ylst[i][j]:
                count+=1
    return count/total





if __name__ == '__main__':

    test_input = sys.argv[1]   
    index_to_word = sys.argv[2]
    index_to_tag = sys.argv[3]
    hmmprior = sys.argv[4]
    hmmemit = sys.argv[5]
    hmmtrans = sys.argv[6]
    predicted_file = sys.argv[7]
    metric_file = sys.argv[8]

    test_data=read_train(test_input)
    word_dict=read_index(index_to_word)
    tag_dict=read_index(index_to_tag)
    tag_lst=read_index2(index_to_tag)
    test_data2=read_train2(test_input,tag_dict)

    # train_data=change_train(train_data,word_dict,tag_dict)
    pi=read_pi(hmmprior)
    A=read_AB(hmmtrans)
    B=read_AB(hmmemit)

    ylst=viterbi(test_data,tag_dict,pi,A,B,word_dict)
    prediction=predict(test_data,ylst,tag_lst)
    accurate=accuracy(test_data2,ylst)
    print(prediction)
    print(accurate)
    writeFile(predicted_file,prediction)

    writeFile(metric_file,str(accurate)) 





