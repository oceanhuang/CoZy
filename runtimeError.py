import inspect
numExtraLines = 2
#numExtraLines corresponds to the number of lines added in errorBeginning

class RuntimeError(object):
    def __init__(self):
        pass

def lineno():
    return inspect.currentframe().f_back.f_lineno

def getLineNumberFunction(startingSection):
    lineNumberFunction = """
def lineno():
    return sys.exc_info()[2].tb_lineno - {0}
"""
    numLines = startingSection.count('\n') + lineNumberFunction.count('\n')
    lineNumberFunction = lineNumberFunction.format(numLines + numExtraLines)
    print "NUM LINES", numLines
    return startingSection + lineNumberFunction
def errorBeginning(body):
    bodyLines = body.splitlines()
    bodyLines = ['    ' + x for x in bodyLines]
    #if toAddBeginning is changed, you have to change numExtraLines to its number of lines
    toAddBeginning = """
try:
"""
    middleStuff = toAddBeginning + '\n'.join(bodyLines)
    return middleStuff

def errorEnd():
    toAddEnd = """
except IndexError:
    sys.stderr.write("ERROR: Nothing lives at that index.\\n")
    sys.exit()
except TypeError:
    sys.stderr.write("ERROR: You seem to be using the wrong type for something.\\n")
    sys.exit()
except KeyboardInterrupt:
    sys.stderr.write("\\nThank you for using CoZy!\\n")
    sys.exit()
except:
    sys.stderr.write("ERROR: Hmmm...that's odd. I don't quite know what went wrong.\\n")
    sys.exit()
"""
    return toAddEnd


if __name__=="__main__":
    print "hello?"
    print lineno()
