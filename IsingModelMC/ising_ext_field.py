import argparse
import logging
import statistics
import numpy as np
import model.costants as c
import module.makedir as mk
import module.utils as ut

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='2D Ising Model with an External field with variable intensity')
    parser.add_argument("-l", "--log", default="info", help=("Provide logging level. Example --log debug', default='info"))
    parser.add_argument('-n','--new', action='store_true', help='Replace everything in the corrisponding folder')
    args = parser.parse_args()

    levels = {'critical': logging.CRITICAL,
              'error': logging.ERROR,
              'warning': logging.WARNING,
              'info': logging.INFO,
              'debug': logging.DEBUG}

    logging.basicConfig(level=levels[args.log])
    new_from_scrath = args.new

    flag = c.FLAG
    i_decorrel = c.IDECORREL
    measures = c.MEASURES
    extfieldHL = c.EXTFIELDHL
    extfieldLH = c.EXTFIELDLH
    beta = c.BETA_FIELD
    lattice_dimension = c.LATTICE_EXT
    # for the creation of the loop the variable extfield need to go from negative (-) 5 (or other value of course) to positive (+) 5
    if new_from_scrath:
        mk.smart_makedir("results/loop_hys_rev")
        mk.smart_makedir("results/loop_hys")
    ret_ = ut.initialize_lattice(flag, lattice_dimension)

    for i in beta:
        print(f'======= Beta : {i:.2f} =======')
        mk.smart_makedir(f"results/loop_hys_rev/{i}")
        mk.smart_makedir(f"results/loop_hys/{i}")
        mean_magn_rev = []
        mean_en_rev = []
        mean_magn = []
        mean_en = []
        for ext in extfieldLH:
            print(f'======= Extfield : {ext:.2f} =======')
            mag, en = ut.run_metropolis(flag, lattice_dimension, ret_, i_decorrel, measures, ext, i)
            mean_en.append(statistics.mean(en))
            mean_magn.append(statistics.mean(mag))
        np.savetxt(f"results/loop_hys/{i}/mean_magn.txt", mean_magn)
        np.savetxt(f"results/loop_hys/{i}/mean_en.txt", mean_en)

        for ext in extfieldHL:
            print(f'======= Extfield : {ext:.2f} =======')
            mag, en = ut.run_metropolis(flag, lattice_dimension, ret_, i_decorrel, measures, ext, i)
            mean_en_rev.append(statistics.mean(en))
            mean_magn_rev.append(statistics.mean(mag))
        np.savetxt(f"results/loop_hys_rev/{i}/mean_magn.txt", mean_magn_rev)
        np.savetxt(f"results/loop_hys_rev/{i}/mean_en.txt", mean_en_rev)
