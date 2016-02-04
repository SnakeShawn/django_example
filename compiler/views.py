import logging, json

from django.shortcuts import render
from django.http import HttpResponse

from quackCompiler.invokeCompile import invoke, getParamList, saveToFile, readResult

# Create your views here.

#Get an instance of a logger
logger = logging.getLogger(__name__)

def index(request):
    return render(request, 'compiler/index.html')

def compile(request):
    response=HttpResponse()
    response['Content-Type']="text/javascript"
    # Get the Post
    modelScript =  request.POST['script']
    modelName =  request.POST['modelName']
    paramCount =  request.POST['paramCount']
    modelName = modelName.replace(' ','')
    modelName = modelName.lower()
    paramCount = int(paramCount)            # Convert the count from string to int
    content = modelScript
    paramList = ''
    if paramCount > 0:
        jsonContent = request.POST['jsonContent']
        paramList = getParamList(jsonContent)
        for (k,v) in paramList.items():
            content = str(modelScript).replace("<%"+k+"%>", v)
        logger.error(paramList)

    logger.error(content)
    logger.error("Param count is:"+str(paramCount))

    outputpath = '/Users/xuzhang/Documents/TOOLS/PYTHON/Django/django_example/data/model/'    # Model's path and the compiler's input

    saveToFile(modelName, modelScript, paramCount, paramList, outputpath)

    outpath = '/Users/xuzhang/Documents/TOOLS/PYTHON/Django/django_example/data/result/'     # The result's saving path.
    # invoke the compiler
    inpath = outputpath+modelName+'.json'   # Compiler's infile.
    invoke(inpath, outpath)     # Invoke the compiler.
    count, resultlist = readResult(outpath)         # Read the result from file.

    result.count = count
    result.resultlist = resultlist

    return HttpResponse(json.dumps({"resultcount":count,"resultlist":resultlist}))

def result(request):
    return render(request, 'compiler/result.html')

