import traceback
import datetime
import re
import sys
everys = 0
temp_def ='''
class Temperature:
    def __init__(self, number, tempType):
        self.startType = tempType
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
    def __str__(self):
        if self.startType == ' K':
            return str(self.KTemp) + ' K'
        elif self.startType == 'C':
            return str(self.CTemp) + ' C'
        elif self.startType == 'F':
            return str(self.FTemp) + ' F'
'''



class codeGenerator(object):
    def __init__(self, tree):
        # Keep track of scopes
        self.scopes = [[]]
        self.scopeDepth = 0
        # Symbols table "id" => {type, value}
        self.symbolTable = {}
        # Variable to store the code
        self.ret = "import datetime\n" + "every_list = []\n" + "log_file = open('cozyLog.txt', 'a')\n" + temp_def + self.dispatch(tree) + '\n'
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

    def inBlock(self, tree, flag=None):
        self.scopeDepth += 1
        self.scopes.append([])

    def outBlock(self, tree, flag=None):
        for variable in self.scopes[self.scopeDepth]:
            del self.symbolTable[variable]
        del self.scopes[self.scopeDepth]
        self.scopeDepth -= 1
        
    def _program(self, tree, flag=None):
        return self.dispatch(tree.children)

    def _external_declaration(self, tree, flag=None):
        return self.dispatch(tree.children)

    # very basic function definition
    def _function_definition(self, tree, flag=None):
        s = "def " + tree.children[0] + "(" + self.dispatch(tree.children[1])+") :\n"
        lines = self.dispatch(tree.children[2]).splitlines()

        for line in lines:
            s+= "    " + line +"\n"
        return s

    def _function_param_list(self, tree, flag=None):
        if len(tree.children)==0:
            return ''
        else:
            return self.dispatch(tree.children[0])

    def _function_param(self, tree, flag=None):
        if tree.leaf==None:
           return  self.dispatch(tree.children[0]) + "," + self.dispatch(tree.children[1])
        else:
           return tree.leaf

    def _function_param_end(self, tree, flag=None):
        return tree.leaf


    
    def _list_start(self, tree, flag=None):
        if len(tree.children)==0:
            return "[]"
        else:
            return "[" + self.dispatch(tree.children[0]) + "]"
    
    def _list_expression(self, tree, flag=None):
        if len(tree.children) == 1:
            return self.dispatchTuple(tree.children[0])
        else:
            return self.dispatchTuple(tree.children[0]) + ", " + self.dispatchTuple(tree.children[1])
        
    def _list_index_double(self, tree, flag=None):
        return self.dispatchTuple(tree.children[0]) + "[ int(" + self.dispatchTuple(tree.children[1]) + ") ]"

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
        return tree.leaf + ".pop( int( " + self.dispatchTuple(tree.children[0]) + "))"


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
        if tree.leaf + "__" + str(self.scopeDepth) + "__" in self.symbolTable:
            var_type = self.symbolTable[tree.leaf + "__" + str(self.scopeDepth) + "__"][0]
            if self.symbolTable[tree.leaf + "__" + str(self.scopeDepth) + "__"][0] != arg[0]:
                exit(tree.leaf + " is of type " + var_type + ". Cannot assign "  + arg[0] + " to it.")

        self.symbolTable[tree.leaf + "__" + str(self.scopeDepth) + "__"] = [arg[0], arg[1]]
        self.scopes[self.scopeDepth].append(tree.leaf + "__" + str(self.scopeDepth) + "__")
        if type(arg) is tuple:
            arg = arg[1]
        # print self.symbolTable #uncomment to check symbol table
        # print self.scopes
        if type(arg) is not str: arg = str(arg)
        return tree.leaf + " = " + arg

    #not sure whether this actually works with the symbol table and everything
    def _assignment_statement_list_index(self, tree, flag=None):
        arg = self.dispatch(tree.children[1]);
        listIndex = self.dispatch(tree.children[0])
        self.symbolTable[listIndex] = [arg[0], arg[1]]
        if type(arg) is tuple:
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

            return "BOOL", str(operand1[1]) + " " + tree.children[2] + " " + str(operand2[1])
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
                print self.symbolTable
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


    def _to_expression(self, tree, flag=None):
        if len(tree.children) == 1:
            return self.dispatch(tree.children[0])
        else:
            retStr = ""
            (operand1, operand2, type1, type2) = self.get_types(tree.children[0], tree.children[1])
            if type1 != type2:
                exit("TypeError! Cannot have range of different types")
            elif type1 == 'DAY':
                start_day = int(self.get_day_value(tree.children[0].leaf))
                end_day = int(self.get_day_value(tree.children[1].leaf))
                retStr += "("+ str(start_day) + " <= datetime.datetime.now().weekday() <= " + str(end_day) + ")"
                return "DAY_RANGE", retStr
            elif type1 == 'MONTH':
                start_month = int(self.get_month_value(tree.children[0].leaf))
                end_month = int(self.get_month_value(tree.children[1].leaf))
                retStr += "(" + str(start_month) + " <= datetime.datetime.now().month <= " + str(end_month) + ")"
                return "MONTH_RANGE", retStr
            elif type1 == "DATE":
                dateTable1 = self.get_date_value(tree.children[0].leaf)
                dateTable2 = self.get_date_value(tree.children[1].leaf)
                start_day = dateTable1.get("day")
                end_day = dateTable2.get("day")
                start_month = dateTable1.get("month")
                end_month = dateTable2.get("month")
                start_year = dateTable1.get("year")
                end_year = dateTable2.get("year")
                #Day
                retStr += "(" + str(start_year*10000 + start_month*100 + start_day)
                retStr += " <= datetime.datetime.now().year*10000 + datetime.datetime.now().month*100 + datetime.datetime.now().day <= " 
                retStr += str(end_year*10000 + end_month*100 + end_day) + ")"
                return "DATE_RANGE", retStr
            elif type1 == "DATETIME":
                dateTimeTable1 = self.get_date_time_values(tree.children[0].leaf)
                dateTimeTable2 = self.get_date_time_values(tree.children[1].leaf)
                start_day = dateTimeTable1.get("day")
                end_day = dateTimeTable2.get("day")
                start_month = dateTimeTable1.get("month")
                end_month = dateTimeTable2.get("month")
                start_year = dateTimeTable1.get("year")
                end_year = dateTimeTable2.get("year")
                start_hour = dateTimeTable1.get("hour")
                end_hour = dateTimeTable2.get("hour")
                start_minute = dateTimeTable1.get("minute")
                end_minute = dateTimeTable2.get("minute")
                retStr += "(" + str(start_year*100000000 + start_month*1000000 + start_day*10000 + start_hour*100 + start_minute)
                retStr += " <= datetime.datetime.now().year*100000000 + datetime.datetime.now().month*1000000 + datetime.datetime.now().day*10000 + datetime.datetime.now().hour*100 + datetime.datetime.now().minute <= " 
                retStr += str(end_year*100000000 + end_month*1000000 + end_day*10000 + end_hour*100 + end_minute) + ")"

                return "DATETIME_RANGE", retStr
            elif type1 == "TIME":
                time1 = self.get_time_value(tree.children[0].leaf)
                time2 = self.get_time_value(tree.children[1].leaf)
                start_hour = time1.get("hour")
                end_hour = time2.get("hour")
                start_minute = time1.get("minute")
                end_minute = time2.get("minute")
                retStr += "("
                #time
                retStr += str(start_hour*100 + start_minute) + " <= datetime.datetime.now().hour*100 + datetime.datetime.now().minute <= " + str(end_hour*100 + end_minute)
                retStr += ")"
                return "TIME_RANGE", retStr
            else:
                exit("TypeError: Cannot use 'to' for type: " + type1)


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
            else:
                arg1 = arg
            return arg[0], "(" + arg1 + ")"
        else:
            # This means this is a variable/ID. 
            # Check if variable is in symbol table and return the variable and its type
            if (tree.leaf + "__" +str(self.scopeDepth) + "__") in self.scopes[self.scopeDepth]:
                (varType, value) = self.symbolTable.get(tree.leaf + "__" +str(self.scopeDepth) + "__")
                return varType, tree.leaf, True
            else:
                exit("Variable " + tree.leaf + " not declared")

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
            if tree.leaf in self.scopes[self.scopeDepth]:
                (varType, value) = self.symbolTable.get(tree.leaf)
                return varType, tree.leaf, True
            else:
                exit("Variable " + tree.leaf + " not declared")
              

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
            return "((" + self.dispatchTuple(tree.children[0], flag) + ") or (" + self.dispatchTuple(tree.children[1], flag) + "))"
      

    def _during_and_expression(self, tree, flag=None):
        if len(tree.children) == 1:
            arg = self.dispatch(tree.children[0], flag)
            if self.check_if_time(arg) and flag=="EVERY": 
                arg = arg[1]

            return arg

        if len(tree.children) == 2:
            arg = self.dispatch(tree.children[1], flag)
            if not self.check_if_time(arg): exit("OH NO. Must use time type in EVERY statements")
            arg = arg[1]
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

        if type(arg) is int or type(arg) is float:
            arg = str(arg)
        s = "print " + arg
        return s

    def _log_statement(self, tree, flag=None):
        arg = self.dispatch(tree.children[0])
        if type(arg) is tuple:
            arg = arg[1]

        if type(arg) is int or type(arg) is float:
            arg = str(arg)
        
            
        s = "log_file.write( str(" + arg + ") + '\\n'" + ")"
        return s

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
        day = self.get_day_value(tree.leaf)
        string = "datetime.datetime.now().weekday() == " + day
        return "DAY", string

    def get_day_value(self, day):
        if day == "Monday":
            return "0"
        elif day == "Tuesday":
            return "1"
        elif day == "Wednesday":
            return "2"
        elif day == "Thursday":
            return "3"
        elif day == "Friday":
            return "4"
        elif day == "Saturday":
            return "5"
        elif day == "Sunday":
            return "6"
        exit("WrongDay: " + day + "is not a valid day")


    def _month_expression(self, tree, flag=None):
        month = self.get_month_value(tree.leaf)
        string = "datetime.datetime.now().month() == " + month
        return "MONTH", string

    def get_month_value(self, month):
        s = ''
        if month == "January":
            s = "0"
        elif month == 'February':
            s = "1"
        elif month == 'March':
            s = "2"
        elif month == 'April':
            s = "3"
        elif month == 'May':
            s = "4"
        elif month == 'June':
            s = "5"
        elif month == 'July':
            s = "6"
        elif month == 'August':
            s = "7"
        elif month == 'September':
            s = "8"
        elif month == 'October':
            s = "9"
        elif month == 'November':
            s = "10"
        elif month == 'December':
            s = "11"
        else:
            s = "12"
        return s

    def _date_time_expression(self, tree, flag=None):
        dateTimeTable = self.get_date_time_values(tree.leaf)
        string = "datetime.datetime(" + str(dateTimeTable.get('year')) + ", " + str(dateTimeTable.get('month')) + ", " + str(dateTimeTable.get('day')) + ", " + str(dateTimeTable.get('hour')) + ", " + str(dateTimeTable.get('minute')) + ")"
        return "DATETIME", string

    def get_date_time_values(self, date_time_str):
        p = re.compile(r'([0-3]?[0-9])/([01]?[0-9])/([0-9]+)[ ]([01]?[0-9]):([0-5][0-9][ ])((AM)|(PM))')
        match = p.search(date_time_str)
        day = int(match.group(1))
        month = int(match.group(2))
        year = int(match.group(3))
        hour = int(match.group(4))
        minute = int(match.group(5))
        self.check_date_time('day', day)
        self.check_date_time('month', month)
        if year < 0:
            exit("Error: Invalid year. Year must be a positive value")
        if hour > 24 or hour < 0:
            exit("Error: Invalid hour. Only 24 hours in a day")
        if minute > 59 or minute < 0:
            exit("Error: Invalid minute. Minute must be between 0 and 59")
        dateTimeTable = {}
        dateTimeTable['day'] = int(match.group(1))
        dateTimeTable['month'] = int(match.group(2))
        dateTimeTable['year'] = int(match.group(3))
        dateTimeTable['hour'] = int(match.group(4))
        dateTimeTable['minute'] = int(match.group(5))
        return dateTimeTable
        

    def _time_expression(self, tree, flag=None):
        timeTable = self.get_time_value(tree.leaf)
        string = "datetime.time(" + str(timeTable.get('hour')) + ", " + str(timeTable.get('minute')) +")"
        return "TIME", string

    def get_time_value(self, time_str):
        p = re.compile(r'([01]?[0-9]):([0-5][0-9])[ ]((AM)|(PM))')
        match = p.search(time_str)
        hour = int(match.group(1))
        minute = int(match.group(2))
        am_pm = match.group(3)
        if am_pm == "PM":
            hour += 12
       
        timeTable = {}
        timeTable['hour'] = hour
        timeTable['minute'] = minute
        timeTable['am_pm'] = am_pm
        return timeTable


    def _date_expression(self, tree, flag=None):
        dateTable = self.get_date_value(tree.leaf)
        string = "datetime.date(" + str(dateTable.get('year')) + ", " + str(dateTable.get('month')) + ", " + str(dateTable.get('day')) + ")"
        return "DATE", string

    def get_date_value(self, date_str):
        # print "type" + str(type(date_str))
        # print date_str
        p = re.compile(r'([0-3]?[0-9])/([01]?[0-9])/([0-9]+)')
        match = p.search(date_str)
        day = int(match.group(1))
        month = int(match.group(2))
        year = int(match.group(3))
        
        dateTable = {}
        dateTable['day'] = day
        dateTable['month'] = month
        dateTable['year'] = year
        return dateTable



    def _temperature_expression(self, tree, flag=None):
        p = re.compile(r'([0-9]+)[ ]*([CFK])')
        match = p.search(tree.leaf)
        number = str(int(match.group(1)))
        temp_type = match.group(2)
        return temp_type, number 
   
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
