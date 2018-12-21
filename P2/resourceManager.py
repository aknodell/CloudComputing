######################################
###    Aaron Knodell               ###
###    420007922                   ###
###    CSCE 689-607 - Fall 2018    ###
###    Project 2                   ###
######################################

from nodeManager import NodeManager
from datetime import datetime
import threading
import queues

class Scheduler:
	def __init__(self, mode):
		self.mode = mode
		self.threadlock = threading.Lock()
		self.runningJobs = []
		self.activePools = {}
		self.allJobsComplete = False
		self.log = open('schedulerLog.txt', 'w')
										
	def get_job_remaining_tasks(self, job, typ):
		return job[typ + 'Tasks'] - (job[typ + 'Active'] + job[typ +'Complete'])
		
	def get_pool_remaining_tasks(self, poolName, typ):
		remaining = 0
		
		for job in self.runningJobs:
			if job['pool'] == poolName:
				remaining += self.get_job_remaining_tasks(job, typ)
				
		return remaining
				
	def get_total_remaining_tasks(self, typ):
		remaining = 0
		
		for j in self.runningJobs:
			remaining += self.get_job_remaining_tasks(j, typ)
		
		return remaining
		
	def get_running_tasks(self, poolName, typ):
		runningTasks = 0
		
		for job in self.runningJobs:
			if job['pool'] == poolName:
				runningTasks += job[typ + 'Active']
				
		return runningTasks
		
	def task_complete(self, task):
		task['job'][task['type'] + 'Active'] -= 1
		task['job'][task['type'] + 'Complete'] += 1
		if task['job'][task['type'] + 'Complete'] == task['job'][task['type'] + 'Tasks']:
			if task['type'] == 'red':
				self.log.write('%s: Job %d completed\n' % (str(datetime.now()), task['job']['id']))
				self.runningJobs.remove(task['job'])

				remainingMapTasks = self.get_pool_remaining_tasks(task['job']['pool'], 'map')
				runningMapTasks = self.get_running_tasks(task['job']['pool'], 'map')
				remainingRedTasks = self.get_pool_remaining_tasks(task['job']['pool'], 'red')
				runningRedTasks = self.get_running_tasks(task['job']['pool'], 'red')
		
				totalIncompleteTasks = remainingMapTasks + runningMapTasks + remainingRedTasks + runningRedTasks
		
				if self.activePools[task['job']['pool']]['queue'].isEmpty() and totalIncompleteTasks == 0:
					del self.activePools[task['job']['pool']]	
		
	def assign_task(self, cluster, task, get_avail_slots, add_task):
		assigned = False
		while assigned == False:
			for node in cluster.nodes:
				if get_avail_slots(node) and node.get_avail_memory() > task['job']['memPer' + task['type'].capitalize()]:
					add_task(node, task)
					task['job'][task['type'] + 'Active'] += 1
					assigned = True
					break
									
	def start_next_job(self, poolName):
		self.threadlock.acquire(1)
		
		job = self.activePools[poolName]['queue'].get()
		if job is not None:
			self.runningJobs.append(job)
			self.log.write('%s: job %d started\n' % (str(datetime.now()), job['id']))
			
		self.threadlock.release()
					
	def get_most_unfair_pool(self, typ):
		pools = []
				
		self.threadlock.acquire(1)
		
		for p in self.activePools:
			if len(pools) == 0:
				pools.append(p)
			else:
				i = 0
				underuse = self.get_running_tasks(p, typ)/self.activePools[p]['fair' + typ.capitalize() + 'Slots']
				while i < len(pools) and underuse > self.get_running_tasks(pools[i], typ)/self.activePools[pools[i]]['fair' + typ.capitalize() + 'Slots']:
					i += 1
				pools.insert(i, p)
					
		self.threadlock.release()
		
		return pools
		
	def get_next_map_task(self, cluster):
		task = None
		pools = self.get_most_unfair_pool('map')
		
		for poolName in pools:
			if self.activePools[poolName]['type'] == 'fifo':
				if self.get_pool_remaining_tasks(poolName, 'map') == 0:
					if self.activePools[poolName]['queue'].peek() is not None:
						self.start_next_job(poolName)
					else:
						continue
			
				for job in self.runningJobs:
					if job['pool'] == poolName and self.get_job_remaining_tasks(job, 'map') > 0:
						task = {'job':job, 'type':'map'}
						return task
			elif self.activePools[poolName]['type'] == 'fair':
				if self.get_pool_remaining_tasks(poolName, 'map') > 0 or self.activePools[poolName]['queue'].peek() is not None:
					while task is None:
						priority = self.activePools[poolName]['queue'].get_priority()
						for job in self.runningJobs:
							if job['pool'] == poolName and job['priority'] == priority and self.get_job_remaining_tasks(job, 'map') > 0:
								task = {'job':job, 'type':'map'}
								return task
								
						self.start_next_job(poolName)
						for job in self.runningJobs:
							if job['pool'] == poolName and job['priority'] == priority and self.get_job_remaining_tasks(job, 'map') > 0:
								task = {'job':job, 'type':'map'}
								return task
			
		return task
					
	def schedule_map_tasks(self, cluster):
		task = self.get_next_map_task(cluster)
		while task is not None:
			self.assign_task(cluster, task, NodeManager.get_avail_map_slots, NodeManager.add_map_task)
			task = self.get_next_map_task(cluster)
		
	def get_next_red_task(self):
		task = None
		pools = self.get_most_unfair_pool('red')
		
		for poolName in pools:
			if self.activePools[poolName]['type'] == 'fifo':
				for job in self.runningJobs:
					if job['pool'] == poolName:
						if job['mapComplete'] == job['mapTasks']:
							task = {'job':job, 'type':'red'}
							return task
			elif self.activePools[poolName]['type'] == 'fair':
				priority = self.activePools[poolName]['queue'].get_priority()
				for job in self.runningJobs:
					if job['pool'] == poolName and job['priority'] == priority:
						if job['mapComplete'] == job['mapTasks']:
							task = {'job':job, 'type':'red'}
							return task
		return task
				
	def schedule_red_task(self, cluster):
		while self.get_total_remaining_tasks('red') or len(self.activePools) > 0:
			task = self.get_next_red_task()
			if task is not None:
				self.assign_task(cluster, task, NodeManager.get_avail_red_slots, NodeManager.add_red_task)
				
		self.allJobsComplete = True
		
	def calc_fair_share_helper(self, pools, availSlots, typ):
		minSlotsKey = 'min' + typ.capitalize() + 'Slots'
		fairSlotsKey = 'fair' + typ.capitalize() + 'Slots'
		totalMinSlots = 0
		totalFairSlots = 0
		
		for p in pools:
			totalMinSlots += pools[p][minSlotsKey]
			totalFairSlots += pools[p][minSlotsKey] * pools[p]['weight']
			
		if totalFairSlots <= availSlots:
			for p in pools:
				pools[p][fairSlotsKey] = float(pools[p][minSlotsKey] * pools[p]['weight'])
		else:
			if totalMinSlots <= availSlots:
				extraSlots = availSlots - totalMinSlots
				for p in pools:
					pools[p][fairSlotsKey] = float(pools[p][minSlotsKey] * pools[p]['weight'] * extraSlots)/totalFairSlots + pools[p][minSlotsKey]
			else:
				for p in pools:
					pools[p][fairSlotsKey] = float(pools[p][minSlotsKey] * pools[p]['weight'] * availSlots)/totalFairSlots
		
	def calculate_fair_shares(self, cluster, pools):
		self.calc_fair_share_helper(pools, cluster.totalMapSlots, 'map')
		self.calc_fair_share_helper(pools, cluster.totalRedSlots, 'red')
		
	def get_active_pools(self, pools):		
		for p in pools:
			if not pools[p]['queue'].isEmpty():
				self.activePools[p] = pools[p]
			
	def schedule(self, cluster, pools):
		self.log.write('%s: Scheduler started in %s mode\n' % (str(datetime.now()), self.mode))
		self.calculate_fair_shares(cluster, pools)
		self.get_active_pools(pools)
		
		cluster.start_cluster()
		
		threading.Thread(target=self.schedule_map_tasks, args=(cluster, )).start()
		threading.Thread(target=self.schedule_red_task, args=(cluster, )).start()
			
		while self.allJobsComplete == False:
			True
			
		cluster.stop_cluster()
		self.log.write('%s: Scheduler finished\n' % (str(datetime.now())))
		self.log.close()
			
