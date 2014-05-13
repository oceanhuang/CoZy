import sys
sys.path.append('..')
from Temperature import *
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
        self.target = float(target_temp)
        self.check()

    def check(self):
        if self.get_temp_value() > self.target and self.on == 1:
            self.turn_off()
        elif self.get_temp_value() < self.target and self.on == 0:
            self.turn_on()
