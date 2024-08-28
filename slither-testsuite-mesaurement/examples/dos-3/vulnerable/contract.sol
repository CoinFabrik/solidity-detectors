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
        while (nextPayeeIndex < payees.length) {
            nextPayeeIndex++;
            payable(payees[nextPayeeIndex - 1].addr).send(
                payees[nextPayeeIndex - 1].value
            );
        }
    }
}

/*
DoS - Block gas limit

In this particular vault, people can deposit and there's a pay out function 
which pays them all.

By paying out to everyone at once, it risks running into the 
block gas limit.

This can lead to problems even in the absence of an intentional attack. However, 
it's especially bad if an attacker can manipulate the amount of gas needed. In the 
case of the previous example, the attacker could add a bunch of addresses, each of 
which needs to get a very small refund. The gas cost of refunding each of the 
attacker's addresses could, therefore, end up being more than the gas limit, 
blocking the refund transaction from happening at all.

Adapted from https://consensys.github.io/smart-contract-best-practices/attacks/denial-of-service/#dos-with-block-gas-limit
*/
