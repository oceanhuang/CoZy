import ply.lex as lex
import re

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
    'or' : 'OR',
    'and' : 'AND',
    'if' : 'IF',
    'else' : 'ELSE',
    'add' : 'ADD',
    'remove' : 'REMOVE',
    'sort' : 'SORT',
    #'elif' : 'ELSEIF',
    'while' : 'WHILE',
    'for' : 'FOR',
    'in' : 'IN', 
    'print' : 'PRINT',
    'not' : 'NOT',
    'to' : 'TO',
    'each' : 'EACH',
    'log' : 'LOG',
    'once' : 'ONCE',
    'during' : 'DURING',
    'true' : 'TRUE',
    'false' : 'FALSE'
    }

tokens = [
    'LPAREN',
    'RPAREN',
    'RBRACK',
    'LBRACK',
    'RBRACE',
    'LBRACE',
    'EQUALS',
    'PLUS',
    'MINUS',
    'ID',
    'SEMICOLON',
    'COLON',
    'CONSTANT',
    'DATE',
    'TIME',
    'DATETIME',
    'TEMPERATURE',
    'MULTIPLY',
    'DIVIDE',
    'EQUIV',
    'NONEQUIV',
    'RELOP',
    'INDENT',
    'DEDENT',
    'WS',
    'NEWLINE',
    'COMMA',
    'STRING',
    'FORRANGE',
] + list(reserved.values())

# Regular expression rules for simple tokens
t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_LBRACK    = r'\{'
t_RBRACK    = r'\}'
t_LBRACE    = r'\['
t_RBRACE    = r'\]'
t_EQUALS    = r'='
t_PLUS      = r'\+'
t_MINUS     = r'\-'
t_SEMICOLON = r';'
t_COLON     = r':'
t_MULTIPLY  = r'\*'
t_DIVIDE    = r'/'
t_EQUIV     = r'(==)'
t_NONEQUIV  = r'(!=)'
t_RELOP     = r'(<=)|(>=)|(<)|(>)'
t_COMMA     = r'(,)'
t_FORRANGE = r'\s*\.\.\.\s*'
# A regular expression rule with some action code

def t_DATETIME(t):
    r'[0-3]?[0-9]/[01]?[0-9]/[0-9][0-9][0-9][0-9][ ][01]?[0-9]:[0-5][0-9][ ]((AM)|(PM))'
    return t

def t_DATE(t):
    r'[0-3]?[0-9]/[01]?[0-9]/[0-9][0-9][0-9][0-9]'
    return t
def t_TEMPERATURE(t):
    r'[0-9]+[ ]*[CFK]'
    return t

def t_TIME(t):
    r'[01]?[0-9]:[0-5][0-9][ ]((AM)|(PM))'
    return t

def t_STRING(t):
    r'((".*") | (\'.*\'))'
    return t

def t_CONSTANT(t):
    r'[0-9]*\.?[0-9]+|((\'|\").*?(\'|\"))'
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID') #looks in reserved list, if can't find, assigns it to type ID 
    return t


# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    t.type = "NEWLINE"
    if t.lexer.paren_count == 0:
        return t

# Whitespace
def t_WS(t):
    r' [ ]+ '
    if t.lexer.at_line_start and t.lexer.paren_count == 0:
        return t


# # A string containing ignored characters (spaces and tabs)
# t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

# the following methods: track_tokens_filter(), _new_token(), DEDENT(), INDENT(), indentation_filter(), filter(), and CoZyLexer() are from:
# http://www.dalkescientific.com/writings/diary/GardenSnake.py
# 
# Python's syntax has three INDENT states
#  0) no colon hence no need to indent
#  1) "if 1: go()" - simple statements have a COLON but no need for an indent
#  2) "if 1:\n  go()" - complex statements have a COLON NEWLINE and must indent
NO_INDENT = 0
MAY_INDENT = 1
MUST_INDENT = 2

