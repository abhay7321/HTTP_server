import socket
import sys
from threading import Thread
import threading
import os
import mimetypes
from configparser import ConfigParser
from utility import *
from HttpRequest import *

file='config.ini'
config=ConfigParser()
config.read(file)


Avalaible_Content_Encoding_on_server = ['gzip', 'deflate']

server_root = str(config['http']['server_root'])

#Dictionary contains Headers and their default values
headers = {    
		'Server': 'http-server',
		'Accept-Ranges': 'bytes',
		'Date' : '01/01/2000',
		'Content-Language': 'en-US'
	}


#Dictionary contains status codes
status_codes = {
		200: 'OK',
		201: 'Created',
  		202: 'Accepted',
		204: 'No Content',
		206: 'Partial Content',
  		304: 'Not Modified',
		404: 'Not Found',
		406: 'Not Acceptable',
  		412: 'Precondition Failed',
		416: 'Range Not Satisfiable',
		501: 'Not Implemented'
	}


#This Function Returns response line
def response_line(status_code):
	reason = status_codes[status_code]
	line = "HTTP/1.1 %s %s\r\n" % (status_code, reason)
    # call encode to convert str to bytes
	return line.encode() 


# Request is object of class HttpRequest class
# This function gives all the headers associated to the response
# extra_headers is a dictionary containg key value pairs of some different header fields
def response_headers(request=None, extra_headers = None): 

	header_response = ""
		
	headers_copy = headers.copy()
 
	if (extra_headers != None):
		headers_copy.update(extra_headers)
  
	for h in headers_copy:
		if (h == "Date"):
			value = get_date_and_time().decode()
			header_response += "%s: %s\r\n" % (h, value)

		elif (h == "Last-Modified" and request != None) :
			value = last_modified(request.uri)
			header_response += "%s: %s\r\n" % (h, value)

		else :
			header_response += "%s: %s\r\n" % (h, headers_copy[h])
   
    # call encode to convert str to bytes
	return header_response.encode() 
