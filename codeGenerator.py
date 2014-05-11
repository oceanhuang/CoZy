import datetime
import re
import sys
everys = 0
temp_def ='''
class Temperature:
    def __init__(self, number, tempType):
        if tempType == 'K':
            self.KTemp = number
            self.CTemp = number + 273.15
            self.FTemp = 5.0/9.0*(number - 32.0) + 273.15
        elif tempType == 'C':
            self.KTemp = number + 273.15
            self.CTemp = number
            self.FTemp = 9.0/5.0*number + 32.0      
        elif tempType == 'F':
            self.KTemp = 5.0/9.0*(number - 32.0) + 273.15
            self.CTemp = 5.0/9.0*(number -32.0)
            self.FTemp = number
    def getCelsius(self):
        return self.CTemp
    def getFarenheit(self):
        return self.FTemp
    def getKelvin(self):
        return self.KTemp

'''



class codeGenerator(object):
    def __init__(self, tree):
        # Keep track of scopes
        self.varScopes = [[]]
        self.scopeDepth = 0
        # Symbols table
        self.symbolTable = {}
        # Function parameter type lookup
        self.functionTable = {}
        self.returnTable = {}
        self.returnNumber = 0
        # Variable to store the code
        self.ret = "import datetime\n" + "every_list = []\n" + "log_file = open('cozyLog.txt', 'a')\n" + temp_def + self.dispatch(tree)
        # 
        # Keeps track of the number of every's

    #temporary exit function when exceptions are raised
    def exit(self, exit_msg):
        print exit_msg
        #sys.exit()

    
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

    def dispatchTuple(self, tree, flag=None):
        arg = self.dispatch(tree, flag)
        if type(arg) is tuple:
            arg = arg[1]
        return str(arg)

    def _program(self, tree, flag=None):
        return self.dispatch(tree.children)

    def _external_declaration(self, tree, flag=None):
        return self.dispatch(tree.children)

   
    #function definition
    def _function_definition(self, tree, flag=None):
        functiontype = "VOID"
        #with parameters
        if len(tree.children) == 2:
            arg = self.dispatch(tree.children[0])
##            self.functionTable[tree.leaf] = arg
            #
##            if type(arg) is tuple:
##                arg = str(arg[1])
                
            s = "def " + tree.leaf + "(" + str(arg[1]) +") :\n"
            lines = self.dispatch(tree.children[1]).splitlines()
            for line in lines:
                if "return" in line:
                    functiontype = self.returnTable[line[0:7]]
                    line = line[0:6] + line[8:len(line)]
                s+= "    " + line +"\n"
            self.functionTable[tree.leaf] = (arg,functiontype)
            return s 

        #no parameters
