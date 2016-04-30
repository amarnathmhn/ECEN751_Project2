from brian2 import *
import matplotlib.pyplot as plt

start_scope()

N=100
tau = 10*ms
v0_max = 3.
duration = 1000*ms
eqs = '''
   dv/dt = ( v0-v )/tau : 1
   v0 : 1
'''

G = NeuronGroup(N, eqs, threshold='v>1', reset='v=0')
G.v0 = 'i*v0_max/(N-1)'

M = SpikeMonitor(G)
run(duration)

plt.figure(figsize=(12,4))
plt.subplot(121)
plt.plot(M.t/ms, M.i, '.k')
plt.xlabel('Time (ms)')
plt.ylabel('Neuron index')
plt.subplot(122)
plt.plot(G.v0, M.count/duration)
plt.xlabel('v0')
plt.ylabel('Firing rate (sp/s)')
plt.show()