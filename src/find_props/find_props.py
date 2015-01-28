# File to calculate properties for a molecule and add these properties back to the molecules
# property to be calculate will be put in using a request.header string
from java import lang
lang.System.loadLibrary('GraphMolWrap')
from org.RDKit import *
from threading import Thread
import os

def num_hba(mol, ret_val=False):
#     print "Calculating number of H-bond acceptors"
     val = RDKFuncs.calcNumHBA(mol)
     if ret_val:
         return val
     return mol

def num_hbd(mol, ret_val=False):
#     print "Calculating number of H-bond donors"
     val = RDKFuncs.calcNumHBD(mol)
     if ret_val:
         return val
     return mol



def num_rings(mol, ret_val=False):
 #    print "Calculating number of rings"
     val = RDKFuncs.calcNumRings(mol)
     if ret_val:
         return val
     return mol


def mol_logp(mol, ret_val=False):
 #    print "Calculating mol log p"
     val = RDKFuncs.calcMolLogP(mol)
     if ret_val:
         return val
     return mol


# A dictionary to relate functioons t ostrings
funct_dict = {"num_hba": num_hba,
"num_hbd": num_hbd,
"num_rings": num_rings,
"mol_logp": mol_logp}


def calc_props(request):
    for mol in request.out_ans:
        funct_dict[request.headers](mol)

# Request will comprise two parts
## 1) Stream of molecuels
## 2) String relating to property

if __name__ == "__main__":
    print "calculating properties"
    calc_props(request)
