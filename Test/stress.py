
import threading

import unittest
import requests

import sys



SERVER_URL = "http://127.0.0.1:12000"




class stress_get(unittest.TestCase):

    def runTest(self):


        print(f"\nDispatching {n_clientThreads} GET Request Threads")

        request_threads = []
        try:
            def get_test():
                try:
                    r = requests.get(SERVER_URL + "/resources/hello.html")

                    print(f"Status : {r.status_code} {r.reason}")
                except:
                    print("Error in making request, maybe server queue is full")

            for i in range(n_clientThreads):
                t = threading.Thread(target=get_test)
                request_threads.append(t)
                t.start()

            # Wait until all of the threads are complete
            for thread in request_threads:
                thread.join()
            
            # print("All GET Requests Complete")
        except Exception as ex:
            print('Something went horribly wrong!', ex)
        finally:
            # Stop all running threads
            return


class stress_post(unittest.TestCase):

    def runTest(self):

        print(f"\nDispatching {n_clientThreads} POST Request Threads")

        request_threads = []
        try:
            def post_test():
                data = 'Hiiii'
                try:
                    r = requests.post(SERVER_URL + "/resources/test",
                        data=data,
                        headers={'Content-Type': 'text/plain'}
                    )
                    print(f"Status : {r.status_code} {r.reason}")
                except:
                    print("Error in making request, maybe server queue is full")
            
            for i in range(n_clientThreads):
                t = threading.Thread(target=post_test)
                request_threads.append(t)
                t.start()

            for thread in request_threads:
                thread.join()
            
        except Exception as ex:
            print('Something went horribly wrong!', ex)
        finally:
            # Stop all running threads
            return

class stress_head(unittest.TestCase):

    def runTest(self):


        print(f"\nDispatching {n_clientThreads} HEAD Request Threads")
        request_threads = []
        try:
            def head_test():
                try:
                    r = requests.head(SERVER_URL + "/resources/hello.html")
                    print(f"Status : {r.status_code} {r.reason}")
                except:
                    print("Error in making request, maybe server queue is full") 

            for i in range(n_clientThreads):
                t = threading.Thread(target=head_test)
                request_threads.append(t)
                t.start()

            for thread in request_threads:
                thread.join()
            
        except Exception as ex:
            print('Something went horribly wrong!', ex)
        finally:
            # Stop all running threads
            return

class stress_put(unittest.TestCase):

    def runTest(self):


        print(f"\nDispatching {n_clientThreads} PUT Request Threads")

        request_threads = []
        try:
            def put_test(fileno):
                data='Hiiii'
                try:
                    r = requests.put(SERVER_URL + "/resources/test",
                        data = data,
                        headers={'Content-Type': 'text/plain'}
                    )
                    print(f"Status : {r.status_code} {r.reason}")
                except:
                    print("Error in making request, maybe server queue is full")
            

            for i in range(n_clientThreads):
                t = threading.Thread(target=put_test, args=(i+1,))
                request_threads.append(t)
                t.start()


            for thread in request_threads:
                thread.join()
            
        except Exception as ex:
            print('Something went horribly wrong!', ex)
        finally:
            # Stop all running threads
            return

class stress_delete(unittest.TestCase):

    def runTest(self):

        print(f"\nDispatching {n_clientThreads} DELETE Request Threads")
        request_threads = []
        try:
            def delete_test(fileno):
                try:
                    r = requests.delete(SERVER_URL + "/resources/deletetest1.txt")
                    print(f"Status : {r.status_code} {r.reason}")
                except:
                    print("Error in making request, maybe server queue is full")


            for i in range(n_clientThreads):
                t = threading.Thread(target=delete_test, args=(i+1,))
                request_threads.append(t)
                t.start()


            for thread in request_threads:
                thread.join()
            
        except Exception as ex:
            print('Something went horribly wrong!', ex)
        finally:

            return

if __name__ == '__main__':

    n_clientThreads = int(sys.argv[1])
    unittest.main(verbosity=2, argv=[sys.argv[0]])