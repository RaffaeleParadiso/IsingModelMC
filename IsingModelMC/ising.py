''' Programma per la simulazione del modello di ising bidimensionale
    con possibilita` di inserire un campo magnetico esterno
'''
import argparse
import statistics
import time
import numpy as np
import matplotlib.pyplot as plt
import module.func as fnc
import module.makedir as mk

measures = 100000   # numero di misure
i_decorrel = 100    # numero di volte che runno il metropolis prima di effettuare la misura
extfield = 0        # valore del campo esterno
beta = 0.3          # valore di 1/(kT) = beta

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ising Model')
    requiredNamed = parser.add_argument_group('Required named arguments')
    requiredNamed.add_argument('-l', '--lattice', type=int, default=10, help='Lattice Dimensions')
    requiredNamed.add_argument('-f', '--start', type=int, default=1,
                                help='Flag (Cold start [spin tutti 1]=0, Hot start [spin random]=1)')
    requiredNamed.add_argument("-p", "--path", type=str, help='File folder')
    args = parser.parse_args()
    path = args.path
    dim_latti = args.lattice
    starts = args.start

    start = time.time()

    ret_ = fnc.initialize_lattice(starts,dim_latti)

    magnet = []
    energies = []
    for val in range(0, measures):
        for iter in range(0, i_decorrel):
            metr = fnc.metropolis(starts, dim_latti, ret_, beta, extfield)
        mag = fnc.magnetization(dim_latti, metr)
        magnet.append(mag)
        ener = fnc.energy(dim_latti, metr, extfield)
        energies.append(ener)
        

    mk.smart_makedir("results")
    np.savetxt("results/magnetization.txt", magnet)
    np.savetxt("results/energy.txt", energies)

    mean_magnetization = statistics.mean(magnet)
    mean_energy = statistics.mean(energies)
    print(mean_magnetization)
    print(mean_energy)

    plt.figure()
    plt.scatter(range(0,measures), magnet, s=0.5)
    plt.show()

    print(time.time() - start)
