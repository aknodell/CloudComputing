######################################
###    Aaron Knodell               ###
###    420007922                   ###
###    CSCE 689-607 - Fall 2018    ###
###    Project 1                   ###
######################################

machines = {}
images = {}
flavors = {}
instances = {}
racks = {}

# check whether a variable is an integer and whether it is within an optional range
def validIntValue(i, intName, minValue = 0, maxValue = False):
	valid = True

	try:
		if (int(i) < minValue) or (maxValue != False and int(i) > maxValue):
			valid = ' '.join(('Invalid value for', intName))
	except ValueError, e:
		valid = ' '.join(('Invalid datatype for', intName))

	return valid

# check that the provided specs for a new rack are valid
def validateRackSpecs(specs):
	valid = True
	
	if len(specs) != 2:
		valid = 'Incorrect number of specifications for new rack'
	elif specs[0] in racks:
		valid = ' '.join(('Rack', specs[0], 'already added'))
	else:
		validRackSize = validIntValue(specs[1], 'rack size', 1)

		if validRackSize != True:
			valid = validRackSize

	return valid

# add a new rack to the master dictionary
def addNewRack(specs):
	racks[specs[0]] = {'name': specs[0], 'capacity': int(specs[1]), 'machines': []}

# check that the provided specs for a new machine are valid
def validateMachineSpecs(specs):
	valid = True
	
	if len(specs) != 6:
		valid = 'Incorrect number of specifications for new machine'
	elif specs[0] in machines:
		valid = ' '.join(('Machine', specs[0], 'already added'))
	elif specs[1] not in racks:
		valid = ' '.join(('Rack', specs[1], 'is not a valid rack'))
	else:
		ipParts = specs[2].split('.')
		if len(ipParts) != 4:
			valid = 'Invalid IP address'
		else:
			part = 0
			while valid == True and part < 4:
				valid = valid and validIntValue(ipParts[part], 'IP address', 0, 255)
				part += 1
				
	if valid == True:
		valid = validIntValue(specs[3], 'memory', 1)
	if valid == True:
		valid = validIntValue(specs[4], 'number of disks', 1)
	if valid == True:
		valid = validIntValue(specs[5], 'number of VCPUs', 1)
	
	return valid

# add a new machine to the master dictionary
def addNewMachine(specs):
	machines[specs[0]] = {'name': specs[0], 'rack': specs[1], 'ip': specs[2], 
		'mem': int(specs[3]), 'num-disks': int(specs[4]), 'num-vcpus': int(specs[5]),
		'display': ' '.join(specs), 'mem-avail': int(specs[3]), 
		'num-disks-avail': int(specs[4]), 'num-vcpus-avail': int(specs[5]),
		'instances': []}
	racks[specs[1]]['machines'].append(specs[0])

# check that the provided specs for a new image are valid
def validateImageSpecs(specs):
	valid = True

	if len(specs) != 2:
		valid = 'Incorrect number of specifications for new image'
	elif specs[0] in images:
		valid = ' '.join(('Image', specs[0], 'already added'))
	return valid

# add a new image to the master dictionary
def addNewImage(specs):
	images[specs[0]] = {'name': specs[0], 'path': specs[1]}

# check that the provided specs for a new flavor are valid
def validateFlavorSpecs(specs):
	valid = True
	
	if len(specs) != 4:
		valid = 'Incorrect number of specifications for new flavor'
	elif specs[0] in flavors:
		valid = ' '.join(('Flavor', specs[0], 'already added'))
		
	if valid == True:
		valid = validIntValue(specs[1], 'memory', 1)
	if valid == True:
		valid = validIntValue(specs[2], 'number of disks', 1)
	if valid == True:
		valid = validIntValue(specs[3], 'number of VCPUs', 1)

	return valid

# add a new flavor to the master dictionary
def addNewFlavor(specs):
	flavors[specs[0]] = {'name': specs[0], 'mem': int(specs[1]),
		'num-disks': int(specs[2]), 'num-vcpus': int(specs[3])}
	
# read the specified number of configurations for a file
# generalized to be used for racks, machines, images, and flavors
def readConfigFile(f, validateMethod, addMethod):
	success = True
	numConfigs = f.readline()
	
	if validIntValue(numConfigs, 'number of configurations', 0) == True:
		count = 0
		while success == True and count < int(numConfigs):
			specs = f.readline().split()
			success = validateMethod(specs)

			if success == True:
				addMethod(specs)
				
			count += 1
		
		if success != True:
			success = {'line':count+1, 'message':success}
	else:
		success = {'line':1, 'message':'Invalid number of configurations'}
		
	return success
	
# generalized method that asks a user for confirmation
def userValidation(message):
	command = raw_input(message)
	
	while command.lower() not in ['y', 'yes', 'n', 'no']:
		command = raw_input('Invalid response. Please enter \'y\' or \'n\':\n>>')
		
	return command.lower()

