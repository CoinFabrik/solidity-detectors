// SPDX-License-Identifier: MIT
pragma solidity ^0.8.15;

contract UnboundedArrayDoS {
    // Dynamic array that could grow without limit
    address[] public users;
    address[] public protectedUsers;
    address[] public protectedUsers2;

    // Function to add a user to the array
    function addUser(address _user) public {
        users.push(_user);
    }
    
    function protectedAddUser(address _user) public {
        if(protectedUsers.length<100){
            protectedUsers.push(_user);
        }
    }

    function protectedAddUser2(address _user) public {
        require(protectedUsers2.length<100);
        protectedUsers2.push(_user);
    }

    // Function to iterate through the array of users
    // Potential DoS risk due to out-of-gas exception
    function processUsers() public view {
        for (uint i = 0; i < users.length; i++) {
            // Some processing logic
        }
    }

    function processProtectedUsers() public view {
        for (uint i = 0; i < protectedUsers.length; i++) {
            // Some processing logic
        }
    }

    function processProtectedUsers2() public view {
        for (uint i = 0; i < protectedUsers2.length; i++) {
            // Some processing logic
        }
    }
}