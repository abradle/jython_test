from java import lang
lang.System.loadLibrary('GraphMolWrap')
from org.RDKit import *
from threading import Thread
import os


class Request():
   """Class to hold requests to dummy the input behaviour"""
   def __init__(self):
       print "Initialsing request"


def make_request():
    """Function to build a request object-for testing"""
    print "Making request"
    my_req = Request()
    my_req.in_stream = "/jython_test/src/test_data/test.inchi"
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
            return file_flag, delim

    my_mols = in_stream.split("\n")
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
#    rdmol = RWMol.MolFromSmiles(test_line.split(delim)[0])
    rdmol = None
    if rdmol:
        file_flag = "smiles"
        return file_flag, delim
    elif rdmol is None:
        pass
    # Needed to get the InChI reading correctly
    my_vals = ExtraInchiReturnValues()
    rdmol = RDKFuncs.InchiToMol(test_line.split(delim)[0], my_vals)
    if rdmol:
        file_flag = "inchi"
        return file_flag, delim
    elif rdmol is None:
        pass
    print "UNKNOWN FILE TYPE"
    return None, None

# Make the request
request = make_request()
# Check the type
file_flag, delim = check_stream_type(request.in_stream)
print "FILE TYPE: ",file_flag
print "DELIMITER: ",delim
# Now read the files and pass out as a stream of molecule


