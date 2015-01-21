from java import lang
lang.System.loadLibrary('GraphMolWrap')
from org.RDKit import *


def make_request():
    """Function to build a request object-for testing"""
    print "Making request"


def check_stream_type(in_stream):
    """Function to check what the input is"""
    # File types, SMILES, SD, MOL, INCHI
    print "Checking stream"
    # First check - is this a file, or a stream
    # If it is a file, then we want to convert to stream, everrything should be stream
    print "Checking type"
    # Now check what file format we have
 

class ReadStream():
     """Class to read stream given an input field"""
#We're having to dummy this here - as the request object is passed in by the calling function
request = make_request()

# Now lets test what kind of functon is required
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