# root method for config command
def config(flag, filename):
	message = 'SUCCESS'
	try:
		f = open(filename, 'r')
		validFormat = True

		if flag == '--hardware':
			# if a config file has already been read
			if len(racks) > 0 or len(machines) > 0:
				if userValidation('Replace existing hardware configuration with ' 
						+ 'new configuration? (y/n)\n>>') in ['y', 'yes']:				
					racks.clear()
					machines.clear()
				else:
					message = 'User cancelled command'
					
			# if no file has been read, or the user chose to overwrite
			if len(racks) == 0 and len(machines) == 0:
				validFormat = readConfigFile(f, validateRackSpecs, addNewRack)
				# if there was not an error reading the rack configs
				if validFormat == True:
					validFormat = readConfigFile(f, validateMachineSpecs, addNewMachine)
					if validFormat != True:
						validFormat['line'] += len(racks) + 1
						
				if validFormat != True:
					racks.clear()
					machines.clear()
					message = ' '.join(('Line', str(validFormat['line']), 
						validFormat['message']))
						
		elif flag == '--images':
			# if a config file has already been read
			if len(images) > 0:
				if userValidation('Replace existing image configuration with '
						+ 'new configuration? (y/n)\n>>') in ['y', 'yes']:				
					images.clear()
				else:
					message = 'User cancelled command'
								
			# if no file has been read, or the user chose to overwrite
			if len(images) == 0:
				validFormat = readConfigFile(f, validateImageSpecs, addNewImage)
				if validFormat != True:
					images.clear()
					message = ' '.join(('Line', str(validFormat['line']), 
						validFormat['message']))
						
		elif flag == '--flavors':
			# if a config file has already been read
			if len(flavors) > 0:
				if userValidation('Replace existing flavor configuration with '
						+ 'new configuration? (y/n)\n>>') in ['y', 'yes']:				
					flavors.clear()
				else:
					message = 'User cancelled command'
					
			# if no file has been read, or the user chose to overwrite
			if len(flavors) == 0:
				validFormat = readConfigFile(f, validateFlavorSpecs, addNewFlavor)
				if validFormat != True:
					flavors.clear()
					message = ' '.join(('Line', str(validFormat['line']), 
						validFormat['message']))
		else:
			message = 'Error: Invalid flag'			 
	except IOError, e:
		message = 'Error: Invalid filename'

	return message

# root method for the non-admin version of the show command
def show(option):
	message = 'Error: Invalid show option'
	if (option == 'hardware') or (option == 'all'):
		print 'Hardware:'
		for m in machines:
			print machines[m]['display']
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

# root method for the admin version of the show command
def adminShow(option):
	message = 'Error: Invalid show option'

	if (option == 'hardware'):
		print 'Hardware Capacity:'
		for m in machines:
			print ' '.join((machines[m]['name'], str(machines[m]['mem-avail']), str(machines[m]['num-disks-avail']), str(machines[m]['num-vcpus-avail'])))
		print ''
		message = 'SUCCESS'
	if (option == 'instances'):
		print 'Instances:'
		for i in instances:
			print ' '.join((instances[i]['name'], instances[i]['machine']))
		message = 'SUCCESS'
		print ''

	return message

# check whether a given machine can host a given flavor
def canHost(machineName, flavor):
	message = True

	if machines[machineName]['mem-avail'] < flavors[flavor]['mem']:
		message = 'Not enough memory'
	elif machines[machineName]['num-disks-avail'] < flavors[flavor]['num-disks']:
		message = 'Not enough disks'
	elif machines[machineName]['num-vcpus-avail'] < flavors[flavor]['num-vcpus']:
		message = 'Not enough VCPUs'

	return message

# root method for the admin can_host command
def adminCanHost(machineName, flavor):
	message = 'Error: '

	if machineName in machines:
		if flavor in flavors:
			canHost = canHost(machineName, flavor)
			if canHost == True:
				print machineName + ' is able to host ' + flavor
				message = 'SUCCESS'
			else:
				print canHost
		else:
			message += 'Invalid flavor'
	else:
		message += 'Invalid machine'

	return message

# add an instance to a machine and update the available resources for that machine
def addInstanceToMachine(instanceName, machineName):
	flavorName = instances[instanceName]['flavor']
	machines[machineName]['instances'].append(instanceName)
	machines[machineName]['mem-avail'] -= flavors[flavorName]['mem']
	machines[machineName]['num-disks-avail'] -= flavors[flavorName]['num-disks']
	machines[machineName]['num-vcpus-avail'] -= flavors[flavorName]['num-vcpus']

# remove an instance from a machine and update the available resources for that machine
def removeInstanceFromMachine(instanceName, machineName):
	flavorName = instances[instanceName]['flavor']
	machines[machineName]['mem-avail'] += flavors[flavorName]['mem']
	machines[machineName]['num-disks-avail'] += flavors[flavorName]['num-disks']
	machines[machineName]['num-vcpus-avail'] += flavors[flavorName]['num-vcpus']
	machines[machineName]['instances'].remove(instanceName)
	
