# Spiking Neural Network Model for XOR
# SNN SETUP :
# 60 input neurons: 30 for input x1, 30 for input x2
# Half of each Input Neuron have Excitatory and rest have Inhibitory STDP
# 60 hidden neurons fully connected with input neurons
# one output neuron


# ENCODING 
# Logical 1 = Poisson Spike Train at 40 Hz
# Logical 0 = No Spike Activity 

# Import required packages
from brian2 import *               # Brian2 Needed. Doesn't work with Brian1
from matplotlib.pyplot import *    # To Plot
from brian2.numpy_ import *        # For array Manipulations
from Visualize import *            # To visualize connections
from random import shuffle

defaultclock.dt = 1*ms
# Leaky Integrate and Fire (LIF) Model Parameters
gamma = 0.1      # Discount Parameter
learningRate = 0.01 # Learning Rate
reward = 0       # Reward Parameter
N = 60           # 
tau    = 10*ms   # Time Constant for Membrane Potential
vt     = -55*mV  # Threshold Voltage
v0     = -70*mV  # Initial Membrane Potential (Nernst), also used for Reset Potential
taupre = taupost = 20*ms # Time Constants for STDP
wmax = 0.005      # Maximum allowable weight of synapse
Apre = 1      # Increment to apre when there is a Pre Synaptic Spike
Apost = -1 # Increment to apost when there is a Post Synaptic Spike

# Simple Leaky Integrate and Fire Neuron Model Equations
eqLIF = '''
dv/dt=(v0-v)/tau : volt
'''
# Define Input Group
InGroup       = PoissonGroup(N, rates=40*Hz)
#a = integer(N/2)
InGroupX1     = InGroup[0:30]   # Input Group for X1
InGroupX2     = InGroup[30:60]  # Input Group for X2
InGroup_Inh   = InGroup[15:45]   # Inhibitory Neurons
InGroup_Exh1  = InGroup[0:15]   # Excitatory In to Hidden 1 
InGroup_Exh2  = InGroup[45:60]  # Excitatory In to Hidden 2
# Define Hidden Group
HidGroup = NeuronGroup(N, eqLIF, threshold='v > vt', refractory=10*ms, reset='v = v0', method='euler') 

# Define Output Group
OutGroup = NeuronGroup(1, eqLIF, threshold='v > vt', refractory=10*ms, reset='v = v0', method='euler')

# Define Synapse between Input Excitatory Group 1 and Hidden Group
InExh1ToHidSyn = Synapses(InGroup_Exh1, HidGroup, 
                          model= '''
                                  w : 1
                                  dapre/dt = -apre/taupre : 1 (clock-driven)
                                  dapost/dt = -apost/taupost : 1 (clock-driven)
                                 ''',
                          on_pre='''
                                  v_post += w*volt
                                  apre += Apre
                                  w = clip(w+gamma*reward*learningRate*apost, 0, wmax)
                                 ''',
                          on_post='''
                                  apost += Apost
                                  w = clip(w+gamma*reward*learningRate*apre, 0, wmax)
                                  ''',
                           method='euler'
                         )

# Define Synapse between Input Excitatory Group 2 and Hidden Group
InExh2ToHidSyn = Synapses(InGroup_Exh2, HidGroup, 
                          model= '''
                                  w : 1
                                  dapre/dt = -apre/taupre : 1 (event-driven)
                                  dapost/dt = -apost/taupost : 1 (event-driven)
                                 ''',
                          on_pre='''
                                  v_post += w*volt
                                  apre += Apre
                                  w = clip(w+gamma*reward*learningRate*apost, 0, wmax)
                                 ''',
                          on_post='''
                                  apost += Apost
                                  w = clip(w+gamma*reward*learningRate*apre, 0, wmax)
                                  '''
                          , method='euler'
                         )
