from java import lang
lang.System.loadLibrary('GraphMolWrap')
from org.RDKit import *
from threading import Thread
import os
from find_props import funct_dict

def filter_prop(request):
    new_ans = []
    for mol in request.body:
        my_val = funct_dict[request.function](mol)
        mol.setProp(request.function, str(my_val))
# Now di tge checjs
        if request.max_ans:
            if my_val > request.max_ans:
                continue
        if request.min_ans:
            if my_val < request.min_ans:
                continue
        new_ans.append(mol)
    request.body = new_ans
    return request

if __name__ == "__main__":
    filter_prop(request)
