import ply.lex as lex

# List of token names.   This is always required
reserved = {
    # Days
    'Monday' : 'MONDAY',
    'Tuesday': 'TUESDAY',
    'Wednesday' : 'WEDNESDAY',
    'Thursday' : 'THURSDAY',
    'Friday' : 'FRIDAY',
    'Saturday' : 'SATURDAY',
    'Sunday' : 'SUNDAY',
    # Months
    'January': 'JANUARY',
    'February': 'FEBRUARY',
    'March': 'MARCH',
    'April': 'APRIL',
    'May': 'MAY',
    'June': 'JUNE',
    'July': 'JULY',
    'August': 'AUGUST',
    'September': 'SEPTEMBER',
    'October': 'OCTOBER',
    'November': 'NOVEMBER',
    'December': 'DECEMBER',
    # Other
    'every' : 'EVERY',
    'def' : 'DEF',
    'to' : 'TO',
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
    'DATE',
    'TIME',
    'DATETIME',
    'TEMPERATURE',
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

def t_DATETIME(t):
    r'[0-3]?[0-9]/[01]?[0-9]/[0-9][0-9][0-9][0-9][ ][01]?[0-9]:[0-5][0-9][ ]((AM)|(PM))'
    return t

def t_DATE(t):
    r'[0-3]?[0-9]/[01]?[0-9]/[0-9][0-9][0-9][0-9]'
    return t
def t_TEMPERATURE(t):
    r'[0-9]+[ ]C|F|K'
    return t

def t_TIME(t):
    r'[01]?[0-9]:[0-5][0-9][ ]((AM)|(PM))'
    return t

def t_CONSTANT(t):
    r'[0-9]+|((\'|\").*?(\'|\"))'
    return t

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
data = """
x=3+3;
y = 2 + "every";
z = Tuesday;
y = 10:30 PM;
x = 17 C;
date = 01/12/1991;
datetime = 12/12/2005 04:50 PM;
"""
# Give the lexer some input
lexer.input(data)
# Tokenize
while True:
    tok = lexer.token()
    if not tok: break      # No more input
    print tok
