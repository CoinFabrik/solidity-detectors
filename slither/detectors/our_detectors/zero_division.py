from collections import defaultdict
from typing import DefaultDict, List, Tuple
import string

from slither.core.cfg.node import Node
from slither.core.declarations.contract import Contract
from slither.core.declarations.function_contract import FunctionContract
from slither.core.declarations.solidity_variables import SolidityVariableComposed
from slither.detectors.abstract_detector import (
    AbstractDetector,
    DetectorClassification,
    DETECTOR_INFO,
)
from slither.core.variables import StateVariable, LocalVariable, Variable
from slither.slithir.variables.variable import SlithIRVariable
from slither.slithir.operations import Binary, Assignment, BinaryType, LibraryCall, Operation, Phi
from slither.slithir.utils.utils import LVALUE
from slither.slithir.variables import Constant, TemporaryVariableSSA
from slither.utils.output import Output
from slither.visitors.expression.constants_folding import ConstantFolding
from slither.core.expressions import (
    Literal,
    BinaryOperationType,
    BinaryOperation,
)
from slither.core.cfg.node import NodeType, Node

def is_division(ir: Operation) -> bool:
    if isinstance(ir, Binary):
        if ir.type == BinaryType.DIVISION:
            return True

    if isinstance(ir, LibraryCall):
        if ir.function.name and ir.function.name.lower() in [
            "div",
            "safediv",
        ]:
            if len(ir.arguments) == 2:
                if ir.lvalue:
                    return True
    return False


def is_assert(node: Node) -> bool:
    if node.contains_require_or_assert():
        return True
    # Old Solidity code where using an internal 'assert(bool)' function
    # While we dont check that this function is correct, we assume it is
    # To avoid too many FP
    if "assert(bool)" in [c.full_name for c in node.internal_calls]:
        return True
    return False

def get_temp_value(variable, final, result):
    # case: the expression has a variable previously calculated
    if variable in final:
        return final[variable]
    # case: multiple operations in the same node
    elif variable in result:
        return Constant(str(result[variable]))
    #case: variables are constant stateVariables
    if (isinstance(variable, StateVariable) and variable.is_constant and variable.name in final):
            return final[variable.name]
    return variable

def process_constant_folding(left, right, ir):
    new_expression = BinaryOperation(
    Literal(str(left),type(str)),
    Literal(str(right),type(str)),
    BinaryOperationType.get_type(ir.type.value))
    return ConstantFolding(new_expression, left.type).result().value

def evaluate_binary_operation(ir: Operation, final, result):
    if (isinstance(ir, Binary)):
        variables_left = []
        variables_right = []
        temp_left = get_temp_value(ir.variable_left, final, result)
        temp_right = get_temp_value(ir.variable_right, final, result)
        #case: branches created due to ifs
        for val in final:
            if isinstance(val, str):
                if (isinstance(ir.variable_right, LocalVariable) and ir.variable_right.ssa_name in val):
                    variables_right.append(val)
                if (isinstance(ir.variable_left, LocalVariable) and ir.variable_left.ssa_name in val):
                    variables_left.append(val)
        # Creates custom operation and calculates de result with constat folding
        if (isinstance(temp_left, Constant) and isinstance(temp_right, Constant)):
            try:
                result[ir.lvalue] = process_constant_folding(temp_left,temp_right,ir)
            except:
                result[ir.lvalue] = None
        # Case: due to the branches created by the ifs, the possible values of the variables are saved in an array
        elif (variables_left or variables_right):
            if not variables_left:
                variables_left = [temp_left]
            if not variables_right:
                variables_right = [temp_right]

            letter_counter = 0
            alphabet = string.ascii_lowercase  # 'abcdefghijklmnopqrstuvwxyz'
            
            # Calculates every result possible and saves it in the final directory
            for left in variables_left:
                for right in variables_right:
                    if isinstance(right,str):
                        right = final[right]
                    if isinstance(left,str):
                        left = final[left]

                    current_letter = alphabet[letter_counter % len(alphabet)]
                    try:
                        result[f"{ir.lvalue.name}_{current_letter}"] = process_constant_folding(left,right,ir)
                    except:
                        result[f"{ir.lvalue.name}_{current_letter}"] = None
                    letter_counter += 1

