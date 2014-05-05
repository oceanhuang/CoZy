import ply.yacc as yacc
from compiler import ast, misc

# Get the token map from the lexer.  This is required.
from cozyLex import *
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

    'function_definition : DEF ID LPAREN function_param_list RPAREN COLON NEWLINE INDENT statement_list DEDENT'

    p[0] = Node("function_definition", [p[2], p[4], p[9]]);

def p_function_param_list(p):
    'function_param_list : function_param' #need to handle empty string
    if len(p)==2:
        p[0] = Node("function_param_list", [p[1]])
    else:
        p[0] = Node("function_param_list", [])


def p_function_param(p):
    '''function_param : ID 
                    | function_param COMMA function_param_end
    '''
    if len(p)==2:
        p[0] = Node('function_param', [], p[1])
    else:
        p[0] = Node('function_param', [p[1], p[3]])

def p_function_param_end(p):
    'function_param_end : ID'
    p[0] = Node('function_param_end', [], p[1])

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
    """ statement : assignment_statement NEWLINE
                  | every_statement
                  | once_every_statement
                  | iteration_statement
                  | selection_statement
                  | print_statement SEMICOLON
                  | log_statement SEMICOLON
                  | for_statement
                  | print_statement NEWLINE
                  | log_statement NEWLINE
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
    """ relational_expression : during_or_expression
                        | relational_expression RELOP during_or_expression
    """
    if len(p) == 2:
        p[0] = Node("relational_expression", [p[1]])
    else:
        p[0] = Node("relational_expression", [p[1], p[3], p[2]])

#maybe put during things here.... need to not allow above cases for during in the grammar!!
def p_during_or_expression(p):
    """during_or_expression : during_and_expression
                            | during_or_expression COMMA during_and_expression"""
#                            | LPAREN during_or_expression RPAREN DURING during_and_expression"""
    if len(p) == 2:
        p[0] = Node("during_or_expression", [p[1]])
    else:
        p[0] = Node("during_or_expression", [p[1],p[3]])
#    else:
#        p[0] = Node("during_and_expression", [p[2],p[5]]) #need to write the code gen for this case

#can do something like(TUESDAY, JANUARY DURING WEDNESDAY) DURING 4:30 PM TO 5:30 PM
#could it do this too (TUESDAY, (WEDS, FRIDAY) DURING 4:30 PM TO 5:30 PM) DURING 4:30 PM TO 5:30 PM??
def p_during_and_expression(p):
    """ during_and_expression : additive_expression
                        | during_and_expression DURING additive_expression """

    if len(p) == 2:
        p[0] = Node("during_and_expression", [p[1]])
    elif len(p) == 4:
        p[0] = Node("during_and_expression", [p[1],p[3]])

        
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
def p_multiplicative_expresion(p):
    """ multiplicative_expression : primary_expression
                             | multiplicative_expression MULTIPLY primary_expression
                             | multiplicative_expression DIVIDE primary_expression
    """
    if len(p) == 2:
        p[0] = Node("multiplicative_expression", [p[1]])
    else:
        p[0] = Node("multiplicative_expression", [p[1], p[3], p[2]])

# needs to be fixed (move not)...... also code generator needs to handle not
def p_primary_expression(p):
    """ primary_expression : ID
                           | LPAREN or_expression RPAREN
                           | NOT LPAREN or_expression RPAREN
    """
    if len(p) == 2:
        p[0] = Node('primary_expression', [], p[1])
    elif len(p) == 4:
        p[0] = Node('primary_expression', [p[2]])
    else:
        p[0] = Node('primary_expression', [p[3]]) #has not in it

def p_primary_expression_string(p):
    """ primary_expression : STRING
    """
    p[0] = Node('primary_expression_string', [], p[1])


def p_primary_expression_constant(p):
    """ primary_expression : CONSTANT
    """
    p[0] = Node('primary_expression_constant', [], p[1])

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
#    """ every_statement : EVERY LPAREN primary_expression RPAREN COLON NEWLINE INDENT statement_list DEDENT """
    """ every_statement : EVERY LPAREN during_or_expression RPAREN COLON NEWLINE INDENT statement_list DEDENT """
    p[0] = Node("every_statement", [p[3], p[8]])

def p_once_every_statement(p):
#    """ once_every_statement : ONCE EVERY LPAREN primary_expression RPAREN COLON NEWLINE INDENT statement_list DEDENT """
    """ once_every_statement : ONCE EVERY LPAREN during_or_expression RPAREN COLON NEWLINE INDENT statement_list DEDENT """
    p[0] = Node("once_every_statement", [p[4], p[9]])

#fix this when tabs and newlines happen
def p_iteration_statement(p):
    """ iteration_statement : WHILE LPAREN or_expression RPAREN COLON NEWLINE INDENT statement_list DEDENT
    """
    p[0] = Node("iteration_statement", [p[3], p[8]])

#need to add elif
def p_selection_statement(p):
    """ selection_statement : IF LPAREN or_expression RPAREN COLON NEWLINE INDENT statement_list DEDENT
                            | IF LPAREN or_expression RPAREN COLON NEWLINE INDENT statement_list DEDENT ELSE COLON NEWLINE INDENT statement_list DEDENT
    """
    if len(p) == 10:
        p[0] = Node("selection_statement", [p[3], p[8]])
    else:
        p[0] = Node("selection_statement", [p[3], p[8], p[14]]) #i dont know if this is even right

def p_print_statement(p):
    """ print_statement : PRINT LPAREN or_expression RPAREN
    """
    p[0] = Node("print_statement", [p[3]])

    
def p_log_statement(p):
    """ log_statement : LOG LPAREN or_expression RPAREN
    """
    p[0] = Node("log_statement", [p[3]])


#need to add foreach/ also confused about the grammar
def p_for_statement(p):
    """ for_statement : FOR primary_expression IN or_expression TO or_expression COLON NEWLINE INDENT statement_list DEDENT
    """
    p[0] = Node("for_statement", [p[2], p[4], p[6], p[10]])

# Error rule for syntax errors
def p_error(p):
    print "Syntax error in input!"
    if not hasattr(p, 'line') and not hasattr(p, 'lexpos'):
        print p.type
    else: print p

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
        # print result
        return result
        # return ast.Module(None, result)

if __name__ == '__main__':

    # Build the parser
    parser = CoZyParser()
    ## Put code to test here
#    s = """
#a = 60 F + 50F + 30F
#d = 35/2/1991 10:00 PM
#c = 10:00 AM
#g = 1 < 3 + 4
#r = 1 + 2 * 3+4
#f = 1:00 PM
#h = 1 < 3 and 4 > 3
#
#z = r + 2
#z = a + z
#bday = 16/07/1991
#every (Monday):
#    print ('5')
#i = 0
#while (i < 7):
#    print ("okay")
#    i = i + 1
#every (January):
#    print ("hello world")
#once every (January during Monday):
#    print ("hello world")
#once every (January during Monday, February during Friday):
#    print ("hello world")
#every ((January during Monday, February during Friday) during Wednesday):
#    print ("hello world")
#    
# """
    s = '''
log("5")
'''


    result = parser.parse(s)

    # ## Prints the AST
    print result
    code = codeGenerator(result)
    # Prints the actual program
    print code.ret

    ## Makes the output file
    f = open("out.py", 'w')
    f.write(code.ret)
    print 'Done!\nCheck "out.py"'
