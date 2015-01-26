# File to calculate properties for a molecule and add these properties back to the molecules
# property to be calculate will be put in using a request.header string
from java import lang
lang.System.loadLibrary('GraphMolWrap')
from org.RDKit import *
from threading import Thread
import os


class Request():
   """Class to hold requests to dummy the input behaviour"""
   def __init__(self):
       print "Initialsing request"


def make_request(n_stream=None, header="num_hba"):
    """Function to build a request object-for testing"""
    print "Making request"
    my_req = Request()
    my_req.in_stream = n_stream
    my_req.header = header
    return my_req

def num_hba(mol):
     print "Calculating number of H-bond acceptors"


def num_hbd(mol):
     print "Calculating number of H-bond donors"


def num_rings(mol):
     print "Calculating number of rings"


def mol_logp(mol):
     print "Calculating mol log p"

# A dictionary to relate functioons t ostrings
funct_dict = {"num_hba": num_hba,
"num_hbd": num_hbd,
"num_rings": num_rings,
"mol_logp": mol_logp}


def make_props_from_list(in_stream, header):
    request = make_request(in_stream, header)
    calc_props(request)

def calc_props(request):
    for mol in request.in_stream:
        funct_dict[request.header](mol)

# Request will comprise two parts
## 1) Stream of molecuels
## 2) String relating to property


if __name__ is "__main__":
    calc_props(request)
#    request = make_request(item, "num_hba")
    # Check the type
#    calc_props(request)




