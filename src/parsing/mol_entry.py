from java import lang
lang.System.loadLibrary('GraphMolWrap')
from org.RDKit import *
from threading import Thread
import os, pickle


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
        # Read the first mol
        rdmol = RWMol.MolFromMolBlock(my_mols[0])
        # If this is none - this may not be a MOL file so we need to test the others
        if rdmol is None:
            # Check if it can read any of the others
            if len([x for x in in my_mols if RWMol.MolFromMolBlock(x)]) == 0:
                return None, None, None, None
            else:
                # IF it reads as an - set the flags accordingly
                file_flag = "sdf"
                delim = "$$$$"
                return file_flag, delim, 0, None
        else:
            # IF it reads as an - set the flags accordingly
            file_flag = "sdf"
            delim = "$$$$"
            return file_flag, delim, 0, None
    # Now split the file on lines
    my_mols = in_stream.split("\n")
    # IF there's only one line assume there isn't a header
    if len(my_mols) == 1:
        test_line = my_mols[0]
    # Otherwise assume the first line MIGHT be a header
    else:
        test_line = my_mols[1]
    header = my_mols[0]
    # Check for tab,  comma and space seperatin
    if len(header.split("\t")) > 1:
        delim = "\t"
    elif len(header.split(",")) > 1:
        delim = ","
    elif len(header.split(" ")) > 1:
        delim = " "
    else:
        print "Assuming only one column"
        delim = " "
    # Check for whitespace delimeter
    rdmol = None
    rdmol = [i for i in range(len(test_line.split(delim))) if None != RWMol.MolFromSmiles(test_line.split(delim)[i])]
    # If we get any ols - this is a smiles file
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
    # Check if there are Inchis
    rdmol = [i for i in range(len(test_line.split(delim))) if RDKFuncs.InchiToMol(test_line.split(delim)[i], my_vals) != None ]
    # If there are Inchis - assign that as the flag
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
    """Function to actually read the mols
    Takes in a file_flag - indicating the type of file
    delim - string indicating what the delimiter is
    col_ind - an int indicating the column
    header - a bool indicating if there is a header
    in_stream - the file path to read
    Returns - a Pythonlist of RDKit molecules"""
    if file_flag == "sdf":
        # Read the SD file
        suppl = SDMolSupplier(in_stream)
        out_l = []
        # Loop through the mols 
        while not suppl.atEnd():
            mol = suppl.next()
            if mol is None:
                continue
            # Append to the list
            out_l.append(mol)
        # Return the list
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

def parse_mols(request):# Make the request
    # Check the type
    print request
    file_flag, delim, col_ind, header = check_stream_type(request.body)
    print "FILE TYPE: ",file_flag
    print "DELIMITER: ",delim
    print "COLUMN IND: ",col_ind
    print "COLUMN HEADER: ",header
    # Now read the files and pass out as a stream of molecule
    request.body = read_mols(file_flag, delim, col_ind, header, request.body)
    return request

if __name__ == "__main__":
# Just replace this with parse_mols and pss in the request and we've got it
   parse_mols(request)
