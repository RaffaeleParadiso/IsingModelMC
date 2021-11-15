import matplotlib.pyplot as plt
import numpy as np

beta_start=0.34
beta_stop=0.48

path='results_analysis'
beta=np.loadtxt(f'{path}/beta/beta_lattice_dim_10.txt')
print(len(beta))
elem=['beta', 'beta_riscalato', 'binder', 'calore_specifico', 'magnetizzazione_media', 'magnetizzazione_riscalata','suscettività', 'suscettività_riscalata']
plt.figure()

for ii in np.arange(10, 60, 10):
    susc_resc=np.loadtxt(f'{path}/{elem[7]}/{elem[7]}_lattice_dim_{ii}.txt')
    err_susc=np.loadtxt(f'{path}/{elem[6]}/sigma_susceptibility_lattice_dim_{ii}.txt')
    beta_resc=np.loadtxt(f'{path}/{elem[1]}/{elem[1]}_lattice_dim_{ii}.txt')
    plt.errorbar(beta_resc, susc_resc, yerr=err_susc*2*(1/ii**(7/4)), label=f'$\chi$ riscalata latt {ii}', fmt='.', mfc='red',
                  mec='green', ms=0.4, mew=2, capsize=2)  
plt.title(f'Suscettività riscalata', fontsize=18)
plt.xlabel(r'($\beta$)L', fontsize=14)
plt.ylabel(r'$\chi / L^{7/4}$ ', fontsize=14)
plt.legend()
plt.show()

for ii in np.arange(10,60,10):
    susc=np.loadtxt(f'{path}/{elem[6]}/{elem[6]}_lattice_dim_{ii}.txt')
    err_susc=np.loadtxt(f'{path}/{elem[6]}/sigma_susceptibility_lattice_dim_{ii}.txt')
    plt.errorbar(beta, susc, yerr=err_susc*2, label=f'Lattice: {ii}', fmt='.', mfc='red',
                  mec='green', ms=0.4, mew=2, capsize=2)
plt.title(f'Suscettività', fontsize=18)
plt.xlabel(r'$\beta$', fontsize=14)
plt.ylabel(r'$\chi$', fontsize=14)
plt.legend()
plt.show()

for ii in np.arange(10,60,10):
    sh=np.loadtxt(f'{path}/{elem[3]}/{elem[3]}_lattice_dim_{ii}.txt')
    err_sh=np.loadtxt(f'{path}/{elem[3]}/sigma_specific_heat_lattice_dim_{ii}.txt')
    beta_resc=np.loadtxt(f'{path}/{elem[1]}/{elem[1]}_lattice_dim_{ii}.txt')
    plt.errorbar(beta_resc, sh, yerr=err_sh*2, label=f'Lattice: {ii}', fmt='.', mfc='red',
                  mec='green', ms=0.4, mew=2, capsize=2)
plt.title(f'Calore specifico', fontsize=18)
plt.xlabel(r'($\beta$-$\beta_c$)L', fontsize=14)
plt.ylabel(r'C', fontsize=14)
plt.legend()
plt.show()

for ii in np.arange(10, 60,10):
    magn_resc=np.loadtxt(f'{path}/{elem[5]}/{elem[5]}_lattice_dim_{ii}.txt')
    err_magn=np.loadtxt(f'{path}/{elem[4]}/sigma_mean_magn_lattice_dim_{ii}.txt')
    beta_resc=np.loadtxt(f'{path}/{elem[1]}/{elem[1]}_lattice_dim_{ii}.txt')
    plt.errorbar(beta_resc, magn_resc, yerr=err_magn*2*ii**(1/8), label=f'Lattice: {ii}', fmt='.', mfc='red',
                  mec='green', ms=0.4, mew=2, capsize=2)
plt.title('Magnetizzazione media riscalata',fontsize=18)
plt.xlabel(r'($\beta$-$\beta_c$)L', fontsize=14)
plt.ylabel(r'$\langle$ |M| $\rangle$ $L^{1/8}$', fontsize=14)
plt.legend()
plt.show()

for ii in np.arange(10,60,10):
    magn=np.loadtxt(f'{path}/{elem[4]}/{elem[4]}_lattice_dim_{ii}.txt')
    err_magn=np.loadtxt(f'{path}/{elem[4]}/sigma_mean_magn_lattice_dim_{ii}.txt')
    plt.errorbar(beta, magn, yerr=err_magn*2, label=f'Lattice: {ii}',fmt='.', mfc='red',
                  mec='green', ms=0.4, mew=2, capsize=2) 
plt.title('Magnetizzazione media', fontsize=18)
plt.xlabel(r'$\beta$', fontsize=14)
plt.ylabel(r'$\langle$ |M| $\rangle$', fontsize=14)
plt.legend()
plt.show()

beta_range=np.loadtxt(f'{path}/{elem[2]}/beta_range_0.34_0.48.txt')
for ii in np.arange(10,60,10):
    binder=np.loadtxt(f'{path}/{elem[2]}/{elem[2]}_lattice_dim_{ii}.txt')
    err_bind=np.loadtxt(f'{path}/{elem[2]}/binder_sigma_lattice_dim_{ii}.txt')
    plt.errorbar(beta_range, binder, yerr=err_bind*2, fmt='.', mfc='red',
                  mec='green', ms=0.4, mew=2, capsize=2) 
plt.title('Cumulante di Binder', fontsize=18)
plt.xlabel(r'$\beta$', fontsize= 14)
plt.ylabel(r'B=$\langle$ $M^4$ $\rangle$ / $(\langle M^2 \rangle)^2$ ', fontsize=14)
plt.legend()
plt.show()

