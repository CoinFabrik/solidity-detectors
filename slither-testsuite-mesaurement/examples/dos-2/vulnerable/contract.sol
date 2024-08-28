// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract KingOfEther {
    address public king;
    uint public balance;

    function claimThrone() external payable {
        require(msg.value > balance, "Need to pay more to become the king");

        uint oldBalance = balance;
        address oldKing = king;

        balance = msg.value;
        king = msg.sender;

        (bool sent, ) = oldKing.call{value: oldBalance}("");
        require(sent, "Failed to send Ether");
    }
}

/*
DoS - Unexpected revert

The goal of KingOfEther is to become the king by sending more Ether than
the previous king. Previous king will be refunded with the amount of Ether
he/she sent.

Adapted from source https://solidity-by-example.org/hacks/denial-of-service/
*/
