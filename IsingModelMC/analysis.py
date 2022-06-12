import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
import model.costants as c
import random


flag = c.FLAG
latt_dim_start = c.LATT_DIM_START
latt_dim_stop = c.LATT_DIM_STOP
passo_latt_dim = c.PASSO_LATT_DIM
i_decorrel = c.IDECORREL
measures = c.MEASURES
extfield = c.EXTFIELD
beta_start = c.BETA_START
beta_stop = c.BETA_STOP
passo_beta = c.PASSO_BETA

monte_history_m = False   # grafico passo montecarlo per la magnetizzazione a fissati beta
monte_history_e = False   # grafico passo montecarlo per l'energia a fissati beta
mean            = False   # grafico magnetizzazione media al variare di beta e L
chi             = False   # grafico suscettività al variare di beta ed L
heat            = False   # grafico calore specifico al variare di beta ed L
binder          = False   # grafico cumulante di Binder
mean_r          = False   # grafico magnetizzazione riscalata al variare di beta e L
susc_r          = False   # grafico suscettività riscalata
heat_r          = False   # grafico calore specifico riscalato
histogram       = False
hsters          = True


color_palette=['deepskyblue','blue', 'yellow', 'lime', 'red']

beta=np.loadtxt('results_analysis/beta/beta_lattice_dim_10.txt')

# passo montecarlo per la magnetizzazione a fissati beta
if monte_history_m == True:
    beta_num = 0.450
    plt.figure()
    for i in range(latt_dim_start, latt_dim_stop, passo_latt_dim):
        magnetization = np.loadtxt(f"results/lattice_dim_{i}/magnetization/magnetization_beta_{beta_num:.3f}.txt")
        plt.plot(np.arange(0,len(magnetization)), magnetization)
    plt.show()

# passo montecarlo per l'energia a fissati beta
if monte_history_e == True:
    beta_num = 0.450
    plt.figure()
    for i in range(latt_dim_start, latt_dim_stop, passo_latt_dim):
        energy = np.loadtxt(f"results/lattice_dim_{i}/energies/energies_beta_{beta_num:.3f}.txt")
        plt.plot(np.arange(0,len(energy)), energy)
    plt.show()

# grafico magnetizzazione media al variare di beta e L
random.shuffle(color_palette)
if mean == True:
    plt.figure()
    for i in range(latt_dim_start, latt_dim_stop, passo_latt_dim):
        bet = np.loadtxt(f"results_analysis/beta/beta_lattice_dim_{i}.txt")
        mean = np.loadtxt(f"results_analysis/magnetizzazione_media/magnetizzazione_media_lattice_dim_{i}.txt")
        error = np.loadtxt(f"results_analysis/magnetizzazione_media/sigma_mean_magn_lattice_dim_{i}.txt")
        plt.errorbar(bet, mean, yerr=error*2, color=color_palette[round(i/10)-1], label=f'Lattice: {i}',fmt='.', mfc='red', mec='green', ms=0.4, mew=2, capsize=2) 
    plt.title('Magnetizzazione media', fontsize=18)
    plt.xlabel(r'$\beta$', fontsize=14)
    plt.ylabel(r'$\langle$ |M| $\rangle$', fontsize=14)
    plt.legend()
    plt.show()

# grafico suscettività al variare di beta ed L
random.shuffle(color_palette)
if chi == True:
    plt.figure()
    for i in range(latt_dim_start, latt_dim_stop, passo_latt_dim):
        bet = np.loadtxt(f"results_analysis/beta/beta_lattice_dim_{i}.txt")
        susc=np.loadtxt(f'results_analysis/suscettività/suscettività_lattice_dim_{i}.txt')
        err_susc=np.loadtxt(f'results_analysis/suscettività/sigma_susceptibility_lattice_dim_{i}.txt')
        plt.errorbar(bet, susc, yerr=err_susc*2, label=f'Lattice: {i}', fmt='.', mfc='red', color=color_palette[round(i/10)-1], mec='green', ms=0.4, mew=2, capsize=2)
    plt.title(f'Suscettività', fontsize=18)
    plt.xlabel(r'$\beta$', fontsize=14)
    plt.ylabel(r'$\chi$', fontsize=14)
    plt.legend()
    plt.show()

