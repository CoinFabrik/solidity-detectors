INFO:Printers:Contract Address
        Function Address.sendValue(address,uint256)
                Expression: address(this).balance < amount
                IRs:
                        TMP_0 = CONVERT this to address
                        TMP_1(uint256) = SOLIDITY_CALL balance(address)(TMP_0)
                        TMP_2(bool) = TMP_1 < amount_1
                        CONDITION TMP_2
                Expression: revert AddressInsufficientBalance(address)(address(this))
                IRs:
                        TMP_3 = CONVERT this to address
                        TMP_4(None) = SOLIDITY_CALL revert AddressInsufficientBalance(address)(TMP_3)
                Expression: (success,None) = recipient.call{value: amount}()
                IRs:
                        TUPLE_0(bool,bytes) = LOW_LEVEL_CALL, dest:recipient_1, function:call, arguments:[''] value:amount_1 
                        success_1(bool)= UNPACK TUPLE_0 index: 0 
                Expression: ! success
                IRs:
                        TMP_5 = UnaryType.BANG success_1 
                        CONDITION TMP_5
                Expression: revert FailedInnerCall()()
                IRs:
                        TMP_6(None) = SOLIDITY_CALL revert FailedInnerCall()()
        Function Address.functionCall(address,bytes)
                Expression: functionCallWithValue(target,data,0)
                IRs:
                        TMP_7(bytes) = INTERNAL_CALL, Address.functionCallWithValue(address,bytes,uint256)(target_1,data_1,0)
                        RETURN TMP_7
        Function Address.functionCallWithValue(address,bytes,uint256)
                IRs:
                        target_1(address) := ϕ(['target_1'])
                        data_1(bytes) := ϕ(['data_1'])
                Expression: address(this).balance < value
                IRs:
                        TMP_8 = CONVERT this to address
                        TMP_9(uint256) = SOLIDITY_CALL balance(address)(TMP_8)
                        TMP_10(bool) = TMP_9 < value_1
                        CONDITION TMP_10
                Expression: revert AddressInsufficientBalance(address)(address(this))
                IRs:
                        TMP_11 = CONVERT this to address
                        TMP_12(None) = SOLIDITY_CALL revert AddressInsufficientBalance(address)(TMP_11)
                Expression: (success,returndata) = target.call{value: value}(data)
                IRs:
                        TUPLE_1(bool,bytes) = LOW_LEVEL_CALL, dest:target_1, function:call, arguments:['data_1'] value:value_1 
                        success_1(bool)= UNPACK TUPLE_1 index: 0 
                        returndata_1(bytes)= UNPACK TUPLE_1 index: 1 
                Expression: verifyCallResultFromTarget(target,success,returndata)
                IRs:
                        TMP_13(bytes) = INTERNAL_CALL, Address.verifyCallResultFromTarget(address,bool,bytes)(target_1,success_1,returndata_1)
                        RETURN TMP_13
        Function Address.functionStaticCall(address,bytes)
                Expression: (success,returndata) = target.staticcall(data)
                IRs:
                        TUPLE_2(bool,bytes) = LOW_LEVEL_CALL, dest:target_1, function:staticcall, arguments:['data_1']  
                        success_1(bool)= UNPACK TUPLE_2 index: 0 
                        returndata_1(bytes)= UNPACK TUPLE_2 index: 1 
                Expression: verifyCallResultFromTarget(target,success,returndata)
                IRs:
                        TMP_14(bytes) = INTERNAL_CALL, Address.verifyCallResultFromTarget(address,bool,bytes)(target_1,success_1,returndata_1)
                        RETURN TMP_14
        Function Address.functionDelegateCall(address,bytes)
                Expression: (success,returndata) = target.delegatecall(data)
                IRs:
                        TUPLE_3(bool,bytes) = LOW_LEVEL_CALL, dest:target_1, function:delegatecall, arguments:['data_1']  
                        success_1(bool)= UNPACK TUPLE_3 index: 0 
                        returndata_1(bytes)= UNPACK TUPLE_3 index: 1 
                Expression: verifyCallResultFromTarget(target,success,returndata)
                IRs:
                        TMP_15(bytes) = INTERNAL_CALL, Address.verifyCallResultFromTarget(address,bool,bytes)(target_1,success_1,returndata_1)
                        RETURN TMP_15
        Function Address.verifyCallResultFromTarget(address,bool,bytes)
                IRs:
                        target_1(address) := ϕ(['target_1', 'target_1', 'target_1'])
                        success_1(bool) := ϕ(['success_1', 'success_1', 'success_1'])
                        returndata_1(bytes) := ϕ(['returndata_1', 'returndata_1', 'returndata_1'])
                Expression: ! success
                IRs:
                        TMP_16 = UnaryType.BANG success_1 
                        CONDITION TMP_16
                Expression: _revert(returndata)
                IRs:
                        INTERNAL_CALL, Address._revert(bytes)(returndata_1)
                Expression: returndata.length == 0 && target.code.length == 0
                IRs:
                        REF_4 -> LENGTH returndata_1
                        TMP_18(bool) = REF_4 == 0
                        TMP_19(bytes) = SOLIDITY_CALL code(address)(target_1)
                        REF_5 -> LENGTH TMP_19
                        TMP_20(bool) = REF_5 == 0
                        TMP_21(bool) = TMP_18 && TMP_20
                        CONDITION TMP_21
                Expression: revert AddressEmptyCode(address)(target)
                IRs:
                        TMP_22(None) = SOLIDITY_CALL revert AddressEmptyCode(address)(target_1)
                Expression: returndata
                IRs:
                        RETURN returndata_1
        Function Address.verifyCallResult(bool,bytes)
                Expression: ! success
                IRs:
                        TMP_23 = UnaryType.BANG success_1 
                        CONDITION TMP_23
                Expression: _revert(returndata)
                IRs:
                        INTERNAL_CALL, Address._revert(bytes)(returndata_1)
                Expression: returndata
                IRs:
                        RETURN returndata_1
        Function Address._revert(bytes)
                IRs:
                        returndata_1(bytes) := ϕ(['returndata_1', 'returndata_1'])
                Expression: returndata.length > 0
                IRs:
                        REF_6 -> LENGTH returndata_1
                        TMP_25(bool) = REF_6 > 0
                        CONDITION TMP_25
                Expression: returndata_size__revert_asm_0 = mload(uint256)(returndata)
                IRs:
                        TMP_26(uint256) = SOLIDITY_CALL mload(uint256)(returndata_1)
                        returndata_size__revert_asm_0_1(uint256) := TMP_26(uint256)
                Expression: revert(uint256,uint256)(32 + returndata,returndata_size__revert_asm_0)
                IRs:
                        TMP_27(uint256) = 32 + returndata_1
                        TMP_28(None) = SOLIDITY_CALL revert(uint256,uint256)(TMP_27,returndata_size__revert_asm_0_1)
                Expression: revert FailedInnerCall()()
                IRs:
                        TMP_29(None) = SOLIDITY_CALL revert FailedInnerCall()()
