######################################
###    Aaron Knodell               ###
###    420007922                   ###
###    CSCE 689-607 - Fall 2018    ###
###    HW1 Task2                   ###
######################################

from mongo_connect import connectMongo
import constants
import pymongo
import redis

collection = connectMongo()
r = redis.StrictRedis(host='localhost', port=6379, db=0)
welcome = 'Welcome to the AggieFit chat!  The following commands can be used to chat with other users:\n\t\'select <messageBoard>\': select the message board you wish to post on\n\t\'list\': list the available message boards\n\t\'topic "<topic>"\': list the available message boards about the selected topic\n\t\'read\': read all the previous messages from the current board\n\t\'write "<message>"\': write a message to the current board\n\t\'listen\': listen for new messages being sent to the current board\n\t\'exit\': exit the chat program\n\t\'help\': print this message again'

messageBoard = ''
cont = True

def listBoards():
	boards = collection.find()
	i = 1
	print 'Current message boards:\n'
	for board in boards:
		print '%d: %s' % (i, board['name'])
		i += 1

def listBoardsByTopic(topic):
	boards = collection.find({'topics' : topic})
	i = 1
	print 'Current message boards about \'%s\':' % topic
	for board in boards:
		print '%d: %s' % (i, board['name'])
		i += 1	

def select(mb):
	global messageBoard
	board = collection.find({'name' : mb})
	
	if board.count() == 0:
		print 'Message board \'' + mb +'\' does not exist'
	else:
		messageBoard = mb

def read():
	print 'Messages from \'%s\':\n' % messageBoard
	messages = r.lrange(messageBoard, 0, -1)
	m_num = 1
	
	for message in messages:
		print '%d: %s' % (m_num, message)
		m_num += 1
	
def listen():
	print '\nListening for new messages from \'%s\'.  Hit Ctrl+C to stop listening\n' % messageBoard
	p = r.pubsub()
	while True:
		try:
			p.subscribe(messageBoard + '-channel')
			for item in p.listen():
				if item['type'] == 'message':
					print item
					print '>> ' + item['data']
		except KeyboardInterrupt:
			return

def write(message):
	success = True
	rpush = r.rpush(messageBoard, message)
	if rpush != r.llen(messageBoard):
		print 'Error saving message to database'
		success = False

	pub = r.publish(messageBoard + '-channel', message)
	if pub != 1:
		print 'Error publishing message to chat channel'
		success = False

	return success

print welcome		
while cont:
	command = raw_input('\nEnter a command >> ') if messageBoard == '' else raw_input('\nEnter a command [%s] >> ' % messageBoard)
	
	if command.split(' ')[0].lower() == 'select':
		parseCommand = command.split(' ')
		if len(parseCommand) != 2:
			print 'Improperly formatted command, please follow the format \'select <messageBoard>\''
		else:
			select(parseCommand[1])

		if messageBoard != '':
			print 'Successfully joined \'%s\'' % messageBoard
	elif command.lower() == 'read':
		if messageBoard != '':
			read()
		else:
			print 'Please select a message board before reading messages'
	elif command.lower() == 'listen':
		if messageBoard != '':
			listen()
		else:
			print 'Please select a message board before listening for new messages'
	elif command.split(' ')[0].lower() == 'write':
		if messageBoard != '':
			parseMessage = command.split('"')
			if len(parseMessage) != 3:
				print 'Improperly formatted command, please follow the format \'write \"<message>\"\''
			else:
				if write(parseMessage[1]):
					print 'Message successfully sent'
		else:
			print 'Please select a message board before writing a new message'
	elif command.lower() == 'list':
		listBoards()
	elif command.split(' ')[0].lower() == 'topic':
		parseTopic = command.split('"')
		if len(parseTopic) != 3:
			print 'Improperly formatted command, please follow the format \'topic \"<topic>\"\''
		else:
			listBoardsByTopic(parseTopic[1])
	elif command.lower() == 'exit':
		cont = False
	elif command.lower() == 'help':
		print welcome
	else:
		print 'Invalid command, please enter \'select\', \'list\', \'topic\', \'read\', \'listen\', \'write\', \'exit\', or \'help\''

