from subprocess import check_output
import time
import copy
import numpy as np
import pandas as pd
import chainer
import chainer.functions as F
import chainer.links as L
from plotly import tools
from plotly.graph_objs import *
from plotly.offline import download_plotlyjs,init_notebook_mode,plot,iplot,iplot_mpl
# init_notebook_mode(connected=True)
import plotly.graph_objs as go
import matplotlib.pyplot as plt

from Rein import train_dqn

data = pd.read_csv('C:\\shihua.csv')
data['Date'] = pd.to_datetime(data['Date'])
data = data.set_index('Date')
print(data.index.min(),data.index.max())
data.head()
date_split = '2016-01-01'
train = data[:date_split]
test = data[date_split:]
len(train),len(test)
data["High"][:'2015'].plot(figsize=(16,4),legend =True)
data["High"][:'2017'].plot(figsize=(16,4),legend =True)
plt.legend(['Training set (Before 2017)','Test set(2017 and beyond)'])
plt.title('pufa stock price')
plt.show()
class Environment1:
    def __init__(self,data,history_t = 90):
        self.data = data
        self.history_t = history_t
        self.reset()
    def reset(self):
        self.t = 0
        self.done = False
        self.profits = 0
        self.positions = []
        self.position_value = 0
        self.history = [0 for _ in range(self.history_t)]
        return [self.position_value]+self.history
    def step(self,act):
        reward = 0
        if act == 1:
            self.positions.append(self.data.iloc[self.t,:]['Close'])
        elif act ==2:
            if len(self.positions) == 0:
                reward = -1
            else:
                profits = 0
                for p in self.positions:
                    profits += (self.data.iloc[self.t,:]['Close']-p)
                    reward +=profits
                    self.profits += profits
                    self.positions = []
        self.t += 1
        self.position_value = 0
        for p in self.positions:
            self.position_value +=(self.data.iloc[self.t,:]['Close']-p)
        self.history.pop(0)
        self.history.append(self.data.iloc[self.t,:]['Close']-self.data.iloc[self.t-1,:]['Close'])
        if reward > 0:
            reward = 1
        elif reward < 0:
            reward = -1
        return [self.position_value] + self.history,reward,self.done

env = Environment1(train)
print(env.reset())
for _ in range(3):
    pact = np.random.randint(3)
    print(env.step(pact))

def train_ddqn(env):

    class Q_Network(chainer.Chain):
        def __init__(self,input_size,hidden_size,output_size):
            super(Q_Network,self).__init__(
                fc1 = L.Linear(input_size,hidden_size),
                fc2 = L.Linear(hidden_size,hidden_size),
                fc3 = L.Linear(hidden_size,output_size)
            )
        def __call__(self, x):
            h = F.relu(self.fc1(x))
            h = F.relu(self.fc2(h))
            y = self.fc3(h)
            return y
        def reset(self):
            self.zerograds()
    Q = Q_Network(input_size=env.history_t+1,hidden_size=100,output_size=3)
    Q_ast = copy.deepcopy(Q)
    optimizer = chainer.optimizers.Adam()
    optimizer.setup(Q)
    epoch_num = 50
    step_max = len(env.data)-1
    memory_size = 200
    batch_size = 20
    epsilon = 1.0
    epsilon_decrease = 1e-3
    epsilon_min = 0.1
    start_reduce_epsilon = 200
    train_freq = 10
    update_q_freq = 20
    gamma = 0.97
    show_log_freq = 5

    memory = []
    total_step = 0
    total_rewards = []
    total_losses = []
    start = time.time()
    for epoch in range(epoch_num):
        pobs = env.reset()
        step = 0
        done = False
        total_reward = 0
        total_loss = 0
        while not done and step < step_max:
            pact = np.random.randint(3)
            if np.random.rand() > epsilon:
                pact = Q(np.array(pobs,dtype=np.float32).reshape(1,-1))
                pact = np.argmax(pact.data)
            obs,reward,done = env.step(pact)
            memory.append((pobs,pact,reward,obs,done))
            if len(memory) > memory_size:
                 memory.pop(0)
            if len(memory) == memory_size:
                if total_step % train_freq == 0:
                    shuffled_memory = np.random.permutation(memory)
                    memory_idx = range(len(shuffled_memory))
                    for i in memory_idx[::batch_size]:
                        batch = np.array(shuffled_memory[i:i+batch_size])
                        b_pobs = np.array(batch[:,0].tolist(),dtype=np.float32).reshape(batch_size,-1)
                        b_pact = np.array(batch[:,1].tolist(),dtype=np.int32)
                        b_reward = np.array(batch[:,2].tolist(),dtype=np.int32)
                        b_obs = np.array(batch[:,3].tolist(),dtype=np.float32).reshape(batch_size,-1)
                        b_done = np.array(batch[:,4].tolist(),dtype=np.bool)

                        q = Q(b_pobs)
                        # maxq = np.max(Q_ast(b_obs).data,axis=1)
                        indices = np.argmax(q.data,axis=1)
                        maxqs = Q_ast(b_obs).data
                        target = copy.deepcopy(q.data)
                        for j in range(batch_size):
                            target[j,b_pact[j]] = b_reward[j]+gamma*maxqs[j,indices[j]]*(not b_done[j])
                        Q.reset()
                        loss = F.mean_squared_error(q,target)
                        total_loss += loss.data
                        loss.backward()
                        optimizer.update()
                if total_step % update_q_freq ==0:
                    Q_ast = copy.deepcopy(Q)
            if epsilon > epsilon_min and total_step > start_reduce_epsilon:
                epsilon -= epsilon_decrease

            total_reward += reward
            pobs = obs
            step += 1
            total_step += 1
        total_rewards.append(total_reward)
        print("计算中"+str(total_step))
        total_losses.append(total_loss)
        if (epoch+1)% show_log_freq ==0:
            a = epoch+1 - show_log_freq
            # los = epoch+1
            fule = sum(total_rewards[a:])
            fule_loss = sum(total_losses[a:])
            log_reward = fule/show_log_freq
            log_loss = fule_loss/show_log_freq
            elapsed_time = time.time() - start
            print('\t'.join(map(str,[epoch+1,epsilon,total_step,log_reward,log_loss,elapsed_time])))
            start = time.time()
    return Q,total_losses,total_rewards
Q,total_losses,total_rewards = train_dqn(Environment1(train))

def plot_loss_reward(total_losses,total_rewards):
    plt.plot(total_rewards, color='red', label='shouyi')
    plt.title('fankui')
    plt.xlabel('epoch')
    plt.ylabel('shoyi')
    plt.legend()
    plt.show()
    plt.plot(total_losses, color='red', label='loss')
    plt.title('loss')
    plt.xlabel('epoch')
    plt.ylabel('loss')
    plt.legend()
    plt.show()
    # figure = tools.make_subplots(rows=1,cols=2,subplot_titles = ('loss','reward'),print_grid=False)
    # figure.append_trace(Scatter(y=total_losses,mode='lines',line = dict(color = 'skyblue')),1,1)
    # figure.append_trace(Scatter(y=total_rewards,mode='lines',line = dict(color = 'orange')),1,1)
    # figure['layout']['xaxis1'].update(title = 'epoch')
    # figure['layout']['xaxis2'].update(title = 'epoch')
    # figure['layout'].update(height=400,width = 900,showlegend = False)
    # iplot(figure)
plot_loss_reward(total_losses,total_rewards)




