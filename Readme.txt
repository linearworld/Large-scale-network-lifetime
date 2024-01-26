This is the implementation code for the study " Large-scale network lifetime inference based on universal scaling function ". The method of implementation is mainly dependent on the Python language. 

Environment and Use Guide:
Python language code needs to open in the Jupyter notebook environment or in the spyder development environment and run the corresponding part of the code.

Python language code useage: 
Our code includes two parts: 1. Code for failure coupling network. 2. Code for wireless sensor network case.

1. Failure coupling network
In the " Model_FailureCouplingNetwork " folder, we have the code and data for failure coupling network study in section II. In this folder, we have two subfolder, namely ¡°life_data¡± and ¡°fig_Maintext¡±, and a Jupyter notebook file "TimeDataProcess.ipynb".

1.1 system setting

In this model, the failure of one component will induce the failure rate increment of other components coupled to it. The impact of neighboring failures on the failure rate of each component is characterized by a sublinear (0<¦Ç<1), linear (¦Ç=1) , or superlinear (¦Ç>1) relationship. When ¦Ç=1, our model corresponds to the Marshall-Olkin model only considering pairwise interaction [1-2], which is widely used in modeling failure coupling system [3-5]. 

The networks in our manuscript include Barabasi-Albert(BA) network, Cayley Tree and two dimension square lattice network. 


1.2 1 simulation code

We use Monte Carlo simulation at each step to sample both the next time a component fails and which component fails. And the failure rate of one component will increases if their coupled component is dead. A network is dead when more than 10%  nodes are dead. Thus we get lifetime data of three networks under three situations(¦Ç=0.5, ¦Ç=1, ¦Ç=2).

The simulation code for generating the lifetime in different neroworks is in folder:
 "Model_FailureCouplingNetwork/ life_data/ code_GenerateSamples". This folder includes 9 code files . They are codes for different networks under different situations. 
For example, ¡°lineBA_shape=5.py¡± is xxxxcode for simulating BA network with linear interaction (¦Ç=1). 
¡°supBA_shape=5.py¡± is code for simulating BA network with superlinear interaction (¦Ç=2). 
¡°subBA_shape=5.py¡± is code for simulating BA network with sublinear interaction (¦Ç=0.5). 


Because Considering the time of simulation is long, we have prepared the simulation data we used for readers in folder ¡°life_data¡±, as following.:

The lifetime data for Cayley tree networks is stored in folder: ' FailureCouplingNet /./life_data/Cayley'.
The lifetime data for 2D Lattice networks is stored in folder: './FailureCouplingNet/life_data/Lattice'.
The lifetime data for BA networks is stored in folder: './FailureCouplingNet/life_data/BA'.
We gathered the lifetime simulation data under different networks types, network sizes (N), impact of neighboring failures on the failure rate of each component (power), shape parameter (shape) and coupling strength (phi). Lifetime simulation data files are named based on these situations. 
For example, ¡°Lattice_N=400_power=1_shape=2_phi=4.txt¡± in folder './life_data/Lattice' means this file is the lifetime data for lattice network with 400 nodes, in which the impact of neighboring failures on the failure rate of each component is 1, shape parameter is 1 and coupling strength is 2.

1.3 2 analysis code

The network lifetime data is analyzed by the jupyter notebook file "./Model_FailureCouplingNetwork/TimeDataProcess". The scaling relationships and universal scaling function are all analyzed in this notebook. The analyzed result will be saved to the corresponding folder in path "./Model_FailureCouplingNetwork/fig_Maintext/", which is the result shown in section III of our manuscript.. Our results figures are already in the folder ¡°fig_Maintext¡± now for readers to refer to. 








2. Wireless sensor
In the " Case_WirelessSensorNet " folder, we have the code and data for wireless sensor network case in section V. In this folder, we have four subfolder, namely ¡°fig_case¡± , ¡°net_percentile_lifetime¡±, ¡°node_lifetime_log¡± and ¡°structure_WSN¡±, and three Jupyter notebook files, namely " AnalyzeWSNLifetime.ipynb", ¡°GenerateNodeLifeSamples.ipynb¡± and ¡°VisualizationWSNRuning.ipynb¡±



