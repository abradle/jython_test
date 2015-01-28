from parsing.mol_entry import parse_mols
from find_props.find_props import calc_props
from camel_objs.models import make_request
from find_props.filter_props import filter_prop

for item in ["/jython_test/src/test_data/test.smi","/jython_test/src/test_data/test.inchi","/jython_test/src/test_data/test.sdf"]:
    request = make_request(body=item)
    request = parse_mols(request)
    for prop in ["num_hba", "num_hbd", "mol_logp"]:
        request = make_request(request=request, headers=prop)
        calc_props(request)
    request = make_request(request=request, headers="2<num_hba<7")
    request = filter_prop(request)
