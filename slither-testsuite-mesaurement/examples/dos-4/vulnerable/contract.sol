// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";

contract NaiveBank is Ownable(msg.sender) {
    uint256 public constant INTEREST_RATE = 5; // 5% interest

    struct Account {
        bool registered;
        uint256 balance;
    }

    mapping(address => Account) private userAccounts;
    address[] private userAddresses;

    function depositBankFunds() external payable onlyOwner {
        require(msg.value > 0, "Require some funds");
    }

    function deposit() external payable {
        require(msg.value > 0, "Require some funds");

        if (!userAccounts[msg.sender].registered) {
            // Register new user
            userAddresses.push(msg.sender);
            userAccounts[msg.sender].registered = true;
        }

        userAccounts[msg.sender].balance += msg.value;
    }

    function withdraw(uint256 _withdrawAmount) external {
        require(
            userAccounts[msg.sender].balance >= _withdrawAmount,
            "Insufficient balance"
        );
        userAccounts[msg.sender].balance -= _withdrawAmount;

        (bool success, ) = msg.sender.call{value: _withdrawAmount}("");
        require(success, "Failed to send Ether");
    }

    function applyInterest()
        external
        onlyOwner
        returns (uint256 minBankBalanceRequired_)
    {
        uint numberOfUsers = userAddresses.length;
        for (uint256 i = 0; i < numberOfUsers; i++) {
            address user = userAddresses[i];
            uint256 balance = userAccounts[user].balance;

            // Update user's compound interest
            userAccounts[user].balance =
                (balance * (100 + INTEREST_RATE)) /
                100;

            // Calculate the minimum bank balance required to pay for each user
            minBankBalanceRequired_ += userAccounts[user].balance;
        }
    }

    function getBankBalance() external view returns (uint256) {
        return address(this).balance;
    }

    function getUserBalance(address _user) external view returns (uint256) {
        return userAccounts[_user].balance;
    }
}
/*
DoS - Block gas limit

Two situations that can cause the unbounded denial-of-service 
issue to the NaiveBank contract:

1. The number of depositor accounts grows over time due to the ordinary adoption
2. The contract encounters a Sybil attack

Adapted from source https://github.com/serial-coder/solidity-security-by-example/tree/main/13_double_spending_02
*/
