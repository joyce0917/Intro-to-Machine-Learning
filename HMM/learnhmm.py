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
            wordslst=[]
            words=line.split()
            for word in words:
                sep=word.strip().split("_")
                wordslst.append([sep[0],sep[1]])
            linelst.append(wordslst)
    return linelst

def read_index(index_to_word):
    word_dict={}
    with open(index_to_word) as f:
        lines=f.readlines()
        for i in range (len(lines)):
            word_dict[lines[i].strip()]=i
    return word_dict

def change_train(train_data,word_dict,tag_dict):
    for line in train_data:
        for words in line:
            words[0]=word_dict.get(words[0])
            words[1]=tag_dict.get(words[1])
    return train_data


def pi(train_data,tag_dict):
    pilst=np.zeros(len(tag_dict))
    for line in train_data:
        pilst[line[0][1]]+=1
    pilst+=1
    pilst=np.divide(pilst,np.sum(pilst))
    return pilst


def A(train_data,tag_dict):
    A_lst=np.zeros((len(tag_dict),len(tag_dict)))
    for line in train_data:
        for i in range(len(line)-1):
            A_lst[line[i][1],line[i+1][1]]+=1
    A_lst+=1
    for i in range(len(A_lst)):
        A_lst[i]=np.divide(A_lst[i],np.sum(A_lst[i]))
    return A_lst


def B(train_data,tag_dict,word_dict):
    B_lst=np.zeros((len(tag_dict),len(word_dict)))
    for line in train_data:
        for word in line:
            B_lst[word[1],word[0]]+=1
    B_lst+=1
    for i in range(len(B_lst)):
        B_lst[i]=np.divide(B_lst[i],np.sum(B_lst[i]))
    return B_lst


def writepi(pi):
    out=""
    for i in range(len(pi)):
        out=out+'%.18e'%(pi[i])+"\n"
    return out

def writeAB(AB):
    out=""
    for i in range(len(AB)):
        for j in range(len(AB[i])):
            out=out+'%.18e'%(AB[i][j])+" "
        out=out+"\n"
    return out


if __name__ == '__main__':

    train_input = sys.argv[1]   
    index_to_word = sys.argv[2]
    index_to_tag = sys.argv[3]
    hmmprior = sys.argv[4]
    hmmemit = sys.argv[5]
    hmmtrans = sys.argv[6]

    train_data=read_train(train_input)
    word_dict=read_index(index_to_word)
    tag_dict=read_index(index_to_tag)

    train_data=change_train(train_data,word_dict,tag_dict)
    pi=pi(train_data,tag_dict)
    A=A(train_data,tag_dict)
    B=B(train_data,tag_dict,word_dict)
    pistr=writepi(pi)
    Astr=writeAB(A)
    Bstr=writeAB(B)

    writeFile(hmmprior,pistr)
    writeFile(hmmemit,Bstr)
    writeFile(hmmtrans,Astr)
    





