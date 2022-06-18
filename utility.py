import os
import datetime
from datetime import timedelta
import time
import stat
import string    
import random # To generate random alphanumeric string (for cookie)
import json
import gzip
import zlib

# Add new cookie with count=1 in our server's cookie file
# Called by set_cookie method
def add_cookie(random_id, user_agent):
    
    try:
    
        #Open cookie file and read data
        with open("cookie.json") as json_file:
            json_decoded = json.load(json_file)
        
        value = {"user-agent" : user_agent, "count" : 1}
        

        #Add the above key-value pair to the content of json file.
        json_decoded[random_id] = value
        
        #Write in cookie file
        with open("cookie.json", 'w') as json_out_file:
            json.dump(json_decoded, json_out_file)
            
    except json.JSONDecodeError:
        pass

# Generate random, unique alphanumeric string(length=9) as cookie id and add it to server's cookie file
# Its called by cookie functionality method , and it returns the cookie id and its expiration date_time(1 day ahead of current date_time) 
# It gives a call to add cookie to add new clients cookie to the server cookie file
def set_cookie(request):
    
    # number of characters in the string.
    n = 9
    
    #generate random alphanumeric string of length = n, here n=9.
    random_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k = n))
    
    #Now calculate the cookie expiry date and time.
    expiry = get_date_and_time(False)

    #Find the user agent from request headers
    user_agent = request.req_headers_dict['User-Agent']
    
    # #Now create the value for Set-Cookie response header 
    # value = "user-agent=" + user_agent + "; count=1"
    
    
    #Append the cookie info in cookie file.
    add_cookie(random_id, user_agent)
    
    #Return data to be sent in Set-Cookie header
    r = "id=" + random_id + "; Expires=" + expiry.decode() 
    
    return r

#Increment the cookie count by one for the specific cookie id extracted from the request header
def update_cookie(request):
    
    try:
    
        #First find the user agent from request headers
        cookies_in_request = request.req_headers_dict['Cookie'].split(";")
        
        # print(cookies_in_request)
        # print(type(cookies_in_request))
        
        with open("cookie.json") as json_file:
            json_decoded = json.load(json_file)
        
        # For cookie in request header, see if that is present in server's cookie file.
        for key in cookies_in_request:
            
            key.strip()
            key = key.split("=")
            key = key[1]
            # print(key)
            
            #if cookie is present in request, increment the count
            if (key in json_decoded.keys()):
                
                #Increase the count for that specific cookie
                value_dict = json_decoded[key]
                n = value_dict["count"]
                value_dict["count"] = n + 1
                
        with open("cookie.json", 'w') as json_out_file:
            json.dump(json_decoded, json_out_file)

    except json.JSONDecodeError:
        pass

# If cookie is in request header of client , it updates the cookie by giving call to update_cookie method
# If cookie is not in request header of client , 
    # A)it sets the cookie by giving call to set_cookie method
    # B)it also sends set-cookie header in response
def cookie_funcationality_in_method(request, respon_headers):
    #If Cookie header is present in request
    if ('Cookie' in request.req_headers_dict.keys()):
        update_cookie(request)
		
    #If Cookie header is not present in request
    else :
        cookie = set_cookie(request)
        respon_headers = append_additional_header(respon_headers, 'Set-Cookie', cookie)

    return respon_headers
    
#It appends Connection and Keep-alive header to response headers, if they are present in request headers(with same values as of request headers)
def connection_parameters_headers_append(request, respon_headers):
    if ('Connection' in request.req_headers_dict.keys()):
        respon_headers = append_additional_header(respon_headers, 'Connection', request.req_headers_dict['Connection'])
        if ('Keep-Alive' in request.req_headers_dict.keys()):
            respon_headers = append_additional_header(respon_headers, 'Keep-Alive', request.req_headers_dict['Keep-Alive'])
    
    return respon_headers

#This function appends new header and its value to already existing headers
def append_additional_header(headers, additional_header_name, additional_header_value):
    
    headers = headers.decode()
    headers += "%s: %s\r\n" % (additional_header_name, additional_header_value)
    return headers.encode()



#To get the value for Date Header Field
def get_date_and_time(today=True) :
    
    months = {'01':"Jan", '02':"Feb" , '03':"Mar", '04':"Apr", '5':"May", '06':"Jun", '07':"Jul", '08':"Aug", '09':"Sep",  '10':"Oct",  '11':"Nov",  '12':"Dec"}
    
    week_days = {0: 'Mon', 1: 'Tue', 2: 'Wed', 3: 'Thu', 4: 'Fri', 5: 'Sat', 6: 'Sun'}
    
    current_time = datetime.datetime.now() 
    
    if (today == False):
        current_time = current_time + timedelta(days=1)
    
    weekday = datetime.datetime.today().weekday()
    
    if (today == False):
        weekday += 1
        weekday = weekday % 7
    weekday = week_days[weekday].encode()
    
    
    day = current_time.day
    day=str(day).encode()
    month = current_time.month
    # print(month)
    month = months[str(month)].encode()
    year = str(current_time.year).encode()
        
        
    hour = current_time.hour
    if (hour <10):
        hour = "0" + str(hour)
    else :
        hour = str(hour)
    hour = hour.encode()
    
    minutes = current_time.minute
    if (minutes <10):
        minutes = "0" + str(minutes)
    else :
        minutes = str(minutes)
    minutes = minutes.encode()
    
    seconds = current_time.second
    if (seconds <10):
        seconds = "0" + str(seconds)
    else :
        seconds = str(seconds)
    seconds = seconds.encode()
    
       
    return b"".join([weekday, b", ", day, b" ", month, b" ", year, b" ", hour, b":", minutes, b":", seconds, b" ", b"GMT"])


#To get the value for Last-Modified Header Field
def last_modified(path) :
    
	path = path.strip("/")
	fileStatsObj = os.stat (path)
	modificationTime = time.ctime ( fileStatsObj [ stat.ST_MTIME ] )
	l = modificationTime.split(" ")
	msg = l[0] + ", " + l[2] + " " + l[1] + " " + l[4] + " "+ l[3] + " GMT"
 
	return msg


#To parse Range header. And storing the list of ranges i.e.[start, end] in a list.
def parse_range(value):
    
	value=value.split('=',1)
	value = value[1]
	value=value.split(',')

	res=[]
	#3 cases are possible here st-end , st- , -end
	for i in value :
		i=i.split('-')
		i[0] = i[0].strip()
		i[1] = i[1].strip()
		res.append([i[0],i[1]])

	#returning list of ranges(also a list of length 2)
	return res


#TO DO : validate the ranges by : check if any 2 pair of range overlap or not,
# check if range lies in 0 - length_of_resource
def validate_ranges(pairs_of_ranges, lenth_of_resource):
    
	
	return True
	
 
#Compares dates, return true when date1 < date2 else false 
def compare_dates(date1, date2):
    #TO DO : complete the function
    return True


#This functions carry out the encoding passed as parameter on the body and returns the encoded body.
def Content_Encoding(response, encoding):
    
    if (encoding == 'gzip'):
        response = gzip.compress(response)
    
    elif (encoding == 'deflate'):
        response = zlib.compress(response)
        
    # print(response)
    return response

