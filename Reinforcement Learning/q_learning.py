from environment import MountainCar
import sys
import numpy as np

np.random.seed(10601)

def getQ(env, bias, weight, action, state):
    Q=0
    for key, value in state.items():
        Q+=value*weight[key,action]
    return Q+bias



def Qlearning(env, episodes, max_iterations, epsilon, gamma, learning_rate, bias, weight):
    rewardlst=[]


    for episode in range(episodes):
        state=env.reset()
        # print(state)
        done=False
        rewardsum=0

        iteration=0
        while (done==False and iteration<max_iterations):
            # print("episode",episode)
            # print("iteration = ", iteration)
            Qlst = [getQ(env,bias,weight,0,state),getQ(env,bias,weight,1,state),getQ(env,bias,weight,2,state)]
            # print("Qlst", Qlst)
            action = Qlst.index(max(Qlst))
            # print("optimalaction", action)

            actionp = np.ones(3, dtype = float) * epsilon / 3 
            actionp[action]+=(1-epsilon)
            action = np.random.choice(np.arange(len(actionp)),p = actionp) 


            Q = Qlst[int(action)]
            nextstate, reward, done = env.step(action) #state, reward, end
            for key in nextstate:
                nextstate[key]=np.float64(nextstate[key])
            Q2=max(getQ(env,bias,weight,0,nextstate),getQ(env,bias,weight,1,nextstate),getQ(env,bias,weight,2,nextstate))
            for key, value in state.items():
                weight[key, action]=weight[key, action]-learning_rate*(Q - (reward + gamma * Q2))*value
            bias=bias-learning_rate*(Q - (reward + gamma * Q2))
            rewardsum+=reward
            iteration+=1
            state=nextstate

            # print(weight)
            # print(bias)




        rewardlst.append(rewardsum)
    return(rewardlst, weight, bias)


def writeFile(path, contents):
    with open(path, "w") as f:
        f.write(contents)


def weightstr(weight, bias):
    out=str(bias)+"\n"
    for row in weight:
        for col in row:
            out=out+str(col)+"\n"
    return out

def rewardstr(reward):
    out=""
    for i in reward:
        out=out+str(i)+"\n"
    return out






if __name__ == '__main__':

    mode = sys.argv[1]      #"raw" or "tile"
    weight_out = sys.argv[2]
    returns_out = sys.argv[3]
    episodes = int(sys.argv[4])
    max_iterations = int(sys.argv[5])
    epsilon = float(sys.argv[6])
    gamma = float(sys.argv[7])
    learning_rate = float(sys.argv[8])

    if mode == "raw":
        initweight = np.zeros((2, 3))
    elif mode == "tile":
        initweight = np.zeros((2048, 3))
    initbias=0



    env=MountainCar(mode)


    rewardlst,weight,bias=Qlearning(env, episodes, max_iterations, epsilon, gamma, learning_rate, initbias, initweight)

    writeFile(weight_out,weightstr(weight,bias))
    writeFile(returns_out,rewardstr(rewardlst))





