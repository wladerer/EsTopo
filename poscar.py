import AutoVASP as av
from kpoints import makeKpath

def makeInputFiles(mp_code: str, miller_index: list[int], api_key: str, directory: str = './', min_slab_size: float = 15, min_vacuum_size: float = 15, use_in_unit_planes: bool = False, ensure_symmetric_slabs: bool = True, min_z: int = 5):
    '''
    Makes input files for VASP calculations
    '''

    structure = av.primitive_from_mpicode(mp_code, api_key)
    slabs = av.primtive_slabs_from_structure(structure, miller_index)
    slab_jobs = [av.vaspInput(slab, av.job_types['slab_relaxation_med_prec']) for slab in slabs]
    for slab_job in slab_jobs:
        slab_job.write_input_files(directory)

    #make kpath file 
    makeKpath(f'{directory}/POSCAR', f'{directory}/KPATH')

    return None


def localMakeInputFiles(structure: str, miller_index: list[int], api_key: str, directory: str = './', min_slab_size: float = 15, min_vacuum_size: float = 15, use_in_unit_planes: bool = False, ensure_symmetric_slabs: bool = True, min_z: int = 5):
    '''
    Makes input files for VASP calculations
    '''

    slabs = av.primtive_slabs_from_structure(structure, miller_index)
    slab_jobs = [av.vaspInput(slab, av.job_types['slab_relaxation_med_prec']) for slab in slabs]
    for slab_job in slab_jobs:
        slab_job.write_input_files(directory)

    #make kpath file 
    makeKpath(f'{directory}/POSCAR', f'{directory}/KPATH')

    return None

#makeInputFiles('mp-541837', [1, 1, 1], directory='./test', api_key='UKRQAw2HZOkwJBpGh96V8zKFXGYLSIVH')

codes = ['mp-11328', 'mp-11329', 'mp-22693', 'mp-541837', 'mp-34202']
ending = '.poscar'
titles = ['wp2_cmc2', 'wp2_c2m' , 'wte2', 'bi2se3', 'bi2te3']
filenames = [f'{title}{ending}' for title in titles]
structures = [av.primitive_from_mpicode(code, 'UKRQAw2HZOkwJBpGh96V8zKFXGYLSIVH') for code in codes]

#write structures to files
for structure, filename in zip(structures, filenames):
    #save to poscar
    structure.to(filename)

