import fileinput
import sys
import re
import getopt

import cozyLex, cozyYacc, codeGenerator

class CoZyTester:
    def __init__(self):
        # Build the parser
        self.parser = cozyYacc.CoZyParser()

    def run_code(self, code_str):
        result = self.parser.parse(code_str)
        code = codeGenerator.codeGenerator(result).ret
        # print code
        exec code in locals()

def main(argv):
    inputfile = ''
    try:
      opts, args = getopt.getopt(argv,"hi:",["ifile="])
    except getopt.GetoptError:
      print 'test.py -i <inputfile>'
      sys.exit(2)

    for opt, arg in opts:
      if opt == '-h':
         print 'test.py -i <inputfile>'
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg

    try: 
        cfile = open(inputfile)
        prog = cfile.read()
        myTester = CoZyTester()
        myTester.run_code(prog)
    except IOError as e:
        print "{1}".format(e.strerror)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print 'test.py -i <inputfile>'
    else:
        main(sys.argv[1:])