class Cluster:
	def __init__(self):
		self.nodes = []
		self.totalMapSlots = 0
		self.totalRedSlots = 0
		
	def start_cluster(self):
		for node in self.nodes:
			node.start()
			
	def stop_cluster(self):
		for node in self.nodes:
			node.stop()
			node.join()
	
class ApplicationsManager:
	def __init__(self):
		self.pools = {'default':{'name':'default', 'type':'fifo', 'weight':1, 'minMapSlots':1, 'minRedSlots':1, 'queue':queues.FifoQueue()}}
		self.mode = 'fifo'
		self.jobsCount = 0
		
	def add_new_job(self, config):
		pool = 'default' if self.mode == 'fifo' else config.split()[0]
		subTime = datetime.now()
		mapTasks = int(config.split()[1])
		redTasks = int(config.split()[2])
		memPerMap = int(config.split()[3])
		memPerRed = int(config.split()[4])
		priority = 1
		
		if len(config.split()) == 6:
			priority = int(config.split()[5])
	
		if pool not in self.pools.keys():
			pool = 'default'

		newJob = {
			'id':self.jobsCount, 
			'pool':pool, 
			'subTime':subTime,
			'mapTasks':mapTasks, 
			'redTasks':redTasks,
			'mapActive':0,
			'redActive':0, 
			'memPerMap':memPerMap, 
			'memPerRed':memPerRed,
			'mapComplete':0,
			'redComplete':0,
			'priority':priority
			}
		
		self.pools[pool]['queue'].put(newJob)
		self.jobsCount += 1

