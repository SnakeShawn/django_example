from ..import glb
from ..module.config import *
from ..utils import parser as parser
from ..utils.executor import execute, evaluate

#module_type
functionType = (functionmodule,)
loopType = (whilemodule, formodule,)
branchType = (ifelsemodule,)


def recursive(content, index, module):
    
    if module.end_recursive:
        return
    else:
        if index < len(content):
            glb.current_line = module.line + index
            if not content[index].split("#")[0] or content[index].split("#")[0].isspace():
                index += 1
            else:
                grammar_type, tokenList, exeToken, param_list = parser.parse(content[index])
                if grammar_type == 'function_def':
                    # case 1: function definition
                    lineCount = get_block_count(content, index)
                    module_content = content[index+1:index+lineCount+1]
                    func_name = param_list[0]
                    func_param_list = param_list[1]
                    glb.current_line += 1
                    funcModule = functionmodule(func_name, func_param_list, module_content, glb.current_line)
                    module._func_inc(func_name, funcModule)
                    index += (lineCount + 1)
                elif grammar_type == 'expression':
                    # case 2: expression
                    from .consoleManager import stdoutIO

                    with stdoutIO() as s:
                        execute(exeToken)
                    consoleOutput = s.getvalue()
                    if consoleOutput:
                        glb.console_output.append(consoleOutput)
                    index += 1
                elif grammar_type == 'statement':   #continue, break, return
                    if tokenList[0][1] == 'return':
                        try:
                            for item in reversed(glb.variable_stack):
                                if isinstance(item, functionmodule):
                                    item.return_list = evaluate(exeToken)
                                    break
                        except AttributeError:
                            raise Exception("SyntaxError: return statement must be used inside function.")
                        for item in reversed(glb.variable_stack):
                            if isinstance(item, functionmodule):
                                break
                            elif isinstance(item, basemodule):
                                item.setEnd()
                        return
                    
                    elif tokenList[0][1] == 'break' or tokenList[0][1] == 'continue':
                        for item in reversed(glb.variable_stack):
                            if isinstance(item, functionmodule):
                                raise Exception("break/countinue can only be used in while or for loops")
                            if isinstance(item, basemodule):
                                if not isinstance(item, loopType):
                                    item.setEnd()
                                else:
                                    item.setEnd()
                                    if tokenList[0][1] == 'continue':
                                        item.setContinue()
                                    break
                        return
                    else :  # if, while, for statement
                        lineCount = get_block_count(content, index)
                        module_content = content[index+1:index+lineCount+1]
                        if tokenList[0][1] == 'if':
                            conditionList = [param_list[0]]
                            contentList = [module_content]

                            index += (lineCount+1)
                            if index < len(content):
                                grammar_type, tokenList, exeToken, param_list = parser.parse(content[index])
                                while len(tokenList) > 0 and tokenList[0][1] == 'else':
                                    lineCount = get_block_count(content, index)
                                    contentList.append(content[index+1:index+lineCount+1])
                                    index += (lineCount+1)
                                    conditionList.append(param_list[0])

                                    if index >= len(content):
                                        break
                                    grammar_type, tokenList, exeToken, param_list = parser.parse(content[index])
                            ifModule = ifelsemodule(conditionList, contentList, glb.current_line)
                            ifModule.run()
                        elif tokenList[0][1] == 'for':
                            forModule = formodule(param_list, module_content, glb.current_line)
                            forModule.run()
                            index += (lineCount+1)
                        elif tokenList[0][1] == 'while':
                            whileModule = whilemodule(param_list[0], module_content, glb.current_line)
                            whileModule.run()
                            index += (lineCount+1)
                        else:
                            raise Exception("Unsupported keyworkd: {} in statement\"{}\"".format(tokenList[0][1], content[index]))
                        
            recursive(content, index, module)


def get_block_count(content, index):
    
    startSpace = len(content[index]) - len(content[index].lstrip())

    curIndex = index + 1
    while curIndex < len(content):
        if not content[curIndex].split('#')[0] or content[curIndex].split('#')[0].isspace():
            curIndex += 1
        else:
            curSpace = len(content[curIndex]) - len(content[curIndex].lstrip())
            if curSpace <= startSpace:
                curIndex -= 1
                break
            else:
                curIndex += 1
    return curIndex - index
