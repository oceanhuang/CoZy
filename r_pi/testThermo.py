import RPi.GPIO as GPIO 
from ThermoStat import Sim_ThermoStat
import time

GPIO.setwarnings(False)
GPIO.cleanup()

myThermoStat = Sim_ThermoStat()

# myThermoStat.turn_on()
# time.sleep(2)
# myThermoStat.turn_off()

myThermoStat.set_temp(27)

for x in xrange(1,20):
    time.sleep(1)
    print 'Current Temp: ' + str(myThermoStat.get_temp())
    myThermoStat.check()

GPIO.cleanup()
