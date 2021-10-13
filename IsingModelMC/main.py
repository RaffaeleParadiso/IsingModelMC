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

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='2D Ising Model')
    parser.add_argument('-n', '--new', default=False, action='store_true', help='Create new folder')
    parser.add_argument('-p', '--path', help='Path folder')

    args = parser.parse_args()
    new_folder = args.new
    path_folder = args.path

    parameters = [x.split(',')[0] for x in open("input.txt", "r").readlines()]

    flag = int(parameters[0])
    lattice_dim = int(parameters[1])
    i_decorrel = int(parameters[2])
    measures = int(parameters[3])
    extfield = float(parameters[4])
    beta = float(parameters[5])

    if new_folder == True:
        mk.smart_makedir(path_folder)
    if new_folder == False:
        pass

    start = time.time()

    ret_ = fnc.initialize_lattice(flag,lattice_dim)
    for i in np.arange(0.35,0.55,0.01):
        magnet = []
        energies = []
        for val in range(0, measures):
            for iter in range(0, i_decorrel):
                metr = fnc.metropolis(flag, lattice_dim, ret_, i, extfield)
            mag = fnc.magnetization(lattice_dim, metr)
            magnet.append(mag)
            ener = fnc.energy(lattice_dim, metr, extfield)
            energies.append(ener)

        np.savetxt(f"results/magnetization_{flag}_{lattice_dim}_{i:.2f}.txt", magnet)
        np.savetxt(f"results/energy{flag}_{lattice_dim}_{i:.2f}.txt", energies)

        mean_magnetization = statistics.mean(magnet)
        mean_energy = statistics.mean(energies)
        print(f"mean_magnetization: {mean_magnetization}")
        print(f"mean_energy: {mean_energy}")
        print(f"time elapsed: {time.time() - start}")
