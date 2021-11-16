'''Finite size scaling in multiprocessing'''
import multiprocessing
import numpy as np

import model.costants as c
import module.func as func
import module.makedir as mk

latt_dim_start=c.LATT_DIM_START
latt_dim_stop=c.LATT_DIM_STOP
latt_dim_passo=c.PASSO_LATT_DIM
latt_dim_list = c.LATT_DIM_L
gamma=c.GAMMA_TEORICO
nu=c.NU_TEORICO
beta_c=c.BETA_CRITICO

def mean_m_r(lattice_dim):
    mean_magn, beta_list=func.mean_magnetization(lattice_dim)
    beta_list = np.array(beta_list)
    mean_magn_rescaled=np.array(mean_magn)*lattice_dim**(1/8)
    beta_rescaled=np.array((np.array(beta_list)-beta_c)*lattice_dim**(1/nu))
    return (mean_magn_rescaled, beta_list, beta_rescaled)

def susc_r(lattice_dim):
    susceptibility, beta_list=func.susceptivity(lattice_dim)
    suscept_rescaled=np.array(np.array(susceptibility)*1/(lattice_dim)**(gamma/nu))
    return suscept_rescaled

def spec_heat(lattice_dim):
      specific_heat, beta_list=func.specific_heat(lattice_dim)
      return specific_heat

if __name__=='__main__':
    path='results_analysis'
    mk.smart_makedir(f'{path}/magnetizzazione_riscalata')
    mk.smart_makedir(f'{path}/beta')
    mk.smart_makedir(f'{path}/beta_riscalato')
    with multiprocessing.Pool(processes=None) as pool:
        results = pool.map(mean_m_r, latt_dim_list)
        j = latt_dim_passo
        for i in range(len(results)):
            mean_m_rescaled, beta_l, beta_r = results[i]
            np.savetxt(f'{path}/magnetizzazione_riscalata/magnetizzazione_riscalata_lattice_dim_{j}.txt', mean_m_rescaled)
            np.savetxt(f'{path}/beta/beta_lattice_dim_{j}.txt', beta_l, fmt="%.3f")
            np.savetxt(f'{path}/beta_riscalato/beta_riscalato_lattice_dim_{j}.txt', beta_r, fmt="%.3f")
            j += latt_dim_passo

    mk.smart_makedir(f'{path}/suscettività_riscalata') 
    with multiprocessing.Pool(processes=None) as pool:
        results = np.array(pool.map(susc_r, latt_dim_list))
        j = latt_dim_passo
        for i in range(len(results)):
            susc_riscaled = results[i]
            np.savetxt(f"{path}/suscettività_riscalata/suscettività_riscalata_lattice_dim_{j}.txt", susc_riscaled)
            j += latt_dim_passo

    mk.smart_makedir(f'{path}/calore_specifico')
    with multiprocessing.Pool(processes=None) as pool:
        results = np.array(pool.map(spec_heat, latt_dim_list))
        j = latt_dim_passo
        for i in range(len(results)):
            specific_h = results[i]
            np.savetxt(f"{path}/calore_specifico/calore_specifico_lattice_dim_{j}.txt", specific_h)
            j += latt_dim_passo
