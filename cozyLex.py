import ply.lex as lex

# List of token names.   This is always required
tokens = (
   'LPAREN',
   'RPAREN',
   'EVERY',
   'FALSE',
   'TRUE',
   'RBRACK',
   'LBRACK',
   'NAND',
)

# Regular expression rules for simple tokens
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LBRACK  = r'\{'
t_RBRACK  = r'\}'
t_EVERY   = r'every'
t_NAND    = r'nand'

# A regular expression rule with some action code
def t_TRUE(t):
    r'true'
    t.value = True
    return t

def t_FALSE(t):
    r'false'
    t.value = False
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()


# Test it out
data = '''
every
'''

# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok: break      # No more input
    print tok
