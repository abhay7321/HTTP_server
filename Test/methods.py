
import threading

import unittest
import requests
import sys



SERVER_URL = "http://127.0.0.1:" + sys.argv[2]



class test_GET(unittest.TestCase):



    def test_for_GET(self):

        print("\n\n\n\n....................Making a GET Request.......................")


        print("\nMaking a GET Request")
        try:
            r = requests.get(SERVER_URL + "/resources/hello.html")
            print("Status : "+ str(r.status_code) + " " + r.reason)
            print("Headers : ", r.headers)
        except Exception as ex:
            print('Exception has occured! = ', ex)


    def test_for_conditional_GET_If_Modified_Since(self):
        
        print("\n\nMaking a conditional GET Request with If-Modified-Since header")

        try:
            headers = dict()
            
            r = requests.get(SERVER_URL + "/resources/hello.html")
            
            print("Status : "+ str(r.status_code) +" " +r.reason)
            lm = r.headers['Last-Modified']
            headers['If-Modified-Since'] = lm
            print("Last Modified Date Obtained : ", lm)
            
            print("Sending a conditional GET with the If-Mod-Since same as Last-Modified")

            r = requests.get(SERVER_URL + "/resources/hello.html", headers=headers)
            print("Status : "+ str(r.status_code) +" " +r.reason)
            
            
            print("Sending a conditional GET with the If-Mod-Since older than Last-Modified")
            headers['If-Modified-Since'] = "Sat, 01 Jan 2000 09:20:08 GMT"
            
            r = requests.get(SERVER_URL + "/resources/hello.html", headers=headers)
            print("Status : "+ str(r.status_code) +" " +r.reason)
            
        except Exception as ex:
            print('Exception has occured! = ', ex)


    def test_for_conditional_GET_Range(self):
        print("\n\nMaking a conditional GET Request with Range header")
        try:
            r = requests.get(SERVER_URL + "/resources/hello.html")
            print("Status : "+ str(r.status_code) +" " +r.reason)
            length = int(r.headers['Content-Length'])
            
            print('Requesting 10 bytes less')
            r= requests.get(SERVER_URL + "/resources/hello.html",
                          headers={'Range': 'bytes=-'+str(length -10)})        
            print("Status : "+ str(r.status_code) +" " +r.reason)

        except Exception as ex:
            print('Exception has occured! = ', ex)


    def test_for_conditional_GET_If_Range(self):

        print("\n\nMaking a conditional GET Request with If-Range and Range header")
        try:
            headers = dict()
            r = requests.get(SERVER_URL + "/resources/hello.html")
            print("Status : "+ str(r.status_code) +" " +r.reason)
            lm = r.headers['Last-Modified']
            headers['If-Range'] = lm
            length = int(r.headers['Content-Length'])
            headers['Range'] = 'bytes=-'+str(length-10)


            print(f"Last Modified Date Obtained : {lm}")
            print(f"Sending a conditional GET with the If-Range same as Last-Modified")
            r = requests.get(SERVER_URL + "/resources/hello.html", headers=headers)
            print("Status : "+ str(r.status_code) +" " +r.reason)


            print(f"Sending a conditional GET with the If-Range older than Last-Modified")
            headers['If-Range'] = "Sat, 01 Jan 2000 09:20:08 GMT"
            r = requests.get(SERVER_URL + "/resources/hello.html", headers=headers)
            print("Status : "+ str(r.status_code) +" " +r.reason)

        except Exception as ex:
            print('Exception has occured! = ', ex)


