# Spiking Neural Network Model for XOR
# SNN SETUP :
# 60 input neurons: 30 for input x1, 30 for input x2
# Half of each Input Neuron have Exhibitory and rest have Inhibitory STDP
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

# Leaky Integrate and Fire (LIF) Model Parameters
gamma = 0.1      # Discount Parameter
reward = 0       # Reward Parameter
N = 60           # 
tau    = 10*ms   # Time Constant for Membrane Potential
vt     = -55*mV  # Threshold Voltage
v0     = -75*mV  # Initial Membrane Potential (Nernst), also used for Reset Potential
taupre = taupost = 20*ms # Time Constants for STDP
wmax = 0.05      # Maximum allowable weight of synapse
Apre = 0.01      # Increment to apre when there is a Pre Synaptic Spike
Apost = -Apre*taupre/taupost*1.05 # Increment to apost when there is a Post Synaptic Spike
# Simple Leaky Integrate and Fire Neuron Model Equations
eqLIF = '''
dv/dt=(v0-v)/tau : volt

'''
# Define Input Group
InGroup       = PoissonGroup(60, rates=40*Hz)
InGroupX1     = InGroup[0:30]   # Input Group for X1
InGroupX2     = InGroup[30:60]  # Input Group for X2
InGroup_Inh   = InGroup[15:45]  # Inhibitory Neurons
InGroup_Exh1  = InGroup[0:15]   # Exhibitory In to Hidden 1 
InGroup_Exh2  = InGroup[45:60]  # Exhibitory In to Hidden 2
# Define Hidden Group
HidGroup = NeuronGroup(1, eqLIF, threshold='v > vt', refractory=10*ms, reset='v = v0') 

# Define Synapse
InToHidSyn = Synapses(InGroup, HidGroup, 
                          model= '''
                                  w : 1
                                  dapre/dt = -apre/taupre : 1 (clock-driven)
                                  dapost/dt = -apost/taupost : 1 (clock-driven)
                                 ''',
                          on_pre='''
                                  v_post += w*volt
                                  apre += Apre
                                  w = clip(w+gamma*reward*apost, 0, wmax)
                                 ''',
                          on_post='''
                                  apost += Apost
                                  w = clip(w+gamma*reward*apre, 0, wmax)
                                  '''
                         )



# Create the Synapse
InToHidSyn.connect()
# Assign random initial weights
InToHidSyn.w =  'clip(rand()*wmax,0,wmax)'




# Define Monitors
HidStateMon   = StateMonitor(HidGroup, 'v', record=0)  # Continuous monitoring of Hidden Layer
InSpikeMon    = SpikeMonitor(InGroup)                  # Spike Monitor input Layer
HidSpikeMon   = SpikeMonitor(HidGroup)                 # Spike Monitor for Hidden Layer
# Continuous monitoring of Synapses
InToHidSynMon = StateMonitor(InToHidSyn, ['w', 'apre', 'apost'], record=0)

# Visual Display of Connectivity
#Visualize().VisualizeConnectivity(InToHidSyn)
# Run the network
run(100*ms)    
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
subplot(312)
plot(InToHidSynMon.t/ms, InToHidSynMon.w[0])
title('Input to Hidden Layer Synaptic Weight Plot')
xlabel('Time (ms)')
ylabel('Hidden Layer Synaptic')
# apre, apost Plot
subplot(313)
plot(InToHidSynMon.t/ms, InToHidSynMon.apre[0], label='apre[0]')
plot(InToHidSynMon.t/ms, InToHidSynMon.apost[0], label='apost[0]' )
title('apre, apost Synaptic Weight Plot')
xlabel('Time (ms)')
ylabel('Hidden Layer Synaptic')
show()









        
        
    