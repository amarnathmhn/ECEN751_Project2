# Class to visualize SNN connectivity
from brian2 import *
from brian2.numpy_ import *
from matplotlib.pyplot import *

class Visualize:
    def VisualizeConnectivity(self, S):
        Ns = len(S.source)
        Nt = len(S.target)
        figure(figsize=(10, 4))
        subplot(111)
        plot(zeros(Ns), arange(Ns), 'ok', ms=10)
        plot(ones(Nt), arange(Nt), 'ok', ms=10)
        for i, j in zip(S.i, S.j):
            plot([0, 1], [i, j], '-k')
        xticks([0, 1], ['Source', 'Target'])
        ylabel('Neuron index')
        xlim(-0.1, 1.1)
        ylim(-1, max(Ns, Nt))
        show()
        
        
    