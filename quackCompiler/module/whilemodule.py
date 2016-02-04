from .. import glb

from ..module.basemodule import basemodule

class whilemodule(basemodule):

    __name__ = 'WhileModule'

    def __init__(self, condition, content, line):
        self.content = content
        self.condition = condition
        self_judge = False
        self.end_recursive = False
        self.continue_flag = False
        self.line = line
    
    def setContinue(self):
        self.continue_flag = True
    def resetContinue(self):
        self.continue_flag = False

    def run(self):
        from ..utils.recursive import recursive
        from ..utils.executor import evaluate

        glb.variable_stack.append(self)

        self.judge = evaluate(self.condition)

        self.line = glb.current_line + 1

        while self._judge:
            if self.end_recursive:
                break
            recursive(self.content, 0, self)

            self._judge = evaluate(self.condition)
            if self.continue_flag:
                self.resetEnd()
                self.resetContinue()
        self._end_module()
