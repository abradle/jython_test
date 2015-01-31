from java import lang
lang.System.loadLibrary('GraphMolWrap')
from org.RDKit import *
from threading import Thread
import os
from find_props import funct_dict

def filter_prop(request):
    """Function to filter a list of mols given a particular property
    Takes a request object with three potential attributes
    1) function - a string indicating the property (e.g. 'num_hba')
    2) Max_ans and 3) min_ans - floats indicating the upper and lower limits"""
    new_ans = []
    # Loop through the mols
    for mol in request.body:
        # Get the value for this property
        my_val = funct_dict[request.function](mol)
        # Add this value to the molecule
        mol.setProp(request.function, str(my_val))
        # Now do the checks
        if request.max_ans:
            if my_val > request.max_ans:
                continue
        if request.min_ans:
            if my_val < request.min_ans:
                continue
        # If it's passed these tests append to the out list
        new_ans.append(mol) 
    # Return the out list in the body of the request
    request.body = new_ans
    return request

if __name__ == "__main__":
    # Call this function when calling the script
    filter_prop(request)
