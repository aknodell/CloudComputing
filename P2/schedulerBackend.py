######################################
###    Aaron Knodell               ###
###    420007922                   ###
###    CSCE 689-607 - Fall 2018    ###
###    Project 2                   ###
######################################

from schedulerConstants import *
from resourceManager import ResourceManager
from nodeManager import NodeManager

rm = ResourceManager()

def is_valid_int(n):
	isValid = VALID
	
	try:
		if int(n) < 1:
			isValid = [False, INVALID_RANGE_MESSAGE]
	except ValueError, e:
		isValid = [False, NOT_AN_INT_MESSAGE]
		
	return isValid

def is_valid_machine_config(config):
	isValid = VALID
	
	if len(config.split()) != 3:
		isValid = [False, INVALID_CONFIG_MESSAGE % ('machine')]
	else:
		for value in config.split():
			isValid = is_valid_int(value)
			if isValid[0] == False:
				break
		
	return isValid
		
def is_valid_pool_config(config):
	isValid = VALID
	
	if len(config.split()) > 6 or len(config.split()) < 2:
		isValid = [False, INVALID_CONFIG_MESSAGE % ('pool')]
	else:
		if config.split()[1] not in SCHEDULING_TYPES:
			isValid = [False, INVALID_SCHEDULING_TYPE_MESSAGE % ('pool')]
							
		for value in config.split()[2:]:
			isValid = is_valid_int(value)
			if isValid[0] == False:
				break
				
	return isValid
	
def is_valid_job_config(config):
	isValid = VALID
	
	if len(config.split()) != 5 and len(config.split()) != 6:
		isValid = [False, INVALID_CONFIG_MESSAGE % ('job')]
	else:
		for value in config.split()[1:]:
			isValid = is_valid_int(value)
			if isValid[0] == False:
				break
				
		if isValid[0] and len(config.split()) == 6:
			if int(config.split()[5]) not in PRIORITY_LEVELS:
				isValid = [False, INVALID_PRIORITY_LEVEL_MESSAGE]

	return isValid
	

def load_configurations(mode = 'fifo'):
	loadSuccess = VALID
	rm.setMode(mode)
	
	CONFIG_FUNCTIONS = {
			CLUSTER_CONFIG_FILE:{'is_valid':is_valid_machine_config, 'add':rm.add_new_machine},
			POOL_CONFIG_FILE:{'is_valid':is_valid_pool_config, 'add':rm.add_new_pool},
			JOB_CONFIG_FILE:{'is_valid':is_valid_job_config, 'add':rm.appManager.add_new_job}
			}

	for config in CONFIG_FILES:
		try:
			configFile = open(config, 'r')
			functions = CONFIG_FUNCTIONS[config]
			for line in configFile:
				if functions['is_valid'](line)[0]:
					functions['add'](line)
				else:
					loadSuccess = functions['is_valid'](line)
					break
			configFile.close()
			
			if loadSuccess[0] == False:
				break

		except IOError, e:
			loadSuccess = [False, UNABLE_TO_FIND_FILE_MESSAGE % (config)]
			break
			
	return loadSuccess

