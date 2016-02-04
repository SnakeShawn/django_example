
from .. import glb

VARRANGE = range(0, 3)
STATEMENTRANGE = range(3, 12)

keywords = {'if':        3,
            'else':     4,
            'for':      5,
            'while':    6,
            'break':    7,
            'continue': 8,
            'return':   9,
            'repeat':   10,
            'until':    11,

            'function': 12,
            'is':       13,
            'in':       14,
            'or':       15,
            'and':      16,
            'not':      17,
            'to':       18,
            'step':     19,
            }
opts = {'+':        41,
        '-':        42,
        '*':        43,
        '/':        44,
        '<':        45,
        '<=':       46,
        '>':        47,
        '>=':       48,
        '<>':       49,
        '!=':       50,
        '=':        51,
        '==':       52,
        ';':        53,
        '(':        54,
        ')':        55,
        '&':        56,
        '&&':       57,
        '|':        58,
        '||':       59,
        '^':        60,
        '%':        61,
        '>>':       62,
        '<<':       63,
        ',':        64,
        '//':       65,
        '[':        66,
        ']':        67,
        '+=':       68,
        '-=':       69,
        '->':       70,
        '++':       71,
        '--':       72,
        '^':        73,
        '.':        74,
        '{':        75,
        '}':        76,
        ':':        77,
        }

def lexical_analyze(sentence):

    token = ''
    tokenList = []

    sentence = sentence.split('#')[0]

    sentence = sentence.replace('->', '=')
    while "+=" in sentence or "-=" in sentence or "++" in sentence or "--" in sentence:
        if "+=" in sentence:
            splitList = sentence.split("+=")
            sentence = splitList[0] + "=" + splitList[0] + "+" + splitList[1]
        elif "-=" in sentence:
            splitList = sentence.split("-=")
            sentence = splitList[0] + "=" + splitList[0] + "-" + splitList[1]
        #Assume "++" and "--" only appear at the end of expression
        elif "++" in sentence:
            splitList = sentence.split("++")
            sentence = splitList[0] + "=" + splitList[0] + "+ 1"
        elif "--" in sentence:
            splitList = sentence.split("--")
            sentence = splitList[0] + "=" + splitList[0] + "- 1"
    index = 0

    while index < len(sentence):
        ch = sentence[index]    #character
        if ch.isspace():
            index += 1
            continue
        if ch.isalpha():
            while (ch.isalpha() or ch.isdigit() or ch == '_') and index < len(sentence):
                token += ch
                index += 1
                if index < len(sentence):
                    ch = sentence[index]
            # skip the spaces
            while ch.isspace() and index < len(sentence):
                index += 1
                if index < len(sentence):
                    ch = sentence[index]
            
            if token in keywords:
                tokenList.append((keywords.get(token), token))
            else:
                #token is function name
                if ch == '(':
                    tokenList.append((1, token))
                # toke is data structure class in glb.function_list
                elif token in glb.function_map:
                    tokenList.append((1, token))
                # token is variable name or other things
                else:
                    tokenList.append((0, token))
            index -= 1
        elif ch.isdigit():
            while (ch.isdigit() or ch == '.') and index < len(sentence):
                token += ch 
                index += 1
                if index < len(sentence):
                    ch = sentence[index]
            index -= 1
            tokenList.append((2, token))
        # if character is singel quote
        elif ch == '\'':
            token += ch
            index += 1
            ch = sentence[index]
            while ch != '\'' and index < len(sentence):
                token += ch
                index += 1
                if index < len(sentence):
                    ch = sentence[index]
            token += ch
            tokenList.append((2, token))
        elif ch == '\"':
            token += ch
            index += 1
            ch = sentence[index]
            while ch != '\"' and index < len(sentence):
                token += ch
                index += 1
                if index < len(sentence):
                    ch = sentence[index]
            token += ch
            tokenList.append((2, token))
        #operators
        else:
            token += ch
            if ch == '<':
                index += 1
                if index < len(sentence):
                    ch = sentence[index]
                    #<=, <>, <<
                    if ch in ('=','>','<'):
                        token += ch
                    else:
                        index -= 1
            elif ch == '>':
                index += 1
                if index < len(sentence):
                    ch = sentence[index]
                    #>=, >>
                    if ch in ('=', '>'):
                        token += ch
                    else:
                        index -= 1
            elif ch == '!':
                index += 1
                if index < len(sentence):
                    ch = sentence[index]
                    if ch == '=':
                        token += ch
                    else:
                        index -= 1
            elif ch == '=':
                index += 1
                if index < len(sentence):
                    ch = sentence[index]
                    if ch == '=':
                        token += ch
                    else:
                        index -= 1
            elif ch == '&':
                index += 1
                if index < len(sentence):
                    ch = sentence[index]
                    # "&&":
                    if ch == '&':
                        token += ch
                    else:
                        index -= 1
            elif ch == '|':
                index += 1
                if index < len(sentence):
                    ch = sentence[index]
                    if ch == '|':
                        token += ch
                    else:
                        index -= 1
            elif ch == '+':
                index += 1
                if index < len(sentence):
                    ch = sentence[index]
                    if ch in ('=', '+'):
                        token += ch
                    else:
                        index -= 1
            elif ch == '-':
                index += 1
                if index < len(sentence):
                    ch = sentence[index]
                    if ch in ('=', '-', '>'):
                        token += ch
                    else:
                        index -= 1
            elif ch == "/":
                index += 1
                if index < len(sentence):
                    ch = sentence[index]
                    if ch in ('/',):
                        token += ch
                    else:
                        index -= 1
            if token in opts:
                tokenList.append((opts.get(token), token))
            else:
                raise Exception("Invalid operator \"" + str(token) +"\" in statement:" + sentence)
        index += 1
        token = ''
    return tuple(tokenList)

