
from .. import glb

class variable():

    def __init__(self, var_name, var_obj=None, var_flag=glb.flag_dict['new'], indexList=[], pointer=None, pointerIndexList=None):
        self.var_name = var_name
        self.var_obj = var_obj
        self.var_flag = var_flag
        self.indexList = indexList
        self.pointer = pointer
        self.pointerIndexList = pointerIndexList
    
    def __str__(self):

        ret = "[name: " + str(self.var_name) + ";" \
            + "value: " + str(self.var_obj) + ";" \
            + "type: " + type(self.var_obj) + ";" \
            + "var_flag: " + str(self.var_flag) + ";" \
            + "indexList: " + str(self.inexList) + ";" \
            + "pointer: " + str(self.pointer) + ";" \
            + "pointerIndexList: " + str(self.pointerIndexList) + "]"
        return ret