##        self.functionTable[tree.leaf] = ""
        s = "def " + tree.leaf + "( ) :\n"
        lines = self.dispatch(tree.children[0]).splitlines()
        for line in lines:
            if "return" in line:
                functiontype = self.returnTable[line[0:7]]
                line = line[0:6] + line[8:len(line)]
            s+= "    " + line +"\n"
        self.functionTable[tree.leaf] = ("",functiontype)
        return s

    def _function_param_list(self, tree, flag=None):
        if len(tree.children) == 1:
            s = self.dispatch(tree.children[0])
            return s
        else:
            s = self.dispatch(tree.children[0]) + ", " + self.dispatch(tree.children[1])
            return s

    def _function_param_number(self, tree, flag=None):
        s = tree.children[1]
        self.symbolTable[s] = ["NUM", None]
        return s

    def _function_param_temperatureF(self, tree, flag=None):
        s = tree.children[1]
        self.symbolTable[s] = ["F", None]
        return s

    def _function_param_temperatureC(self, tree, flag=None):
        s = tree.children[1]
        self.symbolTable[s] = ["C", None]
        return s

    def _function_param_temperatureK(self, tree, flag=None):
        s = tree.children[1]
        self.symbolTable[s] = ["K", None]
        return s
    
    def _function_param_time(self, tree, flag=None):
        s = tree.children[1]
        self.symbolTable[s] = ["TIME", None]
        return s

    def _function_param_datetime(self, tree, flag=None):
        s = tree.children[1]
        self.symbolTable[s] = ["DATETIME", None]
        return s

    def _function_param_boolean(self, tree, flag=None):
        s = tree.children[1]
        self.symbolTable[s] = ["BOOLEAN", None]
        return s

    def _function_param_day(self, tree, flag=None):
        s = tree.children[1]
        self.symbolTable[s] = ["DAY", None]
        return s

    def _function_param_month(self, tree, flag=None):
        s = tree.children[1]
        self.symbolTable[s] = ["MONTH", None]
        return s

    def _function_param_date(self, tree, flag=None):
        s = tree.children[1]
        self.symbolTable[s] = ["DATE", None]
        return s

    def _function_param_dayrange(self, tree, flag=None):
        s = tree.children[1]
        self.symbolTable[s] = ["DAY_RANGE", None]
        return s

    def _function_param_monthrange(self, tree, flag=None):
        s = tree.children[1]
        self.symbolTable[s] = ["MONTH_RANGE", None]
        return s

    def _function_param_daterange(self, tree, flag=None):
        s = tree.children[1]
        self.symbolTable[s] = ["DATE_RANGE", None]
        return s

    def _function_param_timerange(self, tree, flag=None):
        s = tree.children[1]
        self.symbolTable[s] = ["TIME_RANGE", None]
        return s

    def _function_param_string(self, tree, flag=None):
        s = tree.children[1]
        self.symbolTable[s] = ["STRING", None]
        return s

    def _function_param_listparam(self, tree, flag=None):
        s = tree.children[1]
        self.symbolTable[s] = ["LIST", None]
        return s
    
    def _list_start(self, tree, flag=None):
        if len(tree.children)==0:
            return "[]"
        else:
            return "[" + self.dispatchTuple(tree.children[0]) + "]"
    
    def _list_expression(self, tree, flag=None):
        if len(tree.children) == 1:
            return self.dispatch(tree.children[0], flag)[0], self.dispatchTuple(tree.children[0])
        else:
            return self.dispatch(tree.children[0], flag)[0]+ ", " + self.dispatch(tree.children[1], flag)[0], self.dispatchTuple(tree.children[0]) + ", " + self.dispatchTuple(tree.children[1])
        
    def _list_index_double(self, tree, flag=None):
        return self.dispatchTuple(tree.children[0]) + "[" + self.dispatchTuple(tree.children[1]) + "]"

    def _list_index_id(self, tree, flag=None):
        return tree.leaf + "[ int(" + self.dispatchTuple(tree.children[0]) + ") ]"

    
    """
    def _id_id(self, tree, flag=None):
        return tree.leaf
    
    def _id_list(self, tree, flag=None):
        return self.dispatch(tree.children[0])
    """

    
    def _list_primary_expression(self, tree, flag=None):
        if tree.leaf == None:
            return self.dispatch(tree.children[0])
        else:
            return tree.leaf


    def _list_add_expression(self, tree, flag=None):
        return tree.leaf + ".append(" + self.dispatchTuple(tree.children[0]) + ")"


    def _list_sort_expression(self, tree, flag=None):
        return tree.leaf + ".sort()"

    def _list_remove_expression(self, tree, flag=None):
        return tree.leaf + ".pop(" + self.dispatchTuple(tree.children[0]) + ")"


    def _list_add_expression_index(self, tree, flag=None):
        return self.dispatchTuple(tree.children[0]) + ".append(" + self.dispatchTuple(tree.children[1]) + ")"


    def _list_sort_expression_index(self, tree, flag=None):
        return self.dispatchTuple(tree.children[0]) + ".sort()"

    def _list_remove_expression_index(self, tree, flag=None):
        return self.dispatchTuple(tree.children[0]) + ".remove(" + self.dispatchTuple(tree.children[1]) + ")"
    

    def _statement_list(self, tree, flag=None):
        return self.dispatch(tree.children)

    def _statement(self, tree, flag=None):
        return self.dispatch(tree.children) + "\n"

    #whoever wrote this, please have a look at _assignnment_statement_list_index
    def _assignment_statement(self, tree, flag=None):
        arg = self.dispatch(tree.children[0]);
        self.symbolTable[tree.leaf] = [arg[0], arg[1]]
        if type(arg) is tuple:
            if arg[0] == "F" or arg[0] == "C" or arg[0] == "K":
                arg = "Temperature(" + str(arg[1]) + ", '" + arg[0] + "')"
