import os
import glob
import shutil
import MDAnalysis as mda
from MDAnalysis.analysis import align


new_list = ['fold_a276s', 'fold_e285a']
for i in new_list:
    
    name = i.split('.')[0]
    print(name)
    os.system(f'gmx rms -f {name}/{name}_final2.xtc -s {name}/em.tpr -o {name}/{name}_rms.xvg < answer_rms.txt')
    os.system(f'gmx hbond -f {name}/{name}_final2.xtc -s {name}/{name}_final2.tpr -num {name}/{name}_hbond.xvg < answer_hbond.txt')

