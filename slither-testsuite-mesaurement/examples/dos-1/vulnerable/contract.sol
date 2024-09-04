// SPDX-License-Identifier: MIT
pragma solidity 0.8.20;

import {Address} from "@openzeppelin/contracts/utils/Address.sol";

contract SimpleAuction {
    using Address for address payable;

    address payable public currentLeader;
    uint256 public currentBid;

    function bid() external payable {
        require(msg.value > currentBid, "Bid not high enough");

        address payable previousLeader = currentLeader;
        uint256 previousBid = currentBid;

        currentLeader = payable(msg.sender);
        currentBid = msg.value;

        previousLeader.sendValue(previousBid);
    }
}

/*
DoS - Unexpected revert

SimpleAuction contract consists of an auction that keeps track of the highest
bid offered so far and its bidder. When the current bidder loses their place,
their funds are pushed back by the contract.

A denial of service attack can occur to this contract, for instance, placing a
bid thorough a contract that has not declared a receive function (and is thus
unable to receive any Ether). Therefore, if a bid is placed through that
contract, no other bidder will be able to place a higher bid. This is because
sendValue function will be reverted.
*/
