level = 0
class codeGenerator(object):
    def __init__(self, tree):
        # Keep track of scopes
        self.varScopes = [[]]
        self.scopeDepth = 0
        # Symbols table
        self.symbolsTable = {}
        # Keep track of indentation
        self.ret = self.dispatch(tree)
    
    def dispatch(self, tree, flag=None):
        '''Dispatches based on type of node'''
        if isinstance(tree, list):
            temp = ""
            for t in tree:
                temp += self.dispatch(t)
            return temp

        method = getattr(self, "_"+tree.type)
        code = method(tree, flag)
        return code

    def _stmtseq(self, tree, flag=None):
        return self.dispatch(tree.children)

    def _stmt(self, tree, flag=None):
        return self.dispatch(tree.children)

    def _stmt_assign(self, tree, flag=None):
        s1 = self.dispatch(tree.children)
        self.symbolsTable[tree.leaf] = s1
        s2 = tree.leaf + ' = ' + self.symbolsTable[tree.leaf] + "\n"
        return s2
    def _stmtseq_stmt(self, tree, flag=None):
        s = self.dispatch(tree.children[0]) + self.dispatch(tree.children[1])
        return s
    def _plus(self, tree, flag=None):
        s = self.dispatch(tree.children[0]) + ' + ' + self.dispatch(tree.children[1])
        return s
    
    def _expr(self, tree, flag=None):
        s = self.dispatch(tree.children)
        return s

    def _factor(self, tree, flag=None):
        return str(tree.leaf)  

    def _timeexpr(self, tree, flag=None):
        return tree.leaf

    def _every(self, tree, flag=None):
        s = "if " + self.dispatch(tree.children[0]) + " :\n"
        lines = self.dispatch(tree.children[1]).splitlines()
        for line in lines:
            s+= "    " + line +"\n"
        return s

