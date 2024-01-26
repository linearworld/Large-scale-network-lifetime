import numpy as np
import matplotlib.pyplot as plt
import random
from tqdm import tqdm
import os

#System setting 
#protocol: LEACH protocol
##the position of Base Station：(0,0)
# observed region:  -25<=x<=25   and    0<=y<=50.
#the position of sensor nodes: uniformly randomly distributed in the observed region.
#the position of sensor nodes is stored ./structure_WSN/networkUsedInPaper. The i th line represent the coordinates of the i th node.
# Each living sensor node will send 2000bit to nearest cluster-head every day.
# The cluster-heads will fuse received message to 2000 bit and send to base station.
# The cluster-heads are selected every two days based on LEACH protocol proposed in reference[1].

# Two failure mechanism of sensor nodes
#1）battery depletion 
# In the wilderness, it is challenging to recharge sensor nodes.
# The battery of normal sensors will be used for sending messages.
# The battery of cluster-heads is used for compressing messages, receiving messages and sending messages.
# The energy consumption is calculated based on the First Order Radio model proposed in reference[1].

#2）other factors
# The sensors may fail due to other factors, including moisture, corrosion and animals.
# These factors are quantified by failure rate 10^(-3) * day^(-1).
# This failure rate is set based on the report[2].

#Reference:
#[1] Heinzelman W R, Chandrakasan A, Balakrishnan H. Energy-efficient communication protocol for wireless microsensor networks[C]//Proceedings of the 33rd annual Hawaii international conference on system sciences. IEEE, 2000: 10 pp. vol. 2.
#[2] Munir A, Antoon J, Gordon-Ross A. Modeling and analysis of fault detection and fault tolerance in wireless sensor networks[J]. ACM Transactions on Embedded Computing Systems (TECS), 2015, 14(1): 1-43.

#Energy Comsuption Calculation

E_elect=50*10**(-9) # 50 nJ/ bit
e_amp=100*10**(-12) #100 pJ/bit/m^2 the transmit amplifier 
bit_each_packet=2000 #2000 bit for each meassage
e_computation=5*10**(-9) # 5 nJ/ bit/ message
initial_capacity=0.5 # initial energy of sensor nodes
period_sendingMessage=1 # Sending each message during 1 day

#Calculate Energy Comsuption for Sending Message
def EnergySend(k,distance):
    """k: the number of bits;
    distance: distance between sender and receiver"""
    return E_elect*k+e_amp*k*distance**2

#Calculate Energy Comsuption for Recieving Message
def EnergyRecieve(k):
    """k: the number of bits;"""
    return E_elect*k

#Calculate Energy Comsuption for Fusing Message
def EnergyComputation(k):
    """k: the number of bits;"""
    return e_computation*k

#Module 2:Calculate failure Rate

failure_rate_compare=10**(-3) #10^(-3) day^(-1)
def calFailureRate(capacity):
    return failure_rate_compare #In our case, failure rate does not depends on capacity of battery. More complex setting can be realized by modify this function.
def calTimeToFailure(failure_rate,period_sendingMessage):
    time_to_failure=-np.log(1-random.random())/failure_rate
    return time_to_failure

N_list=100*2**np.array(range(0,10))

def select_clusterHeads(living_nodes,round_last_head,P,round_count):
    clusterHead_list=[]
    for node in living_nodes:
        if(round_last_head[node]<(round_count-int(1/P))): #if this node have not been cluster-head in the last 1/P rounds
            threshold=P/(1-P*(round_count%int(1/P)))
            if(random.random()<threshold):
                clusterHead_list.append(node)
    return clusterHead_list

def distributeLivingNodesToHead(living_nodes,pos_list,clusterHead_list):
    head_map=dict()
    living_nodes_not_head=set(living_nodes)-set(clusterHead_list)
    for not_head_node in living_nodes_not_head:
        distance_square_to_Head_min=float('inf')
        Head_min=-1
        for head in clusterHead_list:
            distance_square_to_Head=(pos_list[not_head_node][0]-pos_list[head][0])**2+(pos_list[not_head_node][1]-pos_list[head][1])**2
            if(distance_square_to_Head<distance_square_to_Head_min):
                Head_min=head
                distance_square_to_Head_min=distance_square_to_Head
        head_map[not_head_node]=(Head_min,distance_square_to_Head_min)
    return head_map