# grafico calore specifico al variare di beta ed L
random.shuffle(color_palette)
if heat == True:
    plt.figure()
    for i in range(latt_dim_start, latt_dim_stop, passo_latt_dim):
        sh=np.loadtxt(f'results_analysis/calore_specifico/calore_specifico_lattice_dim_{i}.txt')
        err_sh=np.loadtxt(f'results_analysis/calore_specifico/sigma_specific_heat_lattice_dim_{i}.txt')
        beta_resc=np.loadtxt(f'results_analysis/beta_riscalato/beta_riscalato_lattice_dim_{i}.txt')
        plt.errorbar(beta, sh, yerr=err_sh*2, label=f'Lattice: {i}', fmt='.', mfc='red',
                  mec='green', color=color_palette[round(i/10)-1], ms=0.4, mew=2, capsize=2)
    plt.title(f'Calore specifico', fontsize=18)
    plt.xlabel(r'($\beta$-$\beta_c$)L', fontsize=14)
    plt.ylabel(r'C', fontsize=14)
    plt.legend()
    plt.show()

# grafico cumulante di Binder
if binder == True:
    for i in range(latt_dim_start, latt_dim_stop, passo_latt_dim):
        beta_range=np.loadtxt(f'results_analysis/binder/beta_range_0.34_0.48.txt')
        binder=np.loadtxt(f'results_analysis/binder/binder_lattice_dim_{i}.txt')
        err_bind=np.loadtxt(f'results_analysis/binder/binder_sigma_lattice_dim_{i}.txt')
        plt.errorbar(beta_range, binder, yerr=err_bind*2, label=f'Lattice: {i}',fmt='.', mfc='red',
                    mec='green', color=color_palette[round(i/10-1)], ms=0.4, mew=2, capsize=2) 
    plt.title('Cumulante di Binder', fontsize=18)
    plt.xlabel(r'$\beta$', fontsize= 14)
    plt.ylabel(r'B=$\langle$ $M^4$ $\rangle$ / $(\langle M^2 \rangle)^2$ ', fontsize=14)
    plt.legend()
    plt.show()

# grafico magnetizzazione riscalata al variare di beta e L
random.shuffle(color_palette)
if mean_r == True:
    plt.figure()
    for i in range(latt_dim_start, latt_dim_stop, passo_latt_dim):
        magn_resc=np.loadtxt(f'results_analysis/magnetizzazione_riscalata/magnetizzazione_riscalata_lattice_dim_{i}.txt')
        err_magn=np.loadtxt(f'results_analysis/magnetizzazione_media/sigma_mean_magn_lattice_dim_{i}.txt')
        beta_resc=np.loadtxt(f'results_analysis/beta_riscalato/beta_riscalato_lattice_dim_{i}.txt')
        plt.errorbar(beta_resc, magn_resc, yerr=err_magn*2*i**(1/8), label=f'Lattice: {i}', fmt='.', mfc='red',
                  mec='green',color=color_palette[round(i/10)-1], ms=0.4, mew=2, capsize=2)
    plt.title('Magnetizzazione media riscalata',fontsize=18)
    plt.xlabel(r'($\beta$-$\beta_c$)L$^{1/\nu}$', fontsize=14)
    plt.ylabel(r'$\langle$ |M| $\rangle$ $L^{\beta/\nu}$', fontsize=14)
    plt.legend()
    plt.show()

