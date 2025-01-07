import os
import glob
import shutil
import MDAnalysis as mda


for i in glob.glob('*.zip'):
    name = i.split('.')[0]

    print(name)
    
    #os.system(f'unzip {i} -d {name}')
    
    pdb_name = glob.glob(f'{name}/*model_0.cif')[0]
    os.system(f"python3 cif2pdb.py {pdb_name} {pdb_name.split('.')[0]+'.pdb'}")
    
    pdb_name = pdb_name.split('.')[0]
    for itp in glob.glob('{name}/*.itp'):
        os.remove(itp)
    for top in glob.glob('{name}/*.top'):
        os.remove(top)
    for top in glob.glob('{name}/*.gro'):
        os.remove(top)
    for file in glob.glob('{name}/#*'):
        os.remove(file)
    
    pdb_file = open(pdb_name+'.pdb', 'r').readlines()
    new_pdb_file = []
    cut_res = [str(x) for x in range(203, 235)]
    for i in pdb_file:
        if 'OP3  DG B   1' in i or 'P    DG B   1' in i or 'OP1  DG B   1' in i or 'OP2  DG B   1' in i:
            continue
        elif 'OP3  DT C   1' in i or 'P    DT C   1' in i or 'OP1  DT C   1' in i or 'OP2  DT C   1' in i:
            continue
        elif i[23:26] in cut_res:
            continue
        else:
            new_pdb_file.append(i)
    new_file = open(pdb_name+'.pdb', 'w')
    for i in new_pdb_file:
        new_file.write(i)
    new_file.close()
    
    
    os.system(f'gmx pdb2gmx -f {pdb_name}.pdb -o {pdb_name}_processed.gro -water tip3p < answer_pdb.txt')
    
    os.system(f'gmx editconf -f {pdb_name}_processed.gro -o {pdb_name}_newbox.gro -c -d 0.15 -bt cubic')
    
    os.system(f'gmx solvate -cp {pdb_name}_newbox.gro -cs spc216.gro -o {pdb_name}_solv.gro -p topol.top')
    
    os.system(f'gmx grompp -f ions.mdp -c {pdb_name}_solv.gro -p topol.top -o {name}/ions.tpr')
    os.system(f'gmx genion -s {name}/ions.tpr -o {pdb_name}_solv_ions.gro -p topol.top -pname NA -nname CL -neutral -conc 0.1 < answer_ions.txt')
    
    os.system(f'gmx grompp -f minim.mdp -c {pdb_name}_solv_ions.gro -p topol.top -o {name}/em.tpr -maxwarn 5')
    os.system(f'gmx mdrun -v -deffnm {name}/em -nt 12 -pin on -pinoffset 0')
    
    os.system(f'gmx grompp -f nvt.mdp -c {name}/em.gro -r {name}/em.gro -p topol.top -o {name}/nvt.tpr')
    os.system(f'gmx mdrun -v -deffnm {name}/nvt -nt 12 -pin on -pinoffset 0')
    
    os.system(f'gmx grompp -f md.mdp -c {name}/nvt.gro -p topol.top -o {name}/{name}_final.tpr -maxwarn 5')
    os.system(f'gmx mdrun -v -deffnm {name}/{name}_final -nt 12 -pin on -pinoffset 0')
    
    os.system(f'gmx grompp -f md.mdp -c {name}/{name}_final.gro -p topol.top -o {name}/{name}_final2.tpr -maxwarn 5')
    os.system(f'gmx mdrun -v -deffnm {name}/{name}_final2 -nt 12 -pin on -pinoffset 0')
    
    for itp in glob.glob('*.itp'):
        shutil.copy(itp, name)
        os.remove(itp)
    for top in glob.glob('*.top'):
        shutil.copy(top, name)
        os.remove(top)
    for file in glob.glob('#*'):
        os.remove(file)

    #print(name)
