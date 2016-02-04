'''
Author: Zhang Xu
Date: 2016/01/19
Version: 1.0
Description: Load the code and submit for compilation.
'''
import os
from . import glb
from .structure.config import *
from .module.glbmodule import glbmodule


def quack(content, outputpath):

    glb.contents = content.split('\n')

    glb.function_map.update(globals())
    glb.variable_stack.clear()
    file = outputpath+'result.json'
    if os.path.exists(file):
        os.remove(file)
    glb.output_path = outputpath
    init_module = glbmodule(glb.contents, line=0)

    try:
        init_module.run()
    except Exception as e:
        exception_path = outputpath + 'exception.txt'
        with open(exception_path, 'w') as f:
            f.write(str(e.args))
            f.close()

'''
    try:
        init_module.run()
    except Exception as e:
        print('ERROR!')
        message = 'ERROR!'
    else:
        message = 'SUCESS!'

    return message

'''