def calEnergyConsumptionEach(living_nodes,clusterHead_list,pos_list,head_map,basic_information=2000):
    capacity_consumed=dict()
    living_nodes_not_head=set(living_nodes)-set(clusterHead_list)
    information_to_process_for_head=dict()
    if(clusterHead_list==[]):
        for node in living_nodes:
            capacity_consumed[node]=0
        return capacity_consumed
    for head in clusterHead_list:
        information_to_process_for_head[head]=0
    for node_not_head in living_nodes_not_head:
        Head_min,distance_square_to_Head_min=head_map[node_not_head]
        information_upload=basic_information
        information_to_process_for_head[Head_min]+=information_upload
        capacity_consumed[node_not_head]=EnergySend(information_upload,(distance_square_to_Head_min)**(1/2))
    for clusterHead in clusterHead_list:
        information=information_to_process_for_head[clusterHead]
        distance=np.sqrt(pos_list[clusterHead][0]**2+pos_list[clusterHead][1]**2)
        basic_information=2000
        capacity_consumed[clusterHead]=EnergyRecieve(information)+EnergyComputation(information)+EnergySend(basic_information,distance)
    return capacity_consumed

def CalRemainEnergyJudgeDeadAndUnsensoredNode(capacity_consumed,capacity_list,clusterHead_list,living_nodes,head_map):
    newly_dead_nodes=[] #dead nodes due to wear-out of battery
    unsensor_living_nodes=[] #Living nodes that can not connect with Base Station due to failure of Cluster-Head
    living_nodes_not_head=set(living_nodes)-set(clusterHead_list)
    for node in living_nodes:
        capacity_list[node]-=capacity_consumed[node]
        if(capacity_list[node]<0):
            newly_dead_nodes.append(node)
    for living_node_not_head in (set(living_nodes_not_head)-set(newly_dead_nodes)):
        Head_min,distance_square_to_Head_min=head_map[living_node_not_head]
        if Head_min in newly_dead_nodes:
            unsensor_living_nodes.append(living_node_not_head)
    return newly_dead_nodes,unsensor_living_nodes

#Initialize the position of nodes
N_list=[800,1600,3200,6400, 12800, 25600, 51200] # the WSN of different size simulated in our code
for N in N_list:
    print("N="+str(N))
    pos_list=[]
    file_name='./structure_WSN/networkUsedInPaper/randomSquare_N='+str(N)+'.txt' # read the position of sensor nodes
    f=open(file_name,'r')
    line=f.readline()
    while(line!=''):
        for _ in range(len(line)):
            if(line[_]==' '):
                s=_
        x=float(line[:s])
        y=float(line[s:])
        pos_list.append((x,y))
        line=f.readline()
    f.close()

    num_of_simulation=2  # The number of repeated simulation times for WSN of each size.
    for zzz in tqdm(range(num_of_simulation)):
        capacity_list=np.ones(N)*initial_capacity #initialize capacity of all sensor nodes
        living_nodes=set(list(range(N)))
        lifetime_node=dict()

        days_in_a_round=2 # update cluster-head every two days
        P=0.05 #fraction of cluster heads in wireless sensor network
        round_last_head=np.ones(N)*(-2*int(1/P)) #the last round when node is cluster-head, which is used for selecting cluster-heads
        round_count=0 #
        day_count=0 #

        while(len(list(living_nodes))>0):
            clusterHead_list=select_clusterHeads(living_nodes,round_last_head,P,round_count) #select cluster-head
            for clusterHead in clusterHead_list:
                round_last_head[clusterHead]=round_count
            head_map=distributeLivingNodesToHead(living_nodes,pos_list,clusterHead_list)
            for day in range(days_in_a_round):
                capacity_consumed=calEnergyConsumptionEach(living_nodes,clusterHead_list,pos_list,head_map,basic_information=2000)
                newly_dead_nodes,unsensor_living_nodes=CalRemainEnergyJudgeDeadAndUnsensoredNode(capacity_consumed,capacity_list,clusterHead_list,living_nodes,head_map)
                for node in newly_dead_nodes:
                    lifetime_node[node]=day_count
                living_nodes=living_nodes-set(newly_dead_nodes) # nodes die of battery wear-out
                day_count+=1
            node_to_failure=[]
            for node in living_nodes:
                capacity=capacity_list[node]
                failure_rate=calFailureRate(capacity)
                period_sendingMessage=1
                failure_prob=1-np.exp(-failure_rate*period_sendingMessage)
                if(random.random()<failure_prob):
                    node_to_failure.append(node)
                    lifetime_node[node]=day_count
            living_nodes=living_nodes-set(node_to_failure) #nodes die of failure
            round_count+=1
        id_count=0
        file_name_to_write='./node_lifetime_log/N='+str(N)+'/nodeLife_N='+str(N)+"_id="+str(id_count)+'.txt'
        while(os.path.exists(file_name_to_write)):
            id_count+=1
            file_name_to_write='./node_lifetime_log/N='+str(N)+'/nodeLife_N='+str(N)+"_id="+str(id_count)+'.txt'
        f=open(file_name_to_write,'w')
        for node in range(N):
            f.write(str(lifetime_node[node])+"\n")
        f.close()