from brian2 import *
from matplotlib.pyplot import *
from numpy import *
start_scope()

N = 1000
tau = 10*ms
vr = -70*mV
vt0 = -50*mV
delta_vt0 = 5*mV
tau_t = 100*ms
sigma = 0.5*(vt0-vr)
v_drive = 2*(vt0-vr)
duration = 100*ms

eqs = '''
dv/dt = (v_drive+vr-v)/tau + sigma*xi*tau**-0.5 : volt
dvt/dt = (vt0-vt)/tau_t : volt
'''

reset = '''
v = vr
vt += delta_vt0
'''

G = NeuronGroup(N, eqs, threshold='v>vt', reset=reset, refractory=5*ms)
spikemon = SpikeMonitor(G)
statemon = StateMonitor(G, 'v', record=1)

G.v = 'rand()*(vt0-vr)+vr'
G.vt = vt0

run(duration)


#_ = hist(spikemon.t/ms, 100, histtype='stepfilled', facecolor='k', weights=ones(len(spikemon))/(N*defaultclock.dt))
#xlabel('Time (ms)')
#ylabel('Instantaneous firing rate (sp/s)')

plot(statemon.t/ms, statemon.v[1])
xlabel('Time (ms)')
ylabel('Instantaneous firing rate (sp/s)')
show()