######################################
###    Aaron Knodell               ###
###    420007922                   ###
###    CSCE 689-607 - Fall 2018    ###
###    Project 2                   ###
######################################

class Queue:
	def __init__(self):
		self.jobs = []
		
	def isEmpty(self):
		return len(self.jobs) == 0
			
	def put(self, job):
		self.jobs.append(job)
		
	def get(self):
		job = None
	
		if self.isEmpty() == False:
			job = self.jobs[0]
			self.jobs.remove(job)
		
		return job
			
	def peek(self):
		first = None
	
		if self.isEmpty() == False:
			first = self.jobs[0]
			
		return first

class FifoQueue(Queue):
	def __init__(self):
		Queue.__init__(self)
	
	def put(self, job):
		i = 0
		while i < len(self.jobs) and self.jobs[i]['priority'] >= job['priority'] and self.jobs[i]['subTime'] < job['subTime']:
			i += 1
			
		self.jobs.insert(i, job)
		
class FairQueue(Queue):
	def __init__(self):
		Queue.__init__(self)
		self.counter = 0
		
	def get_priority(self):
		priority = 0
		self.counter = self.counter % 31

		if self.counter % 2 == 0:
			priority = 5
		elif (self.counter-1) % 4 == 0:
			priority = 4
		elif (self.counter-3) % 8 == 0:
			priority = 3
		elif (self.counter-7) % 16 == 0:
			priority = 2
		else:
			priority = 1
		
		self.counter += 1
			
		return priority
		
	def get(self):
		job = None
		
		if self.isEmpty() == False:
			self.counter -= 1
			while job == None:
				priority = self.get_priority()
				for j in self.jobs:
					if j['priority'] == priority:
						self.counter-=1
						job = j
						self.jobs.remove(job)
						break
					
		return job
		
if __name__ == '__main__':
	fq = FairQueue()
	for i in range(62):
		print fq.get_priority()

