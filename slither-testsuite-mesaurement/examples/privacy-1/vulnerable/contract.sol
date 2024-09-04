// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract OddEven {
    struct Player {
        address addr;
        uint number;
    }

    Player[2] private players;
    uint count = 0;

    function play(uint number) public payable {
        require(msg.value == 1 ether, "msg.value must be 1 eth");
        players[count] = Player(msg.sender, number);
        count++;
        if (count == 2) selectWinner();
    }

    function selectWinner() private {
        uint n = players[0].number + players[1].number;
        (bool success, ) = players[n % 2].addr.call{
            value: address(this).balance
        }("");
        require(success, "transfer failed");
        delete players;
        count = 0;
    }
}

/*
Privacy - Unencrypted private data on-chain

It is a common misconception that private type variables cannot be read. 
Even if your contract is not published, attackers can look at contract 
transactions to determine values stored in the state of the contract. For 
this reason, it's important that unencrypted private data is not stored 
in the contract code or state.

Remediation: Any private data should either be stored off-chain, or 
carefully encrypted.

The OddEven contract requires the players to send the number they are using 
as part of the transaction. This means the first player's number will be visible, 
allowing the second player to select a number that they know will make them a winner. 
(This assumption is simplistic to illustrate - there are also possibilities to 
front-run players, among other potential issues).

Adapted from https://swcregistry.io/docs/SWC-136/
*/
