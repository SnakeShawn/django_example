import uuid
import quackCompiler.glb as glb


def printString(string):
    print("The result is:"+str(string))

    filepath = glb.output_path+str(uuid.uuid1())+'.txt'
    with open(filepath,'w') as f:
        try:
            f.write(str(string))
        finally:
            f.close()

    resultDict = {}
    resultDict['type'] = 'string'
    resultDict['value'] = filepath

    outputpath = glb.output_path
    outputpath = outputpath+'result.json'

    print(str(resultDict))
    with open(outputpath, 'a') as f:
        try:
            f.write(str(resultDict)+'\n')
        finally:
            f.close()

def display(string):
    resultDict = {}
    if type(string) == str:
        filepath = glb.output_path+str(uuid.uuid1())+'.txt'
        resultDict['type'] = 'string'
        store_string(string, filepath)
        resultDict['value'] = filepath
    else:
        resultDict['type'] = None


    outputpath = glb.output_path
    outputpath = outputpath+'result.json'

    print(str(resultDict))
    with open(outputpath, 'a') as f:
        try:
            f.write(str(resultDict)+'\n')
        finally:
            f.close()

def store_string(string, filepath):
    with open(filepath,'w') as f:
        try:
            f.write(str(string))
        finally:
            f.close()