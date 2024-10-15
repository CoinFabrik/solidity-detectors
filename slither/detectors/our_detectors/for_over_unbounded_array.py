from typing import List, Optional, Union
from slither.core.variables.variable import Variable
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification

from slither.core.expressions.identifier import Identifier
from slither.core.solidity_types.array_type import ArrayType
from slither.core.solidity_types.elementary_type import ElementaryType
from slither.core.declarations.solidity_variables import SolidityFunction
from slither.core.expressions.member_access import MemberAccess
from slither.core.expressions.binary_operation import BinaryOperation
from slither.core.expressions.call_expression import CallExpression
from slither.core.cfg.node import Node, NodeType

class ForOverUnboundedArray(AbstractDetector):
    """
    Documentation
    """

    ARGUMENT = 'for-over-unbounded-array' # slither will launch the detector with slither.py --detect mydetector
    HELP = 'This detector checks that array.length is not used as a condition in a loop if there is no control limiting the number of elements that can be pushed into the array.'
    IMPACT = DetectorClassification.HIGH
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = " "
    WIKI_TITLE = " "
    WIKI_DESCRIPTION = " "
    WIKI_EXPLOIT_SCENARIO = " "
    WIKI_RECOMMENDATION = " "

    def _is_inside_if_or_after_require(self, node: Node, arrays: list[Variable]) -> bool:
        for dominator in node.dominators:
            if (dominator.contains_require_or_assert() and
                isinstance(dominator.expression, CallExpression) and
                isinstance(dominator.expression.called, Identifier) and
                isinstance(dominator.expression.called.value, SolidityFunction) and 
                (dominator.expression.called.value.name == "require(bool)" or
                dominator.expression.called.value.name == "assert(bool)")
            ):
                if any([var in arrays for var in dominator.variables_read]):
                    return True
        
            if (dominator.type == NodeType.IF and
                isinstance(dominator.expression, BinaryOperation)
            ):
                for expr in dominator.expression.expressions:
                    if (isinstance(expr, MemberAccess) and
                        isinstance(expr.expression, Identifier) and
                        expr.expression.value in arrays
                    ):
                        return True
        return False


    def _fathers_check_array_len(self, node: Node, visited_nodes: list[Node]) -> bool:
        for father in node.fathers:
            if(father not in visited_nodes):
                visited_nodes.append(father)
                if(father.type != NodeType.ENTRYPOINT):
                    self._fathers_check_array_len(father, visited_nodes)

    def _analyze(self):
        results = []
        arrays = set()
        arrays_used_in_loops = set()
        arrays_with_unchecked_push = set()
        for contract in self.compilation_unit.contracts_derived:
            #guardo todos los arrays dinamicos
            for var in contract.variables:
                if isinstance(var.type, ArrayType) and var.type.is_dynamic_array:
                    arrays.add(var)

            for func in contract.functions:
                for node in func.nodes:
                    #pasada para encontrar usos de array.length en las condiciones de los loops
                    if node.type == NodeType.IFLOOP and isinstance(node.expression, BinaryOperation):
                        for expr in node.expression.expressions:
                            if (isinstance(expr, MemberAccess) and
                                isinstance(expr.expression, Identifier) and
                                isinstance(expr.expression.value.type, ArrayType) and
                                expr.member_name == "length"

                                #expr.expression.value in arrays and
                                
                            ):
                                arrays_used_in_loops.add(expr.expression.value)
                    #pasada para encontrar pushes no chequeados
                    if (not self._is_inside_if_or_after_require(node, arrays_used_in_loops) and 
                        isinstance(node.expression, CallExpression) and
                        isinstance(node.expression.called, MemberAccess) and
                        isinstance(node.expression.called.expression, Identifier) and
                        node.expression.called.member_name == "push"
                    ):
                        arrays_with_unchecked_push.add(node.expression.called.expression.value)

            #limpio arrays detectados que no sean dinamicos
            arrays_used_in_loops.intersection_update(arrays)
            arrays_with_unchecked_push.intersection_update(arrays)

            for arr in (arrays_used_in_loops & arrays_with_unchecked_push):
                results.append(arr)
                        
                    
        return results

    def _detect(self):
        res = []
        ret = self._analyze()
        for r in ret:
            res.append(self.generate_result(['The array "', r.name, '" is a variable-sized array used in a loop condition, which may cause a DoS when the array becomes large enough']))
        return res