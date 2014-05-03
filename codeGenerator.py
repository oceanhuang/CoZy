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
        # Variable to store the code
        self.ret = "import datetime\n" + "every_list = []\n" + temp_def + self.dispatch(tree)
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


    def _statement_list(self, tree, flag=None):
        return self.dispatch(tree.children)

    def _statement(self, tree, flag=None):
        return self.dispatch(tree.children) + "\n"

    def _assignment_statement(self, tree, flag=None):
        arg = self.dispatch(tree.children[0]);
        if type(arg) is tuple:
            if arg[0] == "F" or arg[0] == "C" or arg[0] == "K":
                self.symbolTable[tree.leaf] = [arg[0], arg[1]]
                arg = "Temperature(" + str(arg[1]) + ", '" + arg[0] + "')"
            elif arg[0] == "DATETIME":
                self.symbolTable[tree.leaf] = [arg[0], arg[1]]
                arg = "datetime.datetime(" + str(arg[1].get('year')) + ", " + str(arg[1].get('month')) + ", " + str(arg[1].get('day')) + ", " + str(arg[1].get('hour')) + ", " + str(arg[1].get('minute')) + ")"
            elif arg[0] == "DATE":
                self.symbolTable[tree.leaf] = [arg[0], arg[1]]
                arg = "datetime.date(" + str(arg[1].get('year')) + ", " + str(arg[1].get('month')) + ", " + str(arg[1].get('day')) + ")" 
            elif arg[0] == "TIME":
                self.symbolTable[tree.leaf] = [arg[0], arg[1]]
                arg = "datetime.time(" + str(arg[1].get('hour')) + ", " + str(arg[1].get('minute')) +")"
            elif arg[0] == "BOOL" or arg[0] == "NUM":
                self.symbolTable[tree.leaf] = [arg[0], arg[1]]
                arg = arg[1]
            else:
                #TODO add to symbol table
                arg = arg[1]

        print self.symbolTable
        if type(arg) is not str: arg = str(arg)
        return tree.leaf + " = " + arg

    def _or_expression(self, tree, flag=None):
        
        if len(tree.children) == 1:
            return self.dispatch(tree.children[0])
        else:
            (operand1, operand2, type1, type2) = self.get_types(tree.children[0], tree.children[1])
            return "BOOL", str(operand[1]) + " " + tree.children[2] + " " + str(operand2[1])
            #return self.dispatch(tree.children[0]) + " " + tree.children[2] + " " + self.dispatch(tree.children[1])  

    def _and_expression(self, tree, flag=None):
        
        if len(tree.children) == 1:
            return self.dispatch(tree.children[0])
        else:
            (operand1, operand2, type1, type2) = self.get_types(tree.children[0], tree.children[1])
            
            return "BOOL", str(operand1[1]) + " " + tree.children[2] + " " + str(operand2[1])
            #return self.dispatch(tree.children[0]) + " " + tree.children[2] + " " + self.dispatch(tree.children[1])  

    def _equality_expression(self, tree, flag=None):
        
        if len(tree.children) == 1:
            return self.dispatch(tree.children[0])
        else:
            (operand1, operand2, type1, type2) = self.get_types(tree.children[0], tree.children[1])

            if type1 != type2:
                exit("TypeError! Cannot compare objects of type " + type1 + " and objects of type " + type2)

            return "BOOL", str(operand1[1]) + " " + tree.children[2] + " " + str(operand2[2])
            #return self.dispatch(tree.children[0]) + " " + tree.children[2] + " " + self.dispatch(tree.children[1])  

    def _relational_expression(self, tree, flag=None):
        
        if len(tree.children) == 1:
            return self.dispatch(tree.children[0])
        else:

            (operand1, operand2, type1, type2) = self.get_types(tree.children[0], tree.children[1])
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
            return self.dispatch(tree.children[0])
        else:
            
            (operand1, operand2, type1, type2) = self.get_types(tree.children[0], tree.children[1])
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
            return self.dispatch(tree.children[0]) 
        else:
            
            (operand1, operand2, type1, type2) = self.get_types(tree.children[0], tree.children[1])
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
                if type1=="DAY" or type1=="MONTH" or type1=="DATE" or type1=="TIME" or type1=="DATETIME":
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
                start_day = operand1[1].get("day")
                end_day = operand2[1].get("day")
                start_month = operand1[1].get("month")
                end_month = operand2[1].get("month")
                start_year = operand1[1].get("year")
                end_year = operand2[1].get("year")
                retStr += "("
                #Day
                retStr += "(" + str(start_day) + " <= datetime.datetime.now().day <= " + str(end_day) + ")"
                retStr += " and ("
                #Month
                retStr += str(start_month) + " <= datetime.datetime.now().month <= "+ str(end_month) + ")"
                retStr += " and ("
                #Year
                retStr += str(start_year) + " <= datetime.datetime.now().year <= "+ str(end_year) + ")"
                retStr += ")"
                return "DATE_RANGE", retStr
            elif type1 == "DATETIME":
                start_day = operand1[1].get("day")
                end_day = operand2[1].get("day")
                start_month = operand1[1].get("month")
                end_month = operand2[1].get("month")
                start_year = operand1[1].get("year")
                end_year = operand2[1].get("year")
                start_hour = operand1[1].get("hour")
                end_hour = operand2[1].get("hour")
                start_minute = operand1[1].get("minute")
                end_minute = operand2[1].get("minute")
                retStr += "("
                #Day
                retStr += "(" + str(start_day) + " <= datetime.datetime.now().day <= " + str(end_day) + ")"
                retStr += " and ("
                #Month
                retStr += str(start_month) + " <= datetime.datetime.now().month <= " + str(end_month) + ")"
                retStr += " and ("
                #Year
                retStr += str(start_year) + " <= datetime.datetime.now().year <= " + str(end_year) + ")"
                retStr += " and ("
                #hour
                retStr += str(start_hour) + " <= datetime.datetime.now().hour <= " + str(end_hour) + ")"
                retStr += " and ("
                #Minute
                retStr += str(start_minute) + " <= datetime.datetime.now().minute <= " + str(start_minute) + ")"
                retStr += ")"
                return "DATETIME_RANGE", retStr
            elif type1 == "TIME":
                start_hour = operand1[1].get("hour")
                end_hour = operand2[1].get("hour")
                start_minute = operand1[1].get("minute")
                end_minute = operand2[1].get("minute")
                retStr += "(("
                retStr += str(start_hour) + " <= datetime.datetime.now().hour <= " + str(end_hour) + ")"
                retStr += " and ("
                #Minute
                retStr += str(start_minute) + " <= datetime.datetime.now().minute <= " + str(start_minute) + ")"
                retStr += ")"
                return "TIME_RANGE", retStr
            else:
                exit("TypeError: Cannot use 'to' for type: " + type1)

    def _primary_expression(self, tree, flag=None):
        if tree.leaf == None:
            return "( " + self.dispatch(tree.children[0]) + " )"
        else:
            
            # This means this is a variable/ID. 
            # Check if variable is in symbol table and return the variable and its type
            
            #TODO check if variable is in the correct scope
            (varType, value) = self.symbolTable.get(tree.leaf)
            return varType, tree.leaf
    
    def _primary_expression_constant(self, tree, flag=None):
        return "NUM", int(tree.leaf)    
    
    def _every_statement(self, tree, flag=None):
        global everys
        global every_list        
        everys = everys + 1
        
        s = "\ndef every" + str(everys) + "() :\n"
        s += "    print 'executing every" + str(everys) + "'\n"

        lines = self.dispatch(tree.children[1]).splitlines()
        for line in lines:
            s+= "    " + line +"\n"

        s += "def condition" + str(everys) + "():\n"
        s += "    print 'checking" + str(everys) + "'\n"
        s += "    if " + self.dispatch(tree.children[0]) + ": return True\n"
        s += "every_list.append({'func' : 'every" + str(everys)
        s += "', 'condition' : 'condition" + str(everys) + "'})"
        return s

    def _iteration_statement(self, tree, flag=None):
        s = "while(" + self.dispatch(tree.children[0]) + "):\n"
        lines = self.dispatch(tree.children[1]).splitlines()

        for line in lines:
            s+= "    " + line +"\n"
        return s

    def _selection_statement(self, tree, flag=None):
        if len(tree.children) == 2:
            s = "if(" + self.dispatch(tree.children[0])[1] + "):\n"
            lines = self.dispatch(tree.children[1]).splitlines()
            for line in lines:
                s+= "    " + line +"\n"
            return s
        else:
            s = "if(" + self.dispatch(tree.children[0])[1] + "):\n"
            lines = self.dispatch(tree.children[1]).splitlines()
            for line in lines:
                s+= "    " + line +"\n"
            s += "else:\n"
            lines = self.dispatch(tree.children[2]).splitlines()

            for line in lines:
                s+= "    " + line +"\n"
            return s

    def _print_statement(self, tree, flag=None):
        s = "print " + self.dispatch(tree.children[0])
        return s

    def _for_statement(self, tree, flag=None):
        #for iterator in a range
        s = "for " + self.dispatch(tree.children[0]) + " in range( " + self.dispatch(tree.children[1]) + " , " + self.dispatch(tree.children[2]) + " + 1 ) : \n"
        lines = self.dispatch(tree.children[3]).splitlines()

        for line in lines:
            s+= "    " + line +"\n"
        return s
    
    def _day_expression(self, tree, flag=None):
        s = "datetime.datetime.now().weekday() == "
        s += self.get_day_value(tree.leaf)
        return "DAY", s

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
        else:
            exit("WrongDay: " + day + "is not a valid day")


    def _month_expression(self, tree, flag=None):
        s = "datetime.datetime.now().month() == " + self.get_month_value(tree.leaf)
        return "MONTH", s


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
    def get_types(self, children1, children2):
            operand1 = self.dispatch(children1)
            operand2 = self.dispatch(children2)
            type1 = operand1[0]
            type2 = operand2[0]

            return operand1, operand2, type1, type2
       

class TypeError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
