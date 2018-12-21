import aggiestack_backend

allTestsPassed = True

def runTest(number, expected, actual):
	if expected != actual:
		print '%d. Failed\nExpected: %s\nActual: %s' % (number, expected, actual)
		allTestsPassed = False

###################positive tests

#validIntValue
runTest(1, True, aggiestack_backend.validIntValue(0, 'test', 0, 255))
runTest(2, True, aggiestack_backend.validIntValue(128, 'test', 0, 255))
runTest(3, True, aggiestack_backend.validIntValue(255, 'test', 0, 255))
runTest(4, True, aggiestack_backend.validIntValue(0, 'test', 0))
runTest(5, True, aggiestack_backend.validIntValue(0, 'test'))

#validateRackSpecs
runTest(6, True, aggiestack_backend.validateRackSpecs(['r1', '40960']))

#addNewRack
aggiestack_backend.addNewRack(['r1', '40960'])
if 'r1' not in aggiestack_backend.racks or aggiestack_backend.racks['r1']['name'] != 'r1' or aggiestack_backend.racks['r1']['capacity'] != 40960 or aggiestack_backend.racks['r1']['machines'] != []:
	print aggiestack_backend.racks
	print '7. Failed\n'
	allTestsPassed = False

#validateMachineSpecs
runTest(8, True, aggiestack_backend.validateMachineSpecs(['m1', 'r1','128.0.0.1','64','64','64']))

#addNewMachine

#validateImageSpecs
runTest(10, True, aggiestack_backend.validateImageSpecs(['i1', 'path']))

#addNewImage


#validateFlavorSpecs
runTest(12, True, aggiestack_backend.validateFlavorSpecs(['f1','1','1','1']))

#addNewFlavor


#userValidation


#canHost


#adminCanHost


#addInstanceToMachine


#removeInstanceFromMachine


#findAvailableMachine


#serverCreate


#serverDelete


#migrateInstances


#adminEvacuate


#adminRemove


#adminAdd


###################negative tests

#validIntValue
runTest(14, 'Invalid value for test', aggiestack_backend.validIntValue(-1, 'test', 0, 255))
runTest(15, 'Invalid value for test', aggiestack_backend.validIntValue(256, 'test', 0, 255))
runTest(16, 'Invalid value for test', aggiestack_backend.validIntValue(-1, 'test', 0))
runTest(17, 'Invalid value for test', aggiestack_backend.validIntValue(-1, 'test'))
runTest(18, 'Invalid datatype for test', aggiestack_backend.validIntValue('a', 'test', 0, 255))
runTest(19, 'Invalid datatype for test', aggiestack_backend.validIntValue('a', 'test', 0))
runTest(20, 'Invalid datatype for test', aggiestack_backend.validIntValue('a', 'test'))

#validateRackSpecs


#validateMachineSpecs


#validateImageSpecs


#validateFlavorSpecs


#userValidation


#show


#adminShow


#canHost


#adminCanHost


#findAvailableMachine


#serverCreate


#serverDelete


#migrateInstances


#adminEvacuate


#adminRemove


#adminAdd


if allTestsPassed == True:
	print 'All Tests Passed'