def list_variables(node: Node, final)-> dict:
    vals = {}
    result = {}
    if (node.type == NodeType.VARIABLE or node.type == NodeType.EXPRESSION or node.type == NodeType.ENTRYPOINT):
        for ir in node.irs_ssa:
            if (isinstance(ir, Phi)):
                #case: constant state variables declared in phi nodes
                if (isinstance(ir.lvalue, StateVariable) and ir.lvalue.is_constant):
                    if ir.rvalues[0].name in final:
                        final[ir.lvalue] = final[ir.rvalues[0].name]

            if (isinstance(ir, Binary)):
                evaluate_binary_operation(ir, final, result)

            if (isinstance(ir, Assignment)):
                vals[ir.rvalue] = ir.lvalue
                # In case the assigment is a constant (eg: a = 2), will be loaded to de dictionary automaticly
                if isinstance(ir.rvalue, Constant):
                    final[ir.lvalue] = ir.rvalue
                # case constant state variables
                if (isinstance(ir.rvalue, StateVariable) and ir.rvalue.is_constant and ir.rvalue in final):
                    final[ir.lvalue] = final[ir.rvalue]
                
    if (node.type == NodeType.ENDIF):
        for ir in node.irs_ssa:
            # phi node declaration from the two possible cases due to the ifs
            if (isinstance(ir, Phi)):
                letter_counter = 0
                alphabet = string.ascii_lowercase  # 'abcdefghijklmnopqrstuvwxyz'
                for v in ir.rvalues:
                    if v in final:
                        current_letter = alphabet[letter_counter % len(alphabet)]
                        final[f"{ir.lvalue.ssa_name}_{current_letter}"] = final[v]
                        letter_counter +=1

    # Case: State variables declaration
    if (node.type == NodeType.OTHER_ENTRYPOINT):
        for ir in node.irs:
            if (isinstance(ir, Assignment)):
                if ir.lvalue.is_constant:
                    vals[ir.rvalue] = ir.lvalue
                    # In case the assigment is a constant (eg: a = 2), will be loaded to de dictionary automaticly
                    if isinstance(ir.rvalue, Constant):
                        final[ir.lvalue.name] = ir.rvalue
            # There is no need to check if variables are constant, the compiler handles that
            if (isinstance(ir, Binary)):
                evaluate_binary_operation(ir, final, result)

    # save the results in the final dictionary
    letter_counter = 0
    alphabet = string.ascii_lowercase  # 'abcdefghijklmnopqrstuvwxyz'
    for v,s in result.items():
        if v in vals:
            name = vals.get(v)
            final[name] = Constant(str(s))
        else:
            for t, f in vals.items():
                if isinstance(v,str) and t.name in v:
                    current_letter = alphabet[letter_counter % len(alphabet)]
                    if hasattr(f, 'ssa_name'):
                        final[f"{f.ssa_name}_{current_letter}"] = s
                    else:
                        final[f"{f.name}_{current_letter}"] = s
                    letter_counter +=1

