// SPDX-License-Identifier: MIT
pragma solidity 0.8.20;

contract ParticularVault {
    struct Payee {
        address addr;
        uint256 value;
    }

    Payee[] payees;
    uint256 nextPayeeIndex;

    function deposit() external payable {
        payees.push(Payee(msg.sender, msg.value));
    }

    function payOut() external {
        uint256 i = nextPayeeIndex;
        while (i < payees.length && gasleft() > 200000) {
            payable(payees[i].addr).transfer(payees[i].value);
            i++;
        }
        nextPayeeIndex = i;
    }
}

/*
DoS - Block gas limit

If you absolutely must loop over an array of unknown size, then you should plan for it 
to potentially take multiple blocks, and therefore require multiple transactions. You will 
need to keep track of how far you've gone, and be able to resume from that point.

Adapted from https://consensys.github.io/smart-contract-best-practices/attacks/denial-of-service/#dos-with-block-gas-limit
*/
