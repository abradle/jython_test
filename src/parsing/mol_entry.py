from java import lang
lang.System.loadLibrary('GraphMolWrap')
from org.RDKit import *
from threading import Thread
import os, pickle


class Request():
   """Class to hold requests to dummy the input behaviour"""
   def __init__(self):
       print "Initialsing request"


def make_request(n_stream=None):
    """Function to build a request object-for testing"""
    print "Making request"
    my_req = Request()
    if n_stream:
        my_req.in_stream = n_stream
    else:
        my_req.in_stream = "/jython_test/src/test_data/test.smi"
    return my_req


def check_stream_type(in_stream):
    """Function to check what the input is"""
    # File types, SMILES, SD, MOL, INCHI
    print "Checking stream"
    # First check - is this a file, or a stream
    if os.path.isfile(in_stream):
        in_stream = open(in_stream).read()
        print "OPENED FILE INPUT STREAM"
    else:
        print in_stream
        print "READING FROM INPUT STREAM"
    # If it is a file, then we want to convert to stream, everrything should be stream
    print "Checking type"
    # Now check what file format we havea
    my_mols = in_stream.split("$$$$")
    if len(my_mols) > 1:
        rdmol = RWMol.MolFromMolBlock(my_mols[0])
        # If this is none - this may not be a MOL file so we need to test the others
        if rdmol is None:
            print "MAY NOT BE SDF FILE"
        else:
            file_flag = "sdf"
            delim = "$$$$"
            return file_flag, delim, 0, None

    my_mols = in_stream.split("\n")
    if len(my_mols) == 1:
        test_line = my_mols[0]
    else:
        test_line = my_mols[1]
    header = my_mols[0]
    # Check for a comma seperatin
    if len(header.split("\t")) > 1:
        delim = "\t"
    elif len(header.split(",")) > 1:
        delim = ","
    elif len(header.split(" ")) > 1:
        delim = " "
    else:
        print "Assuming only one column"
        delim = " "
    # Check for whitespace delimerter
    rdmol = None
    rdmol = [i for i in range(len(test_line.split(delim))) if None != RWMol.MolFromSmiles(test_line.split(delim)[i])]
    if rdmol:
         file_flag = "smiles"
         if RWMol.MolFromSmiles(header.split(delim)[rdmol[0]]):
             return file_flag, delim, rdmol[0], True
         else:
             return file_flag, delim, rdmol[0], False
    elif rdmol is None:
        pass
    # Needed to get the InChI reading correctly
    my_vals = ExtraInchiReturnValues()
    rdmol = [i for i in range(len(test_line.split(delim))) if RDKFuncs.InchiToMol(test_line.split(delim)[i], my_vals) != None ]
    if rdmol:
        file_flag = "inchi"
        if RDKFuncs.InchiToMol(header.split(delim)[rdmol[0]], my_vals):
            return file_flag, delim, rdmol[0], True
        else:
            return file_flag, delim, rdmol[0], False
    elif rdmol is None:
        pass
    print "UNKNOWN FILE TYPE"
    return None, None, None, None


def read_mols(file_flag, delim, col_ind, header, in_stream):
    """Function to actually read the mols"""
    if file_flag == "sdf":
        suppl = SDMolSupplier(in_stream)
        out_l = []
        while not suppl.atEnd():
            mol = suppl.next()
            if mol is None:
                continue
            out_l.append(mol)
        return out_l
    elif file_flag == "smiles":
        me=  """Need to add header identifier etc"""
        suppl = SmilesMolSupplier(in_stream)
        out_l = []
        while not suppl.atEnd():
            mol = suppl.next()
            if mol is None:
                continue
            out_l.append(mol)
        return out_l
    elif file_flag == "inchi":
        my_vals = ExtraInchiReturnValues()
        out_mols = []
        in_mols = open(in_stream).read().split("\n")
        if header:
            out_vals = [x for x in in_mols[0].split(delim)]
            for mol in in_mols:
                o_mol = RDKFuncs.InchiToMol(mol.split(delim)[col_ind], my_vals)
                if o_mol:
                    out_mols.append(RDKFuncs.InchiToMol(mol.split(delim)[col_ind], my_vals))
            return out_mols
        else:
            return [RDKFuncs.InchiToMol(mol.split(delim)[col_ind], my_vals) for mol in in_mols if RDKFuncs.InchiToMol(mol.split(delim)[col_ind], my_vals)]        


def do_test():
    for item in ["/jython_test/src/test_data/test.smi","/jython_test/src/test_data/test.inchi","/jython_test/src/test_data/test.sdf"]:
        parse_mols(item)
    

def parse_mols(item):# Make the request
    request = make_request(item)
    # Check the type
    file_flag, delim, col_ind, header = check_stream_type(request.in_stream)
    print "FILE TYPE: ",file_flag
    print "DELIMITER: ",delim
    print "COLUMN IND: ",col_ind
    print "COLUMN HEADER: ",header
    # Now read the files and pass out as a stream of molecule
    request.out_ans = read_mols(file_flag, delim, col_ind, header, request.in_stream)
    return request.out_ans

if __name__ == "__main__":
# Just replace this with parse_mols and pss in the request and we've got it
    do_test()
