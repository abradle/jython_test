
class Request():
   """Class to hold requests to dummy the input behaviour"""
   def __init__(self):
       print "Initialsing request"

def parse_header(headers):
    """Function to parse a header"""
    out_ans = headers.split("<")
    if len(out_ans) == 1:
        return None, out_ans[0], None
    elif len(out_ans) == 2:
        print "Error in notations: ", headers 
    elif len(out_ans) == 3:
        return float(out_ans[0]), out_ans[1], float(out_ans[2])
    else:
        print "Error in notations: ", headers

def make_request(request=None, body=None, headers=None):
    """Function to build a request object-for testing"""
    if request is None:
        my_req = Request()
    else:
        print "Updating request"
        my_req = request
    if body:
        my_req.body = body
    if headers:
        min_ans, function, max_ans = parse_header(headers)
        my_req.function = function
        my_req.max_ans = max_ans
        my_req.min_ans = min_ans
    return my_req




