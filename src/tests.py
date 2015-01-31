from parsing.mol_entry import parse_mols
from find_props.find_props import calc_props
from camel_objs.models import make_request
from find_props.filter_props import filter_prop

for item in ["/jython_test/src/test_data/test.smi","/jython_test/src/test_data/test.inchi","/jython_test/src/test_data/test.sdf"]:
    # Make the request like object
    request = make_request(body=item)
    # Parse the mols and retunr them in body
    request = parse_mols(request)
    # Now loop through properties calculating them for each mol
    for prop in ["num_hba", "num_hbd", "mol_logp"]:
        # Make the request object - updating the headers
        request = make_request(request=request, headers=prop)
        # Calculate the properties
        calc_props(request)
    # Now update the header to a filter
    request = make_request(request=request, headers="2<num_hba<7")
    # Make the request
    request = filter_prop(request)
