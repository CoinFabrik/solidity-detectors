// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract GuessTheRandomNumber {
    constructor() payable {
        require(msg.value == 1 ether, "Need to send 1 ETH");
    }

    function guess(uint _guess) public {
        uint answer = uint(
            keccak256(
                abi.encodePacked(blockhash(block.number - 1), block.timestamp)
            )
        );

        if (_guess == answer) {
            (bool sent, ) = msg.sender.call{value: 1 ether}("");
            require(sent, "Failed to send Ether");
        }
    }
}

/*
Block Attributes - Source of randomness

GuessTheRandomNumber is a game where you win 1 Ether if you can guess the
pseudo random number generated from block hash and timestamp.

At first glance, it seems impossible to guess the correct number.
But let's see how easy it is win.

1. Alice deploys GuessTheRandomNumber with 1 Ether
2. Eve deploys Attack
3. Eve calls Attack.attack() and wins 1 Ether

What happened?
Attack computed the correct answer by simply copying the code that computes the random number.

Adapted from https://solidity-by-example.org/hacks/randomness/
*/
