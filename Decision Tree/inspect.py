import sys
import math
import csv


def readFile(path):
    with open(path) as f:
        csvlst=list(csv.reader(f,delimiter='\t'))
        return csvlst

def writeFile(path, contents):
    with open(path, "w") as f:
        f.write(contents)

def inspect(lst):
    option1=""
    option1_count=0
    option2=""
    option2_count=0

    for i in range(1,len(lst)):
        option=lst[i][len(lst[0])-1]
        if option1=="" or option1==option:
            option1=option
            option1_count+=1
        else:
            option2=option
            option2_count+=1

    #entropy
    if option1_count==0 or option2_count==0:
        entropy=0
    else:
        p1=float(option1_count)/float(option1_count+option2_count)
        p2=float(option2_count)/float(option1_count+option2_count)
        entropy= -(p1*math.log(p1)/math.log(2)+p2*math.log(p2)/math.log(2))

    #error
    majority=max(option1_count,option2_count)
    error=1-float(majority)/float(option1_count+option2_count)

    return "entropy: "+str(entropy)+"\n"+"error: "+str(error)



if __name__ == '__main__':
    infile = sys.argv[1]
    outfile = sys.argv[2]
    csvlst=readFile(infile)
    output=inspect(csvlst)
    writeFile(outfile,output)



