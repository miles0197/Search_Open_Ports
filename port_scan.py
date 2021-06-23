import socket
import threading
from queue import Queue

target = '127.0.0.1' #loopback, could be changed to something else
queue = Queue()
open_ports = []
##############################################################################################################################
# We start by creating a function called portscan with the givenparameter  port. 
# Then we create our socket with the imported socket module and use it on line 18
# In order to establish end-to-end connection initialization, bound the socket inside tuple with the parameters,
# a target IP address and a port number as seen in line 19.
# Portscan function will return true, but if there is some error such as not being able to create a network socket, 
# it will go to the except clause and return False.
##############################################################################################################################
def portscan(port): #scan port 
	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create socket
		sock.connect((target,port))
		return True 
	except:
		return False

##############################################################################################################################
# We  define a for loop and for each port along the range (1,1024), we define a result variable that is equal to 
# calling the function portscan to check for establishing connection for each port number.
# and if that result returns to be True, we print open ports, otherwise, we print that the port is closed.		
##############################################################################################################################
for port in range(1,1024):
	result = portscan(port)
	if result:
		print("Port {} is open...".format(port))
	else:
		print("Port {} is closed...".format(port))

##############################################################################################################################
# However, doing this as a very slow process checking each port one by one, you can check this by running the code thus far.
# But to change that, we can introduce multi-threading and Queues
# import modules threading and “from queue import Queue”
# then we want to create a function that will fill our queue with open ports.
# the method fill_queue with parameters (from_port, to_port)
# for each port in the port_list, we will put that port to the queue.
##############################################################################################################################
def fill_queue(port_list):
	for port in port_list:
		queue.put(port)

##############################################################################################################################
# The next step is to define a worker method which will actually be used by our threads, so this will be the main portion 
# where we run threads while referring to the worker function. We say that while q is not empty,
# meaning as long as there are elements in the Queue, we say port = queue.get() and we get a port,
# and if that port is open, we will print it’s open.
# Additionally, we will add the open port to our open_ports list with the .append method.		
##############################################################################################################################
def worker():

	while not queue.empty():
		port = queue.get()
		if portscan(port):
			print("Port [] is open...".format(port))
			open_ports.append(port)

		#otherwise don't do anything
		#You could potentially throw and else statement there but since we will run a lot of threads, 
		#not necessary for now
		 
# We define a range of numbers and assign it to a variable called variable_list that will store them.
# Then we call the fill_queue function with our current port_list parameter for evaluation. You can follow what the code does when
# it calls the fill_queue function.
port_list = range(1,1024)
fill_queue(port_list)

# Next, we will define a thread_list, you do not really need to define a list to run your threads
thread_list = []

# Specifiy the number of threads we want to run and assign it to our target function worker, we are not calling it but referring to it.
for t in range(1000):
	thread = threading.Thread(target = worker)
	thread_list.append(thread) #add the threads to our thread list 

for thread in thread_list: #now we run all of the threads
	thread.start()

for thread in thread_list: # Need this join method cuz this method allows the each process to wait for another to finish. 
						  
	thread.join()

print("Open ports are: ", open_ports)
