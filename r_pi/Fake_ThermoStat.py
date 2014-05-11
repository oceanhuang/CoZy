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

class Fake_ThermoStat(object):

    def __init__(self):
        self.on = 0
        self.target = None
    
    def turn_on(self):
        # Turn on the pin and see the LED light up. 
        print 'Heater on'
        self.on = 1

    def turn_off(self):
        print 'Heater off'
        self.on = 0

    def get_temp_value(self):
        tfile = open("r_pi/fake_temp") 
        text = tfile.read() 
        tfile.close() 
        temperature = float(text) 
        return temperature

    def get_temp(self):
        tfile = open("r_pi/fake_temp") 
        text = tfile.read() 
        tfile.close() 
        temperature = float(text)
        temperature = Temperature(temperature, 'C')
        return temperature

    def set_temp(self, target_temp):
        # sets the global temp for this thermostat
        print 'Thermostat set to ' + str(target_temp) + ' C'
        self.target = int(target_temp)
        self.check()

    def check(self):
        if self.get_temp() > self.target and self.on == 1:
            self.turn_off()
        elif self.get_temp() < self.target and self.on == 0:
            self.turn_on()
