import argparse
import logging
import os.path
import statistics
import time
import numpy as np
import model.costants as c
import module.func as fnc
import module.makedir as mk
import module.utils as ut

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='2D Ising Model')
    parser.add_argument("-l", "--log", default="info", help=("Provide logging level. Example --log debug', default='info"))
    parser.add_argument('-nl','--lattice', action='store_true', help='Replace everything in the corrisponding folder')
    args = parser.parse_args()

    levels = {'critical': logging.CRITICAL,
              'error': logging.ERROR,
              'warning': logging.WARNING,
              'info': logging.INFO,
              'debug': logging.DEBUG}

    logging.basicConfig(level=levels[args.log])

    new_lattice = args.lattice

    flag = c.FLAG
    latt_dim_start = c.LATT_DIM_START
    latt_dim_stop = c.LATT_DIM_STOP
    passo_latt_dim = c.PASSO_LATT_DIM
    list_l_dim = c.LATT_DIM_L
    i_decorrel = c.IDECORREL
    measures = c.MEASURES
    extfield = c.EXTFIELD
    beta_start = c.BETA_START
    beta_stop = c.BETA_STOP
    passo_beta = c.PASSO_BETA

    start = time.time()
    for lattice_dim in range(latt_dim_start,latt_dim_stop,passo_latt_dim):
        logging.info(f'======= Lattice_dimension: {lattice_dim} =======')
        if new_lattice == True:
            mk.smart_makedir(f"results/lattice_dim_{lattice_dim}/magnetization")
            mk.smart_makedir(f"results/lattice_dim_{lattice_dim}/energies")
        ret_ = ut.initialize_lattice(flag,lattice_dim)    
        for beta in np.arange(beta_start,beta_stop,passo_beta):
            if os.path.exists(f'results/lattice_dim_{lattice_dim}/magnetization/magnetization_beta_{beta:.3f}.txt') == True:
                if os.path.exists(f'results/lattice_dim_{lattice_dim}/energies/energies_beta_{beta:.3f}.txt') == True:
                    continue
            logging.info(f'============ Beta: {beta:.3f} ============')
            mag, en = ut.run_metropolis(flag, lattice_dim, ret_, i_decorrel, measures, extfield, beta)
            print(f"time elapsed: {time.time() - start}")
            np.savetxt(f"results/lattice_dim_{lattice_dim}/magnetization/magnetization_beta_{beta:.3f}.txt", mag)
            np.savetxt(f"results/lattice_dim_{lattice_dim}/energies/energies_beta_{beta:.3f}.txt", en)
            mean_magn = statistics.mean(mag)
            mean_ener = statistics.mean(en)
            print(f"mean_magn: {mean_magn}")
            print(f"mean_ener: {mean_ener}")

    for i in range(latt_dim_start,latt_dim_stop,passo_latt_dim):
        mean_m, beta_list = fnc.mean_magnetization(i)
        mk.smart_makedir("results_analysis/magnetizzazione_media")
        np.savetxt(f"results_analysis/magnetizzazione_media/magnetizzazione_media_lattice_dim_{i}.txt", mean_m)
        chi, beta_list = fnc.susceptivity(i)
        mk.smart_makedir("results_analysis/suscettività")
        np.savetxt(f"results_analysis/suscettività/suscettività_lattice_dim_{i}.txt", chi)
