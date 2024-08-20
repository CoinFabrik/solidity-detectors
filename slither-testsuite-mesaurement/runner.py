from slither.slither import Slither
from slither import *
from slither.detectors import all_detectors
from slither.printers import all_printers
from slither.detectors.abstract_detector import *
import json
import os
from solc_select import solc_select
from our_detectors.our_detector import OurDetector
from our_detectors.zero_division import DivisionByZero
from our_detectors.unprotected_set_owner import UnprotectedSetOwner


#TODO: revisar mas detenidamente que esto este completo. Por ahora solo consideramos detectores de impacto MEDIUM o HIGH (sin importar confianza)
class_to_detector_mapping = {
    "Arithmetic":["divide-before-multiply", "tautological-compare", "tautology"],
    "Authorization":["tx-origin", "arbitrary-send-eth", "controlled-delegatecall"],
    "Block attributes":["weak-prng"],
    "Delegate call":["controlled-delegatecall", "delegatecall-loop"],
    "DoS":[],
    "MEV":["arbitrary-send-eth"],
    "Reentrancy":["reentrancy-eth", "reentrancy-no-eth", "token-reentrancy"],
    "Privacy":[],
}


#all_detector_classes = dict([(name, cls) for name, cls in all_detectors.__dict__.items() if isinstance(cls, type)])
all_printer_classes = dict([(name, cls) for name, cls in all_printers.__dict__.items() if isinstance(cls, type)])
#all custom detectors may be appended here for testing
#all_detector_classes["OurDetector"] = OurDetector
all_detector_classes = {"OurDetector": OurDetector, "DivisonByZero": DivisionByZero, "UnprotectedSetOwner": UnprotectedSetOwner} #this is if you want to test it by itself


def solc_path_finder(version:str):
    #Helper function to find the correct solc version (according to the config file)
    #for a specific contract.sol example. If the solc version is not installed,
    #the script installs it before selecting it.
    if not solc_select.artifact_path(version).exists():
        print("Installing solc version", version)
        solc_select.install_artifacts([version])
    return solc_select.artifact_path(version).as_posix()


def get_triggered_function_elements(det_output:dict()):
    out_function_det = []
    if len(det_output) > 0:
        for t in det_output[0]:
            for elem in t['elements']:
                if elem['type'] == 'function':
                    out_function_det.append(elem)
    return out_function_det


def result_comparison(run_out : dict(), exp_out : dict()):
    comparison_result = {"FOUND":0, "NOT FOUND":0, "FALSE POSITIVE":0, "FALSE NEGATIVE":0}
    mismatches = []

    #count detectors triggered
    triggered_detectors = [val for val in run_out if len(val) != 0]
    comparison_result["FOUND"] = len(triggered_detectors)
    triggered_detector_function_elems = get_triggered_function_elements(triggered_detectors)
    
    #expected and detected function names
    exp_function_names = [exp_out['function']]
    if (len(exp_function_names) == 1 and exp_function_names[0] == ''):
        exp_function_names = []
    det_function_names = [f['name'] for f in triggered_detector_function_elems]

    #check vulnerability. If the contract is known to be vulnerable, we perform further checks
    if exp_out['vulnerable'] == True:
        expected_detector_name_list = class_to_detector_mapping[exp_out["class"]]

        #agregar caso funcion vacia
        if (len(triggered_detectors) == 0):
            #contract is vulnerable but no detectors were triggered
            #constitutes a false positive for all vulnerabilities present
            comparison_result["NOT FOUND"] = len(exp_function_names) if len(exp_function_names) > 0 else 1
            comparison_result["FALSE NEGATIVE"] = comparison_result["NOT FOUND"]
            if len(exp_function_names) > 0:
                mismatches.append({"EXPECTED FUNCTIONS": exp_function_names, "GOT FUNCTIONS": []})
            else:
                mismatches.append({"SET OF EXPECTED DETECTORS": expected_detector_name_list, "TRIGGERED DETECTOR": []})
        else: 
            #first, we check that the functions match
            #if not, anything found is a false positive
            if any([f not in det_function_names for f in exp_function_names]):
                #at least one function detected as vulnerable was not expected to be vulnerable, add false positives
                mismatches.append({"EXPECTED FUNCTIONS": exp_function_names, "GOT FUNCTIONS": det_function_names})
                comparison_result["FALSE POSITIVE"] += sum([f not in det_function_names for f in exp_function_names])
            
            elif len(exp_function_names) > 0 and any([f not in exp_function_names for f in det_function_names]):
                #at least one vulnerable function was not detected, add false negatives
                mismatches.append({"EXPECTED FUNCTIONS": exp_function_names, "GOT FUNCTIONS": det_function_names})
                comparison_result["FALSE NEGATIVE"] += sum([f not in exp_function_names for f in det_function_names])
            
            else:
                for det_out in triggered_detectors:
                    #if functions match, check detectors
                    if det_out[0]['check'] not in expected_detector_name_list:
                        mismatches.append({"SET OF EXPECTED DETECTORS": expected_detector_name_list, "TRIGGERED DETECTOR": det_out[0]['check']})
                        comparison_result["FALSE POSITIVE"] += 1
    else:
        #if the contract is not vulnerable, all found vulns. are false positives
        # note that for the purpose of this application we exclude informational and low impact detectors
        comparison_result["FALSE POSITIVE"] = comparison_result["FOUND"]
        if len(det_function_names):
            mismatches.append({"EXPECTED FUNCTIONS": [], "GOT FUNCTIONS": det_function_names})
    
    #all false negatives are vulnerabilities not found
    # assert(comparison_result["NOT FOUND"] == comparison_result["FALSE NEGATIVE"])

    return (comparison_result, mismatches)




