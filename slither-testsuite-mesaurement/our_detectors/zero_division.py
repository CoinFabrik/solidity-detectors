from collections import defaultdict
from typing import DefaultDict, List, Tuple

from slither.core.cfg.node import Node
from slither.core.declarations.contract import Contract
from slither.core.declarations.function_contract import FunctionContract
from slither.detectors.abstract_detector import (
    AbstractDetector,
    DetectorClassification,
    DETECTOR_INFO,
)
from slither.slithir.operations import Binary, Assignment, BinaryType, LibraryCall, Operation
from slither.slithir.utils.utils import LVALUE
from slither.slithir.variables import Constant
from slither.utils.output import Output


def is_division(ir: Operation) -> bool:
    if isinstance(ir, Binary):
        if ir.type == BinaryType.DIVISION:
            a = ir.variable_left
            b = ir.variable_right
            print(a, "right:", b)
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


# pylint: disable=too-many-branches
def _explore(
    to_explore: List[Node], f_results: List[List[Node]], divisions: DefaultDict[LVALUE, List[Node]]
) -> None:
    explored = set()
    while to_explore:  # pylint: disable=too-many-nested-blocks
        node = to_explore.pop()

        if node in explored:
            continue
        explored.add(node)

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
                print(node)
                f_results.append(node_results)

        for son in node.sons:
            to_explore.append(son)


def detect_divsion_by_zero(
    contract: Contract,
) -> List[Tuple[FunctionContract, List[Node]]]:

    results: List[Tuple[FunctionContract, List[Node]]] = []

    # Loop for each function and modifier.
    for function in contract.functions_declared + contract.modifiers_declared:
        if not function.entry_point:
            continue

        # List of list(nodes)
        # Each list(nodes) is one bug instances
        f_results: List[List[Node]] = []

        # lvalue -> node
        # track all the division results (and the assignment of the division results)
        divisions: DefaultDict[LVALUE, List[Node]] = defaultdict(list)

        _explore([function.entry_point], f_results, divisions)

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
