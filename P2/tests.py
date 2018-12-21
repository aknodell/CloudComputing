######################################
###    Aaron Knodell               ###
###    420007922                   ###
###    CSCE 689-607 - Fall 2018    ###
###    Project 2                   ###
######################################

from schedulerConstants import *
from schedulerBackend import *

VALID = [True]

def test(output, expected):
	return output == expected
	
print test(is_valid_int('1'), VALID)
print test(is_valid_int('0'), [False, INVALID_RANGE_MESSAGE])
print test(is_valid_int('-1'), [False, INVALID_RANGE_MESSAGE])
print test(is_valid_int('a'), [False, NOT_AN_INT_MESSAGE])

print test(is_valid_machine_config('16 4 4'), VALID)
print test(is_valid_machine_config('0 4 4'), [False, INVALID_RANGE_MESSAGE])
print test(is_valid_machine_config('16 0 4'), [False, INVALID_RANGE_MESSAGE])
print test(is_valid_machine_config('16 4 0'), [False, INVALID_RANGE_MESSAGE])
print test(is_valid_machine_config('a 4 4'), [False, NOT_AN_INT_MESSAGE])
print test(is_valid_machine_config('16 a 4'), [False, NOT_AN_INT_MESSAGE])
print test(is_valid_machine_config('16 4 a'), [False, NOT_AN_INT_MESSAGE])
print test(is_valid_machine_config('16 4'), [False, INVALID_CONFIG_MESSAGE % ('machine')])
print test(is_valid_machine_config('16 4 4 4'), [False, INVALID_CONFIG_MESSAGE % ('machine')])

