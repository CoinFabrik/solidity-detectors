// SPDX-License-Identifier: MIT
pragma solidity 0.8.13;

contract PotentiallyInsecureReentrant {
    bool public not_called;

    function bug() public{
        require(not_called);
        (bool success, ) = msg.sender.call("");
        require(success, "Failed to call");
        not_called = false;
    }
}

/*
Reentrancy

A toy contract showing a reentrancy that does not involve an ether transfer. 
Possible vulnerability is in bug function.

Adapted from https://github.com/crytic/slither/wiki/Detector-Documentation#reentrancy-vulnerabilities-1
*/