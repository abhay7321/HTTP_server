#This class contains all imp attributes([method, uri, http_version], [request_headers_dict], [request_msg]) from http request
#It also has a parser method to parse the http request msg and populate the above attribute feilds.



#Flow of data(raw http reuqest)
# 1.recieved from connection socket					(In client thread class run method)
# 2.passed as a parameter to handle_request			(In client thread class run method)
# 3.in handle request HttpRequest class object is created in which this "data" is passed to its constructor
# 4.Data is then parsed into above fields, where paraser function is called in constructor itself.



# Class to Parse Request recieved from clients
class HttpRequest:
	def __init__(self, data):
		self.method = None
		self.uri = ""
		self.http_version = "1.1"

		# collected the message body and store them in a list
		self.request_msg = []
	
		# created a dictonary for headers to eaisly access the headers and values for the headers 
		self.req_headers_dict = {}
	 
		# call self.parse() method to parse the request data
		self.parse(data)

	# data is the HTTP request made by the client
	def parse(self, data):
		try:
			# To remove LWS from beggining and end of the data 
			data = data.strip(b" ")
			
			#Created a List where each element contains a line from request made by client 
			lines = data.split(b"\r\n")

			#First line of request is request line 
			request_line = lines[0]

			#Request-Line = Method SP Request-URI SP HTTP-Version CRLF
			words = request_line.split(b" ")

			#Extracting method , uri , http version from the request line
			self.method = words[0].decode() # call decode to convert bytes to str
			self.uri = words[1].decode() 
			self.http_version = words[2].decode()


			# Removed request line from the request
			lines = lines[1:]


			# find the index for the blank line  ,so we can separate the headers and the message body
			blank_line_index = 0
			for l in lines:
				if (l == b""):
					break
				blank_line_index += 1


			# collected the message body and store it in a list
			for m in lines[blank_line_index+1:]:
				self.request_msg.append(m.decode())


			# collected all the headers (All Headers present before the blank line)
			request_headers = lines[:blank_line_index]


			# created a dictonary for headers to eaisly access the headers and values for the headers  
			for i in request_headers:
				entry = i.split(b":")
				self.req_headers_dict[entry[0].decode().strip()] = entry[1].decode().strip()


		except Exception as e:
			pass

	# Returns a list of connection_parameter(which we saw in run method of ClientTheread class)
	# connection_parameters = [connection, keep_alive]
	#Connection: keep-alive/close
	# keep_alive = [timeout, max]
	def get_connection_parameters(self):
		
		lst = [[None], [None, None]]
  
		if ('Connection' in self.req_headers_dict.keys()) :
			
			#Connection: keep-alive/close
			conn_value =  self.req_headers_dict['Connection']
			lst[0][0] = conn_value

   
			if (conn_value == 'keep-alive'):

				# keep_alive = [timeout, max]
				if ('Keep-Alive' in self.req_headers_dict.keys()) :
					
					param = self.req_headers_dict['Keep-Alive']
					param = param.split(",")

					par1 = param[0]
					p1 = par1.split('=')
					if (p1[0].strip() == 'timeout'):
						lst[1][0] = p1[1]
					elif (p1[0].strip() == 'max'):
						lst[1][1] = p1[1]

					if (len(param) != 1):
						par2 = param[1]
						p2 = par2.split('=')
						if (p2[0].strip() == 'timeout'):
							lst[1][0] = p2[1]
						elif (p2[0].strip() == 'max'):
							lst[1][1] = p2[1]

		return lst 



