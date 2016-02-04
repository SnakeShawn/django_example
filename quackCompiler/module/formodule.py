from .. import glb

from ..module.basemodule import basemodule
from ..utils.variable import variable

class formodule(basemodule):

    __name__ = 'ForModule'

    def __init__(self, param, content, line):
        self.content = content
        self.iter_var = param[0]
        self.loop_range = param[1]
        self.range_var_name = param[2]
        self.end_recursive = False
        self.continue_flag = False
        self.line = line
    
    def setContinue(self):
        self.continue_flag = True
    def resetContinue(self):
        self.continue_flag = False

    def run(self):
        from ..utils.recursive import recursive
        from ..utils.executor import containVariableInGlbStack, getVariableFromGlbStack

        glb.variable_stack.append(self)

        iterVarObj = variable(self.iter_var, None)
        glb.variable_stack.append([self.iter_var, iterVarObj])
        setPointer = False

        var_being_iter = getVariableFromGlbStack(self.range_var_name)

        if self.range_var_name and containVariableInGlbStack(self.range_var_name):
            setPointer = True
        self.line = glb.current_line + 1

        for index, value in enumerate(self.loop_range):
            if self.end_recursive:
                break
            iterVarObj.var_obj = value
            iterVarObj.var_flag = glb.flag_dict['changed']
            if setPointer:
                iterVarObj.pointerIndexList = [index]
                iterVarObj.pointer = getVariableFromGlbStack(self.range_var_name).var_name
            if var_being_iter:
                var_being_iter.indexList = [index]

            recursive(self.content, 0, self)

            if self.continue_flag:
                self.resetEnd()
                self.resetContinue()

        self._end_module()
