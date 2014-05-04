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
        self.testCount = 0

    def run_code(self, code_str, output, debug=False):
        result = self.parser.parse(code_str)
        code = codeGenerator.codeGenerator(result).ret
        self.testCount += 1
        print "-------TEST NUMBER : " + `self.testCount` + " --------- "
        
        if debug: print code
        #print locals()
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
a = [2,1,3+5, [5,4]]
a[0] = 153
add(a[3], 14)
remove(a, 1)
sort(a[2])
ret = a
'''
myTester.run_code(s, [153,8,[4,5,14]])

s = '''
ret = Tuesday
'''
myTester.run_code(s, None)

#testing checking date
s = '''
if(Friday):
    print("Hooray!")
ret = 5
'''
myTester.run_code(s, 5)

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
s= '''
z = 4
if (z > 5):
    a = 3
else:
    ret = z
'''
myTester.run_code(s, 4)

# test for:
s= '''
x = 0
i = 0
for i in 1 to 30:
    x = i
    x = i + 1
ret = x
'''
myTester.run_code(s, 31)

#test for function def
s='''
def poop(x):
    x = 2+2
ret = 4
'''
myTester.run_code(s, 4)

# test every
s='''
print ('6')
ret = 5
every (Monday):
    print ('5')
'''
myTester.run_code(s, 5)

#test once every
s='''
print ('5')
ret = 5
once every (Monday):
    print ('5')
'''
myTester.run_code(s, 5)

#test during 1
s = '''
ret = 5
once every (April during Friday):
    print ("hello world")
'''
myTester.run_code(s, 5)

#test during 2
s = '''
ret = 5
once every (January during Monday, February during Friday):
    print ("hello world")
'''
myTester.run_code(s, 5)

#test during 3
s = '''
ret = 5
every ((January during Monday, February during Friday) during Wednesday):
    print ("hello world")
'''
myTester.run_code(s, 5)

# test datetime
s='''
ret = 21/7/1991 10:00 PM
ret = 2:00 PM
ret = 19/12/1991
'''
myTester.run_code(s, None)

# test temp
s='''
ret = 70 K
ret = 50 C
ret = 80 F
'''
myTester.run_code(s, None)

#test date
s='''
ret = 14/2/1991
'''
myTester.run_code(s, None)

#test log
s='''
ret = 5000
log(5000 + 70)
'''
myTester.run_code(s, 5000)

#test log 2
s='''
ret = 5000 
log(ret)
'''
myTester.run_code(s, 5000)

###test print DOESNT WORK
##s='''
##ret = 5000 F
##print(ret)
##'''
##myTester.run_code(s, 5000)

### test every -- THIS GUY DOESNT WORK BUT IT SHOULD
##s='''
##h = Monday
##every(h):
##    print("Hooray!")
##ret = 5
##'''
##myTester.run_code(s, 5)

# test temp
s='''
print("hello")
ret = 5
'''
myTester.run_code(s, 5)

#This code should work BUT IT DOESNT
s='''
a = 70 F
print (a)
ret = 5
'''
myTester.run_code(s, 5)

#This code should work BUT IT DOESNT
s='''
print(60 F)
ret = 5
'''
myTester.run_code(s, 5)

###This code should fail 
##s='''
##b = 15/9/1991
##c = 14/7/2011
##a = c * b
##'''
##myTester.run_code(s, None)

###this should fail
##s = '''
##b = Monday
##c = 70 F
##a = c + b * January
##'''
##myTester.run_code(s, None)

###this should fail 
##s = '''
##b = January
##c = 15/9/1991
##a = c + b
##'''
##myTester.run_code(s, None)

###this should fail
##s = '''
##b = Monday
##c = 70 F
##a = c + b
##'''
##myTester.run_code(s, None)

###this should fail
##s = '''
##b = 15/9/1991
##c = 70 F
##a = b + c
##'''
##myTester.run_code(s, None)

#this should fail and it does
s = '''
b = 15/9/1991
every(Monday + Tuesday during January):
    print("Hello!")
ret = 5
'''
myTester.run_code(s, 5)

#this should work but it doesnt
##s = '''
##b = 15/9/1991
##every(b):
##    print("Hello!")
##ret = 5
##'''
##myTester.run_code(s, 5)

#this should fail
s = '''
b = 15/9/1991
c = 14/7/2011
a = b + 70 F
'''
myTester.run_code(s, None)

#this should fail
s = '''
b = 15/9/1991
c = 14/7/2011
a = 15/9/1991 + 70 F
'''
myTester.run_code(s, None)

#this should fail
s = '''
b = 15/9/1991
c = 14/7/2011
a = 15/9/1991 * 14/7/2011
'''
myTester.run_code(s, None)

#This code should fail
s='''
a = January * February
'''
myTester.run_code(s, None)

#This code should fail
s='''
a = 60 F + 50F * Tuesday
'''
myTester.run_code(s, None)

#This code should fail
s='''
a = 60 F + 50F + 30F
d = 25/2/1991 10:00 PM
c = 10:00 AM
g = 1 < 3 + 4
r = 1 + 2 * 3+4
f = 1:00 PM
h = 1 < 3 and 4 > 3
z = r + 2
y = 7 * 80F
ret = 5
z = a + z
'''

myTester.run_code(s, None)


