import os
import glob
import shutil
import MDAnalysis as mda
from MDAnalysis.analysis import align


ref = mda.Universe('fold_wt.gro')

for i in glob.glob('*.zip'):
    name = i.split('.')[0]
    
    if len(glob.glob(f'{name}/*_us.gro'))>=1:
        continue
    print(name)

    os.system(f'gmx trjconv -f {name}/{name}_final2.xtc -s {name}/{name}_final2.gro -o {name}/{name}_final2.trr < answers_trjconv1.txt')
    os.system(f'gmx trjconv -f {name}/{name}_final2.trr -s {name}/{name}_final2.tpr -o {name}/{name}_final2.xtc -center -pbc mol < answers_trjconv2.txt')
    os.system(f'gmx make_ndx -f {name}/{name}_final2.gro -o {name}/new.ndx < answers_ndx.txt')
    os.system(f'gmx trjconv -f {name}/{name}_final2.trr -s {name}/{name}_final2.tpr -o {name}/{name}_final_frame.gro -center -pbc mol -b 49999 -e 50000 -n {name}/new.ndx < answers_trjconv3.txt')
    pdb_file = mda.Universe(f'{name}/{name}_final_frame.gro')
    align.alignto(pdb_file, ref, tol_mass=1000)
    pdb_file.atoms.write(f'{name}/{name}_final_us.gro')
