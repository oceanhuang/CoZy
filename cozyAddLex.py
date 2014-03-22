import ply.lex as lex

# List of token names.   This is always required
reserved = {
    'every' : 'EVERY',
}

tokens = [
   'LPAREN',
   'RPAREN',
   'FALSE',
   'TRUE',
   'RBRACK',
   'LBRACK',
   'NAND',

   'PLUS',
   'ID',
   'INT',
   'SEMICOLON',
   'EQUALS',
] + list(reserved.values())

# Regular expression rules for simple tokens
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LBRACK  = r'\{'
t_RBRACK  = r'\}'
t_PLUS    = r'\+'
t_NAND    = r'nand'
t_EQUALS  = r'='
t_SEMICOLON = r';'

# A regular expression rule with some action code
def t_INT(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID') #looks in reserved list, if can't find, assigns it to type ID 
    return t

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


# Error handling rule
def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

# A string containing ignored characters (spaces and tabs)

t_ignore  = ' \t'
# Build the lexer
lexer = lex.lex()



# Test it out
data = 'x = 5 + 5; every(0) { y = 5 + 1; x = y + 2;} y++;'

# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok: break      # No more input
    print tok
