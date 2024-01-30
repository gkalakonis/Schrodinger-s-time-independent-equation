import matplotlib.pyplot as plt
import numpy as np
from solve import nm,eV

def plot_qw(result,x,V):
    E=result[0]
    psis=result[1]
    fig=plt.figure()
    plt.plot(x / nm, V / eV, 'k', label='Potential Well')
    plt.grid(True)
    plt.xlabel('x [nm]', fontweight='bold', fontsize=16)
    plt.ylabel('V (eV)', fontweight='bold', fontsize=16)
    plt.xlim([min(x / nm), max(x / nm)])
    plt.ylim([min(V / eV), max(1.1 * V / eV)])

    plot_modes = np.sum((E > V.min()) & (E < V.max()))
    for plot_mode in range(plot_modes):
        rescale = (E[0] - V.min()) / (np.max(psis[:, plot_mode]) - np.min(psis[:, plot_mode]))
        psis_rescaled = psis[:, plot_mode] * rescale + E[plot_mode]
        plt.plot(x / nm, psis_rescaled / eV, 'k--', label=f'Mode {plot_mode + 1}')
        plt.plot(x / nm, np.ones_like(x) * E[plot_mode] / eV, label='_nolegend_')


    plt.title('Schrödinger\'s Equation Solution', fontweight='bold', fontsize=18)
    return  fig

def plot_hp(result, z, V, n):
    E = result[0]
    psis = result[1]
    fig = plt.figure()

    plt.xlabel('x [nm]', fontweight='bold', fontsize=16)
    colormap = plt.cm.viridis

    for plot_mode in range(n):
        color = colormap(plot_mode / n) 
        plt.plot(z / nm, psis[:, plot_mode], linestyle='--', label=f'State {plot_mode + 1}', color=color)

    plt.legend(loc='upper right', fontsize=12)
    plt.title('Schrödinger\'s Equation Solution', fontweight='bold', fontsize=18)

    return fig

def plot_pt(result, z, V,n):
    E = result[0]
    psis = result[1]
    fig = plt.figure()
    plt.xlabel('x [nm]', fontweight='bold', fontsize=16)
    plt.ylabel('V (eV)', fontweight='bold', fontsize=16)
    plot_modes = np.sum((E > V.min()) & (E < V.max()))
    for plot_mode in range(n):
        rescale = (E[0] - V.min()) / (np.max(psis[:, plot_mode]) - np.min(psis[:, plot_mode]))
        psis_rescaled = psis[:, plot_mode] * rescale + E[plot_mode]
        plt.plot(z / nm, psis_rescaled / eV, 'k--', label=f'State {plot_mode + 1}')
        plt.plot(z / nm, np.ones_like(z) * E[plot_mode] / eV, label='_nolegend_')

    plt.title('Schrödinger\'s Equation Solution', fontweight='bold', fontsize=18)

    return fig
