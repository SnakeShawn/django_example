from .. import glb
from ..module.basemodule import basemodule
from ..utils.parser import lexical_analyze, opts, VARRANGE
from ..utils.variable import variable

equalToken = (opts['='], '=')
dotToken = (opts['.'], '.')

def execute(statement):
    tokenList = lexical_analyze(statement)
    
    if equalToken in tokenList:
        indexOfEqual = tokenList.index(equalToken)
        leftOpTokens = tokenList[:indexOfEqual]
        rightOpTokens = tokenList[indexOfEqual+1:]
        
        rightOpStr = ''
        for token in rightOpTokens:
            rightOpStr += token[1] + ' '

        leftObjectName = leftOpTokens[0][1]

        if not containVariableInGlbStack(leftObjectName):
            if len(leftOpTokens) > 1:
                raise Exception("\"" + leftObjectName + "\" is undefined in statement: " + statement)
            else:
                rightOpValue = evaluate(rightOpStr)
                variableObj = variable(leftObjectName, rightOpValue)
                glb.variable_stack.append([leftObjectName, variableObj])

        else:
            variableInstance = getVariableFromGlbStack(leftObjectName)
            rightOpValue = evaluate(rightOpStr)
            variableInstance.var_flag = glb.flag_dict['changed']
            if len(leftOpTokens) == 1:
                variableInstance.var_obj = rightOpValue
            else:
                leftOpObject = variableInstance.var_obj
                storeVisitedIndex(leftOpTokens)

                index = 0
                splitIndex = 0

                while index < len(leftOpTokens):
                    if leftOpTokens[index][1] == '.' or leftOpTokens[index][1] == '[':
                        splitIndex = index
                    index += 1
                index = 1
                exp = ''
                token = ''
                currentObject = leftOpObject

                while index < len(leftOpTokens):
                    token = leftOpTokens[index][1]
                    if token == '.':
                       index += 1
                       token = leftOpTokens[index][1]
                       if token not in dir(currentObject):
                           raise Exception("AttributeError: \"" + leftObjectName + "\" object has no attribute\""+token+"\"")
                       else:
                           if index > splitIndex:
                               setattr(currentObject, token, rightOpValue)
                           else:
                               currentObject = getattr(currentObject, token)
                    elif token == '(':
                        bracket_stack = []
                        bracket_stack.append(token)
                        isMultipleParam = False

                        while index < len(leftOpTokens) -1 and bracket_stack:
                            index += 1
                            token = leftOpTokens[index][1]

                            if token == ',' and len(bracket_stack) == 1:
                                isMultipleParam = True
                            if token == '(':
                                bracket_stack.append(token)
                            elif token == ')':
                                bracket_stack.pop()
                            if bracket_stack:
                                exp += token
                        paramResult = evaluate(exp)

                        if isMultipleParam:
                            currentObject = currentObject(*paramResult)
                        else:
                            currentObject = currentObject(paramResult)
                    elif token == '[':
                        bracket_stack = []
                        bracket_stack.append(token)
                        while index < len(leftOpTokens)-1 and bracket_stack:
                            index += 1
                            token - leftOpTokens[index][1]
                            if token == '[':
                                bracket_stack.append(token)
                            elif token == ']':
                                bracket_stack.pop()
                            if bracket_stack:
                                exp += token
                        paramResult = evaluate(exp)
                        if index >= splitIndex:
                            currentObject[paramResult] = rightOpValue
                        else:
                            currentObject = currentObject[paramResult]
                    else:
                        raise Exception("Incalid syntax at "+token +" in statement" + statement)
                    token = ''
                    exp =''
                    index += 1
        storePointer(leftOpTokens, rightOpTokens)
    else:
        evaluate(statement)
def evaluate(expression):
    tokenList = lexical_analyze(expression)

    index = 0
    token = ''
    modifiedExp = ''

    bracket_stack = []

    while index < len(tokenList):
        token = tokenList[index][1]

        if token == '[' and (index == 0 or (index >0 and tokenList[index -1][0] not in VARRANGE and tokenList[index-1][1] not in [']',')'])):
            modifiedExp += "Array(["
        elif token == '[':
            modifiedExp += token
            bracket_stack.append('[')
        elif token == ']':
            if bracket_stack:
                bracket_stack.pop()
                modifiedExp += token
            else:
                modifiedExp += "])"
        elif token == '{':
            modifiedExp += "Dict({"
        elif token == '}':
            modifiedExp += "})"
        else:
            modifiedExp += token

        modifiedExp += ' '
        index += 1

    expression = modifiedExp

    from ..module.basemodule import basemodule
    varDict = {}
    for variablePair in glb.variable_stack:
        if not isinstance(variablePair, basemodule):
            varDict[variablePair[0]] = variablePair[1].var_obj
    result = eval(expression, glb.function_map, varDict)
    return result

