INFO:Printers:Contract InsecureEtherVault
        Function InsecureEtherVault.deposit() (*)
                Expression: ko = 87
                IRs:
                        ko(uint256) := 87(uint256)
                Expression: userBalances[msg.sender] += msg.value
                IRs:
                        REF_0(uint256) -> userBalances[msg.sender]
                        REF_0(-> userBalances) = REF_0 + msg.value
                Expression: e = ko / myval
                IRs:
                        TMP_0(uint256) = ko / myval
                        e(uint256) := TMP_0(uint256)
        Function InsecureEtherVault.withdraw(uint256) (*)
                Expression: b = 6542345
                IRs:
                        b(uint256) := 6542345(uint256)
                Expression: a = 324
                IRs:
                        a(uint256) := 324(uint256)
                Expression: balance = getUserBalance(msg.sender)
                IRs:
                        TMP_1(uint256) = INTERNAL_CALL, InsecureEtherVault.getUserBalance(address)(msg.sender)
                        balance(uint256) := TMP_1(uint256)
                Expression: require(bool,string)(balance - _amount >= 0,Insufficient balance)
                IRs:
                        TMP_2(uint256) = balance - _amount
                        TMP_3(bool) = TMP_2 >= 0
                        TMP_4(None) = SOLIDITY_CALL require(bool,string)(TMP_3,Insufficient balance)
                Expression: userBalances[msg.sender] -= _amount / e
                IRs:
                        REF_1(uint256) -> userBalances[msg.sender]
                        TMP_5(uint256) = _amount / e
                        REF_1(-> userBalances) = REF_1 - TMP_5
                Expression: (success) = msg.sender.call{value: _amount}()
                IRs:
                        TUPLE_0(bool,bytes) = LOW_LEVEL_CALL, dest:msg.sender, function:call, arguments:[''] value:_amount 
                        success(bool)= UNPACK TUPLE_0 index: 0 
                Expression: require(bool,string)(success,Failed to send Ether)
                IRs:
                        TMP_6(None) = SOLIDITY_CALL require(bool,string)(success,Failed to send Ether)
        Function InsecureEtherVault.getEtherBalance() (*)
                Expression: address(this).balance
                IRs:
                        TMP_7 = CONVERT this to address
                        TMP_8(uint256) = SOLIDITY_CALL balance(address)(TMP_7)
                        RETURN TMP_8
        Function InsecureEtherVault.getUserBalance(address) (*)
                Expression: userBalances[_user]
                IRs:
                        REF_3(uint256) -> userBalances[_user]
                        RETURN REF_3
        Function InsecureEtherVault.slitherConstructorVariables() (*)
                Expression: myval = 16 / 2
                IRs:
                        TMP_9(uint256) = 16 / 2
                        myval(uint256) := TMP_9(uint256)
                Expression: e = myval - 8
                IRs:
                        TMP_10(uint256) = myval - 8
                        e(uint256) := TMP_10(uint256)
                Expression: f = e / 2
                IRs:
                        TMP_11(uint256) = e / 2
                        f(uint256) := TMP_11(uint256)

INFO:Slither:examples/arithmetic-1/vulnerable/contract.sol analyzed (1 contracts)