import ply.yacc as yacc

# Get the token map from the lexer.  This is required.
from cozyLex import tokens
def p_start_semicolon(p):
    'start : everyexp'
    p[0] = p[1] + ';'

def p_everyexp_every(p):
    'everyexp : EVERY LPAREN root RPAREN LBRACK expression RBRACK'
    rootvar = 'false'
    expressionvar = 'false'
    if(p[3]): rootvar = 'true'
    if(p[6]): expressionvar = 'true'

    p[0] = 'if('+rootvar+'){'+expressionvar+'}'

def p_expression_nand(p):
    'expression : expression NAND term'
    p[0] = not(p[1] * p[3])

def p_expression_parenth(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2] 

def p_expression_root(p):
    'expression : root'
    p[0] = p[1] 

def p_term_paren(p):
    'term : LPAREN expression RPAREN'
    p[0] = p[2]

def p_term_root(p):
    'term : root'
    p[0] = p[1]

def p_root_true(p):
    'root : TRUE'
    p[0] = p[1]

def p_root_false(p):
    'root : FALSE'
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
