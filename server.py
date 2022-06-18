from HttpMethods import *


class TCP:
    
	#Just populating ip_address(host) and port number of server
	def __init__(self, host='127.0.0.1'):
		self.host = host
		try:
			self.port = int(sys.argv[1])
		except Exception as e:
			self.port = int(config['TCP']['port'])

	#server starts on calling the start_tcp function
	def start_tcp(self):
     
		# create a TCP socket object for listening to TCP requests
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        		
		
		# bind the socket object to the address and port
		s.bind((self.host, self.port))	        
		
		# start listening for connection requests
		s.listen(int(config['TCP']['queuesize']))

		print("Server is listening at : ", s.getsockname(),'\n')

		# List which stores ClientThreads objects
		threads = []

		# MAX TCP connections that we can have working simultaneously
		max_simul_connec = int(config['TCP']['max_conn'])

		# Server is listening
		# It is waiting on s.accept() till any client makes an http request to it
		# When some client makes an request, it creates an connection socket for it
		# Then this http request is processed on new thread
		while True:
      
			# Creates a new connection socket and accept new connection
			conn, (ip, port) = s.accept()
			print("\n\nConnected by a client with address : ", ip," ",port)

			if(threading.active_count()<=max_simul_connec):
				#Creating a new client thread object 
				newthread = ClientThread(conn, ip, port)

				#Whenever we use multithreading in python we must have a run method in the class(which is inheriting Thread class) to do multi-threading.
				# The class that inherits Thread class must have a run method in it , which will be executed as a thread function when an instance of that class(child of thread class) calls .start method.

				newthread.start()
				threads.append(newthread)
			else:
				print("\nMaximum Connections reached\n")


#Instances of this class are created every time server receives a connection request.
class ClientThread(Thread):

	def __init__(self, conn, ip, port): 
		Thread.__init__(self)
		self.conn = conn 
		self.ip = ip 
		self.port = port 
		print ("New server socket thread started for " + ip + ":" + str(port), '\n')
 
	# This methods executes on a separate thread ,  when an instance of this class calls the start method (Becoz this class is inherited from Thread class).
	def run(self):

		#Connection: keep-alive/close
		connection = ['keep-alive']

		# keep_alive = [timeout, max]
		# max tells the maximum nos of http requests that can be handled through a single tcp connection
		# it will get overwritten when connection_parameter is overwritten
		keep_alive = [None, None]

		# this will get over-written in the HttpMethods class
		connection_parameters = [connection, keep_alive]
		
		#Request count for a specific socket(in persistent connection)
		request_count = 0

		#DOUBT : ithe kay kelay SHETTA kahi samjana
		self.conn.settimeout(2)


		#Accept request on the same connection socket till Connetion(Header in request) is keep-alive.
		while(connection_parameters[0][0] == 'keep-alive'):

			try:
			
				#Recive data(request) from the connection socket.
				data = self.conn.recv(2048) 

				#If server didn't receive any data
				if (len(data) == 0):
					self.conn.close()
					break;

				#Increment request count, request count is used for maximum nos of request through a single TCP connection
				request_count += 1

				print("client :" + str(self.ip) +':'+ str(self.port) + '   request count = ', request_count)

				print("\nRequest : \n", data)

				#Created object of HttpMethods class to call handle_request() function
				http_server_object = HttpMethods()
				response = http_server_object.handle_request(data, connection_parameters)


				# Send response back to client
				self.conn.send(response)


				max_requests = connection_parameters[1][1]
				if (max_requests != None):
					max_requests = int(max_requests)

				
				# If maximum nos of request through the same connections have been made then close the connection.
				if (request_count == max_requests):
					self.conn.close()
					break

				#Setting the timeout value for connection socket, if no request received within this time then throw socket.timeout exception
				t_out = connection_parameters[1][0]
				if (t_out == None):
					t_out = 2		#default server timeout
				else :
					t_out = int(t_out)
     
				# Setting timeout value here
				self.conn.settimeout(t_out)
    
			except socket.timeout as t:
				self.conn.close()
				break


if __name__ == '__main__':
    tcp_server = TCP()
    tcp_server.start_tcp()