#grafico suscettività riscalata
if susc_r == True:
    for i in range(latt_dim_start, latt_dim_stop, passo_latt_dim):
        susc_resc=np.loadtxt(f'results_analysis/suscettività_riscalata/suscettività_riscalata_lattice_dim_{i}.txt')
        err_susc=np.loadtxt(f'results_analysis/suscettività/sigma_susceptibility_lattice_dim_{i}.txt')
        beta_resc=np.loadtxt(f'results_analysis/beta_riscalato/beta_riscalato_lattice_dim_{i}.txt')
        plt.errorbar(beta_resc, susc_resc, yerr=err_susc*2*(1/i**(7/4)), label=f'Lattice: {i}', fmt='.', mfc='red',
                    mec='green', ms=0.4, mew=2, capsize=2)
    plt.title(f'Suscettività riscalata', fontsize=18)
    plt.xlabel(r'($\beta$-$\beta_c$)L$^{1/\nu}$', fontsize=14)
    plt.ylabel(r'$\chi / L^{7/4}$ ', fontsize=14)
    plt.legend()
    plt.show()

if heat_r == True:
    for i in range(latt_dim_start, latt_dim_stop, passo_latt_dim):
        heat=np.loadtxt(f'results_analysis/calore_specifico/calore_specifico_lattice_dim_{i}.txt')
        err_heat=np.loadtxt(f'results_analysis/calore_specifico/sigma_specific_heat_lattice_dim_{i}.txt')
        beta_resc=np.loadtxt(f'results_analysis/beta_riscalato/beta_riscalato_lattice_dim_{i}.txt')
        plt.errorbar(beta_resc, heat, yerr=err_heat*2, label=f'Lattice: {i}', fmt='.', mfc='red',
                    mec='green', ms=0.4, mew=2, capsize=2)
    plt.title(f'Calore specifico riscalato', fontsize=18)
    plt.xlabel(r'($\beta$-$\beta_c$)$L^{1/\nu}$', fontsize=14)
    plt.ylabel(r'$\chi / L^{\gamma/\nu}$ ', fontsize=14)
    plt.legend()
    plt.show()

if histogram == True:
    magn_0_35=np.loadtxt('results/lattice_dim_50/magnetization/magnetization_beta_0.350.txt')
    magn_0_45=np.loadtxt('results/lattice_dim_50/magnetization/magnetization_beta_0.450.txt')
    plt.figure()
    plt.hist(magn_0_45, bins=300, color='darkblue', label='beta 0.45')
    plt.hist(magn_0_35, bins=300, color='lime', label='beta 0.35')
    plt.legend()
    plt.title('Istogramma di M', fontsize=18)
    plt.xlabel('M', fontsize=14)
    plt.ylabel('Densità campionaria di M', fontsize=14)
    plt.show()

# plot della magnetizzazione e dell'energia in funzione del campo magnetico esterno applicato 
# e al variare della temperatura attraverso il parametro \beta
if hsters == True:
    hvsm = False
    hvse = True
    cmap = colors.ListedColormap(['magenta','blue','orange','green','red','lime'])
    beta = c.BETA_FIELD
    extfieldHL = c.EXTFIELDHL
    extfieldLH = c.EXTFIELDLH
    plt.figure()
    for index, i in enumerate(beta):
        mm = np.loadtxt(f"results/loop_hys/{i}/mean_magn.txt")
        mm_inv = np.loadtxt(f"results/loop_hys_rev/{i}/mean_magn.txt") 
        me = np.loadtxt(f"results/loop_hys/{i}/mean_en.txt")
        me_inv = np.loadtxt(f"results/loop_hys_rev/{i}/mean_en.txt")
        if hvsm:
        #plot magnetizzazione vs H
            plt.plot(extfieldLH, mm, marker="o", c=cmap(index), ls="-",markersize=4, label= f"$beta = {i}$")
            plt.plot(extfieldHL, mm_inv, marker="o", c=cmap(index), ls="-",markersize=4)
        if hvse:
        # plot energia vs H
            plt.plot(extfieldLH, me, marker="o", c=cmap(index), ls="-",label= f"$beta = {i}$")
            plt.plot(extfieldHL, me_inv, marker="o", c=cmap(index), ls="-")
    plt.xlabel('B = External field', fontsize=14)
    plt.ylabel('Magnetizzazione M', fontsize=14)
    plt.legend()
    plt.show()