# Define Synapse between Input Inhibitory Group and Hidden Group
InInhToHidSyn = Synapses(InGroup_Inh, HidGroup, 
                          model= '''
                                  w : 1
                                  dapre/dt = -apre/taupre : 1 (event-driven)
                                  dapost/dt = -apost/taupost : 1 (event-driven)
                                 ''',
                          on_pre='''
                                  v_post += w*volt
                                  apre += Apre
                                  apre  = -apre
                                   
                                  w = clip(w+gamma*learningRate*reward*apost, -0.005, 0)
                                 ''',
                          on_post='''
                                  apost += Apost
                                  apost  = -apost
                                  
                                  w = clip(w+gamma*learningRate*reward*apre, -0.005, 0)
                                  '''
                          , method='euler'
                         )

HidToOutSyn  = Synapses(HidGroup, OutGroup, 
                          model= '''
                                  w : 1
                                  dapre/dt = -apre/taupre : 1 (event-driven)
                                  dapost/dt = -apost/taupost : 1 (event-driven)
                                 ''',
                          on_pre='''
                                  v_post += w*volt
                                  apre += Apre
                                  w = clip(w+gamma*reward*learningRate*apost, 0, wmax)
                                 ''',
                          on_post='''
                                  apost += Apost
                                  w = clip(w+gamma*reward*learningRate*apre, 0, wmax)
                                  '''
                           , method='euler'
                         )
# Create the Synapse
InExh1ToHidSyn.connect()
InExh2ToHidSyn.connect()
InInhToHidSyn.connect()
HidToOutSyn.connect()

# Assign random initial weights
InInhToHidSyn.w  =  'clip(rand()*-0.005,-0.005,0)'
InExh1ToHidSyn.w =  'clip(rand()*wmax,0,wmax)'
InExh2ToHidSyn.w =  'clip(rand()*wmax,0,wmax)'
HidToOutSyn.w    =  'clip(rand()*wmax,0,wmax)'

# Define Monitors
#HidStateMon   = StateMonitor(HidGroup, 'v', record=0)  # Continuous monitoring of Hidden Layer
#InSpikeMon    = SpikeMonitor(InGroup)                  # Spike Monitor input Layer
#HidSpikeMon   = SpikeMonitor(HidGroup)                 # Spike Monitor for Hidden Layer


# Continuous monitoring of Synapses between Inhibitory input and Hidden Neurons

#OutGroupMon   = SpikeMonitor(OutGroup,record=False)
# Visual Display of Connectivity
#Visualize().VisualizeConnectivity(InToHidSyn)
# Run the network

##*********************************** TRAINING ***********************************************************##
# list of tests
trainNo = [[1,0],[0,0],[0,1],[1,1]]
for idx in range(300): 
    # shuffle for randomness
    shuffle(trainNo)
    # Train first 
    print("Iteration ",idx, ", Training ",trainNo[0][0]," ",trainNo[0][1])
    InGroupX1.rates = (trainNo[0][0])*Hz
    InGroupX2.rates = (trainNo[0][1])*Hz
    reward = -1   # set reward
    OutGroupMon   = SpikeMonitor(OutGroup,record=False)
    run(500*ms)  
    # Train 1,0
    #print("Iteration ",idx, ", Training 1,0")
    print("Iteration ",idx, ", Training ",trainNo[1][0]," ",trainNo[1][1])
    InGroupX1.rates = (trainNo[1][0])*Hz
    InGroupX2.rates = (trainNo[1][1])*Hz
    reward = 1   # set reward
    run(500*ms)
    # Train 1,0
    print("Iteration ",idx, ", Training ",trainNo[2][0]," ",trainNo[2][1])
    InGroupX1.rates = (trainNo[2][0])*Hz
    InGroupX2.rates = (trainNo[2][1])*Hz
    reward = 1   # set reward
    run(500*ms)
    # Train 1,0
    print("Iteration ",idx, ", Training ",trainNo[3][0]," ",trainNo[3][1])
    InGroupX1.rates = (trainNo[3][0])*Hz
    InGroupX2.rates = (trainNo[3][1])*Hz
    reward = -1   # set reward
    run(500*ms)
    

        

