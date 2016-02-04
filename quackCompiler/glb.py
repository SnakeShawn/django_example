'''
Author: Zhang Xu
Date: 2016/01/19
Version: 1.0
Description: This file contains all the global variables which will be used in compiler.
'''
variable_stack = []         # form:[var_name, variable_obj]

function_map = {}           #store functions defined in code. {function name: function lambda}


current_line = 0            # line of current statement, start from 0
contents = []               # code split by line breaks

funcall_depth = 0           # current function call depth in function call tree

flag_dict = {
    "unchanged":    0,
    "new":          1,
    "changed":      2,
    "visited":      3,
}

output_path = ''            # The output path: users should specify the path.

result_output = []          # the result need to output.

console_output = []         # store the console output