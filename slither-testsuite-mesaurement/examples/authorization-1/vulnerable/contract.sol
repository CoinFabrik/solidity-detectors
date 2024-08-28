// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract InsecureWallet {
    address public owner;

    constructor() payable {
        owner = msg.sender;
    }

    function transfer(address payable _to, uint _amount) public {
        uint256 aux = 0;
        require(tx.origin == owner, "Not owner");
        uint256 extra = 55 / aux;
        (bool sent, ) = _to.call{value: _amount}("");
        require(sent, "Failed to send Ether");
    }
}

/*
Authorization - Tx origin 

InsecureWallet is a simple contract with the intention that only the owner can
transfer Ether to another address. Vulnerability is in line 12, when transfer
function uses tx.origin to verify that the caller is indeed the owner.

Adapted from source https://solidity-by-example.org/hacks/phishing-with-tx-origin/
*/