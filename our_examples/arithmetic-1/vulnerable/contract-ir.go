INFO:Printers:Contract InsecureEtherVault
        Function InsecureEtherVault.deposit() (*)
                Expression: myval = 16 / 2 + 65 - 25
                IRs:
                        TMP_0(uint256) = 16 / 2
                        TMP_1(uint256) = TMP_0 + 65
                        TMP_2(uint256) = TMP_1 - 25
                        myval(uint256) := TMP_2(uint256)
                Expression: e = myval - 48
                IRs:
                        TMP_3(uint256) = myval - 48
                        e(uint256) := TMP_3(uint256)
                Expression: f = 2 / e
                IRs:
                        TMP_4(uint256) = 2 / e
                        f(uint256) := TMP_4(uint256)
                Expression: ko = 88 + e
                IRs:
                        TMP_5(uint256) = 88 + e
                        ko(uint256) := TMP_5(uint256)
                Expression: userBalances[msg.sender] += msg.value
                IRs:
                        REF_0(uint256) -> userBalances[msg.sender]
                        REF_0(-> userBalances) = REF_0 + msg.value
                Expression: e == 15
                IRs:
                        TMP_6(bool) = e == 15
                        CONDITION TMP_6
                Expression: myval = 2
                IRs:
                        myval(uint256) := 2(uint256)
                Expression: myval = 4
                IRs:
                        myval(uint256) := 4(uint256)
                Expression: e = ko / myval
                IRs:
                        TMP_7(uint256) = ko / myval
                        e(uint256) := TMP_7(uint256)
                Expression: f = stateVariable + 56
                IRs:
                        TMP_8(uint256) = stateVariable + 56
                        f(uint256) := TMP_8(uint256)
                Expression: e == 22
                IRs:
                        TMP_9(bool) = e == 22
                        CONDITION TMP_9
                Expression: f = 58 + stateVariable
                IRs:
                        TMP_10(uint256) = 58 + stateVariable
                        f(uint256) := TMP_10(uint256)
                Expression: f = stateVariable
                IRs:
                        f(uint256) := stateVariable(uint256)
                Expression: ko = f * 6
                IRs:
                        TMP_11(uint256) = f * 6
                        ko(uint256) := TMP_11(uint256)
                Expression: myval = otherVar
                IRs:
                        myval(uint256) := otherVar(uint256)
        Function InsecureEtherVault.withdraw(uint256) (*)
                Expression: b = 6542345
                IRs:
                        b(uint256) := 6542345(uint256)
                Expression: a = 324
                IRs:
                        a(uint256) := 324(uint256)
                Expression: r = otherVar
                IRs:
                        r(uint256) := otherVar(uint256)
                Expression: balance = getUserBalance(msg.sender)
                IRs:
                        TMP_12(uint256) = INTERNAL_CALL, InsecureEtherVault.getUserBalance(address)(msg.sender)
                        balance(uint256) := TMP_12(uint256)
                Expression: require(bool,string)(balance - _amount >= 0,Insufficient balance)
                IRs:
                        TMP_13(uint256) = balance - _amount
                        TMP_14(bool) = TMP_13 >= 0
                        TMP_15(None) = SOLIDITY_CALL require(bool,string)(TMP_14,Insufficient balance)
                Expression: otherVar = balance
                IRs:
                        otherVar(uint256) := balance(uint256)
                Expression: userBalances[msg.sender] -= _amount
                IRs:
                        REF_1(uint256) -> userBalances[msg.sender]
                        REF_1(-> userBalances) = REF_1 - _amount
                Expression: (success) = msg.sender.call{value: _amount}()
                IRs:
                        TUPLE_0(bool,bytes) = LOW_LEVEL_CALL, dest:msg.sender, function:call, arguments:[''] value:_amount 
                        success(bool)= UNPACK TUPLE_0 index: 0 
                Expression: require(bool,string)(success,Failed to send Ether)
                IRs:
                        TMP_16(None) = SOLIDITY_CALL require(bool,string)(success,Failed to send Ether)
        Function InsecureEtherVault.getEtherBalance() (*)
                Expression: localModified = stateVariable + 85
                IRs:
                        TMP_17(uint256) = stateVariable + 85
                        localModified(uint256) := TMP_17(uint256)
                Expression: anotherzero = 89 / localModified
                IRs:
                        TMP_18(uint256) = 89 / localModified
                        anotherzero(uint256) := TMP_18(uint256)
                Expression: raiseserror = 2 / anotherzero
                IRs:
                        TMP_19(uint256) = 2 / anotherzero
                        raiseserror(uint256) := TMP_19(uint256)
                Expression: otherVar = localModified + 7
                IRs:
                        TMP_20(uint256) = localModified + 7
                        otherVar(uint256) := TMP_20(uint256)
                Expression: address(this).balance
                IRs:
                        TMP_21 = CONVERT this to address
                        TMP_22(uint256) = SOLIDITY_CALL balance(address)(TMP_21)
                        RETURN TMP_22
        Function InsecureEtherVault.getUserBalance(address) (*)
                Expression: userBalances[_user]
                IRs:
                        REF_3(uint256) -> userBalances[_user]
                        RETURN REF_3
        Function InsecureEtherVault.slitherConstructorVariables() (*)
                Expression: otherVar = 65465
                IRs:
                        otherVar(uint256) := 65465(uint256)
        Function InsecureEtherVault.slitherConstructorConstantVariables() (*)
                Expression: stateVariable = 55
                IRs:
                        stateVariable(uint256) := 55(uint256)
                Expression: stateVariableany = stateVariable + 29
                IRs:
                        TMP_23(uint256) = stateVariable + 29
                        stateVariableany(uint256) := TMP_23(uint256)

INFO:Slither:examples/arithmetic-1/vulnerable/contract.sol analyzed (1 contracts)