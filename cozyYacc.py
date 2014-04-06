import ply.yacc as yacc
from compiler import ast, misc

# Get the token map from the lexer.  This is required.
from cozyLex import *
from codeGenerator import *

class Node(object):
    """ Node class. Used to build the AST. Each node has a type,
    children and a leaf. If it has a leaf it has *no* children.
    """
    # Function to initialize the node, needs type, the rest is
    # optional.
    def __init__(self, type, children=None, leaf=None):
        self.type = type
        if children:
            self.children = children
        else:
            self.children = [ ]
        self.leaf = leaf
    
    # Function to print out the tree.
    def __str__(self):
        return "\n" + self.traverse(1)
    # Function to traverse the tree and print it out.
    def traverse(self, i):
        temp = ""
        if self.leaf:
            temp = ": " + `self.leaf`
        s = self.type + temp + "\n"
        for children in self.children:
            if isinstance(children, Node):
                s += "-"*(i-1) + ">" + children.traverse(i+1)
            else:
                s += "-"*(i-1) + ">" + children
        return s

def p_program(p):
    """ program : external_declaration
                | program external_declaration
    """
    if len(p) == 2:
        p[0] = Node("program", [p[1]])
    else:
        p[0] = Node("program", [p[1], p[2]])

def p_external_declaration(p):
    """ external_declaration : function_definition
                             | statement
    """
    p[0] = Node("external_declaration", [p[1]])

# Needs to include parameter_list
def p_function_definition(p):
    'function_definition : DEF ID LPAREN RPAREN COLON NEWLINE INDENT statement_list DEDENT'

    p[0] = Node("function_definition", [p[2], p[8]]);

def p_statement_list(p):
    """ statement_list : statement
                       | statement_list statement
    """
    if len(p) == 2:
        p[0] = Node("statement_list", [p[1]])
    else:
        p[0] = Node("statement_list", [p[1], p[2]])

# Add types of statements here, e.g. selection, iteration, etc!
def p_statement(p):
    """ statement : assignment_statement SEMICOLON NEWLINE
                  | every_statement
    """
    p[0] = Node("statement", [p[1]])

# Modify this to go to 'or_expression' once the expression depending
# on it are finished
def p_assignment_statement(p):
    """ assignment_statement : ID EQUALS additive_expression 
                             | ID EQUALS assignment_statement
                             | ID EQUALS primary_expression
    """
    
    p[0] = Node("assignment_statement", [p[3]], p[1])
# Change to continue sequence in grammar i.e. multiplicative_expression, etc
def p_additive_expresion(p):
    """ additive_expression : primary_expression
                             | additive_expression PLUS primary_expression
                             | additive_expression MINUS primary_expression
    """
    if len(p) == 2:
        p[0] = Node("additive_expression", [p[1]])
    else:
        p[0] = Node("additive_expression", [p[1], p[3], p[2]])

# Change to include arrays
def p_primary_expression(p):
    """ primary_expression : CONSTANT
                           | ID
                           | LPAREN additive_expression RPAREN
    """
    if len(p) == 2:
        p[0] = Node('primary_expression', [], p[1])
    else:
        p[0] = Node('primary_expression', [p[1]])

def p_every_statement(p):
    """ every_statement : EVERY LPAREN additive_expression RPAREN LBRACK statement_list RBRACK """
    p[0] = Node("every_statement", [p[3], p[6]])

# Error rule for syntax errors
def p_error(p):
    print "Syntax error in input!"
    print p

# wrap default parser into CoZy parser
class CoZyParser(object):
    def __init__(self, lexer = None):
        if lexer is None:
            lexer = CoZyLexer()
        self.lexer = lexer
        self.parser = yacc.yacc()

    def parse(self, code):
        self.lexer.input(code)
        result = self.parser.parse(lexer = self.lexer)
        print result
        return result
        # return ast.Module(None, result)

# Build the parser
parser = CoZyParser()

## Put code to test here
s = """
x = 3;
def fun():
    y=5;
    c=6+7;
    z=c+y;
"""
# every(1){ 
#     y = 10;
#     y = y - 100;
# }
# every(0){
#     x = 20;
#     x = x + 2;
# }

result = parser.parse(s)

# ## Prints the AST
# print result

code = codeGenerator(result)
# Prints the actual program
print code.ret

## Makes the output file
f = open("out.py", 'w')
f.write(code.ret)
print 'Done!\nCheck "out.py"'
