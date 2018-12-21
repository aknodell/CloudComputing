hardware = {}
images = {}
flavors = {}
capacity = {}
run = True

def parseMachineConfig(specifications):
	validFormat = True
	specs = specifications.split()

	if len(specs) != 5:
		validFormat = False
		print '1'
	if validFormat:
		try:
			for i in range(2, 5):
				int(specs[i])
		except ValueError, e:
			validFormat = False
			print '2'
	
	if validFormat:
		ipParts = specs[1].split('.')
		if len(ipParts) != 4:
			validFormat = False
			print '3'
		if validFormat:
			try:
				for i in range(0, 4):
					validFormat = validFormat and int(ipParts[i]) >= 0 and int(ipParts[i]) <= 255
			except ValueError, e:
				validFormat = False
				print '4'

	if validFormat:
		hardware[specs[0]] = {'name': specs[0], 'ip': specs[1], 'mem': int(specs[2]), 'num-disks': int(specs[3]), 'num-vcpus': int(specs[4]), 'display':specifications.rstrip()}
		capacity[specs[0]] = {'name': specs[0], 'ip': specs[1], 'mem': int(specs[2]), 'num-disks': int(specs[3]), 'num-vcpus': int(specs[4]), 'display':specifications.rstrip()}

	return validFormat

def parseImageConfig(specifications):
	validFormat = True
	specs = specifications.split()

	if len(specs) != 2:
		validFormat = False

	if validFormat:
		images[specs[0]] = {'name': specs[0], 'path': specs[1]}

	return validFormat

def parseFlavorConfig(specifications):
	validFormat = True
	specs = specifications.split()

	if len(specs) != 4:
		validFormat = False

	if validFormat:
		try:
			for i in range(1,4):
				int(specs[i])
		except ValueError, e:
			validFormat = False

	if validFormat:
		flavors[specs[0]] = {'name': specs[0], 'mem': int(specs[1]), 'num-disks': int(specs[2]), 'num-vcpus': int(specs[3])}

	return validFormat

def config(flag, filename):
	message = 'Error: '
	try:
		f = open(filename, 'r')
		f.readline()
		validFormat = True

		if flag == '--hardware':
			for line in f:
				validFormat = validFormat and parseMachineConfig(line)
			if not validFormat:
				hardware = {}
		elif flag == '--images':
			for line in f:
				validFormat = validFormat and parseImageConfig(line)
			if not validFormat:
				images = {}
		elif flag == '--flavors':
			for line in f:
				validFormat = validFormat and parseFlavorConfig(line)
			if not validFormat:
				flavors = {}
		else:
			message = message + 'Invalid flag'

		if validFormat:
			if message != 'Error: Invalid flag':
				message = 'SUCCESS'
		else:
			message = message + 'Invalid file format'
	except IOError, e:
		message = message + 'Invalid filename'

	return message

def show(option):
	message = 'Error: Invalid show option'
	if (option == 'hardware') or (option == 'all'):
		print 'Hardware:'
		for h in hardware:
			print hardware[h]['display']
		print ''
		message = 'SUCCESS'
	if (option == 'images') or (option == 'all'):
		print 'Images:'
		for i in images:
			print i
		message = 'SUCCESS'
		print ''
	if (option == 'flavors') or (option == 'all'):
		print 'Flavors:'
		for f in flavors:
			print f
		message = 'SUCCESS'
		print ''

	return message

def adminShow(option):
	message = 'Error: Invalid show option'

	if (option == 'hardware'):
		for machine in capacity:
			print capacity[machine]['display']
		message = 'SUCCESS'

	return 'SUCCESS'

def adminCanHost(machineName, flavor):
	message = 'Error: '

	if machineName in capacity:
		if flavor in flavors:
			canHost = True
			if capacity[machineName]['mem'] <= flavors[flavor]['mem']:
				canHost = False
				print 'Not enough memory'
			if capacity[machineName]['num-disks'] <= flavors[flavor]['num-disks']:
				canHost = False
				print 'Not enough disks'
			if capacity[machineName]['num-vcpus'] <= flavors[flavor]['num-vcpus']:
				canHost = False
				print 'Not enough VCPUs'
			if canHost:
				print machineName + ' is able to host ' + flavor

			message = 'SUCCESS'
		else:
			message += 'Invalid flavor'
	else:
		message += 'Invalid machine'

	return message

def parseCommand(command):
	message = 'Error: Invalid command'
	commandParts = command.split()
	if commandParts[0] == 'aggiestack':
		if commandParts[1] == 'config':
			if len(commandParts) == 4:
				message = config(commandParts[2], commandParts[3])
		elif commandParts[1] == 'show':
			if len(commandParts) == 3:
				message = show(commandParts[2])
		elif commandParts[1] == 'admin':
			if commandParts[2] == 'show':
				if len(commandParts) == 4:
					message = adminShow(commandParts[3])
			elif commandParts[2] == 'can_host':
				if len(commandParts) == 5:
					message = adminCanHost(commandParts[3], commandParts[4])
	
	return message

log = open('aggiestack-log.txt', 'a')

print 'Welcome to Aggiestack0.1 CLI!'
log.write('aggiestack started\n')

while run:
	command = raw_input('>>')
	if command == 'exit':
		run = False
	else:
		message = parseCommand(command)
		if message == 'SUCCESS':
			log.write(command + ': SUCCESS\n')
		else:
			log.write(command + ': FAILURE\n')
			log.write(message + '\n')
			print message

log.write('aggiestack exited\n')

log.close()