2.1 system setting 

To verify our method in a more realistic scenario, we test our method in a wireless sensor network.

Most setting of our simulation is same to the classical paper[6].
The wireless sensor network compose of numerous sensor nodes and one base station. 
The sensor nodes are deployed in the a rectangular region (-25<=x<=25   and    0<=y<=50.).
The base station is deployed in the origin (x=0, y=0).

Each living sensor node will send 2000bit to nearest cluster-head every day.
The cluster-heads will fuse received message to 2000 bit and send to base station.
The cluster-heads are selected every two days based on LEACH protocol proposed in literature[6].
The energy consumption is calculated based on the First Order Radio model proposed in literature[6]. 


2.2 Failure mechanism of system

In the wilderness, it is challenging to recharge and repair sensor nodes. The failure of WSN comes from the failure of sensor nodes. There are two main failure mechanism incorporated in previous literature. 


a) battery depletion 

In the wilderness, it is challenging to recharge sensor nodes.
The battery of normal sensors will be used for sending messages.
The battery of cluster-heads is used for compressing messages, receiving messages and sending messages.
The energy consumption is calculated based on the First Order Radio model proposed in reference[xx]


b) other accident factors
# The sensors may fail due to other factors, including moisture, corrosion and wild animals.
# These factors are quantified by failure rate 10^(-3) * day^(-1).
# This failure rate is set based on the report[7]. The only difference with work[6] is that we consider the failure rate other than battery depletion.


The process of WSN running is visualized in the jupyter notebook VisualizationWSNRuning.ipynb.

2.3 1 Simulation Code
The simulation code for generating wireless sensor node lifetime in different size of networks is ¡°GenerateNodeLifeSamples.py¡±. Running this code will output the lifetime of each sensor node to the path:
 "./Case_WirelessSensorNet/node_lifetime_log/N=.../", where N is the size of simulated network size.

Considering the time of simulation is long, we have prepared the node lifetime simulation data we used in our case for readers. Readers can directly run the data analysis code to analyze simulation data. Specifically, the node lifetime data are already stored in "./Case_WirelessSensorNet /node_lifetime_log". 
The simulation code is in "./Case_WirelessSensorNet/GenerateNodeLifeSamples.py". 
Running this code will output the lifetime of each sensor nodes to the path "./Case_WirelessSensorNet/node_lifetime_log/N=.../".
The position data of sensor nodes used in our simulation is shown in "./structure_WSN /networkUsedInPaper"


The simulation time of WSN increases at a quadratic rate with the growth of system size.
Because the time of simulation is long, we have prepare the simulation data.
Readers can directly run the data analysis code to analyze simulation data.
The node lifetime data is stored in "./Case_WirelessSensorNet/node_lifetime_log".


2.4 2 Data Analysis Code
The simulation code for analyzing the lifetime data of WSN is ¡°AnalyzeWSNLifetime.ipynbAnalyzeWSNLifetime.py¡±. 
We analyze the lifetime data of WSN in the file "AnalyzeWSNLifetime.ipynb".
In this notebook, the network lifetime is calculated based on the criterion that a network is dead if 80% nodes dead. The network lifetime data will be saved into ¡°./ WirelessSensorNet /net_percentile_lifetime . 

And the scaling law for mean value, standard deviation of lifetime distribution are .
We use lifetime data of small WSN to infer lifetime distribution of large.

This notebook also generate the figures shown in the section V manuscript to the path "./Case_WirelessSensorNet/fig_case/..". Our results figures are already in the folder ¡°fig_case¡± now for readers to refer to.

2.3 net_percentile_lifetime 

2.34. WSN Visualization Code
The code for WSN Visualization as shown in Fig. 10 in the paper is ¡°VisualizationWSNRuning.ipynb¡±. The notebook demonstrate the process of WSN aging.Reference:

