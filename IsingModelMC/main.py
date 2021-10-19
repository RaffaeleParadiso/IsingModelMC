''' Programma per la simulazione del modello di ising bidimensionale
    con possibilita` di inserire un campo magnetico esterno
'''
import argparse
import statistics
import time
import numpy as np
import module.utils as fnc
import module.makedir as mk
import model.costants as c

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='2D Ising Model')
    parser.add_argument('-n','--lattice', action='store_true', help='replace everything in the corrisponding folder')
    args = parser.parse_args()
    new_lattice = args.lattice

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

    start = time.time()
    for lattice_dim in range(latt_dim_start,latt_dim_stop,passo_latt_dim):
        if new_lattice == True:
            mk.smart_makedir(f"results/lattice_dim_{lattice_dim}/magnetization")
            mk.smart_makedir(f"results/lattice_dim_{lattice_dim}/energies")
        ret_ = fnc.initialize_lattice(flag,lattice_dim)    
        for beta in np.arange(beta_start,beta_stop,passo_beta):
            mag, en = fnc.run_metropolis(flag, lattice_dim, ret_, i_decorrel, measures, extfield, beta)
            print(f"time elapsed: {time.time() - start}")
            np.savetxt(f"results/lattice_dim_{lattice_dim}/magnetization/magnetization_beta_{beta:.2f}.txt", mag)
            np.savetxt(f"results/lattice_dim_{lattice_dim}/energies/energies_beta_{beta:.2f}.txt", en)
            mean_magn = statistics.mean(mag)
            mean_ener = statistics.mean(en)
            print(f"mean_magn: {mean_magn}")
            print(f"mean_ener: {mean_ener}")