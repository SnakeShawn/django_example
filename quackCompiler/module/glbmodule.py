from .. import glb
from ..module.basemodule import basemodule

class glbmodule(basemodule):
    
    __name__ = 'GlobalModule'
    
    def __init__(self, content, line):
        self.content = content 
        self.line = line
        self.end_recursive = False

    def run(self):
        from ..utils import recursive as recursive
#        import utils.recursive as recursive

        glb.variable_stack.append(self)

        recursive.recursive(self.content, 0, self)

        self._end_module()