def containVariableInGlbStack(var_name):

    from ..module.basemodule import basemodule

    for variablePair in reversed(glb.variable_stack):
        if not isinstance(variablePair, basemodule) and var_name == variablePair[0]:
            return True
    return False

def getVariableFromGlbStack(var_name):

    from ..module.basemodule import basemodule
    
    for variablePair in reversed(glb.variable_stack):
        if not isinstance(variablePair, basemodule) and var_name == variablePair[0]:
            return variablePair[1]
    return None

def getMatchingObject(obj):
    '''
    Find matching object from global variable stack. Start from bottom of stack.
    a <- b <- c, we want to find c -> a, so start from the bottom of stack
    :param obj:
    :return: return object of type "variable" if found, return None otherwise.
    '''
    from ..module.basemodule import basemodule

    for variablePair in glb.variable_stack:
        if not isinstance(variablePair, basemodule) and obj is variablePair[1].var_obj:
            return variablePair[1]
    return None

def storeVisitedIndex(tokens):
    firstDotIndex = len(tokens)
    if dotToken in tokens:
        firstDotIndex = tokens.index(dotToken)
    objectName = tokens[0][1]
    variableInstance = getVariableFromGlbStack(objectName)
    
    if variableInstance is None:
        raise Exception("\"" + objectName + "\" is undefined in statement: " + str(tokens))
    indexList = []
    bracketStack = []
    token = ''
    ch = ''
    i = 1
    while i < firstDotIndex:
        ch = tokens[i][1]
        if ch == '[':
            bracketStack.append(ch)
            while bracketStack and i < firstDotIndex-1:
                i += 1
                ch = tokens[i][1]
                if ch == '[':
                    bracketStack.append(ch)
                elif ch == ']':
                    bracketStack.pop()
                if bracketStack:
                    token += ch + ''
            indexList.append(evaluate(token))
        else:
            raise Exception("Brackets not closed in statement: " + str(tokens))
        token = ''
        i += 1
    variableInstance.indexList = indexList

def storePointer(leftOpTokens, rightOpTokens):
    from ..module.basemodule import basemodule
    if len(leftOpTokens) != 1:
        return
    leftVar = getVariableFromGlbStack(leftOpTokens[0][1])

    if leftVar is None or isPrimitiveType(leftVar.var_obj):
        return
    for variablePair in glb.variable_stack:
        if not isinstance(variablePair, basemodule):
            varInstance = variablePair[1]

            if varInstance.var_obj is leftVar.var_obj:
                if varInstance.var_name != leftVar.var_name:
                    leftVar.pointer = varInstance.var_name
                    break
            elif isinstance(varInstance.var_obj, list) or isinstance(varInstance.var_obj, dict):
                isFound, indexList = findMatchingObjInVar(leftVar.var_obj, varInstance.var_obj)
                if isFound:
                    leftVar.pointer = varInstance.var_name
                    leftVar.pointerIndexList = indexList
                    break
def findMatchingObjInVar(obj, targetObj, indexList=[]):
    if obj is targetObj:
        return True, indexList
    if isinstance(targetObj, list):
        for index, element in enumerate(targetObj):
            indexList.append(index)
            isFound, returnList = findMatchingObjInVar(obj, element, indexList)
            if not isFound:
                indexList.pop()
            else:
                return True, indexList
    elif isinstance(targetObj, dict):
        for key in targetObj:
            indexList.append(key)
            isFound, returnList = findMatchingObjInVar(obj, targetObj[key], indexList)
            if not isFound:
                indexList.pop()
            else:
                return True, indexList
    return False, indexList

def isPrimitiveType(var):

    primitive = (int, float, str, bool)
    return type(var) in primitive or var == None

def resetFlagInStack():
        '''
        Reset all the modification flags in variable stack
        '''
        for item in glb.variable_stack:
            if not isinstance(item, basemodule):
                variableObj = item[1]
                variableObj.var_flag = glb.flag_dict['unchanged']
            if 'resetFlags' in dir(variableObj.var_obj):
                variableObj.var_obj.resetFlags()