# only care about whitespace at the start of a line
def track_tokens_filter(lexer, tokens):
    lexer.at_line_start = at_line_start = True
    indent = NO_INDENT
    saw_colon = False
    for token in tokens:
        token.at_line_start = at_line_start

        if token.type == "COLON":
            at_line_start = False
            indent = MAY_INDENT
            token.must_indent = False
            
        elif token.type == "NEWLINE":
            at_line_start = True
            if indent == MAY_INDENT:
                indent = MUST_INDENT
            token.must_indent = False

        elif token.type == "WS":
            assert token.at_line_start == True
            at_line_start = True
            token.must_indent = False

        else:
            # A real token; only indent after COLON NEWLINE
            if indent == MUST_INDENT:
                token.must_indent = True
            else:
                token.must_indent = False
            at_line_start = False
            indent = NO_INDENT

        yield token
        lexer.at_line_start = at_line_start

def _new_token(type, lineno):
    tok = lex.LexToken()
    tok.type = type
    tok.value = None
    tok.lineno = lineno
    return tok

# Synthesize a DEDENT tag
def DEDENT(lineno):
    return _new_token("DEDENT", lineno)

# Synthesize an INDENT tag
def INDENT(lineno):
    return _new_token("INDENT", lineno)

# Track the indentation level and emit the right INDENT / DEDENT events.
def indentation_filter(tokens):
    # A stack of indentation levels; will never pop item 0
    levels = [0]
    token = None
    depth = 0
    prev_was_ws = False
    for token in tokens:
##        if 1:
##            print "Process", token,
##            if token.at_line_start:
##                print "at_line_start",
##            if token.must_indent:
##                print "must_indent",
##            print
                
        # WS only occurs at the start of the line
        # There may be WS followed by NEWLINE so
        # only track the depth here.  Don't indent/dedent
        # until there's something real.
        if token.type == "WS":
            assert depth == 0
            depth = len(token.value)
            prev_was_ws = True
            # WS tokens are never passed to the parser
            continue

        if token.type == "NEWLINE":
            depth = 0
            if prev_was_ws or token.at_line_start:
                # ignore blank lines
                continue
            # pass the other cases on through
            yield token
            continue

        # then it must be a real token (not WS, not NEWLINE)
        # which can affect the indentation level

        prev_was_ws = False
        if token.must_indent:
            # The current depth must be larger than the previous level
            if not (depth > levels[-1]):
                raise IndentationError("expected an indented block")

            levels.append(depth)
            yield INDENT(token.lineno)

        elif token.at_line_start:
            # Must be on the same level or one of the previous levels
            if depth == levels[-1]:
                # At the same level
                pass
            elif depth > levels[-1]:
                raise IndentationError("indentation increase but not in new block")
            else:
                # Back up; but only if it matches a previous level
                try:
                    i = levels.index(depth)
                except ValueError:
                    raise IndentationError("inconsistent indentation")
                for _ in range(i+1, len(levels)):
                    yield DEDENT(token.lineno)
                    levels.pop()

        yield token

    ### Finished processing ###

    # Must dedent any remaining levels
    if len(levels) > 1:
        assert token is not None
        for _ in range(1, len(levels)):
            yield DEDENT(token.lineno)
    
# The top-level filter adds an ENDMARKER, if requested.
# Python's grammar uses it.
def filter(lexer, add_endmarker = False):
    token = None
    tokens = iter(lexer.token, None)
    tokens = track_tokens_filter(lexer, tokens)
    for token in indentation_filter(tokens):
        yield token

    if add_endmarker:
        lineno = 1
        if token is not None:
            lineno = token.lineno
        yield _new_token("ENDMARKER", lineno)


class CoZyLexer(object):
    def __init__(self, debug=0, optimize=0, lextab='lextab', reflags=0):
        self.lexer = lex.lex(debug=debug, optimize=optimize, lextab=lextab, reflags=reflags)
        self.token_stream = None
    def input(self, s, add_endmarker=False):
        self.lexer.paren_count = 0
        self.lexer.input(s)
        self.token_stream = filter(self.lexer, add_endmarker)
    def token(self):
        try:
            return self.token_stream.next()
        except StopIteration:
            return None


# Put CODE HERE TO TEST LEXER
if __name__ == '__main__':

    # Build the lexer
    lexer = CoZyLexer()
    # code
    #this doesnt work RGGGGGG
    data = """
for x in 1...100:
    print(x)
"""

    # Give the lexer some input
    lexer.input(data)

    # Check tokens
    while True:
        tok = lexer.token()
        if not tok: break      # No more input
        elif not hasattr(tok, 'line') and not hasattr(tok, 'lexpos'):
            print tok.type
        else: print tok
