from .. import glb

from ..module.basemodule import basemodule

class functionmodule(basemodule):
    
    __name__ = 'FunctionModule'

    def __init__(self, func_name, param_list, content, line):
        self.func_name = func_name
        self.param_list = param_list
        self.content = content
        self.end_recursive = False
        self.return_list = None
        self.line = line
    def __call__(self, *args, **kwargs):
        from ..utils.variable import variable
        from ..utils.executor import isPrimitiveType, getMatchingObject
        from ..utils.recursive import recursive

        glb.funcall_depth += 1

        glb.variable_stack.append(self)
        
        try:
            if len(args) + len(kwargs) != len(self.param_list):
                raise TypeError('{} positional arguments but {} given'
                        .format(len(self.paramList),len(args)+len(kwargs)))
            else:
                from itertools import zip_longest

                args = list(args) + list(kwargs.values())

                for param, arg in zip_longest(self.param_list, args):
                    paramVarObj = variable(param, arg)

                    if not isPrimitiveType(arg):
                        findObj = getMatchingObject(arg)
                        paramVarObj.pointer = findObj.var_name
                    glb.variable_stack.append([param, paramVarObj])

                recursive(self.content, 0, self)

                return self.return_list
        except Exception as e:
            raise Exception("Exception: \"{}\" occutted during execution of functon {}".format(e, self.func_name))
        finally:
            self._end_module()
            glb.funcall_depth -=1
