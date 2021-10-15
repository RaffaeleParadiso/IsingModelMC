''' Programma per la simulazione del modello di ising bidimensionale
    con possibilita` di inserire un campo magnetico esterno
'''
import argparse
import time
import numpy as np
import module.func as fnc
import module.makedir as mk
import model.costants as c

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='2D Ising Model')
    args = parser.parse_args()

    flag = c.FLAG
    # lattice_dim = c.LATT_DIM
    i_decorrel = c.IDECORREL
    measures = c.MEASURES
    extfield = c.EXTFIELD
    # beta = c.BETA
    beta_start = c.BETA_START
    beta_stop = c.BETA_STOP
    passo_beta = c.PASSO_BETA
    start = time.time()
    for lattice_dim in range(10,100,10):
        mk.smart_makedir(f"results/lattice_dim_{lattice_dim}")
        ret_ = fnc.initialize_lattice(flag,lattice_dim)    
        for beta in np.arange(beta_start,beta_stop,passo_beta):
            mag, en = fnc.run_metropolis(flag, lattice_dim, ret_, i_decorrel, measures, extfield, beta)
            print(f"time elapsed: {time.time() - start}")
            fnc.info_save(flag, lattice_dim, beta, mag, "magnetization")
            fnc.info_save(flag, lattice_dim, beta, en, "energies")