#            elif arg[0] == "DATETIME":
#                self.symbolTable[tree.leaf] = [arg[0], arg[1]]
#                arg = "datetime.datetime(" + str(arg[1].get('year')) + ", " + str(arg[1].get('month')) + ", " + str(arg[1].get('day')) + ", " + str(arg[1].get('hour')) + ", " + str(arg[1].get('minute')) + ")"
#            elif arg[0] == "DATE":
#                self.symbolTable[tree.leaf] = [arg[0], arg[1]]
#                arg = "datetime.date(" + str(arg[1].get('year')) + ", " + str(arg[1].get('month')) + ", " + str(arg[1].get('day')) + ")" 
#            elif arg[0] == "TIME":
#                self.symbolTable[tree.leaf] = [arg[0], arg[1]]
#                arg = "datetime.time(" + str(arg[1].get('hour')) + ", " + str(arg[1].get('minute')) +")"
            elif arg[0] == "BOOLEAN" or arg[0] == "NUM":
                arg = arg[1]
            elif self.check_if_time(arg):
                arg = self.convert_time(arg)

            else:
                arg = arg[1]

        
        #print self.symbolTable #uncomment to check symbol table
        if type(arg) is not str: arg = str(arg)
        return tree.leaf + " = " + arg

    #not sure whether this actually works with the symbol table and everything
    def _assignment_statement_list_index(self, tree, flag=None):
        arg = self.dispatch(tree.children[1]);
        listIndex = self.dispatch(tree.children[0])
        self.symbolTable[listIndex] = [arg[0], arg[1]]
        if type(arg) is tuple:
            if arg[0] == "F" or arg[0] == "C" or arg[0] == "K":
                arg = "Temperature(" + str(arg[1]) + ", '" + arg[0] + "')"