class test_HEAD(unittest.TestCase):
    
    
    
    def test_for_HEAD(self):
        
        print("\n\n\n\n....................Making a HEAD Request.......................")
        
        
        print("\nMaking a HEAD Request")
        try:
            r = requests.head(SERVER_URL + "/resources/hello.html")
            print(f"Status : {r.status_code} {r.reason}")
            print("Headers:", r.headers)
        except Exception as ex:
            print('Exception has occured! = ', ex)

       
    def test_for_conditional_HEAD_If_Modified_Since(self):
        
        print("\n\nMaking a conditional HEAD Request with If-Modified-Since header")

        try:
            headers = dict()
            r = requests.head(SERVER_URL + "/resources/hello.html")
            print(f"Status : {r.status_code} {r.reason}")
            lm = r.headers['Last-Modified']
            headers['If-Modified-Since'] = lm
            print(f"Last Modified Date Obtained : {lm}")
            print("Sending a conditional HEAD with the If-Mod-Since same as Last-Modified")
            r = requests.head(SERVER_URL + "/resources/hello.html", headers=headers)
            print(f"Status : {r.status_code} {r.reason}")
            
            
            print("Sending a conditional HEAD with the If-Mod-Since older than Last-Modified")
            headers['If-Modified-Since'] = "Tue, 27 Oct 1999 08:57:08 GMT"
            r = requests.head(SERVER_URL + "/resources/hello.html", headers=headers)
            print(f"Status : {r.status_code} {r.reason}")

        except Exception as ex:
            print('Exception has occured! = ', ex)


    def test_for_conditional_HEAD_Range(self):
        print("\n\nMaking a conditional HEAD Request with Range header")
        try:
            r = requests.head(SERVER_URL + "/resources/hello.html")
            print(f"Status : {r.status_code} {r.reason}")


            length = int(r.headers['Content-Length'])
            print('Requesting 7 bytes less')
            r= requests.head(SERVER_URL + "/resources/hello.html",
                          headers={'Range': 'bytes=-'+str(length -7)})        
            print(f"Status : {r.status_code} {r.reason}")

        except Exception as ex:
            print('Exception has occured! = ', ex)


    def test_for_conditional_HEAD_If_Range(self):


        print("\n\nMaking a Normal HEAD Request")
        try:
            headers = dict()
            r = requests.head(SERVER_URL + "/resources/hello.html")
            print(f"Status : {r.status_code} {r.reason}")
            lm = r.headers['Last-Modified']
            headers['If-Range'] = lm
            length = int(r.headers['Content-Length'])
            headers['Range'] = 'bytes=-'+str(length-10)



            print(f"Last Modified Date Obtained : {lm}")
            print(f"Sending a conditional HEAD with the If-Range same as Last-Modified")
            r = requests.head(SERVER_URL + "/resources/hello.html", headers=headers)
            print(f"Status : {r.status_code} {r.reason}")


            print(f"Sending a conditional HEAD with the If-Range older than Last-Modified")
            headers['If-Range'] = "Tue, 27 Oct 1999 08:57:08 GMT"
            r = requests.head(SERVER_URL + "/resources/hello.html", headers=headers)
            print(f"Status : {r.status_code} {r.reason}")

        except Exception as ex:
            print('Exception has occured! = ', ex)



class test_DELETE(unittest.TestCase):



    def test_for_DELETE(self):

        print("\n\n\n\n....................Making a DELETE Request.......................")
        
        
        print("\nMaking a normal DELETE Request")
        try:
            r = requests.delete(SERVER_URL + "/resources/deletetest1.txt")
            print("Status : "+ str(r.status_code) +" " +r.reason)
            print("Headers:", r.headers)
        except Exception as ex:
            print('Exception has occured! = ', ex)



class test_POST(unittest.TestCase):
    def test_for_POST(self):
        try:
            print("\n\n\n\n.......................Making a POST Request.................")
            data = b"hIIIIII"
            r = requests.post(SERVER_URL + "/test",
                data=data,
                headers={'Content-Type': 'text/plain'}
            )
            print("Status : "+ str(r.status_code) +" " +r.reason)
            print("Headers:", r.headers)
        except Exception as ex:
            print('Exception has occured! = ', ex)
 
 


class test_PUT(unittest.TestCase):
    def test_for_PUT(self):
        print("\n\n\n\n....................Making a PUT Request.......................")
        try:            
            data = b"hIIIIII"
            r = requests.put(SERVER_URL + "/test.txt",
                data=data,
                headers={'Content-Type': 'text/plain'}
            )
            print("Status : "+ str(r.status_code) +" " +r.reason)
            print("Headers:", r.headers)
        except Exception as ex:
            print('Exception has occured! = ', ex)





if __name__ == '__main__':

    n_clientThreads = int(sys.argv[1])
    unittest.main(verbosity=2, argv=[sys.argv[0]])
      
    