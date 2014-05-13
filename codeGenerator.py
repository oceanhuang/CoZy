import traceback
import datetime
import re
import sys
import runtimeError
everys = 0
temp_def ='''
from Temperature import *
'''

def module_exists(module_name):
    try:
        __import__(module_name)
    except ImportError:
        return False
    else:
        return True

if module_exists("RPi.GPIO"):
    thermoStat = '''
from r_pi import ThermoStat
myThermoStat = ThermoStat.Sim_ThermoStat()
'''
else:
    thermoStat = '''
from r_pi import Fake_ThermoStat
myThermoStat = Fake_ThermoStat.Fake_ThermoStat()   
'''

loop_def = '''
while 1:
    for e in every_list:
        if eval(e['condition'] + "()"):
            eval(e['func']+ "()")
    
'''

class codeGenerator(object):
    def __init__(self, tree):
        # Keep track of scopes
        self.scopes = [[]]
        self.scopeDepth = 0
        # Symbols table "id" => {type, value}
        self.symbolTable = {}
        # Function parameter type lookup
        self.functionTable = {}
        self.returnTable = {}
        self.returnNumber = 0
        # Variable to store the code
        self.ret = "import datetime\n" 
        self.ret += "import sys\n"
        self.ret += "every_list = []\n" + "log_file = open('cozyLog.txt', 'a')\n" + temp_def + thermoStat
        self.ret += "print \"Welcome to CoZy \\n==================== \"\n"
        body = self.dispatch(tree)
        body += loop_def
        self.ret += runtimeError.errorBeginning(body)
        self.ret += runtimeError.errorEnd()
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

    def inBlock(self):
        self.scopeDepth += 1
        self.scopes.append([])

    def outBlock(self):
        for variable in self.scopes[self.scopeDepth]:
            del self.symbolTable[variable]
        del self.scopes[self.scopeDepth]
        self.scopeDepth -= 1
        
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
            if type(arg) is tuple:
               arg1 = str(arg[1])
            else:
                arg1 = arg
                
            s = "def " + tree.leaf + "(" + str(arg1) +") :\n"
            self.inBlock() #added scoping
            lines = self.dispatch(tree.children[1]).splitlines()
            for line in lines:
                if "return" in line:
                    functiontype = self.returnTable[line[0:7]]
                    line = line[0:6] + " "+ line[8:len(line)]
                s+= "    " + line +"\n"
            self.outBlock() #added scoping
            self.functionTable[tree.leaf] = (arg,functiontype)
            return s 

        s = "def " + tree.leaf + "( ) :\n"
        self.inBlock()
        lines = self.dispatch(tree.children[0]).splitlines()
        for line in lines:
            if "return" in line:
                functiontype = self.returnTable[line[0:7]]
                line = line[0:6] + " " + line[8:len(line)]
            s+= "    " + line +"\n"
        self.outBlock
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

    def _set_temp_statement(self, tree, flag=None):
        # print tree.children[0]
        arg = self.dispatch(tree.children[0])
        return "myThermoStat.set_temp(" + arg[1] + ".getCelsius())\n"
                

    #whoever wrote this, please have a look at _assignnment_statement_list_index
    def _assignment_statement(self, tree, flag=None):
        arg = self.dispatch(tree.children[0]);
        scpDepth = 0
        for scpDepth in range(0, self.scopeDepth + 1):
            if tree.leaf + "__" + str(scpDepth) + "__" in self.symbolTable:
                var_type = self.symbolTable[tree.leaf + "__" + str(scpDepth) + "__"][0]
                if self.symbolTable[tree.leaf + "__" + str(scpDepth) + "__"][0] != arg[0]:
                    exit(tree.leaf + " is of type " + var_type + ". Cannot assign "  + arg[0] + " to it.")
                break
        self.symbolTable[tree.leaf + "__" + str(scpDepth) + "__"] = [arg[0], arg[1]]
        if scpDepth == self.scopeDepth:
            self.scopes[self.scopeDepth].append(tree.leaf + "__" + str(self.scopeDepth) + "__")
        if type(arg) is tuple:
            arg = arg[1]
        if type(arg) is str:
            if arg.startswith('myThermoStat'):
                self.symbolTable[tree.leaf] = ['GET_TEMP', '']
        # print self.symbolTable #uncomment to check symbol table
        # print self.scopes

        if type(arg) is not str: arg = str(arg)
        string = ""
        if scpDepth != self.scopeDepth:
            string += "global " + tree.leaf + "\n"
        string += tree.leaf + " = " + arg
        return string

    def _get_temp_expression(self, tree, flag=None):
        return "C", "myThermoStat.get_temp()"

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
            # else:
            #     if type1 != "NUM" and tree.children[2] != "!=":
            #         exit("Error: Cannot use '>' or '<' for non-numbers") 

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
            first_left_side = (type1 != "DATE" and type1 != "DATETIME" and type1 != "TIME")
            first_right_side = (type2 != "MINUTES" and type2 != "HOURS" and type2 != "DAYS" and type2 != "MONTHS" and type2 != "YEARS")
            second_left_side = (type1 != "MINUTES" and type1 != "HOURS" and type1 != "DAYS" and type1 != "MONTHS" and type1 != "YEARS")
            second_right_side = (type2 != "DATE" and type2 != "DATETIME" and type2 != "TIME")
            if type1 != type2 and ((first_left_side or first_right_side) and (second_left_side or second_right_side)):
                exit("TypeError! " + type1 + " is not of type " +type2)
            elif type1 == type2:
                if type1=="DAY" or type1=="MONTH" or type1=="DATE" or type1=="TIME" or type1=="DATETIME":
                    exit("TypeError! Cannot add " + type1 + " types together")
            if not ((first_left_side or first_right_side) and (second_left_side or second_right_side)):
                if first_left_side:
                    type1 = type2
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
                if start_day <= end_day:
                    retStr += "("+ str(start_day) + " <= datetime.datetime.now().weekday() <= " + str(end_day) + ")"
                else:
                    retStr += "(("+ str(start_day) + " <= datetime.datetime.now().weekday()) or (datetime.datetime.now().weekday() <= " + str(end_day) + "))"
                return "DAY_RANGE", retStr
            elif type1 == 'MONTH':
                start_month = int(self.get_month_value(tree.children[0].leaf))
                end_month = int(self.get_month_value(tree.children[1].leaf))
                if start_month <= end_month:
                    retStr += "(" + str(start_month) + " <= datetime.datetime.now().month <= " + str(end_month) + ")"
                else:
                    retStr += "(("+ str(start_month) + " <= datetime.datetime.now().month) or (datetime.datetime.now().month <= " + str(end_month) + "))"
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
                sTIME = start_year*10000 + start_month*100 + start_day
                eTIME = end_year*10000 + end_month*100 + end_day
                nTIME = datetime.datetime.now().year*10000 + datetime.datetime.now().month*100 + datetime.datetime.now().day
                if sTIME <= eTIME:
                    retStr += "(" + str(sTIME) 
                    retStr += " <= " + str(nTIME) + "<= " 
                    retStr += str(eTIME) + ")"
                else:
                    retStr += "(" + str(sTIME) 
                    retStr += " <= " + str(nTIME) + " or " + str(nTIME) + " <= " 
                    retStr += str(eTIME) + ")"
                    
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
                sTIME = start_year*100000000 + start_month*1000000 + start_day*10000 + start_hour*100 + start_minute
                nTIME = datetime.datetime.now().year*100000000 + datetime.datetime.now().month*1000000 + datetime.datetime.now().day*10000 + datetime.datetime.now().hour*100 + datetime.datetime.now().minute
                eTIME = end_year*100000000 + end_month*1000000 + end_day*10000 + end_hour*100 + end_minute
                if sTIME <= eTIME:
                    retStr += "(" + str(sTIME)
                    retStr += " <= " +str(nTIME) + " <= " 
                    retStr += str(eTIME) + ")"
                else:
                    retStr += "(" + str(sTIME)
                    retStr += " <= " + str(nTIME) + " or " + str(nTIME) + " <= " 
                    retStr += str(eTIME) + ")"

                return "DATETIME_RANGE", retStr
            elif type1 == "TIME":
                time1 = self.get_time_value(tree.children[0].leaf)
                time2 = self.get_time_value(tree.children[1].leaf)
                start_hour = time1.get("hour")
                end_hour = time2.get("hour")
                start_minute = time1.get("minute")
                end_minute = time2.get("minute")
                sTIME = start_hour*100 + start_minute
                nTIME = datetime.datetime.now().hour*100 + datetime.datetime.now().minute
                eTIME = end_hour*100 + end_minute
                if sTIME <= eTIME:
                    retStr += "("
                    retStr += str(sTIME) + " <= " + str(nTIME) + " <= " + str(eTIME)
                    retStr += ")"
                else:
                    retStr += "("
                    retStr += str(sTIME) + " <= " + str(nTIME) + " or " + str(nTIME) + " <= " + str(eTIME)
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
            for scpDepth in range(0, self.scopeDepth + 1):
                if (tree.leaf + "__" +str(scpDepth) + "__") in self.scopes[scpDepth]:
                    (varType, value) = self.symbolTable.get(tree.leaf + "__" +str(scpDepth) + "__")
                    return varType, tree.leaf, True
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
        # s += "    print 'executing every" + str(everys) + "'\n"
        self.inBlock()
                
        lines = self.dispatch(tree.children[1]).splitlines()
        for line in lines:
            s+= "    " + line +"\n"

        s += "def condition" + str(everys) + "():\n"
        # s += "    print 'checking" + str(everys) + "'\n"
        self.inBlock()
        s += "    if " + self.dispatchTuple(tree.children[0], everyFlag) + ": return True\n"
        s += "every_list.append({'func' : 'every" + str(everys)
        s += "', 'condition' : 'condition" + str(everys) + "'})"
        self.outBlock()
        self.outBlock()
        return s

    def _once_every_statement(self, tree, flag=None):
        global everys
        global every_list        
        everys = everys + 1
        everyFlag = "EVERY"

        s = "happened" + str(everys) + " = False\n"
        s += "\ndef every" + str(everys) + "() :\n"
        self.inBlock()
        # s += "    print 'executing once every" + str(everys) + "'\n"

        lines = self.dispatch(tree.children[1]).splitlines()
        for line in lines:
            s+= "    " + line +"\n"
        s += "def condition" + str(everys) + "():\n"
        # s += "    print 'checking" + str(everys) + "'\n"
        self.inBlock()
        s += "    global happened" + str(everys) + "\n"
        s += "    if " + self.dispatchTuple(tree.children[0], everyFlag) + " and happened" + str(everys) + " == False"+ ":\n"
        s += "        happened" + str(everys) + " = True\n"
        s += "        return True\n"
        s += "    if not(" + self.dispatchTuple(tree.children[0], everyFlag) + "):\n"
        s += "        happened" + str(everys) + " = False\n"
        s += "every_list.append({'func' : 'every" + str(everys)
        s += "', 'condition' : 'condition" + str(everys) + "'})"
        self.outBlock()
        self.outBlock()
        return s

    def _iteration_statement(self, tree, flag=None):
        condition = self.dispatch(tree.children[0])
        if type(condition) is tuple:
            condition = condition[1]
        
        #s = "while(" + self.dispatch(tree.children[0]) + "):\n"
        s = "while(" + condition + "):\n"
        self.inBlock()
        lines = self.dispatch(tree.children[1]).splitlines()

        for line in lines:
            s+= "    " + line +"\n"
        self.outBlock()
        return s

    def _selection_statement(self, tree, flag=None):
        condition = self.dispatch(tree.children[0])
        if type(condition) is tuple:
            condition = condition[1]
        if len(tree.children) == 2:
            s = "if(" + condition + "):\n"
            self.inBlock()
            lines = self.dispatch(tree.children[1]).splitlines()
            for line in lines:
                s+= "    " + line +"\n"
            self.outBlock()
            return s
        else:
            s = "if(" + condition + "):\n"
            self.inBlock()
            lines = self.dispatch(tree.children[1]).splitlines()
            for line in lines:
                s+= "    " + line +"\n"
            self.outBlock()
            s += "else:\n"
            self.inBlock()
            lines = self.dispatch(tree.children[2]).splitlines()
            for line in lines:
                s+= "    " + line +"\n"
            self.outBlock()
            return s

    def _print_statement(self, tree, flag=None):
        arg = self.dispatch(tree.children[0])
        # print arg
        if type(arg) is tuple:
            if arg[0] == "TIME":
                arg = "(" + arg[1] + ").time()"
            else:
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
        if tree.leaf not in self.functionTable:
            exit("Function " + str(tree.leaf) + " not defined")
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
        self.inBlock()
        lines = self.dispatch(tree.children[2]).splitlines()

        for line in lines:
            s+= "    " + line +"\n"
        self.outBlock()
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
        string = "datetime.datetime.now().month == " + month
        return "MONTH", string

    def get_month_value(self, month):
        s = ''
        if month == "January":
            s = "1"
        elif month == 'February':
            s = "2"
        elif month == 'March':
            s = "3"
        elif month == 'April':
            s = "4"
        elif month == 'May':
            s = "5"
        elif month == 'June':
            s = "6"
        elif month == 'July':
            s = "7"
        elif month == 'August':
            s = "8"
        elif month == 'September':
            s = "9"
        elif month == 'October':
            s = "10"
        elif month == 'November':
            s = "11"
        elif month == 'December':
            s = "12"
        else:
            s = "13"
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
        string = "datetime.datetime(100,1,1," + str(timeTable.get('hour')) + ", " + str(timeTable.get('minute')) +")"
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
        string = "Temperature(" + number + ", '" + temp_type + "')"
        return temp_type, string

    def _days_expression(self, tree, flag=None):
        p = re.compile(r'([0-9]+)[ ]Days')
        match = p.search(tree.leaf)
        number = match.group(1)
        string = "datetime.timedelta(days=" + number + ")"
        return "DAYS",  string

    def _months_expression(self, tree, flag=None):
        p = re.compile(r'([0-9]+)[ ]Months')
        match = p.search(tree.leaf)
        number = match.group(1)
        string = "datetime.timedelta(weeks=" + number*4 + ")"
        return "MONTHS",  string
    
    def _years_expression(self, tree, flag=None):
        p = re.compile(r'([0-9]+)[ ]Years')
        match = p.search(tree.leaf)
        number = match.group(1)
        string = "datetime.timedelta(weeks=" + number*4*12 + ")"
        return "YEARS",  string

    def _hours_expression(self, tree, flag=None):
        p = re.compile(r'([0-9]+)[ ]Hours')
        match = p.search(tree.leaf)
        number = match.group(1)
        string = "datetime.timedelta(hours=" + number + ")"
        return "HOURS",  string

    def _minutes_expression(self, tree, flag=None):
        p = re.compile(r'([0-9]+)[ ]Minutes')
        match = p.search(tree.leaf)
        number = match.group(1)
        string = "datetime.timedelta(minutes=" + number + ")"
        return "MINUTES",  string
        
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
            arg = "datetime.datetime.now().month == " + arg[1]
        else:
            return None

        return arg
    
    #check if arg is a tuple of some sort of time type
    def check_if_time(self, arg):
       
        if type(arg) is tuple:
            myType = arg[0]
        else: 
            myType = arg
        if myType == "DATETIME" or myType == "DATE" or myType == "TIME" or myType == "DAY" or myType == "MONTH"\
        or myType == "TIME_RANGE" or myType == "DAY_RANGE" or myType == "MONTH_RANGE" or myType == "DATE_RANGE" or myType == "DATETIME_RANGE": 
            return True
        return False

class TypeError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
