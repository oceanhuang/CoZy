'''
Run this test by going to the top directory of this project and running:

python -m test.testCoZy

To add new CoZy codes, just follow the examples below.

CoZyTester does the following:
__init__:
    initializes a parser

run_code:    
    run_code takes two inputs: 
        1. the string of CoZy code
        2. your expected output of a variable called 'ret', could also be 'None'

    it prints the resulted python code
    
    if an expected output is supplied:
        asserts the variable 'ret' with the expected output (be careful about types here!)
    else:
        prints the variable 'ret'
'''
import sys
sys.path.append("..")

import cozyLex, cozyYacc, codeGenerator

class CoZyTester:
    def __init__(self):
        # Build the parser
        self.parser = cozyYacc.CoZyParser()


    def run_code(self, code_str, output):
        result = self.parser.parse(code_str)
        code = codeGenerator.codeGenerator(result).ret
        print code
        # print locals()
        exec code in locals()
        if output == None: print locals()['ret']
        else: assert locals()['ret'] == output

myTester = CoZyTester()

# test expressions:
s = '''
ret=3+3
'''
myTester.run_code(s, 6)

s = '''
ret = 'hello ' + "world"
'''
myTester.run_code(s, 'hello world')

s = '''
ret = Tuesday
'''
myTester.run_code(s, None)

# testing while loop:
s = '''
z = 4
while (z > 2):
    z = z-1
    k = 5
    if (k == 5):
        k = k+1
        k = k-1
    else:
        k = k-1
        k = k+1
ret = z    
'''
myTester.run_code(s, 2)

# test if:
s= '''
z = 4
if (z > 5):
    print("z > 5")

else:
    ret = z
'''
myTester.run_code(s, 4)

# test for:
s= '''
x = 0
for i in 1 to 30:
    x = i
    x = i + 1
ret = x
'''
myTester.run_code(s, 31)