from java import lang
lang.System.loadLibrary('GraphMolWrap')
from org.RDKit import *

m = RWMol.MolFromSmiles('c1ccccc1')

my_mols = SmilesMolSupplier('test.smi')

out_mols = SDWriter("out_sd.sdf")

while my_mols.atEnd() != True:
    mol = my_mols.next()
    num_HBA = RDKFuncs.calcNumHBA(mol)
    logp = RDKFuncs.calcMolLogP(mol)
    rmm = RDKFuncs.calcMolMR(mol)
    num_HA =  mol.getNumHeavyAtoms()
    num_HBD =  RDKFuncs.calcNumHBD(mol)
    out_mols.write(mol)
