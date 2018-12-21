######################################
###    Aaron Knodell               ###
###    420007922                   ###
###    CSCE 689-607 - Fall 2018    ###
###    Project 2                   ###
######################################

import time
import random
import resourceManager
import threading

class NodeManager(threading.Thread):
	def __init__(self, rm, mem, mapS, redS):
		threading.Thread.__init__(self)
		self.rm = rm
		self.memory = mem * 1000
		self.mapSlots = [None]*mapS
		self.redSlots = [None]*redS
		self.cont = False
		
	def __str__(self):
		return 'memory: %d, map slots: %d, reduce slots: %d' % (self.memory, len(self.mapSlots), len(self.redSlots))
		
	def add_map_task(self, task):
		for slot in range(len(self.mapSlots)):
			if self.mapSlots[slot] is None:
				self.mapSlots[slot] = task
				self.memory -= task['job']['memPerMap']
				break
				
	def show_map_slots(self):
		print self.mapSlots
		
	def get_avail_map_slots(self):
		return self.mapSlots.count(None)
		
	def add_red_task(self, task):
		for slot in range(len(self.redSlots)):
			if self.redSlots[slot] is None:
				self.redSlots[slot] = task
				self.memory -= task['job']['memPerRed']
				break

	def get_avail_red_slots(self):
		return self.redSlots.count(None)
		
	def get_avail_memory(self):
		return self.memory
		
	def finish_task(self, task):
		self.rm.scheduler.threadlock.acquire(1)
		
		self.memory += task['job']['memPer' + task['type'].capitalize()]
		self.rm.scheduler.task_complete(task)

		self.rm.scheduler.threadlock.release()
		
	def work(self, tasks):
		for task in tasks:
			if task is not None:
				if random.randint(0,4) == 0:
					self.finish_task(task)
					tasks[tasks.index(task)] = None
		
	def run(self):
		self.cont = True
		while self.cont or len(self.mapSlots) != self.mapSlots.count(None) or len(self.redSlots) != self.redSlots.count(None):
			self.work(self.mapSlots)
			self.work(self.redSlots)
			
			time.sleep(0.25)
			
	def stop(self):
		self.cont = False
		
if __name__ == '__main__':
	rm = resourceManager.ResourceManager()
	node1 = NodeManager(rm, 8, 2, 2)
	node2 = NodeManager(rm, 4, 2, 2)
	node1.start()
	node2.start()
	
	time.sleep(3)