# pylint: disable=too-many-branches
def _explore(
    to_explore: List[Node], f_results: List[List[Node]], divisions: DefaultDict[LVALUE, List[Node]], variables: dict
) -> None:
    explored = set()
    while to_explore:  # pylint: disable=too-many-nested-blocks
        node = to_explore.pop(0)

        if node in explored:
            continue
        explored.add(node)

        list_variables(node, variables)

        equality_found = False
        # List of nodes related to one bug instance
        node_results: List[Node] = []

        for ir in node.irs_ssa:
            if isinstance(ir, Assignment):
                if ir.rvalue in divisions:
                    # Avoid duplicate. We dont use set so we keep the order of the nodes
                    if node not in divisions[ir.rvalue]:  # type: ignore
                        divisions[ir.lvalue] = divisions[ir.rvalue] + [node]  # type: ignore
                    else:
                        divisions[ir.lvalue] = divisions[ir.rvalue]  # type: ignore
            
            if is_division(ir):
                divisions[ir.lvalue] = [node]  # type: ignore
                div_arguments = ir.read if isinstance(ir, Binary) else ir.arguments  # type: ignore
                nodes = []
                for r in div_arguments:
                    if not isinstance(r, Constant):
                        if node in divisions[r]:
                            nodes += [n for n in divisions[r] if n not in nodes]
                        else:
                            nodes += [n for n in divisions[r] + [node] if n not in nodes]

                # Check if the divisor is zero
                if len(div_arguments) == 2:
                    divisor = div_arguments[1]
                    is_zero_division = False

                    for val in variables:
                        valaux = val
                        if isinstance(val, SlithIRVariable):
                            valaux = val.ssa_name
                        if isinstance(divisor, (LocalVariable, Constant, StateVariable)):
                            if  isinstance(valaux,str) and (valaux == divisor.ssa_name or valaux.startswith(divisor.ssa_name + "_")):
                                if isinstance(variables[val], Constant):
                                    is_zero_division = variables[val].value == 0

                    if is_zero_division:
                        node_results.append(node)

            if isinstance(ir, Binary) and ir.type == BinaryType.EQUAL:
                equality_found = True

        if node_results:
            if not (is_assert(node) and equality_found):
                f_results.append(node_results)

        for son in node.sons:
            to_explore.append(son)


def detect_division_by_zero(
    contract: Contract,
) -> List[Tuple[FunctionContract, List[Node]]]:

    results: List[Tuple[FunctionContract, List[Node]]] = []
    variables = {}
    constantconsturctorarray: List[FunctionContract] = []
    constructorprocessed = False

    # Loop for each function and modifier.
    constantconsturctor = next((n for n in contract.functions_declared if n.name == "slitherConstructorConstantVariables"), None)
    
    if constantconsturctor:
        constantconsturctorarray.append(constantconsturctor)

    for function in constantconsturctorarray + contract.functions_declared + contract.modifiers_declared:
        if not function.entry_point:
            continue

        # Constant state variables will be analyzed the first
        if (function.name == "slitherConstructorConstantVariables"):
            if (not constructorprocessed):
                constructorprocessed = True
            else:
                continue
        # List of list(nodes)
        # Each list(nodes) is one bug instances
        f_results: List[List[Node]] = []

        # lvalue -> node
        # track all the division results (and the assignment of the division results)
        divisions: DefaultDict[LVALUE, List[Node]] = defaultdict(list)

        _explore([function.entry_point], f_results, divisions, variables)

        for f_result in f_results:
            results.append((function, f_result))

    return results


class DivisionByZero(AbstractDetector):
    """
    Division By Zero
    """

    ARGUMENT = "division-by-zero"
    HELP = "Imprecise arithmetic operations valur"
    IMPACT = DetectorClassification.MEDIUM
    CONFIDENCE = DetectorClassification.MEDIUM

    WIKI = " "

    WIKI_TITLE = "Division By Zero"
    WIKI_DESCRIPTION = "This operation can lead to a division by 0, check the arguments"

    # region wiki_exploit_scenario
    WIKI_EXPLOIT_SCENARIO = """not defined"""
    # endregion wiki_exploit_scenario

    WIKI_RECOMMENDATION = """Consider checking the arguments"""

    def _detect(self) -> List[Output]:
        """
        Detect divisions by zero
        """
        results = []
        for contract in self.contracts:
            divisions_by_zero = detect_division_by_zero(contract)
            if divisions_by_zero:
                for (func, nodes) in divisions_by_zero:

                    info: DETECTOR_INFO = [
                        func,
                        " can divide by zero:\n",
                    ]

                    # sort the nodes to get deterministic results
                    nodes.sort(key=lambda x: x.node_id)

                    for node in nodes:
                        info += ["\t- ", node, "\n"]

                    res = self.generate_result(info)
                    results.append(res)

        return results