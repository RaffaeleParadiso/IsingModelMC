''' Programma per la simulazione del modello di ising bidimensionale
con possibilita` di inserire un campo magnetico esterno
'''
import argparse
import logging
import numpy as np
import makedir as mk

iflag = 1           # partenza caldo(1)/freddo(0)/precedente(altro)
measures = 5000     # numero di misure
i_decorrel = 1      # updating fra una misura e l'altra
extfield = 0        # valore del campo esterno
beta = 0.3          # valore di 1/(kT) = beta

def initialize_lattice(iflag, nlatt):
    '''
    '''
    lattice_n = np.zeros((nlatt, nlatt))
    if iflag == 0:
        lattice_n = np.ones((nlatt, nlatt))
    if iflag == 1:
        init_matrix_random = np.random.random((nlatt, nlatt))
        lattice_n[init_matrix_random>=0.5]=1
        lattice_n[init_matrix_random<0.5]=-1

    print(lattice_n)

def geometry(nlatt):
    npp = [i+1 for i in range(1,nlatt+1)]
    nmm = [i-1 for i in range(1,nlatt+1)]
    npp[nlatt-1]=1
    nmm[0]=nlatt
    print(npp, nmm)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ising Model')
    requiredNamed = parser.add_argument_group('Required named arguments')
    requiredNamed.add_argument('-l', '--lattice', type=int, default=10, help='Lattice Dimensions')
    requiredNamed.add_argument('-f', '--flag', type=int, default=1,
                                help='Flag (Partenza a freddo [s=1]=0, partenza a caldo[s=random]=1)')
    # requiredNamed.add_argument('--path', '-p', type=str, help='Path first folder')
    parser.add_argument("-log", "--log", default="info",
                        help=("Provide logging level. Example --log debug', default='info"))

    args = parser.parse_args()

    levels = {'critical': logging.CRITICAL,
              'error': logging.ERROR,
              'warning': logging.WARNING,
              'info': logging.INFO,
              'debug': logging.DEBUG}
    logging.basicConfig(level=levels[args.log])

    # path = args.path
    lattice = args.lattice
    flag = args.flag
    # mk.smart_makedir(path)

    initialize_lattice(flag, lattice)
    geometry(lattice)
