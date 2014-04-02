import ply.yacc as yacc

# Get the token map from the lexer.  This is required.
from cozyLex import tokens
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
    """ statement : assignment_statement SEMICOLON
                  | every_statement
                  | iteration_statement
                  | selection_statement
                  | print_statement SEMICOLON
    """
    p[0] = Node("statement", [p[1]])

# is this correct?? need to fix according to grammar...
def p_assignment_statement(p):
    """ assignment_statement : ID EQUALS or_expression
                             | ID EQUALS assignment_statement or_expression
    """
    
    p[0] = Node("assignment_statement", [p[3]], p[1])

def p_or_expresion(p):
    """ or_expression : and_expression
                        | or_expression OR and_expression
    """
    if len(p) == 2:
        p[0] = Node("or_expression", [p[1]])
    else:
        p[0] = Node("or_expression", [p[1], p[3], p[2]])

def p_and_expresion(p):
    """ and_expression : equality_expression
                        | and_expression AND equality_expression
    """
    if len(p) == 2:
        p[0] = Node("and_expression", [p[1]])
    else:
        p[0] = Node("and_expression", [p[1], p[3], p[2]])

def p_equality_expresion(p):
    """ equality_expression : relational_expression
                        | equality_expression EQUIV relational_expression
                        | equality_expression NONEQUIV relational_expression
    """
    if len(p) == 2:
        p[0] = Node("equality_expression", [p[1]])
    else:
        p[0] = Node("equality_expression", [p[1], p[3], p[2]])

def p_relational_expresion(p):
    """ relational_expression : additive_expression
                        | relational_expression RELOP additive_expression
    """
    if len(p) == 2:
        p[0] = Node("relational_expression", [p[1]])
    else:
        p[0] = Node("relational_expression", [p[1], p[3], p[2]])
        
def p_additive_expresion(p):
    """ additive_expression : multiplicative_expression
                             | additive_expression PLUS multiplicative_expression
                             | additive_expression MINUS multiplicative_expression
    """
    if len(p) == 2:
        p[0] = Node("additive_expression", [p[1]])
    else:
        p[0] = Node("additive_expression", [p[1], p[3], p[2]])

# Change to continue sequence in grammar i.e. function_expression, etc
#also something is wrong because you can't do 7 + 3 *4
def p_multiplicative_expresion(p):
    """ multiplicative_expression : primary_expression
                             | multiplicative_expression MULTIPLY primary_expression
                             | multiplicative_expression DIVIDE primary_expression
    """
    if len(p) == 2:
        p[0] = Node("multiplicative_expression", [p[1]])
    else:
        p[0] = Node("multiplicative_expression", [p[1], p[3], p[2]])

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

#is this correct?
def p_every_statement(p):
    """ every_statement : EVERY LPAREN additive_expression RPAREN LBRACK statement_list RBRACK """
    p[0] = Node("every_statement", [p[3], p[6]])

#fix this when tabs and newlines happen
def p_iteration_statement(p):
    """ iteration_statement : WHILE LPAREN or_expression RPAREN COLON LBRACK statement_list RBRACK
    """
    p[0] = Node("iteration_statement", [p[3], p[7]])

#need to add elif
def p_selection_statement(p):
    """ selection_statement : IF LPAREN or_expression RPAREN COLON LBRACK statement_list RBRACK
                            | IF LPAREN or_expression RPAREN COLON LBRACK statement_list RBRACK ELSE COLON LBRACK statement_list RBRACK 
    """
    if len(p) == 9:
        p[0] = Node("selection_statement", [p[3], p[7]])
    else:
        p[0] = Node("selection_statement", [p[3], p[7], p[12]]) #i dont know if this is even right

def p_print_statement(p):
    """ print_statement : PRINT LPAREN or_expression RPAREN
    """
    p[0] = Node("print_statement", [p[3]])

# Error rule for syntax errors
def p_error(p):
    print "Syntax error in input!"
    print p

# Build the parser
parser = yacc.yacc()
    

## Put code to test here
s = """
print(3 <= 2);
print(3);
print(3 + 2 / 3 * 8.0);
"""
result = parser.parse(s)

## Prints the AST
print result

code = codeGenerator(result)
## Prints the actual program
print code.ret

## Makes the output file
f = open("out.py", 'w')
f.write(code.ret)
print 'Done!\nCheck "out.py"'
