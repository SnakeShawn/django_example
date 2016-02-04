from .. import glb
from ..module.config import *


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