#            elif arg[0] == "DATETIME":
#                self.symbolTable[listIndex] = [arg[0], arg[1]]
#                arg = "datetime.datetime(" + str(arg[1].get('year')) + ", " + str(arg[1].get('month')) + ", " + str(arg[1].get('day')) + ", " + str(arg[1].get('hour')) + ", " + str(arg[1].get('minute')) + ")"
#            elif arg[0] == "DATE":
#                self.symbolTable[listIndex] = [arg[0], arg[1]]
#                arg = "datetime.date(" + str(arg[1].get('year')) + ", " + str(arg[1].get('month')) + ", " + str(arg[1].get('day')) + ")" 
#            elif arg[0] == "TIME":
#                self.symbolTable[listIndex] = [arg[0], arg[1]]
#                arg = "datetime.time(" + str(arg[1].get('hour')) + ", " + str(arg[1].get('minute')) +")"
            elif arg[0] == "BOOLEAN" or arg[0] == "NUM":
                arg = arg[1]
            elif self.check_if_time(arg):
                arg = self.convert_time(arg)

            else:
                arg = arg[1]

        
        #print self.symbolTable #uncomment to check symbol table
        if type(arg) is not str: arg = str(arg)
        return listIndex + " = " + arg



    def _or_expression(self, tree, flag=None):
        
        if len(tree.children) == 1:
            return self.dispatch(tree.children[0], flag)
        else:
            (operand1, operand2, type1, type2) = self.get_types(tree.children[0], tree.children[1], flag)
            return "BOOLEAN", str(operand1[1]) + " " + tree.children[2] + " " + str(operand2[1])
            #return self.dispatch(tree.children[0]) + " " + tree.children[2] + " " + self.dispatch(tree.children[1])  

    def _and_expression(self, tree, flag=None):
        
        if len(tree.children) == 1:
            return self.dispatch(tree.children[0], flag)
        else:
            (operand1, operand2, type1, type2) = self.get_types(tree.children[0], tree.children[1], flag)
            
            return "BOOLEAN", str(operand1[1]) + " " + tree.children[2] + " " + str(operand2[1])
            #return self.dispatch(tree.children[0]) + " " + tree.children[2] + " " + self.dispatch(tree.children[1])  

    def _equality_expression(self, tree, flag=None):
        
        if len(tree.children) == 1:
            return self.dispatch(tree.children[0],flag)
        else:
            (operand1, operand2, type1, type2) = self.get_types(tree.children[0], tree.children[1], flag)

            if type1 != type2:
                exit("TypeError! Cannot compare objects of type " + type1 + " and objects of type " + type2)

            return "BOOLEAN", str(operand1[1]) + " " + tree.children[2] + " " + str(operand2[1])
            #return self.dispatch(tree.children[0]) + " " + tree.children[2] + " " + self.dispatch(tree.children[1])  

    def _relational_expression(self, tree, flag=None):
        
        if len(tree.children) == 1:
            return self.dispatch(tree.children[0], flag)
        else:

            (operand1, operand2, type1, type2) = self.get_types(tree.children[0], tree.children[1], flag)
            #operand1 = self.dispatch(tree.children[0])
            #operand2 = self.dispatch(tree.children[1])
            #type1 = operand1[0]
            #type2 = operand2[0]

            if type1 != type2:
                exit("TypeError! Can not use relop between type " + type1 + " and " + type2)
            else:
                if type1 != "NUM" and tree.children[2] != "!=":
                    exit("Error: Cannot use '>' or '<' for non-numbers") 

            return type1, str(operand1[1]) + " " + tree.children[2] + " " + str(operand2[1])  

    def _additive_expression(self, tree, flag=None):
        
        if len(tree.children) == 1:
            return self.dispatch(tree.children[0], flag)
        else:
            
            (operand1, operand2, type1, type2) = self.get_types(tree.children[0], tree.children[1], flag)
            #operand1 = self.dispatch(tree.children[0])
            #operand2 = self.dispatch(tree.children[1])
            #type1 = operand1[0]
            #type2 = operand2[0]

            if type1 != type2:
                exit("TypeError! " + type1 + " is not of type " +type2)
            else:
                if type1=="DAY" or type1=="MONTH" or type1=="DATE" or type1=="TIME" or type1=="DATETIME":
                    exit("TypeError! Cannot add " + type1 + " types together")

                return type1, str(operand1[1]) + " " + tree.children[2] + " " + str(operand2[1]) 

    def _multiplicative_expression(self, tree, flag=None):
        
        if len(tree.children) == 1:
            return self.dispatch(tree.children[0], flag) 
        else:
            
            (operand1, operand2, type1, type2) = self.get_types(tree.children[0], tree.children[1], flag)
            #operand1 = self.dispatch(tree.children[0])
            #operand2 = self.dispatch(tree.children[1])
            #type1 = operand1[0]
            #type2 = operand2[0]
            
            if type1 != type2:
                #allow NUM * TEMP and TEMP * NUM
                if type1=="NUM" and (type2=="F" or type2=="C" or type2=="K"):
                    return type2, str(operand1[1]) + " " + tree.children[2] + " " + str(operand2[1])
                elif (type1=="F" or type1=="C" or type2=="K") and type2=="NUM":
                    return type1, str(operand1[1]) + " " + tree.children[2] + " " + str(operand2[1])
                
                exit("TypeError! " + type1 + " is not of type " +type2)

            else:
                if self.check_if_time(type1) or type1=="F" or type1=="C" or type1=="K":
                    exit("TypeError! Cannot multiply " + type1 + " types together")

                return type1, str(operand1[1]) + " " + tree.children[2] + " " + str(operand2[1])
                    #return self.dispatch(tree.children[0]) + " " + tree.children[2] + " " + self.dispatch(tree.children[1])

    def _power_expression(self, tree, flag=None):

        if len(tree.children) == 1:
            return self.dispatch(tree.children[0], flag) 
        else:
            (operand1, operand2, type1, type2) = self.get_types(tree.children[0], tree.children[1], flag)

            if type1 != "NUM" or type2 != "NUM":
                exit("TypeError! Cannot raise " + type1 + " to " + type2 + ". Must both be numbers");
            else:
                return type1, str(operand1[1]) + "**" + str(operand2[1])

    #this needs to be fixed        
    def _primary_expression(self, tree, flag=None):
        
        if tree.leaf == None:
            arg = self.dispatch(tree.children[0])
            if type(arg) is tuple:
                arg1 = str(arg[1])
            return arg[0], "(" + arg1 + ")"
        else:
            """
            This means this is a variable/ID. 
                Check if variable is in symbol table and return the variable and its type
            """
            #TODO check if variable is in the correct scope
            (varType, value) = self.symbolTable.get(tree.leaf)
            return varType, tree.leaf

    def _primary_expression_not(self, tree, flag=None):
        if tree.leaf == None:
            arg = self.dispatch(tree.children[0])
            if type(arg) is tuple:
                arg = str(arg[1])
            return "BOOLEAN", "not(" + arg + ")"
        else:
            """
            This means this is a variable/ID. 
                Check if variable is in symbol table and return the variable and its type
            """
            #TODO check if variable is in the correct scope
            (varType, value) = self.symbolTable.get(tree.leaf)
            return vartype, tree.leaf
              

    def _primary_expression_boolean(self, tree, flag=None):
        return "BOOLEAN", str(tree.leaf).title()
    
    def _primary_expression_string(self, tree, flag=None):
        return "STRING", tree.leaf


    def _primary_expression_constant(self, tree, flag=None):
        return "NUM", float(tree.leaf)    
    

    def _during_or_expression(self, tree, flag=None):
        if len(tree.children) == 1:
            return self.dispatch(tree.children[0], flag)
        if len(tree.children) == 2:
            #this is stealing lists
            return "((" + self.dispatch(tree.children[0], flag) + ") or (" + self.dispatch(tree.children[1], flag) + "))"
      

    def _during_and_expression(self, tree, flag=None):
        if len(tree.children) == 1:
            arg = self.dispatch(tree.children[0], flag)
            if self.check_if_time(arg) and flag=="EVERY": 
                arg = self.convert_time(arg)
            return arg

        if len(tree.children) == 2:
            arg = self.dispatch(tree.children[1], flag)
            if not self.check_if_time(arg): exit("OH NO. Must use time type in EVERY statements")
            arg = self.convert_time(arg)
            poop = self.dispatch(tree.children[0], flag)
            return "((" + self.dispatchTuple(tree.children[0], flag) + ") and (" + arg + "))"
      
               
    def _every_statement(self, tree, flag=None):
        global everys
        global every_list        
        everys = everys + 1
        everyFlag = "EVERY"

        s = "\ndef every" + str(everys) + "() :\n"
        s += "    print 'executing every" + str(everys) + "'\n"
        
        lines = self.dispatch(tree.children[1]).splitlines()
        for line in lines:
            s+= "    " + line +"\n"

        s += "def condition" + str(everys) + "():\n"
        s += "    print 'checking" + str(everys) + "'\n"
        s += "    if " + self.dispatch(tree.children[0], everyFlag) + ": return True\n"
        s += "every_list.append({'func' : 'every" + str(everys)
        s += "', 'condition' : 'condition" + str(everys) + "'})"
        return s

    def _once_every_statement(self, tree, flag=None):
        global everys
        global every_list        
        everys = everys + 1
        everyFlag = "EVERY"

        s = "\ndef every" + str(everys) + "() :\n"
        s += "    print 'executing once every" + str(everys) + "'\n"

        lines = self.dispatch(tree.children[1]).splitlines()
        for line in lines:
            s+= "    " + line +"\n"

        s += "    happened" + str(everys) + " = False\n"
        s += "def condition" + str(everys) + "():\n"
        s += "    print 'checking" + str(everys) + "'\n"
        s += "    global happened" + str(everys) + "\n"
        s += "    if " + self.dispatch(tree.children[0], everyFlag) + " and happened" + str(everys) + " == False"+ ":\n"
        s += "        happened" + str(everys) + " = True\n"
        s += "        return True\n"
        s += "    if not(" + self.dispatch(tree.children[0], everyFlag) + "):\n"
        s += "        happened" + str(everys) + " = False\n"
        s += "every_list.append({'func' : 'every" + str(everys)
        s += "', 'condition' : 'condition" + str(everys) + "'})"
        return s

    def _iteration_statement(self, tree, flag=None):
        condition = self.dispatch(tree.children[0])
        if type(condition) is tuple:
            condition = condition[1]
        
        #s = "while(" + self.dispatch(tree.children[0]) + "):\n"
        s = "while(" + condition + "):\n"
        lines = self.dispatch(tree.children[1]).splitlines()

        for line in lines:
            s+= "    " + line +"\n"
        return s

    def _selection_statement(self, tree, flag=None):
        condition = self.dispatch(tree.children[0])
        if type(condition) is tuple:
            condition = condition[1]
        if len(tree.children) == 2:
            s = "if(" + condition + "):\n"
            lines = self.dispatch(tree.children[1]).splitlines()
            for line in lines:
                s+= "    " + line +"\n"
            return s
        else:
            s = "if(" + condition + "):\n"
            lines = self.dispatch(tree.children[1]).splitlines()
            for line in lines:
                s+= "    " + line +"\n"
            s += "else:\n"
            lines = self.dispatch(tree.children[2]).splitlines()

            for line in lines:
                s+= "    " + line +"\n"
            return s

    def _print_statement(self, tree, flag=None):
        arg = self.dispatch(tree.children[0])
        if type(arg) is tuple:
            arg = arg[1]

        if type(arg) is int:
            arg = str(arg)
        s = "print " + arg
        return s

    def _log_statement(self, tree, flag=None):
        arg = self.dispatch(tree.children[0])
        if type(arg) is tuple:
            arg = arg[1]

        if type(arg) is int:
            arg = str(arg)
        
            
        s = "log_file.write( str(" + arg + ") + '\\n'" + ")"
        return s

    def _return_statement(self, tree, flag=None):
        self.returnNumber +=1
        arg = self.dispatch(tree.children[0])
        self.returnTable["return"+ str(self.returnNumber)] = arg[0]
        if type(arg) is tuple:
            arg = arg[1]

        if type(arg) is int:
            arg = str(arg)
        s = "return" + str(self.returnNumber) + " " + arg ## add return type
        return s

    def _primary_expression_funct(self, tree, flag= None):
        arg = self.dispatch(tree.children[0])
        funcname = arg.split("(")[0]
        return self.functionTable[funcname][1], arg

    def _function_expression(self, tree, flag=None):
        functiontype = self.functionTable[tree.leaf][1]
        self.symbolTable[tree.leaf] = (functiontype, None)
        if len(tree.children) == 1:
            arg = self.dispatch(tree.children[0])
            #getting the function types
            informallist = arg[0].split(", ")
            if self.functionTable[tree.leaf][0] == "":
                exit("Parameters given but function definition has no parameters")
            formal = self.functionTable[tree.leaf][0].split(", ")
            formallist = list()
            for f in formal:
                formallist.append(self.symbolTable[f][0])
                
            if formallist == informallist:
                return tree.leaf + "(" + str(arg[1]) + ")"
            else:
                exit( "Type error in function params: \nInput " + str(informallist) + " does not match definition " + str(formallist))
        else:
            if self.functionTable[tree.leaf][0] != "":
                exit("No parameters given in function but parameters needed")
            return tree.leaf + "()"
        
    def _for_statement(self, tree, flag=None):
        #for iterator in a range
        or_expression1 = self.dispatch(tree.children[0])
        or_expression2 = self.dispatch(tree.children[1])
        the_id = tree.leaf
        self.symbolTable[tree.leaf] = ["NUM", None] #this might be bad because it just holds a dummy variable but we'll deal
        
        if type(or_expression1) is tuple: or_expression1 = or_expression1[1]
        if type(or_expression2) is tuple: or_expression2 = or_expression2[1]
        if type(or_expression1) is float: or_expression1 = str(int(or_expression1))
        if type(or_expression2) is float: or_expression2 = str(int(or_expression2))
        
        s = "for " + the_id + " in range( " + or_expression1 + " , " + or_expression2 + " + 1 ) : \n"
        lines = self.dispatch(tree.children[2]).splitlines()

        for line in lines:
            s+= "    " + line +"\n"
        return s
    
    def _day_expression(self, tree, flag=None):
        s = ""
        if tree.leaf == "Monday":
            s += "0"
        elif tree.leaf == "Tuesday":
            s += "1"
        elif tree.leaf == "Wednesday":
            s += "2"
        elif tree.leaf == "Thursday":
            s += "3"
        elif tree.leaf == "Friday":
            s += "4"
        elif tree.leaf == "Saturday":
            s += "5"
        elif tree.leaf == "Sunday":
            s += "6"

        return "DAY", s
    
    def _month_expression(self, tree, flag=None):
        s = ""
        if tree.leaf == "January":
            s+= "0"
        elif tree.leaf == 'February':
            s+= "1"
        elif tree.leaf == 'March':
            s+= "2"
        elif tree.leaf == 'April':
            s+= "3"
        elif tree.leaf == 'May':
            s+= "4"
        elif tree.leaf == 'June':
            s+= "5"
        elif tree.leaf == 'July':
            s+= "6"
        elif tree.leaf == 'August':
            s+= "7"
        elif tree.leaf == 'September':
            s+= "8"
        elif tree.leaf == 'October':
            s+= "9"
        elif tree.leaf == 'November':
            s+= "10"
        elif tree.leaf == 'December':
            s+= "11"
        else:
            s+= "12"
        return "MONTH", s

    def _date_time_expression(self, tree, flag=None):
        p = re.compile(r'([0-3]?[0-9])/([01]?[0-9])/([0-9][0-9][0-9][0-9])[ ]([01]?[0-9]):([0-5][0-9][ ])((AM)|(PM))')
        match = p.search(tree.leaf)
        day = int(match.group(1))
        month = int(match.group(2))
        year = int(match.group(3))
        hour = int(match.group(4))
        minute = int(match.group(5))
        
        #check for valid time entries
        #if day > 31 or day < 1:
        #    exit("Error: day value must be between 1 and 31")
        #if month > 12 or month < 1:
        #    exit("Error: month value must be between 1 and 12")
        self.check_date_time('day', day)
        self.check_date_time('month', month)
        if year < 0:
            exit("Error: Invalid year. Year must be a positive value")
        if hour > 24 or hour < 0:
            exit("Error: Invalid hour. Only 24 hours in a day")
        if minute > 59 or minute < 0:
            exit("Error: Invalid minute. Minute must be between 0 and 59")
       
        dateTimeTable = {}
        dateTimeTable['day'] = day
        dateTimeTable['month'] = month
        dateTimeTable['year'] = year
        dateTimeTable['hour'] = hour
        dateTimeTable['minute'] = minute
        
        return "DATETIME", dateTimeTable 

    def _time_expression(self, tree, flag=None):
        p = re.compile(r'([01]?[0-9]):([0-5][0-9])[ ]((AM)|(PM))')
        match = p.search(tree.leaf)
        hour = int(match.group(1))
        minute = int(match.group(2))
        am_pm = match.group(3)
        #print "Hour: " + str(hour)
        #print "Minute: " + minute
        #print "Time of Day: '" + am_pm + "'"
        if am_pm == "PM":
            hour += 12
        #print "Hour: " + str(hour)
        #print "Minute: " + minute
        #print "Time of Day: '" + am_pm + "'"
       
        timeTable = {}
        timeTable['hour'] = hour
        timeTable['minute'] = minute
        timeTable['am_pm'] = am_pm

        return "TIME", timeTable
        #return "datetime.time(" + str(hour) + ", " + minute +")" 

    def _date_expression(self, tree, flag=None):
        p = re.compile(r'([0-3]?[0-9])/([01]?[0-9])/([0-9][0-9][0-9][0-9])')
        match = p.search(tree.leaf)
        day = int(match.group(1))
        month = int(match.group(2))
        year = int(match.group(3))
        
        dateTable = {}
        dateTable['day'] = day
        dateTable['month'] = month
        dateTable['year'] = year
        return "DATE", dateTable
        #return "datetime.date(" + year + ", " + month + ", " + day + ")"


    def _temperature_expression(self, tree, flag=None):
        p = re.compile(r'([0-9]+)[ ]*([CFK])')
        match = p.search(tree.leaf)
        number = str(int(match.group(1)))
        temp_type = match.group(2)
        return temp_type, number 
        #return "Temperature(" + number + ", '" + temp_type + "')"
   
    """
    Used to check if a day, month, year, hour, etc. is valid
    If invalid calls exit()
    check_date_time('month', month)
    """
    def check_date_time(self, time, time_arg):
        return {
            'day': self.check_day, 
           'month': self.check_month
                    }[time]
      #  if year < 0:
      #      exit("Error: Invalid year. Year must be a positive value")
      #  if hour > 24 or hour < 0:
      #      exit("Error: Invalid hour. Only 24 hours in a day")
      #  if minute > 59 or minute < 0:
      #      exit("Error: Invalid minute. Minute must be between 0 and 59")
    def check_day(self, time_arg):
       if time_arg > 31 or time_arg < 1:
           exit("Error: day value must be between 1 and 31"),
    def check_month(self, time_arg):
       if time_arg > 12 or time_arg < 1:
           exit("Error: month value must be between 1 and 12")


    #worth it to use this function?
    def get_types(self, children1, children2, flag=None):
            operand1 = self.dispatch(children1, flag)
            operand2 = self.dispatch(children2, flag)
            type1 = operand1[0]
            type2 = operand2[0]

            return operand1, operand2, type1, type2
    
    #take in a type tuple and return the appropriate python string
    def convert_time(self, arg):
        if arg[0] == "DATETIME":
            arg = "datetime.datetime(" + str(arg[1].get('year')) + ", " + str(arg[1].get('month')) + ", " + str(arg[1].get('day')) + ", " + str(arg[1].get('hour')) + ", " + str(arg[1].get('minute')) + ")"
        elif arg[0] == "DATE":
            arg = "datetime.date(" + str(arg[1].get('year')) + ", " + str(arg[1].get('month')) + ", " + str(arg[1].get('day')) + ")" 
        elif arg[0] == "TIME":
            arg = "datetime.time(" + str(arg[1].get('hour')) + ", " + str(arg[1].get('minute')) +")"
        elif arg[0] == "DAY" : 
            arg = "datetime.datetime.now().weekday() == " + arg[1]
        elif arg[0] == "MONTH":
            arg = "datetime.datetime.now().month() == " + arg[1]
        else:
            return None

        return arg
    
    #check if arg is a tuple of some sort of time type
    def check_if_time(self, arg):
       
        if type(arg) is tuple:
            myType = arg[0]
        else: 
            myType = arg
        if myType == "DATETIME" or myType == "DATE" or myType == "TIME" or myType == "DAY" or myType == "MONTH":
            return True
        return False


class TypeError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
