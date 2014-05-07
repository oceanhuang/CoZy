import fileinput
import sys
sys.path.append("..")

import cozyLex, cozyYacc, codeGenerator

class CoZyTester:
    def __init__(self):
        # Build the parser
        self.parser = cozyYacc.CoZyParser()

    def run_code(self, code_str, output, debug=False):
        result = self.parser.parse(code_str)
        code = codeGenerator.codeGenerator(result).ret
        
        print code
        exec code in locals()
        
        if output != "None":
            result = locals()['ret']
            if type(result) is int: result = str(result)
            if type(result) is list: output = eval(output)
            assert result == output



prog = ''
arg = ''
getArg = False
#ret = ''
#ignores all lines starting with #
for line in sys.stdin.readlines():
    if getArg is False:
        ret = line
        getArg = True
    else:
        prog += line

myTester = CoZyTester()

ret = ret[1:].rstrip('\n')
myTester.run_code(prog, ret)


