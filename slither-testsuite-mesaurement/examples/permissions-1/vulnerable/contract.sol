/*
 * @source: https://github.com/trailofbits/not-so-smart-contracts/blob/master/unprotected_function/Unprotected.sol
 * @author: -
 * @vulnerable_at_lines: 25
 */

pragma solidity ^0.8.15;

contract Unprotected{
    address private owner;

    modifier onlyowner {
        require(msg.sender==owner);
        _;
    }

    modifier onlyowner2 {
        assert(msg.sender==owner);
        _;
    }

    modifier onlyowner3 {
        if(msg.sender==owner) {
            _;
        }
    }

    constructor()
    {
        owner = msg.sender;
    }

    // This function should be protected
    // <yes> <report> ACCESS_CONTROL
    function changeOwner(address _newOwner)
        public
    {
        owner = _newOwner;
    }

    function protectedChangeOwner(address _newOwner)
        public
        onlyowner 
    {
        owner = _newOwner;
    }

    function protectedChangeOwner2(address _newOwner)
        public
        onlyowner2
    {
        owner = _newOwner;
    }

    function protectedChangeOwner3(address _newOwner)
        public
        onlyowner3
    {
        owner = _newOwner;
    }


    function changeOwner_fixed(address _newOwner)
        public
        onlyowner
    {
        owner = _newOwner;
    }
}