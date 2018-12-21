######################################
###    Aaron Knodell               ###
###    420007922                   ###
###    CSCE 689-607 - Fall 2018    ###
###    Project 2                   ###
######################################

EXIT_COMMANDS = ['exit', 'quit', 'q']

CLUSTER_CONFIG_FILE = 'clusterConfig.txt'
POOL_CONFIG_FILE = 'poolConfig.txt'
JOB_CONFIG_FILE = 'jobConfig.txt'

CONFIG_FILES = [CLUSTER_CONFIG_FILE, POOL_CONFIG_FILE, JOB_CONFIG_FILE]

SCHEDULING_TYPES = ['fifo', 'fair']

PRIORITY_LEVELS = xrange(1, 6)

VALID = [True]
INVALID_RANGE_MESSAGE = 'Invalid range'
NOT_AN_INT_MESSAGE = 'Not and int'
INVALID_CONFIG_MESSAGE = 'Invalid configuration format for %s'
UNABLE_TO_FIND_FILE_MESSAGE = 'unable to find %s'
INVALID_SCHEDULING_TYPE_MESSAGE = 'Invalid schdeuling type for %s'
INVALID_PRIORITY_LEVEL_MESSAGE = 'Invalid job priority level'