# find a machine that can host a particular instance
def findAvailableMachine(instanceName, flavorName, oldRack = False):
	machineName = False
	for r in racks:
		# if an old rack has been specified, machines on that rack shouldn't be considered
		if oldRack == False or r != oldRack:
			for m in racks[r]['machines']:
				# if the instance already exists, its current machine shouldn't be considered
				if (instanceName in instances and m != instances[instanceName]['machine']) or (instanceName not in instances):
					if canHost(m, flavorName) == True:
						machineName = m
						break
		if machineName != False:
			break

	return machineName

# root method for the server create command
def serverCreate(arguments):
	message = 'Error: '

	# input validation
	if (arguments[0] != '--image') or (arguments[2] != '--flavor'):
		message += 'Invalid flags'
	else:
		image = arguments[1]
		flavorName = arguments[3]
		instanceName = arguments[4]

		if image not in images:
			message = message + 'Invalid image'
		elif flavorName not in flavors:
			message = message + 'Invalid flavor'
		elif instanceName in instances:
			message = message + 'Invalid instance name, already in use'
		else:
			machineName = findAvailableMachine(instanceName, flavorName)
			if machineName == False:
				message += 'No available machines'
			else:
				# add the new instance to the master dictionary
				instances[instanceName] = {'name': instanceName, 'image':image, 'flavor': flavorName, 'machine': machineName, 'display': ' '.join((instanceName, image, flavorName))}
				addInstanceToMachine(instanceName, machineName)
				message = 'SUCCESS'

	return message

# root method for the server delete command
def serverDelete(instanceName):
	message = 'Error: '

	if instanceName in instances:
		machineName = instances[instanceName]['machine']

		removeInstanceFromMachine(instanceName, machineName)

		del instances[instanceName]

		message = 'SUCCESS'
	else:
		message += ' Invalid instance name'

	return message

# root method for the server list command
def serverList():
	message = 'SUCCESS'

	print 'Instances:'
	for i in instances:
		print instances[i]['display']
	print ''

	return message

# migrate all instances from a particular machine, optional old rack argument for evacuation
def migrateInstances(oldMachine, oldRack = False):
	success = True
	for i in machines[oldMachine]['instances']:
		# old rack check is performed in the findAvailableMachine method, the variable is just passed along
		newMachine = findAvailableMachine(i, instances[i]['flavor'], oldRack)
		if newMachine == False:
			success = False
		else:
			addInstanceToMachine(i, newMachine)
			instances[i]['machine'] = newMachine
			removeInstanceFromMachine(i, oldMachine)

	return success

# root method for the admin evacuate command
def adminEvacuate(rackName):
	message = 'Error: '

	if rackName in racks:
		successfulMigration = True
		for m in racks[rackName]['machines']:
			successfulMigration = successfulMigration and migrateInstances(m, rackName)
		if successfulMigration:
			message = 'SUCCESS'
		else:
			if userValidation('WARNING: Unable to migrate all instances.  Continue evacuating rack ' + rackName + '? (y/n)\n>>') in ['y', 'yes']:
				for m in racks[rackName]['machines']:
					for i in machines[m]['instances']:
						del instances[i]
					racks[rackName]['machines'].remove(m)
					del machines[m]
				message = 'SUCCESS'
			else:
				message = 'User cancelled command'						
	else:
		message += 'Invalid rack name'

	return message

# root method for the admin remove command
def adminRemove(machine):
	message = 'Error: '

	if machine in machines:
		if migrateInstances(machine):
			racks[machines[machine]['rack']]['machines'].remove(machine)
			del machines[machine]
			message = 'SUCCESS'
		else:
			if userValidation('WARNING: Unable to migrate all instances.  Continue removing machine ' + machine + '? (y/n)\n>>') in ['y', 'yes']:
				for i in machines[machine]['instances']:
					del instances[i]
				racks[machines[machine]['rack']]['machines'].remove(machine)
				del machines[machine]
				message = 'SUCCESS'
			else:
				message = 'User cancelled command'
	else:
		message += 'Invalid machine name'

	return message

# root method for the admin add command
def adminAdd(arguments):
	message = 'Error: '

	if (arguments[0] != '--mem') or (arguments[2] != '--disk') or (arguments[4] != '--vcpus') or (arguments[6] != '--ip') or (arguments[8] != '--rack'):
		message += 'Invalid flags'
	else:
		specs = [arguments[10],arguments[9],arguments[7],arguments[1],arguments[3],arguments[5]]
		valid = validateMachineSpecs(specs)

		if valid == True:
			addNewMachine(specs)
			message = 'SUCCESS'
		else:
			message += valid

	return message

