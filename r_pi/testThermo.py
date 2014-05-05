import RPi.GPIO as GPIO 
from r_pi import Sim_ThermoStat
import time

myThermoStat = Sim_ThermoStat()

# myThermoStat.turn_on()
# time.sleep(2)
# myThermoStat.turn_off()

# myTermoStat.set_temp(29)

for x in xrange(1,20):
    time.sleep(1)
    print myThermoStat.get_temp()
    myThermoStat.check

GPIO.cleanup()