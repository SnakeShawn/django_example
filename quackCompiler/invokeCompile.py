
import json, os
import logging

from quackCompiler.quack import quack

#Get an instance of a logger
logger = logging.getLogger(__name__)

def invoke(inputpath, outputpath):

    settingJson = getScriptFromPath(inputpath)
    settingJson = json.loads(settingJson)

    logger.error(settingJson['paramCount'])
    logger.error(settingJson['outputpath'])

    inputmodel = settingJson['outputpath']
    modelScript = getScriptFromPath(inputmodel)
    paramCount = int(settingJson['paramCount'])
    content = modelScript
    if paramCount > 0:
        logger.error(settingJson['parameters'])
        paramList = settingJson['parameters']
        for (k,v) in paramList.items():
            content = str(modelScript).replace("<%"+k+"%>", str("'"+v+"'"))

    logger.error(content)
    quack(content, outputpath)

def getParamList(jsonContent):
    jc = json.loads(str(jsonContent))
    return jc

def getScriptFromPath(inputpath):
    content = ''
    with open(inputpath, 'r') as f:
        try:
            content = f.read()
        finally:
            f.close()
    return content

def saveToFile(modelName, modelScript, paramCount, paramList = None, outputpath = None):
    '''
    Save the model to a .model file and the related information to .json
    :param modelName:
    :param modelScript:
    :param paramCount:
    :param paramList:
    :param outputpath:
    :return:
    '''
    if not outputpath:
        outputpath = '/Users/xuzhang/Documents/TOOLS/PYTHON/Django/django_example/quackCompiler/output/'
    outputmodel = outputpath+modelName+'.model'
    with open(outputmodel, 'w') as f:
        f.write(modelScript)
        f.close()

    outputdict = {};
    outputdict['paramCount'] = paramCount   # count of parameters
    outputdict['outputpath'] = outputmodel  # the model's script

    if paramCount > 0:
        outputdict['parameters'] = paramList
    logger.error(outputdict)

    outputsetting = outputpath+modelName+'.json'
    with open(outputsetting, 'w') as f:
        json.dump(outputdict,f)
        f.close()

def readResult(infilepath):
    result_file = infilepath+'result.json'
    if not os.path.exists(result_file):
        return 0,[]
    count = 0
    result_list = []
    with open(result_file, 'r') as f:
        for line in f:
            count += 1
            jsonline = eval(line)
            if 'type' in jsonline:
                if jsonline['type'] == 'string':
                    subresultpath = jsonline['value']
                    with open(subresultpath, 'r') as subf:
                        subresult = subf.readlines()
                        result_list.append(subresult)
                    print(jsonline['value'])
                elif jsonline['type'] == 'picture':
                    print(jsonline['value'])
                elif jsonline['type'] == 'pdf':
                    print(jsonline['value'])
                else:
                    pass
        f.close()
    return count,result_list

