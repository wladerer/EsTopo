from poscar import makeInputFiles
from AutoVASP import *
from pymatgen.core import Structure
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
from pymatgen.io.vasp import Poscar, Potcar, Kpoints
import pandas as pd



class Slab:

    def __init__(self, structure: Structure, plane: list[int] , min_slab_size: int = 10):
        self.bulk_structure = structure
        self.min_slab_size = min_slab_size
        self.plane = plane
        self.plane_str = f'{plane[0]}{plane[1]}{plane[2]}'
        self.is_symmetric = None
        self.slab_structures = self.get_slabs()
        self.poscars, self.potcars, self.kpaths = self.get_input_files()
        self.symmetry = SpacegroupAnalyzer(self.bulk_structure).get_space_group_symbol()
        self.basename = f'{self.bulk_structure.composition.reduced_formula}_{self.plane_str}'

    def get_slabs(self):

        try:
            slabs = primtive_slabs_from_structure(self.bulk_structure, self.plane, min_slab_size=self.min_slab_size, ensure_symmetric_slabs=True)
            self.is_symmetric = True 
        except:
            slabs = primtive_slabs_from_structure(self.bulk_structure, self.plane, min_slab_size=self.min_slab_size, ensure_symmetric_slabs=False)
            self.is_symmetric = False
        return slabs
    
    def get_input_files(self):

        poscars = [ make_poscar(slab) for slab in self.slab_structures]
        potcars = [ make_potcar(slab) for slab in self.slab_structures]
        kpaths = [ make_kpath(slab) for slab in self.slab_structures]
        
        return poscars, potcars, kpaths

    @classmethod
    def from_mpicode(cls, mpi_code: str, plane: list[str], min_slab_size: int = 10):
        bulk_structure = primitive_from_mpicode(mpi_code)
        return cls(bulk_structure, plane, min_slab_size)
    
    def to_dataframe(self):
        
        # Composition | Thickness | Number of Atoms | Plane | Symmetric | Symmetry Group | 

        df = pd.DataFrame(columns=['Composition', 'Thickness', 'Vacuum', 'Number of Atoms', 'Plane', 'Symmetric', 'Symmetry Group'])
        
        for i,poscar in enumerate(self.poscars):

            composition = poscar.structure.composition.reduced_formula

            num_atoms = len(poscar.structure)
            plane = self.plane_str
            is_symmetric = self.is_symmetric
            symmetry_group = self.symmetry

            #get position of top atom
            top_atom = poscar.structure.sites[0]
            top_atom_pos = top_atom.coords[2]
            #get position of bottom atom
            bottom_atom = poscar.structure.sites[-1]
            bottom_atom_pos = bottom_atom.coords[2]
            #get thickness
            thickness = top_atom_pos - bottom_atom_pos
            vacuum = poscar.structure.lattice.abc[2] - top_atom_pos
            df.loc[i] = [composition, thickness, vacuum, num_atoms, plane, is_symmetric, symmetry_group]

        return df
    
structure = primitive_from_mpicode('mp-11328', api_key='UKRQAw2HZOkwJBpGh96V8zKFXGYLSIVH')
import numpy as np

#array starts at 5, ends at 30, and increments by 5

sizes = np.arange(5, 30, 5)
slabs = [ Slab(structure, [1,1,1], size) for size in sizes]
more_slabs = [ Slab(structure, [0,0,1], size) for size in sizes]

df = pd.concat([slab.to_dataframe() for slab in slabs])

df = pd.concat([slab.to_dataframe() for slab in more_slabs])

#write the 5th slabs poscar to a file
slabs[4].poscars[0].write_file('POSCAR')
print(df)