def parse(sentence):
    grammar_type = ''
    exeToken = ''
    param_list = []
    
    tokens = lexical_analyze(sentence)
    
    if tokens:
        if tokens[0][1] == 'function':
            # case 1: function definition. E.g. function inser(param)
            grammar_type = 'function_def'

            function_name, function_param = function_analyze(tokens[1:])
            param_list = [function_name, function_param]
        elif tokens[0][0] == 1:
            if tokens[1][0] == 0:
                # case 2: variable definition. E.g. Stack s = [1,2]
                grammar_type = 'expression'
                var_type = tokens[0][1]
                var_name = tokens[1][1]
                param_list = [var_name]
                exeToken = var_name + '=' + var_type

                if len(tokens) == 2:
                    exeToken += '()'
                else:
                    if tokens[2][1] == '=':
                        exeToken += '('
                        for indx in range(3, len(tokens)):
                            exeToken += tokens[indx][1] + ' '
                        exeToken += ')'
            else:
                # case 3: expression
                grammar_type = 'expression'
                # leave param_list empty
                for token in tokens:
                    exeToken += token[1] + ' '  # to remove unnecessary space
        elif tokens[0][0] in STATEMENTRANGE:
           # case 4: statement
           grammar_type = 'statement'
           try:
               if tokens[0][1] == 'for':
                   var_name = tokens[1][1]
                   loop_range = None    #[iter_list]
                   range_var_name = ""

                   from .executor import evaluate
                   # first type
                   if tokens[2][1] == 'in':
                       range_exp = ''.join([token[1] for token in tokens[3:]])
                       loop_range = evaluate(range_exp)
                       range_var_name = range_exp
                   # second type
                   elif tokens[2][1] == '=':
                       
                       exp_index = 3
                       start_exp = ''
                       while exp_index < len(tokens) and tokens[exp_index][1] != 'to':
                           start_exp += tokens[exp_index][1] + ' '
                           exp_index += 1
                       startPos = evaluate(start_exp)
                       exp_index += 1

                       end_exp = ''
                       while exp_index < len(tokens) and tokens[exp_index][1] != 'step':
                           end_exp += tokens[exp_index][1] + ' '
                           exp_index += 1
                       endPos = evaluate(end_exp)

                       exp_index += 1
                       step = 1
                       if exp_index < len(tokens):
                           step_exp = ''
                           while exp_index < len(tokens):
                               step_exp += tokens[exp_index][1] + ' '
                               exp_index += 1
                           step = evaluate(step_exp)
                       loopr_range = range(startPos, endPos, step)
                   else:
                       raise Exception("Invalid for loop syntax:"+ sentence)
                   param_list = [var_name, loop_range, range_var_name]

               else:
                    if tokens[0][0] in STATEMENTRANGE:
                        for token in tokens[1:]:
                            if token[0] in STATEMENTRANGE:
                                continue
                            exeToken += token[1] + ' '
                        if exeToken == '':
                            exeToken = 'True'
                        param_list = [exeToken]
                    else:
                        raise Exception("Invalid syntax find in parser step: " + sentence)
           except Exception:
               raise
        # all other situations?!
        else:
            grammar_type = 'expression'
            for token in tokens:
                exeToken += token[1] + ' '
    return grammar_type, tokens, exeToken, param_list

def function_analyze(tokenList):

    if len(tokenList) < 3 or tokenList[1][1] != '(' or tokenList[-1][1] != ')':
        raise Exception("Invalid function definition:" + str(tokenList))
    function_name = tokenList[0][1].strip()
    param_list = []

    for token in tokenList[2:-1]:
        if token[1] != ',':
            param_list.append(token[1])
    param_list = list(map(str.strip, param_list))

    return function_name, tuple(param_list)
