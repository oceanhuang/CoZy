import ply.lex as lex

# List of token names.   This is always required
reserved = {
    'every' : 'EVERY',
    # 'Monday' : 'MONDAY',
    # 'Tuesday': 'TUESDAY',
    # 'Wednesday' : 'WEDNESDAY',
    # 'Thursday' : 'THURSDAY',
    # 'Friday' : 'FRIDAY',
    # 'Saturday' : 'SATURDAY',
    # 'Sunday' : 'SUNDAY',
    'def' : 'DEF',
}

tokens = [
    'LPAREN',
    'RPAREN',
    'RBRACK',
    'LBRACK',
    'EQUALS',
    'PLUS',
    'MINUS',
    'ID',
    'SEMICOLON',
    'CONSTANT',
] + list(reserved.values())

# Regular expression rules for simple tokens
t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_LBRACK    = r'\{'
t_RBRACK    = r'\}'
t_EQUALS    = r'='
t_PLUS      = r'\+'
t_MINUS     = r'\-'
t_SEMICOLON = r';'
t_CONSTANT  = r'[0-9]+|((\'|\").*?(\'|\"))'
# A regular expression rule with some action code

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID') #looks in reserved list, if can't find, assigns it to type ID 
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

# Uncomment this lines to test
# Put CODE HERE TO TEST LEXER
# data = """
# x=3+3;
# y = 2 + "every";
# z = Tuesday;
# """
# Give the lexer some input
#lexer.input(data)
# Tokenize
# while True:
#     tok = lexer.token()
#     if not tok: break      # No more input
#     print tok
