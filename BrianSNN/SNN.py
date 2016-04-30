from brian2 import *
import matplotlib.pyplot as plt
from matplotlib.pyplot import axvline

start_scope()

tau = 5*ms
eqs = '''
dv/dt = (1-v)/tau : 1
'''

G = NeuronGroup(1, eqs, threshold='v>0.8', reset='v = 0', refractory=15*ms)

statemon = StateMonitor(G, 'v', record=0)
spikemon = SpikeMonitor(G)

run(50*ms)

plt.plot(statemon.t/ms, statemon.v[0])
for t in spikemon.t:
    plt.axvline(t/ms, ls='--', c='r', lw=3)
plt.axhline(0.8, ls=':', c='g', lw=3)
plt.xlabel('Time (ms)')
plt.ylabel('v')
print ("Spike times:", spikemon.t[:])
    

plt.xlabel('Time (ms)')
plt.ylabel('v')
plt.show()
