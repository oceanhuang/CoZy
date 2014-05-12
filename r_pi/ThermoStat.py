import RPi.GPIO as GPIO 

class Temperature(object):
    def __init__(self, number, tempType):
        self.startType = tempType
        if tempType == 'K':
            self.KTemp = number
            self.CTemp = number - 273.15
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

    def __class__(self):
        return "Temperature"

    def __str__(self):
        if self.startType == ' K':
            return str(self.KTemp) + ' K'
        elif self.startType == 'C':
            return str(self.CTemp) + ' C'
        elif self.startType == 'F':
            return str(self.FTemp) + ' F'

    def __add__(self, other):
        if other.__class__() == "Temperature":
            temp = Temperature(self.CTemp + other.getCelsius(), 'C')
            temp.startType = self.startType
            return temp
        else:
            return NotImplemented

    def __sub__(self, other):
        if other.__class__() == "Temperature":
            temp = Temperature(self.CTemp - other.getCelsius(), 'C')
            temp.startType = self.startType
            return temp
        else:
            return NotImplemented

class Sim_ThermoStat(object):

    def __init__(self):
        self.on = 0
        GPIO.setmode(GPIO.BCM) 
        # Set up the pin you are using. 18 in this case 
        GPIO.setup(18, GPIO.OUT) 
        self.target = None
    
    def turn_on(self):
        # Turn on the pin and see the LED light up. 
        print 'Heater on'
        GPIO.output(18, GPIO.HIGH) 
        self.on = 1

    def turn_off(self):
        print 'Heater off'
        GPIO.output(18, GPIO.LOW)
        self.on = 0

    def get_temp_value(self):
        tfile = open("/sys/bus/w1/devices/28-00000554bd80/w1_slave") 
        text = tfile.read() 
        tfile.close() 
        secondline = text.split("\n")[1] 
        temperaturedata = secondline.split(" ")[9] 
        temperature = float(temperaturedata[2:]) 
        temperature = temperature / 1000 
        return temperature

    def get_temp(self):
        return Temperature(self.get_temp_value(), 'C')

    def set_temp(self, target_temp):
        # sets the global temp for this thermostat
        print 'Thermostat set to ' + str(target_temp) + ' C'
        self.target = int(target_temp)
        self.check()

    def check(self):
        if self.get_temp_value() > self.target and self.on == 1:
            self.turn_off()
        elif self.get_temp_value() < self.target and self.on == 0:
            self.turn_on()
