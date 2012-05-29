#!/usr/bin/python
'''
blurb: a Simple Python Threading Example with Thread Timeouts

If you're writing a threaded application in python, you need to be able to manage your threads. I have done this following this strategy:

Use a handful of initiator threads to manage Threading.
Put all threads onto a global stack ( a python list ) for tracking.
Attach a timeout thread to each thread when spawning it with a timeout value and function to call when timeout reached, This function will kill the parent thread.
Upon work completion a thread will stop the timeout thread and start a new one with timeout of 1 second
The timeout method calls the threads internal self.nuke() method.
A periodic watchdog will go through the thread stack and cleanup stuck threads
REMEMBER! If you call sys.exit() from within a thread, it will only exit the thread and not your whole program.

ALSO! Threading runs much better on 64bit OS's

Heres a example python script for creating thousands of threads and attaching a timer to each one to forcefully kill the thread if it stops responding.I wrote this for a threaded monitoring application which suffered from socket timeouts when monitoring targets were down.

'''

import threading
import thread
import sys
import time
from random import randrange

# max threads to run simultaneously
max_threads = 1000

# initiators are the number of threads initiating the someThreadFunction, I use more multiple initiators to spawn threads even faster
initiators = 2

# timeout in seconds for a thread to live
thread_timeout = 30

# initializing some counters
threads_spawned_count = 0
threads = []
running = True
debug = True
initiator_count = 0
initiatorThreads = []

def debugMsg(msg):
	if debug == True:
		sys.stdout.write("DEBUG: " + msg + "\n")

class someThreadFunction(threading.Thread):
	def __init__(self,threadId):
		# Initialize the Threading
		threading.Thread.__init__(self)
		# I use threads_spawned_count in the calling function to name and track
		# my thread, this also used to cleanup the thread and recover memory
		self.threadId = threadId
		# a boolean which says this thread is allowed to live or not
		self.allowedToLive = True
		# Start the timer and call self.nuke when it is reached
		self.t = threading.Timer(thread_timeout,self.nuke)

		self.exectime = randrange(20,45,5)
		debugMsg(str(self) + " will take " + str(self.exectime) + " to complete")

	def run(self):
		debugMsg(str(self) + " Initializing my timer ")
		self.t.start()
		if self.allowedToLive: 
			#while self.allowedToLive: # if you use while, the self.allowedToLive is critical to ending the while
			debugMsg(str(self) + " EXECUTING ")
			# Just going to sleep for random time, This is where your code executes...
			time.sleep(self.exectime)
			debugMsg(str(self) + " managed to complete its task within timeout")
			self.allowedToLive = False

		# kill via a schedule
		debugMsg(str(self) + " Happily scheduling my own descruction")
		self.t.cancel()
		self.t = threading.Timer(1,self.nuke)
		self.t.start()
			

	def nuke(self):
		# set autodestruct, remove thread from stack and exit thread
		global threads
		try:
			threads.remove([self.threadId,self])
			debugMsg("SUCCESS, I managed to nuke myself")
		except:
			# If this happens Its up to the watchdog to garbage collect this thread...
			debugMsg("WARNING: thread: " + str(self.threadId) + ":" + str(self) + " could not be deleted from list")
		sys.exit()


class initiatorFunction(threading.Thread):
	def __init__(self):
		# Initialize the Threading
		threading.Thread.__init__(self)
	
	def run(self):
		try:
			global threads
			global max_threads
			global threads_spawned_count
			while running == True:
				if len(threads) < max_threads:
					try:
						debugMsg(str(self)+" INITIATOR Spawning new thread since len(threads) is less than " + str(max_threads))
						current = someThreadFunction(threads_spawned_count)
						threads.append([threads_spawned_count,current])
						current.start()
						del current
						threads_spawned_count = threads_spawned_count + 1
						debugMsg(str(self)+" INITIATOR Running " + str(len(threads)) + " threads so far")
						print "INITIATOR Active Threads " + str(threading.activeCount()) + " including thread timeout timers"
					except:
						debugMsg("Unable to spawn thread, probably os limit")
						time.sleep(1)
				else:
					debugMsg(str(self)+" INITIATOR Waiting for a thread to timeout / die which will reduce threads_count")
					time.sleep(randrange(2,5,1))
					debugMsg(str(self)+" INITIATOR Running Threads " + str(threads))
					print "INITIATIOR " + str(len(threads)) + " threads in stack"
					print "INITIATIOR Active Threads:" + str(threading.activeCount()) + " including thread timeout timers"
					time.sleep(1)
		except Exception, e:
			debugMsg("WARNING: a initiator has died")
			debugMsg(str(e))
			global initiator_count
			initiator_count = initiator_count - 1
			

	

# Main loop, if you dont need the initiators like I did, you can redirect this to your function directly
while True:
	try:
		if initiator_count < initiators:
			debugMsg("NEW INITIATOR THREAD")
			current = initiatorFunction()
			current.start()
			initiator_count = initiator_count + 1
			initiatorThreads.append(current)
			del current
			time.sleep(0.3)
		else:
			debugMsg(str(initiator_count) + " INITIATORS ALREADY SPAWNED")
			# lets babysit the stack
			for th in threads:
				if not th[1].isAlive():
					debugMsg("I think thread " + str(th) + " is dead because " + str(th[1].isAlive()))
					th[1].nuke
					threads.remove(th)
			time.sleep(10)

	except KeyboardInterrupt, e:
		running = False
		debugMsg("Terminating All Threads")
		for mythread in threads:
			debugMsg("Stopping Thread by force " + str(mythread))
			mythread[1].nuke
		sys.exit()
