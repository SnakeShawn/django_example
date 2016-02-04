
from .. import glb

from ..module.basemodule import basemodule

class ifelsemodule(basemodule):

    __name__ = 'IfElseModule'

    def __init__(self, conditionList, contentList, line):
        assert(len(conditionList) == len(contentList))

        self.conditionList = conditionList
        self.contentList = contentList
        self._judge = False
        self.end_recursive = False
        self.line = line

    def run(self):
        from itertools import zip_longest
        from ..utils.executor import evaluate
        from ..utils.recursive import recursive

        glb.variable_stack.append(self)
        
        for condition, content in zip_longest(self.conditionList, self.contentList):
            self._judge = evaluate(condition)

            if self._judge:
                self.line = glb.current_line + 1
                recursive(content, 0, self)
                break
            else:
                glb.current_line += len(content) + 1
        self._end_module()

