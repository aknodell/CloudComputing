######################################
###    Aaron Knodell               ###
###    420007922                   ###
###    CSCE 689-607 - Fall 2018    ###
###    Project 1                   ###
######################################

import aggiestack_backend

log = open('aggiestack-log.txt', 'a')
run = True

# parse a command to determine which root method to call
# checks for validity of the command and number of flags/arguments
def parseCommand(command):
	message = 'Error: Invalid command'
	commandParts = command.split()
	if commandParts[0] == 'aggiestack':
		if commandParts[1] == 'config':
			if len(commandParts) == 4:
				message = aggiestack_backend.config(commandParts[2], commandParts[3])
		elif commandParts[1] == 'show':
			if len(commandParts) == 3:
				message = aggiestack_backend.show(commandParts[2])
		elif commandParts[1] == 'admin':
			if commandParts[2] == 'show':
				if len(commandParts) == 4:
					message = aggiestack_backend.adminShow(commandParts[3])
			elif commandParts[2] == 'can_host':
				if len(commandParts) == 5:
					message = aggiestack_backend.adminCanHost(commandParts[3], commandParts[4])
			elif commandParts[2] == 'evacuate':
				if len(commandParts) == 4:
					message = aggiestack_backend.adminEvacuate(commandParts[3])
			elif commandParts[2] == 'remove':
				if len(commandParts) == 4:
					message = aggiestack_backend.adminRemove(commandParts[3])
			elif commandParts[2] == 'add':
				if len(commandParts) == 14:
					message = aggiestack_backend.adminAdd(commandParts[3:])
		elif commandParts[1] == 'server':
			if commandParts[2] == 'create':
				if len(commandParts) == 8:
					message = aggiestack_backend.serverCreate(commandParts[3:])
			elif commandParts[2] == 'delete':
				if len(commandParts) == 4:
					message = aggiestack_backend.serverDelete(commandParts[3])
			elif commandParts[2] == 'list':
				if len(commandParts) == 3:
					message = aggiestack_backend.serverList()
	
	return message

print 'Welcome to the Aggiestack0.1 CLI!'
log.write('aggiestack started\n')

# main loop for the command line interface
while run:
	command = ' '.join(raw_input('>>').split())
	if command == 'exit':
		run = False
	else:
		if len(command.split()) > 0:
			message = parseCommand(command)
			if message == 'SUCCESS':
				log.write(command + ': SUCCESS\n')
			else:
				log.write(command + ': FAILURE\n')
				log.write(message + '\n')
				if message[:5] == 'Error':
					print message

log.write('aggiestack exited\n')

log.close()