Contract InsecureEtherVault
        Function InsecureEtherVault.deposit()
                IRs:
                        balanceOf_1(mapping(address => uint256)) := ϕ(['balanceOf_4', 'balanceOf_2', 'balanceOf_0'])
                Expression: balanceOf[msg.sender] += msg.value
                IRs:
                        REF_7(uint256) -> balanceOf_1[msg.sender]
                        balanceOf_2(mapping(address => uint256)) := ϕ(['balanceOf_1'])
                        REF_7(-> balanceOf_2) = REF_7 (c)+ msg.value
        Function InsecureEtherVault.withdraw()
                IRs:
                        balanceOf_3(mapping(address => uint256)) := ϕ(['balanceOf_4', 'balanceOf_2', 'balanceOf_0'])
                Expression: zero = 0
                IRs:
                        zero_1(uint256) := 0(uint256)
                Expression: extra = 55 / zero
                IRs:
                        TMP_30(uint256) = 55 (c)/ zero_1
                        extra_1(uint256) := TMP_30(uint256)
                Expression: require(bool,string)(balanceOf[msg.sender] > 0,Nothing to withdraw)
                IRs:
                        REF_8(uint256) -> balanceOf_3[msg.sender]
                        TMP_31(bool) = REF_8 > 0
                        TMP_32(None) = SOLIDITY_CALL require(bool,string)(TMP_31,Nothing to withdraw)
                Expression: address(msg.sender).sendValue(balanceOf[msg.sender])
                IRs:
                        TMP_33 = CONVERT msg.sender to address
                        REF_10(uint256) -> balanceOf_3[msg.sender]
                        LIBRARY_CALL, dest:Address, function:Address.sendValue(address,uint256), arguments:['TMP_33', 'REF_10'] 
                Expression: balanceOf[msg.sender] = 0
                IRs:
                        REF_11(uint256) -> balanceOf_3[msg.sender]
                        balanceOf_4(mapping(address => uint256)) := ϕ(['balanceOf_3'])
                        REF_11(uint256) (->balanceOf_4) := 0(uint256)

INFO:Slither:slither-testsuite-mesaurement/examples/reentrancy-3/vulnerable/ analyzed (2 contracts)