slither_objects = {}
run_results = {}
expected_results = {}
files_to_run = []

#Traverse directories. For each contract: extract expected results and create the corresponding slither object (with the desired solc version)
for folder in os.listdir("examples"):
    for subfolder in os.listdir(os.path.join("examples", folder)):
        if (subfolder not in ['vulnerable', 'remediated']):
            continue

        # if folder not in ["authorization-1"]:
        #     continue

        contract_filepath = os.path.join("examples", folder, subfolder, "contract.sol")
        config_filepath = os.path.join("examples", folder, subfolder, "config.json")
        expout_filepath = os.path.join("examples", folder, subfolder, "expected-output.json")
        files_to_run.append(contract_filepath)
        
        with open(expout_filepath) as expout:
            expected_results[folder + " " + subfolder] = json.load(expout)
        
        solc_version = ""
        remaps = ""
        with open(config_filepath) as config_file:
            config = json.load(config_file)
            solc_version = config["solc"]
            if "dependencies" in config.keys():
                for dep in config["dependencies"]:
                    remaps += dep + '=node_modules/' + dep + ' '
        remaps = remaps[:-1]

        slither_objects[folder + " " + subfolder] = Slither(contract_filepath, solc = solc_path_finder(solc_version), solc_remaps = remaps)


for example_name, slither_obj in slither_objects.items():
    for d in all_detector_classes.values():
        slither_obj.register_detector(d)
    run_results[example_name] = slither_obj.run_detectors()
    #print(run_results[example_name])
    #print(slither_obj.run_printers())


with open('output.json', 'w') as archivo_json:
    json.dump(run_results, archivo_json, indent=4)

#run result comparison
# f = 0
# final_results = []
# for example_name, run_out in run_results.items():
#     exp_out = expected_results[example_name]

#     print(files_to_run[f])
#     f += 1

#     res = result_comparison(run_out, exp_out)
#     final_results.append(res)
    
#     print(res)
#     print('\n')


#construct summary of results
# found_n = sum([res[0]["FOUND"] - res[0]["FALSE POSITIVE"] for res in final_results])
# vuln_n = len(expected_results.keys())
# p_false_pos = sum([res[0]["FALSE POSITIVE"] for res in final_results]) / (sum([res[0]["FOUND"] for res in final_results]) if sum([res[0]["FOUND"] for res in final_results]) != 0 else 1)
# p_false_neg = sum([res[0]["FALSE NEGATIVE"] for res in final_results]) / len(files_to_run)
# print("SUMMARY \nRan", len(files_to_run), "examples.\nCorrectly identified", found_n, "vulns. out of a universe of", vuln_n, "vulns.")
# print("Proportion of false positives over found vulns.:", p_false_pos)
# print("Proportion of false negatives over total examples:", p_false_neg)