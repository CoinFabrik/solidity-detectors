// SPDX-License-Identifier: MIT
pragma solidity 0.6.12;

contract InsecureEtherVault {
    mapping (address => uint256) private userBalances;

    function deposit() external payable {
        uint256 myval = 16 / 2;
        uint256 e = myval - 8;
        uint256 f = e /2;
        uint256 ko = 88;
        userBalances[msg.sender] += msg.value;
        e = ko / myval;
    }

    function withdraw(uint256 _amount) external {
        uint256 b = 6542345;
        uint256 a = 324;
        uint256 balance = getUserBalance(msg.sender);
        require(balance - _amount >= 0, "Insufficient balance");

        userBalances[msg.sender] -= _amount;
        
        (bool success, ) = msg.sender.call{value: _amount}("");
        require(success, "Failed to send Ether");
    }

    function getEtherBalance() external returns (uint256) {
        return address(this).balance;
    }

    function getUserBalance(address _user) public view returns (uint256) {
        return userBalances[_user];
    }
}

/*
Arithmetic - Integer Underflow 

A simple vault in which users can deposit Ether, withdraw Ether and check their
balances. Vulnerability is in withdraw function, line 13.

Adapted from https://github.com/serial-coder/solidity-security-by-example/tree/main/01_integer_underflow
*/
