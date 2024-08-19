INFO:Printers:Contract InsecureEtherVault
        Function InsecureEtherVault.deposit()
                IRs:
                        userBalances_1(mapping(address => uint256)) := ϕ(['userBalances_0', 'userBalances_2', 'userBalances_5', 'userBalances_6'])
                        stateVariable_1(uint256) := ϕ(['stateVariable_0'])
                        otherVar_1(uint256) := ϕ(['otherVar_3', 'otherVar_0', 'otherVar_4'])
                Expression: myval = 16 / 2 + 65 - 25
                IRs:
                        TMP_0(uint256) = 16 / 2
                        TMP_1(uint256) = TMP_0 + 65
                        TMP_2(uint256) = TMP_1 - 25
                        myval_1(uint256) := TMP_2(uint256)
                Expression: e = myval - 48
                IRs:
                        TMP_3(uint256) = myval_1 - 48
                        e_1(uint256) := TMP_3(uint256)
                Expression: f = 2 / e
                IRs:
                        TMP_4(uint256) = 2 / e_1
                        f_1(uint256) := TMP_4(uint256)
                Expression: ko = 88
                IRs:
                        ko_1(uint256) := 88(uint256)
                Expression: userBalances[msg.sender] += msg.value
                IRs:
                        REF_0(uint256) -> userBalances_1[msg.sender]
                        userBalances_2(mapping(address => uint256)) := ϕ(['userBalances_1'])
                        REF_0(-> userBalances_2) = REF_0 + msg.value
                Expression: e == 15
                IRs:
                        TMP_5(bool) = e_1 == 15
                        CONDITION TMP_5
                Expression: myval = 0
                IRs:
                        myval_2(uint256) := 0(uint256)
                IRs:
                        myval_3(uint256) := ϕ(['myval_1', 'myval_2'])
                Expression: e = ko / myval
                IRs:
                        TMP_6(uint256) = ko_1 / myval_3
                        e_2(uint256) := TMP_6(uint256)
                Expression: f = stateVariable + 56
                IRs:
                        TMP_7(uint256) = stateVariable_1 + 56
                        f_2(uint256) := TMP_7(uint256)
                Expression: f = 58 + stateVariable
                IRs:
                        TMP_8(uint256) = 58 + stateVariable_1
                        f_3(uint256) := TMP_8(uint256)
                Expression: ko = otherVar
                IRs:
                        ko_2(uint256) := otherVar_1(uint256)
        Function InsecureEtherVault.withdraw(uint256)
                IRs:
                        userBalances_3(mapping(address => uint256)) := ϕ(['userBalances_0', 'userBalances_2', 'userBalances_5', 'userBalances_6'])
                        otherVar_2(uint256) := ϕ(['otherVar_3', 'otherVar_0', 'otherVar_4'])
                Expression: b = 6542345
                IRs:
                        b_1(uint256) := 6542345(uint256)
                Expression: a = 324
                IRs:
                        a_1(uint256) := 324(uint256)
                Expression: r = otherVar
                IRs:
                        r_1(uint256) := otherVar_2(uint256)
                Expression: balance = getUserBalance(msg.sender)
                IRs:
                        TMP_9(uint256) = INTERNAL_CALL, InsecureEtherVault.getUserBalance(address)(msg.sender)
                        userBalances_4(mapping(address => uint256)) := ϕ(['userBalances_6'])
                        balance_1(uint256) := TMP_9(uint256)
                Expression: require(bool,string)(balance - _amount >= 0,Insufficient balance)
                IRs:
                        TMP_10(uint256) = balance_1 - _amount_1
                        TMP_11(bool) = TMP_10 >= 0
                        TMP_12(None) = SOLIDITY_CALL require(bool,string)(TMP_11,Insufficient balance)
                Expression: otherVar = balance
                IRs:
                        otherVar_3(uint256) := balance_1(uint256)
                Expression: userBalances[msg.sender] -= _amount
                IRs:
                        REF_1(uint256) -> userBalances_4[msg.sender]
                        userBalances_5(mapping(address => uint256)) := ϕ(['userBalances_4'])
                        REF_1(-> userBalances_5) = REF_1 - _amount_1
                Expression: (success) = msg.sender.call{value: _amount}()
                IRs:
                        TUPLE_0(bool,bytes) = LOW_LEVEL_CALL, dest:msg.sender, function:call, arguments:[''] value:_amount_1 
                        success_1(bool)= UNPACK TUPLE_0 index: 0 
                Expression: require(bool,string)(success,Failed to send Ether)
                IRs:
                        TMP_13(None) = SOLIDITY_CALL require(bool,string)(success_1,Failed to send Ether)
        Function InsecureEtherVault.getEtherBalance()
                IRs:
                        stateVariable_2(uint256) := ϕ(['stateVariable_0'])
                Expression: localModified = stateVariable + 85
                IRs:
                        TMP_14(uint256) = stateVariable_2 + 85
                        localModified_1(uint256) := TMP_14(uint256)
                Expression: anotherzero = 89 / localModified
                IRs:
                        TMP_15(uint256) = 89 / localModified_1
                        anotherzero_1(uint256) := TMP_15(uint256)
                Expression: raiseserror = 2 / anotherzero
                IRs:
                        TMP_16(uint256) = 2 / anotherzero_1
                        raiseserror_1(uint256) := TMP_16(uint256)
                Expression: otherVar = localModified + 7
                IRs:
                        TMP_17(uint256) = localModified_1 + 7
                        otherVar_4(uint256) := TMP_17(uint256)
                Expression: address(this).balance
                IRs:
                        TMP_18 = CONVERT this to address
                        TMP_19(uint256) = SOLIDITY_CALL balance(address)(TMP_18)
                        RETURN TMP_19
        Function InsecureEtherVault.getUserBalance(address)
                IRs:
                        _user_1(address) := ϕ(['msg.sender'])
                        userBalances_6(mapping(address => uint256)) := ϕ(['userBalances_0', 'userBalances_2', 'userBalances_5', 'userBalances_6'])
                Expression: userBalances[_user]
                IRs:
                        REF_3(uint256) -> userBalances_6[_user_1]
                        RETURN REF_3
        Function InsecureEtherVault.slitherConstructorVariables()
                Expression: otherVar = 65465
        Function InsecureEtherVault.slitherConstructorConstantVariables()
                Expression: stateVariable = 55
                Expression: stateVariableany = stateVariable + 29

INFO:Slither:examples/arithmetic-1/vulnerable/contract.sol analyzed (1 contracts)