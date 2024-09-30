from typing import List, Optional
from slither.core.cfg.node import NodeType, Node
from slither.detectors.abstract_detector import (
    AbstractDetector,
    DetectorClassification,
    DETECTOR_INFO,
)
from slither.core.declarations import Contract
from slither.utils.output import Output
from slither.slithir.operations import (
    HighLevelCall,
    LibraryCall,
    LowLevelCall,
    Send,
    Transfer,
    InternalCall,
)


def detect_call_in_loop(contract: Contract) -> List[Node]:
    ret: List[Node] = []
    for f in contract.functions_entry_points:
        if f.is_implemented:
            call_in_loop(f.entry_point, 0, [], ret)

    return ret


def detect_DoSable_loop(contract: Contract) -> List[Node]:
    #a DoS-able loop is a loop with an unprotected call inside, 
    #that is potentially unbounded
    #a loop is potentially unbounded if a call can fail and revert inside it,
    #before the start variable is updated in the loop
    #and if the indexing variable is used to access a dictionary

    ret: List[Node] = []
    for f in contract.functions_entry_points:
        if f.is_implemented:
            unbounded_failable_loop(f.entry_point, 0, [], ret)

    return ret


def call_in_loop(node: Optional[Node], in_loop_counter: int, visited: List[Node], ret: List[Node]) -> None:
    if node is None:
        return
    if node in visited:
        return
    # shared visited
    visited.append(node)

    if node.type == NodeType.STARTLOOP:
        in_loop_counter += 1
    elif node.type == NodeType.ENDLOOP:
        in_loop_counter -= 1

    if in_loop_counter > 0:
        for ir in node.all_slithir_operations():
            if isinstance(ir, (LowLevelCall, HighLevelCall, Send, Transfer)):
                if isinstance(ir, LibraryCall):
                    continue
                ret.append(ir.node)
            if isinstance(ir, (InternalCall)):
                assert ir.function
                call_in_loop(ir.function.entry_point, in_loop_counter, visited, ret)

    for son in node.sons:
        call_in_loop(son, in_loop_counter, visited, ret)


def unbounded_failable_loop(node: Optional[Node], in_loop_counter: int, visited: List[Node], ret: List[Node]) -> None:
    if node is None:
        return
    if node in visited:
        return
    # shared visited
    
    visited.append(node)
    if node.type == NodeType.STARTLOOP:
        in_loop_counter += 1
    elif node.type == NodeType.ENDLOOP:
        in_loop_counter -= 1

    if in_loop_counter > 0:
        #here I know I am inside a loop
        # node.
        pass
    
    pass




class OurDetector(AbstractDetector):
    """
    Detect ...
    """

    ARGUMENT = "our-detector"  # slither will launch the detector with slither.py --mydetector
    HELP = "detector example"
    IMPACT = DetectorClassification.HIGH
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = "https://github.com/trailofbits/slither/wiki/Adding-a-new-detector"
    WIKI_TITLE = "example"
    WIKI_DESCRIPTION = "example"
    WIKI_EXPLOIT_SCENARIO = ".."
    WIKI_RECOMMENDATION = ".."

    def _detect(self) -> List[Output]:
        results = []

        for contract in self.compilation_unit.contracts_derived:
            # Check if a function has 'backdoor' in its name
            for f in contract.functions:
                # Info to be printed
                info: DETECTOR_INFO = ["Backdoor function found in ", f, "\n"]

                # Add the result in result
                res = self.generate_result(info)

                # results.append(res)
        return results