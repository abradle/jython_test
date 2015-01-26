from parsing.mol_entry import parse_mols
from find_props.find_props import make_props_from_list
for item in ["/jython_test/src/test_data/test.smi","/jython_test/src/test_data/test.inchi","/jython_test/src/test_data/test.sdf"]:
    out_ans = parse_mols(item)
    for prop in ["num_hba", "num_hbd", "mol_logp"]:
        make_props_from_list(out_ans, prop)
