
import unittest
import requests
import sys


SERVER_URL = "http://127.0.0.1:" + sys.argv[2]



class test_cookies(unittest.TestCase):
    
    def runTest(self):
        """Testing Cookies"""
        try:
            print("\nCreating a cookie store...")
            session = requests.Session()
            print("Content in cookie store before request:")
            print(session.cookies.get_dict())
            print("Making 1st GET Request...")
            response = session.get(SERVER_URL + "/")
            print("Content in cookie store after request:")
            print(session.cookies.get_dict())
            print("Making 2nd GET Request... (Cookie returned should now be same)")
            response = session.get(SERVER_URL + "/")
            print("Content in cookie store after 2nd request:")
            print(session.cookies.get_dict())
            print("Clearing cookie store...")
            session.cookies.clear()
            print("Making 3rd GET Request... (Cookie returned should now be a new unique cookie since cookie store is empty)")
            response = session.get(SERVER_URL + "/")
            print("Content in cookie store after 3rd request:")
            print(session.cookies.get_dict())
        except Exception as ex:
            print('Something went horribly wrong!', ex)
        finally:
            return



if __name__ == '__main__':
    
    n_clientThreads = int(sys.argv[1])
    unittest.main(verbosity=2, argv=[sys.argv[0]])
  