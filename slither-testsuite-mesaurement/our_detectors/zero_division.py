from collections import defaultdict
from typing import DefaultDict, List, Tuple

from slither.core.cfg.node import Node
from slither.core.declarations.contract import Contract
from slither.core.declarations.function_contract import FunctionContract
from slither.core.declarations.solidity_variables import SolidityVariableComposed
from slither.detectors.abstract_detector import (
    AbstractDetector,
    DetectorClassification,
    DETECTOR_INFO,
)
from slither.core.variables import StateVariable
from slither.slithir.operations import Binary, Assignment, BinaryType, LibraryCall, Operation, Phi
from slither.slithir.utils.utils import LVALUE
from slither.slithir.variables import Constant
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

def evaluate_binary_operation(ir, final, result):
    temp_left = ir.variable_left
    temp_right = ir.variable_right
    if (ir.variable_left in final):
        temp_left = final[ir.variable_left]
    elif ir.variable_left in result:
        temp_left = Constant(str(result[ir.variable_left]))
    if (ir.variable_right in final):
        temp_right = final[ir.variable_right]
    elif ir.variable_right in result:
        temp_right = Constant(str(result[ir.variable_right]))
    if (isinstance(ir.variable_left, StateVariable) and ir.variable_left.is_constant):
        temp_left = final[ir.variable_left.name]
    if (isinstance(ir.variable_right, StateVariable) and ir.variable_right.is_constant):
        temp_right = final[ir.variable_right.name]
    if (isinstance(temp_left, Constant) and isinstance(temp_right, Constant)):
        new_expression = BinaryOperation(
            Literal(str(temp_left),type(str)),
            Literal(str(temp_right),type(str)),
            BinaryOperationType.get_type(ir.type.value))
        try:
            result[ir.lvalue] = ConstantFolding(new_expression, temp_left.type).result().value
        except:
            result[ir.lvalue] = None

def list_variables(node, final)-> dict:
    explored = set()
    vals = {}
    result = {}
    if (node.type == NodeType.VARIABLE or node.type == NodeType.EXPRESSION or node.type == NodeType.ENTRYPOINT):
        for ir in node.irs_ssa:
            if (isinstance(ir, Phi)):
                if (isinstance(ir.lvalue, StateVariable) and ir.lvalue.is_constant):
                    final[ir.lvalue] = final[ir.rvalues[0].name]

            if (isinstance(ir, Binary)):
                evaluate_binary_operation(ir, final, result)

            if (isinstance(ir, Assignment)):
                vals[ir.rvalue] = ir.lvalue
                # In case the assigment is a constant (eg: a = 2), will be loaded to de dictionary automaticly
                if isinstance(ir.rvalue, Constant):
                    final[ir.lvalue] = ir.rvalue

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
    for v,s in result.items():
        if v in vals:
            name = vals.get(v)
            final[name] = Constant(str(s))

# pylint: disable=too-many-branches
def _explore(
    to_explore: List[Node], f_results: List[List[Node]], divisions: DefaultDict[LVALUE, List[Node]], variables: dict
) -> None:
    explored = set()
    while to_explore:  # pylint: disable=too-many-nested-blocks
        node = to_explore.pop()

        if node in explored:
            continue
        explored.add(node)

        list_variables(node, variables)

        equality_found = False
        # List of nodes related to one bug instance
        node_results: List[Node] = []

        for ir in node.irs:
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
                if nodes:
                    node_results = nodes

            if isinstance(ir, Binary) and ir.type == BinaryType.EQUAL:
                equality_found = True

        if node_results:
            # We do not track the case where the division is done in a require() or assert()
            # Which also contains a ==, to prevent FP due to the form
            # assert(a == b * c + a % b)
            if not (is_assert(node) and equality_found):
                f_results.append(node_results)

        for son in node.sons:
            to_explore.append(son)


def detect_divsion_by_zero(
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

    for v,s in variables.items():
        print("FINAL", v, s)
    return results


class DivisionByZero(AbstractDetector):
    """
    Division By Zero
    """

    ARGUMENT = "division-by-zero"
    HELP = "Imprecise arithmetic operations valur"
    IMPACT = DetectorClassification.MEDIUM
    CONFIDENCE = DetectorClassification.MEDIUM

    WIKI = "No hay wiki"

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
            divisions_by_zero = detect_divsion_by_zero(contract)
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
