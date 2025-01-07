import os
import glob
import shutil
import MDAnalysis as mda
from MDAnalysis.analysis import align

file_results = open('results_pull1.csv', 'w')
file_results.write('name,pull_max,\n')

for i in glob.glob('*.zip'):
    name = i.split('.')[0]
    if len(glob.glob(f'{name}/*pullf.xvg'))>=1:
        continue
    print(name)
    print(name)
    os.system(f'gmx editconf -f {name}/{name}_final_us.gro -o {name}/{name}_us_newbox.gro -center 4 4 3.5 -box 8 8 26')
    
    file_topol = open(f'{name}/topol.top', 'r').readlines()
    file_out = open(f'{name}/system.top', 'w')
    for i in file_topol:
        if 'SOL' in i:
            continue
        if 'NA ' in i or 'CL ' in i:
            continue
        file_out.write(i)
    file_out.close()
    
    os.system(f'gmx solvate -cp {name}/{name}_us_newbox.gro -cs spc216.gro -o {name}/{name}_final_us_solv.gro -p {name}/system.top')
    
    os.system(f'gmx grompp -f ions.mdp -c {name}/{name}_final_us_solv.gro -p {name}/system.top -o {name}/{name}_final_us_ions.tpr')
    os.system(f'gmx genion -s {name}/{name}_final_us_ions.tpr -o {name}/{name}_final_us_ions.gro -p {name}/system.top -pname NA -nname CL -neutral -conc 0.1 < answer_ions.txt')
    
    os.system(f'gmx grompp -f minim.mdp -c {name}/{name}_final_us_ions.gro -p {name}/system.top -o {name}/us_em.tpr -maxwarn 5')
    os.system(f'gmx mdrun -v -deffnm {name}/us_em -nt 12 -pin on -pinoffset 0')

    os.system(f'gmx grompp -f npt.mdp -c {name}/us_em.gro -p {name}/system.top -r {name}/us_em.gro -o {name}/us_npt.tpr -maxwarn 5')
    os.system(f'gmx mdrun -deffnm {name}/us_npt -v -nt 12 -pin on -pinoffset 0')
    
    os.system(f'gmx make_ndx -f {name}/us_npt.gro -o {name}/new.ndx < answers_ndx.txt')
    os.system(f'gmx grompp -f md_pull.mdp -c {name}/us_npt.gro -p {name}/system.top -r {name}/us_npt.gro -n {name}/new.ndx -t {name}/us_npt.cpt -o {name}/us_pull.tpr -maxwarn 5')
    os.system(f'gmx mdrun -deffnm {name}/us_pull -pf {name}/pullf.xvg -px {name}/pullx.xvg -v -nt 12 -pin on -pinoffset 0')
    
    
    file_force = open(f'{name}/pullf.xvg', 'r').readlines()[17:]
    file_force = [float(x.split('\t')[-1].split('\n')[0]) for x in file_force]
    file_results.write(f'{name},{max(file_force)},\n')

file_results.close()
