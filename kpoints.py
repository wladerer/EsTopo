import pyprocar as pr

#use pyprocar to create kpoints file
def makeKpath(poscar_file: str = 'POSCAR', kpath_filename: str = 'KPOINTS'):
    pr.kpath(poscar_file, kpath_filename)
