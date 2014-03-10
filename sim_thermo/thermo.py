import sys
import time

curr_temp = int(sys.argv[1])
target_temp = int(sys.argv[2])

print 'target temp: ' + str(curr_temp)

while curr_temp < target_temp:
    time.sleep(2) # every 20 seconds, up 1 degree
    print 'current temp:' + str(curr_temp);
    curr_temp += 1

print 'reached target_temp..'