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

# Set the default clock to 1*ms
defaultclock.dt = 1*ms
# Leaky Integrate and Fire (LIF) Model Parameters
gamma = 0.1      # Discount Parameter
learningRate = 0.01 # Learning Rate
reward = 0       # Reward Parameter
N = 60           # 
tau    = 10*ms   # Time Constant for Membrane Potential
vt     = -55*mV  # Threshold Voltage
v0     = -70*mV  # Initial Membrane Potential (Nernst), also used for Reset Potential
tauplus = tauminus = 20*ms # Time Constants for STDP
wmax = 0.005      # Maximum allowable weight of synapse
Aplus   = 1      # Increment to apre when there is a Pre Synaptic Spike
Apminus = -1 # Increment to apost when there is a Post Synaptic Spike

# Simple Leaky Integrate and Fire Neuron Model Equations
eqLIF = '''
dv/dt=(v0-v)/tau : volt
'''

# Define Input group
InGroup = SpikeGeneratorGroup()

# Define Hidden Group
HidGroup = NeuronGroup(1, )
