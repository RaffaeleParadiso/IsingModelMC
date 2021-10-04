from setuptools import setup, find_packages

setup(
    name='IsingModelMC',
    version='0.0.1',
    description='Compute the MonteCarlo algorithm for the Ising model',
    url='https://github.com/RaffaeleParadiso/Ising',
    author='Paradiso Raffaele, Gennaro Calandriello',
    author_email='raffaele05@gmail.com',
    license='gnu general public license',
    packages = find_packages(),
    install_requires=['numpy', 'pandas', 'matplotlib'],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.8',
    ],
)

