// SPDX-License-Identifier: MIT
pragma solidity 0.8.20;

import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";

contract InsecureEtherVault is ReentrancyGuard {
    mapping (address => uint256) private userBalances;

    function deposit() external payable {
        userBalances[msg.sender] += msg.value;
    }

    function withdrawAll() external nonReentrant {
        uint256 balance = getUserBalance(msg.sender);
        require(balance > 0, "Insufficient balance");

        (bool success, ) = msg.sender.call{value: balance}("");
        require(success, "Failed to send Ether");
        
        userBalances[msg.sender] = 0;
    }

    function getBalance() external view returns (uint256) {
        return address(this).balance;
    }

    function getUserBalance(address _user) public view returns (uint256) {
        return userBalances[_user];
    }
}

/*
Reentrancy  

A simple vault in which users can deposit Ether, withdraw Ether, 
and check their balances. There's no check-effects-interaction pattern,
which is a bad practice. However, in this toy contract, reentrancy is 
remediated by the nonReentrant modifier.
*/