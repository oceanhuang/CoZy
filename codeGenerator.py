class codeGenerator(object):
    
    def __init__(self, tree):
        # Keep track of scopes
        self.varScopes = [[]]
        self.scopeDepth = 0
        # Symbols table
        self.symbolsTable = {}
        # Keep track of indentation
        self._indent = 0
        self.ret = self.dispatch(tree)
    
    def dispatch(self, tree, flag=None):
        '''Dispatches based on type of node'''
        method = getattr(self, "_"+tree.type)
        code = method(tree, flag)
        return code
    
    
