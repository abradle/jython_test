from java import lang
lang.System.loadLibrary('GraphMolWrap')
from org.RDKit import *
from threading import Thread
import os
from find_props import funct_dict

def filter_prop(request):
    request.out_stream = []
    for mol in request.in_stream:
        my_val = funct_dict[request.header](ret_val=True)
# Now di tge checjs
        if request.max_ans:
            if my_val > request.max_ans:
                continue
        if request.min_ans:
            if my_val < request.min_ans:
                continue
        request.out_stream.append(mol)

if __name__ is "__main__":
    filter_prop(request)
