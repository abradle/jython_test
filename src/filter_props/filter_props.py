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


#### All functions in this class take two args - less than and more than

