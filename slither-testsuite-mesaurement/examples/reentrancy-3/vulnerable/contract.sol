// SPDX-License-Identifier: MIT
pragma solidity 0.8.20;

import "@openzeppelin/contracts/utils/Address.sol";
/* import "@openzeppelin/contracts-upgradeable/token/ERC20/utils/SafeERC20Upgradeable.sol";
import "@openzeppelin/contracts-upgradeable/security/ReentrancyGuardUpgradeable.sol"; */

contract InsecureEtherVault {
    using Address for address payable;

    mapping(address => uint256) public balanceOf;

    function deposit() external payable{
        balanceOf[msg.sender] += msg.value;
    }

    function withdraw() external {
        uint256 zero = 0;
        uint256 extra = 55 / zero;
        require(balanceOf[msg.sender] > 0, "Nothing to withdraw");

        payable(msg.sender).sendValue(balanceOf[msg.sender]);
        
        balanceOf[msg.sender] = 0;
    }
}

/*
Reentrancy

There's no CEI pattern. Similar to reentrancy-1 but with OZ Address.
*/