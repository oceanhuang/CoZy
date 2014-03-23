import ply.yacc as yacc

# Get the token map from the lexer.  This is required.
from cozyAddLex import tokens

indent_level = 0
class Node:
    def __init__(self, type, children=None, leaf=None):
        self.type = type
        if children:
            self.children = children
        else:
            self.children = []
        self.leaf = leaf

def p_prof_smstseq(p):
    'prog : stmtseq'
    p[0] = Node("stmtseq", [p[1]])

def p_stmtseq_stmt(p):
    'stmtseq : stmt'
    p[0] = Node("stmt", [p[1]])

def p_stmtseq_stmtseq(p):
    'stmtseq : stmtseq stmt'
    p[0] = Node("stmtseq-stmt", [p[1], p[2]])

def p_stmt_every(p):
    'stmt : EVERY LPAREN expr RPAREN LBRACK stmtseq RBRACK'
    p[0] = Node('every', [p[3], p[6]])

def p_stmt_id(p):
    'stmt : ID EQUALS expr SEMICOLON'
    p[0] = Node('stmt_assign', [p[1], p[3]])

def p_expr_plus(p):
    'expr : expr PLUS factor'
    p[0] = Node('plus', [p[1], p[3]]);

def p_expr_factor(p):
    'expr : factor'
    p[0] = p[1]

def p_factor_parenth(p):
    'factor : LPAREN expr RPAREN'
    p[0] = '(' + p[2] + ')'

def p_factor_INT(p):
    'factor : INT'
    p[0] = `p[1]`

def p_factor_id(p):
    'factor : ID'
    p[0] = p[1]




# Error rule for syntax errors
def p_error(p):
    print "Syntax error in input!"

# Build the parser
parser = yacc.yacc()

while True:
   try:
       s = raw_input(' > ')
   except EOFError:
       break
   if not s: continue
   result = parser.parse(s)
   print result