print("Printing Learned Coefficients ..")   
print("Input  to Hidden Inhibitory   = ",InInhToHidSyn.w)
print("Input  to Hidden Excitatory 1 = ",InExh1ToHidSyn.w)
print("Input  to Hidden Excitatory 2 = ",InExh2ToHidSyn.w)
print("Hidden to Output Layer        = ",HidToOutSyn.w)
print ("Output Spike Count =", OutGroupMon.count)

print("************************** TRAINING DONE, NOW TESTING *******************************************************")    
##****************************** TESTING **************************************************************##

learningRate = 0
for idx in range(10):
    OutGroupMon   = SpikeMonitor(OutGroup,record=False)
    # Train 0,0
    print("Iteration ",idx, ", Testing 0,0")
    InGroupX1.rates = 0*Hz
    InGroupX2.rates = 0*Hz
    reward = -1   # set reward
    run(500*ms)    
    # Plot
    print ("Output Spike Count =", OutGroupMon.count)
    # Train 1,0
    print("Iteration ",idx, ", Testing 1,0")
    InGroupX1.rates = 40*Hz
    InGroupX2.rates = 0*Hz
    reward = 1   # set reward
    run(500*ms)
    print ("Output Spike Count =", OutGroupMon.count)
    # Train 1,0
    print("Iteration ",idx, ", Testing 0,1")
    InGroupX1.rates = 0*Hz
    InGroupX2.rates = 40*Hz
    reward = 1   # set reward
    run(500*ms)
    print ("Output Spike Count =", OutGroupMon.count)
    # Train 1,0
    print("Iteration ",idx, ", Testing 1,1")
    InGroupX1.rates = 40*Hz
    InGroupX2.rates = 40*Hz
    reward = -1   # set reward
    run(500*ms)
    print ("Output Spike Count =", OutGroupMon.count)
 
"""
# Plot Desired Variables
figure(1)

# Input Spike Raster
subplot(211)
plot(InSpikeMon.t/ms, InSpikeMon.i, '.k')
title('Input Layer Spike Raster Plot')
xlabel('Time (ms)')
ylabel('Input Layer Neuron Index')
# Hidden Spike Raster
subplot(212)
plot(HidSpikeMon.t/ms, HidSpikeMon.i, '.k')
title('Hidden Layer Spike Raster Plot')
xlabel('Time (ms)')
ylabel('Hidden Layer Neuron Index')
# Hidden State Plot
figure(2)
subplot(311)
plot(HidStateMon.t/ms, HidStateMon.v[0])
title('Hidden Layer Membrane Potential Plot')
xlabel('Time (ms)')
ylabel('Hidden Layer Membrane Potential')
# Synapse Weight Plot
"""
"""
subplot(312)
plot(InInhToHidSynMon.t/ms, InInhToHidSynMon.w[0])
title('Inhibitory Input to Hidden Layer Synaptic Weight Plot')
xlabel('Time (ms)')
ylabel('Hidden Layer Synaptic')
# apre, apost Plot
subplot(313)
plot(InInhToHidSynMon.t/ms, InInhToHidSynMon.apre[0], label='apre')
plot(InInhToHidSynMon.t/ms, InInhToHidSynMon.apost[0], label='apost')
legend(loc='best')
title('Inhibitory apre, apost Synaptic Weight Plot')
xlabel('Time (ms)')
ylabel('Hidden Layer Synaptic')

figure(3)
plot(InExh1ToHidSynMon.t/ms, InExh1ToHidSynMon.apre[0],label='apre exh')
plot(InExh1ToHidSynMon.t/ms, InExh1ToHidSynMon.apost[0],label='apost exh')
legend(loc='best')
"""
show()










        
        
    