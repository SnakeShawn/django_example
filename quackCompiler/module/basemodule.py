import sys

from .. import glb


class basemodule:
    __name__ = "BaseModule"

    def _func_inc(self, func_name, func_module):
        if func_name not in glb.function_map:
            glb.function_map[func_name] = \
                    lambda *args, **kwargs: func_module.__call__(*args, **kwargs)
        else:
            raise NameError('Function name \'{}\' already exist, conflict definition.'.format(func_name))
            sys.exit(1)
    def _end_module(self):
        item = glb.variable_stack.pop()
        while not isinstance(item, basemodule) and len(glb.variable_stack) > 0:
            item = glb.variable_stack.pop()
    def setEnd(self):
        self.end_recursive = True
    def resetEnd(self):
        self.end_recursive = False
    def run(self):
        '''
        Override this method in each derived module.
        '''
        pass