class ResourceManager:	
	def __init__(self, mode = 'fifo'):
		self.scheduler = Scheduler(mode)
		self.appManager = ApplicationsManager()
		self.cluster = Cluster()
		self.mode = mode
			
	def add_new_machine(self, config):
		memory = int(config.split()[0])
		mapSlots = int(config.split()[1])
		redSlots = int(config.split()[2])
		self.cluster.totalMapSlots += mapSlots
		self.cluster.totalRedSlots += redSlots
		self.cluster.nodes.append(NodeManager(self, memory, mapSlots, redSlots))
		
	def add_new_pool(self, config):
		if self.mode == 'fair':
			name = config.split()[0]
			typ = config.split()[1]
			weight = int(config.split()[2]) if len(config.split()) > 2 else 1
			minMapSlots = int(config.split()[3]) if len(config.split()) > 3 else 1
			minRedSlots = int(config.split()[4]) if len(config.split()) > 4 else 1		
			
			if typ == 'fifo':
				self.appManager.pools[name] = {'name':name, 'type':typ, 'weight':weight, 'minMapSlots':minMapSlots, 'minRedSlots':minRedSlots, 'queue':queues.FifoQueue()}
			elif typ == 'fair':
				self.appManager.pools[name] = {'name':name, 'type':typ, 'weight':weight, 'minMapSlots':minMapSlots, 'minRedSlots':minRedSlots, 'queue':queues.FairQueue()}
			
	def add_new_job(self, config):
		self.appManager.add_new_job(config)
		
	def setMode(self, mode):
		self.mode = mode
		self.scheduler.mode = mode
		self.appManager.mode = mode
		
	def run(self):
		self.scheduler.schedule(self.cluster, self.appManager.pools)
			
