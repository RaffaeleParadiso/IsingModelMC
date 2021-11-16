import matplotlib.pyplot as plt
import numpy as np
import model.costants as c

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

monte_history_m = True # grafico passo montecarlo per la magnetizzazione a fissati beta
monte_history_e = True # grafico passo montecarlo per l'energia a fissati beta
mean = True            # grafico magnetizzazione media al variare di beta e L
chi = True             # grafico suscettività al variare di beta ed L
heat = True            # grafico calore specifico al variare di beta ed L
binder = True          # grafico cumulante di Binder
mean_r = True          # grafico magnetizzazione riscalata al variare di beta e L
susc_r = True          # grafico suscettività riscalata

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
if mean == True:
    plt.figure()
    for i in range(latt_dim_start, latt_dim_stop, passo_latt_dim):
        bet = np.loadtxt(f"results_analysis/beta/beta_lattice_dim_{i}.txt")
        mean = np.loadtxt(f"results_analysis/magnetizzazione_media/magnetizzazione_media_lattice_dim_{i}.txt")
        error = np.loadtxt(f"results_analysis/magnetizzazione_media/sigma_mean_magn_lattice_dim_{i}.txt")
        plt.errorbar(bet, mean, yerr=error*2, label=f'Lattice: {i}',fmt='.', mfc='red', mec='green', ms=0.4, mew=2, capsize=2) 
    plt.title('Magnetizzazione media', fontsize=18)
    plt.xlabel(r'$\beta$', fontsize=14)
    plt.ylabel(r'$\langle$ |M| $\rangle$', fontsize=14)
    plt.legend()
    plt.show()

# grafico suscettività al variare di beta ed L
if chi == True:
    plt.figure()
    for i in range(latt_dim_start, latt_dim_stop, passo_latt_dim):
        bet = np.loadtxt(f"results_analysis/beta/beta_lattice_dim_{i}.txt")
        susc=np.loadtxt(f'results_analysis/suscettività/suscettività_lattice_dim_{i}.txt')
        err_susc=np.loadtxt(f'results_analysis/suscettività/sigma_susceptibility_lattice_dim_{i}.txt')
        plt.errorbar(bet, susc, yerr=err_susc*2, label=f'Lattice: {i}', fmt='.', mfc='red', mec='green', ms=0.4, mew=2, capsize=2)
    plt.title(f'Suscettività', fontsize=18)
    plt.xlabel(r'$\beta$', fontsize=14)
    plt.ylabel(r'$\chi$', fontsize=14)
    plt.legend()
    plt.show()

# grafico calore specifico al variare di beta ed L
if heat == True:
    plt.figure()
    for i in range(latt_dim_start, latt_dim_stop, passo_latt_dim):
        sh=np.loadtxt(f'results_analysis/calore_specifico/calore_specifico_lattice_dim_{i}.txt')
        err_sh=np.loadtxt(f'results_analysis/calore_specifico/sigma_specific_heat_lattice_dim_{i}.txt')
        beta_resc=np.loadtxt(f'results_analysis/beta_riscalato/beta_riscalato_lattice_dim_{i}.txt')
        plt.errorbar(beta_resc, sh, yerr=err_sh*2, label=f'Lattice: {i}', fmt='.', mfc='red',
                  mec='green', ms=0.4, mew=2, capsize=2)
    plt.title(f'Calore specifico', fontsize=18)
    plt.xlabel(r'($\beta$-$\beta_c$)L', fontsize=14)
    plt.ylabel(r'C', fontsize=14)
    plt.legend()
    plt.show()

# grafico magnetizzazione riscalata al variare di beta e L
if mean_r == True:
    plt.figure()
    for i in range(latt_dim_start, latt_dim_stop, passo_latt_dim):
        magn_resc=np.loadtxt(f'results_analysis/magnetizzazione_riscalata/magnetizzazione_riscalata_lattice_dim_{i}.txt')
        err_magn=np.loadtxt(f'results_analysis/magnetizzazione_media/sigma_mean_magn_lattice_dim_{i}.txt')
        beta_resc=np.loadtxt(f'results_analysis/beta_riscalato/beta_riscalato_lattice_dim_{i}.txt')
        plt.errorbar(beta_resc, magn_resc, yerr=err_magn*2*i**(1/8), label=f'Lattice: {i}', fmt='.', mfc='red',
                  mec='green', ms=0.4, mew=2, capsize=2)
    plt.title('Magnetizzazione media riscalata',fontsize=18)
    plt.xlabel(r'($\beta$-$\beta_c$)L', fontsize=14)
    plt.ylabel(r'$\langle$ |M| $\rangle$ $L^{1/8}$', fontsize=14)
    plt.legend()
    plt.show()

# grafico cumulante di Binder
if binder == True:
    for i in range(latt_dim_start, latt_dim_stop, passo_latt_dim):
        beta_range=np.loadtxt(f'results_analysis/binder/beta_range_0.34_0.48.txt')
        binder=np.loadtxt(f'results_analysis/binder/binder_lattice_dim_{i}.txt')
        err_bind=np.loadtxt(f'results_analysis/binder/binder_sigma_lattice_dim_{i}.txt')
        plt.errorbar(beta_range, binder, yerr=err_bind*2, label=f'Lattice: {i}',fmt='.', mfc='red',
                    mec='green', ms=0.4, mew=2, capsize=2) 
    plt.title('Cumulante di Binder', fontsize=18)
    plt.xlabel(r'$\beta$', fontsize= 14)
    plt.ylabel(r'B=$\langle$ $M^4$ $\rangle$ / $(\langle M^2 \rangle)^2$ ', fontsize=14)
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
    plt.xlabel(r'($\beta$)L', fontsize=14)
    plt.ylabel(r'$\chi / L^{7/4}$ ', fontsize=14)
    plt.legend()
    plt.show()
