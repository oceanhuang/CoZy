import ply.yacc as yacc

# Get the token map from the lexer.  This is required.
from cozyLex import tokens
from codeGenerator import *

class Node(object):
    """ Node class. Used to build the AST. Each node has a type,
    children and a leaf.
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
    'function_definition : DEF ID LPAREN RPAREN LBRACK statement_list RBRACK'

    p[0] = Node("function_definition", [p[2], p[4], p[6]]);

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
    """ statement : assignment_statement  SEMICOLON
                  | every_statement
    """
    p[0] = Node("statement", [p[1]])

# Modify this to go to 'or_expression' once the expression depending
# on it are finished
def p_assignment_statement(p):
    """ assignment_statement : ID EQUALS additive_expression 
                             | ID EQUALS assignment_statement
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

def p_primary_expression_days(p):
    """ primary_expression : MONDAY
                           | TUESDAY
                           | WEDNESDAY
                           | THURSDAY
                           | FRIDAY
                           | SATURDAY
                           | SUNDAY
    """
    p[0] = Node('day_expression', [], p[1])

def p_primary_expression_months(p):
    """ primary_expression : JANUARY
                           | FEBRUARY
                           | MARCH
                           | APRIL
                           | MAY
                           | JUNE
                           | JULY
                           | AUGUST
                           | SEPTEMBER
                           | OCTOBER
                           | NOVEMBER
                           | DECEMBER
    """
    p[0] = Node('month_expression', [], p[1])
def p_primary_expression_date_time(p):
    """ primary_expression : DATETIME """
    p[0] = Node('date_time_expression', [], p[1])
def p_primary_expression_date(p):
    """ primary_expression : DATE """
    p[0] = Node('date_expression', [], p[1])
def p_primary_expression_temperature(p):
    """ primary_expression : TEMPERATURE """
    p[0] = Node('temperature_expression', [], p[1])
def p_primary_expression_time(p):
    """ primary_expression : TIME """
    p[0] = Node('time_expression', [], p[1])


def p_every_statement(p):
    """ every_statement : EVERY LPAREN additive_expression RPAREN LBRACK statement_list RBRACK """
    p[0] = Node("every_statement", [p[3], p[6]])

# Error rule for syntax errors
def p_error(p):
    print "Syntax error in input!"
    print p

# Build the parser
parser = yacc.yacc()
    

## Put code to test here
s = """
x=3+3;
y = 2 + "every";
z = Tuesday;
y = April;
datetime = 12/12/2005 04:50 PM;
"""
result = parser.parse(s)

## Prints the AST
# print result

code = codeGenerator(result)
## Prints the actual program
# print code.ret

## Makes the output file
f = open("out.py", 'w')
print code.ret
f.write(code.ret)
print 'Done!\nCheck "out.py"'
