######################################
###    Aaron Knodell               ###
###    420007922                   ###
###    CSCE 689-607 - Fall 2018    ###
###    Project 2                   ###
######################################

import schedulerBackend
#import threading
import schedulerConstants
import time

command = raw_input('Fair or FIFO:\n>>').lower()
while command not in schedulerConstants.SCHEDULING_TYPES:
	command = raw_input('Fair or FIFO:\n>>').lower()

run = schedulerBackend.load_configurations(command.lower())

if run[0] == False:
	print run[1]
else:
	schedulerBackend.rm.run()
		
	print 'goodbye!'
