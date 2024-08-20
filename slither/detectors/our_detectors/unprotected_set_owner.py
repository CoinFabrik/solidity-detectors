from typing import List, Optional, Union
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification

from slither.core.declarations import Function, Contract, Modifier
from slither.core.variables import Variable
from slither.slithir.operations.phi import Phi
from slither.slithir.operations.binary import Binary, BinaryType
from slither.slithir.operations.condition import Condition
from slither.slithir.operations.assignment import Assignment
from slither.slithir.operations.solidity_call import SolidityCall
from slither.slithir.variables.state_variable import StateIRVariable
from slither.core.cfg.node import Node, NodeType

class UnprotectedSetOwner(AbstractDetector):
    """
    Documentation
    """

    ARGUMENT = 'unprotected-set-owner' # slither will launch the detector with slither.py --detect mydetector
    HELP = 'Check if a function modifies a value used for permission checks without first verifying that the user is authorized to make such changes'
    IMPACT = DetectorClassification.HIGH
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = " "
    WIKI_TITLE = " "
    WIKI_DESCRIPTION = " "
    WIKI_EXPLOIT_SCENARIO = " "
    WIKI_RECOMMENDATION = " "

    def _modifier_check_permissions(self, modifier: Modifier) -> Optional[List[StateIRVariable]]:
        var: Variable
        phi_var: List[StateIRVariable]
        ops = modifier.slithir_ssa_operations
        for op in ops:
            if isinstance(op, Phi) and isinstance(op.lvalue, StateIRVariable):
                phi_var = [op.lvalue] + op.rvalues
            if isinstance(op, Binary) and op.type == BinaryType.EQUAL:
                if (op.variable_left.name == "msg.sender" and op.variable_right.name == phi_var[0].name or
                    op.variable_right.name == "msg.sender" and op.variable_left.name == phi_var[0].name):
                    var = op.lvalue
            if isinstance(op, SolidityCall) and any(arg == var for arg in op.arguments):
                return phi_var
            if isinstance(op, Condition) and any(arg == var for arg in op.read):
                return phi_var
        return None

    def _analyze(self):
        modifiers = []
        results = []
        for contract in self.compilation_unit.contracts_derived:
            for modifier in contract.modifiers:
                ret = self._modifier_check_permissions(modifier)
                if ret != None:
                    modifiers.append(tuple([modifier, ret]))
            for func in contract.functions:
                checker_modifiers_used = [m[1] for m in modifiers if m[0] in func.modifiers]
                if func.is_constructor or len(checker_modifiers_used) != 0:
                    continue
                for op in func.slithir_ssa_operations:
                    if isinstance(op, Assignment) and any(op.lvalue in checker_modifier[1] for checker_modifier in modifiers):
                        results.append([func, op.lvalue])
        return results

    def _detect(self):
        res = []
        ret = self._analyze()
        for r in ret:
            res.append(self.generate_result(['The function: "', r[0], '" writes into the variable "', r[1].name,'" used to check permissions on a modifier ']))
        return res