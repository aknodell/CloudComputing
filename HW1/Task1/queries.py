######################################
###    Aaron Knodell               ###
###    420007922                   ###
###    CSCE 689-607 - Fall 2018    ###
###    HW1 Task1                   ###
######################################

from mongo_connect import connectMongo
import constants
import pymongo
import json
import pprint


## Re-set database to initial condition
collection = connectMongo()
collection.delete_many({})
updateInfo = open(constants.initialData, 'r')
parsedInfo = json.loads(updateInfo.read())
WQ0 = collection.insert(parsedInfo)
updateInfo.close()
	
print 'WQ1:\n'
updateInfo = open(constants.dummyFitness, 'r')
parsedInfo = json.loads(updateInfo.read())
WQ1 = collection.insert_many(parsedInfo)
pprint.pprint(WQ1)
updateInfo.close()

print '\nWQ2:\n'
updateInfo = open(constants.user1001Update, 'r')
parsedInfo = json.loads(updateInfo.read())
WQ2 = collection.update_one({'uid': parsedInfo['uid']}, {'$set': parsedInfo})
print WQ2
updateInfo.close()

##### FIND ALL ENTRIES IN THE DATABASE #####
# Assuming RQ0 is the query to find all entries in the database
#print 'RQ0:\n'
#RQ0 = collection.find()
#for data in RQ0:
#	pprint.pprint(data)

print '\n\nRQ1 (Number of Employees in database):\n'
RQ1Pipeline = [
	{'$group': {'_id': '$uid'}},
	{'$count': 'numberOfEmployees'}
]
RQ1 = collection.aggregate(RQ1Pipeline)
for data in RQ1:
	print data

print '\n\nRQ2 (Employees with "active" tag:)\n'
RQ2 = collection.find({'tags' : 'active'})
for data in RQ2:
	print data['uid']

print '\n\nRQ3 (Empoyees with stepGoal > 5000):\n'
RQ3 = collection.find({'goal.stepGoal' : { '$gt' : 5000 }})
for data in RQ3:
	# print data['goal']['stepGoal']
	print '%s: stepGoal = %d' % (data['uid'], data['goal']['stepGoal'])

RQ4Pipeline = [
	{'$project': {'totalActivity': {'$sum':'$activityDuration'}, '_id': '$uid'}}
]
RQ4 = collection.aggregate(RQ4Pipeline)
print '\n\nRQ4 (Total Activity for all employees):\n'
for data in RQ4:
	print data

######## FIND ENTRIES WITH CONDITION #######
######## collection.find(CONDITION) #######
######## E.g., collection.find({"Name" : "Alice"}) #######

######## UPDATE ENTRIES WITH CONDITION ########
######## collection.update_one(CONDITION, _update_) #######
######## collection.update_many(CONDITION, _update_)
######## E.g., collection.find({"Name" : "Alice"}, {"$inc" : {"age" : 1} })

######## DELETE ENTRIES WITH CONDITION ########
######## collection.delete_one(CONDITION) #######
######## collection.delete_many(CONDITION)
######## E.g., collection.find({"Name" : "Alice"})

######## AGGREGATE ENTRIES WITH PIPELINE ########
######## collection.aggregate(PIPELINE) ########

