<div align="center">
	<h1>Http Server</h1>
</div>
<div align="center">
   <img align="center" width=50% src="assets/server.png" >
</div>

---

## Contents

- [About](#about)
- [Building](#building)
- [Configuration](#configuration)
- [Implementation Details](#implementation_details)
- [Running Tests](#tests)
- [Resources](#resources)

## About

This is a multi-threaded web server based on HTTP/1.1 Protocol. It can host different resources and can handle basic `HTTP` methods like `GET`, `POST`, `PUT`, `DELETE` and `HEAD` simultaneously.

### Prerequisites

1. Python 3.x

## Building 

Follow the below steps to start the server

```sh
python3 server.py <port_no>
```

This will start the server on the port passed as command line argument. If port is not specified then the server will start on the default port as mentioned in the configuration file.

Once the server starts, it can process multiple `HTTP Requests` from different clients simultaneously.

## Configuration

To specify custom configuration edit the config file `config.ini`. The following options are available in the config file

```
1. port = Specify the port on which the server will keep listenting
2. queuesize = Specifies the number of unaccepted connections that the server will allow before refusing new connections
3. max_conn = Specify the maximum number of simultaneous connections that the server will process
4. resp_code_del = Specify the response code for DELETE  method
5. server_root = Specify the document root directory that will serve the requests
```

## Implementation Details

### HTTP Request [refer](https://www.tutorialspoint.com/http/http_requests.htm)

The structure of HTTP request is as follows
  * A Request line
  * Zero or more header fields followed by CRLF
  * An empty line
  * Optionally a message-body

When a client sends a HTTP request to the server, first the server will parse the request into the respective fields mentioned above. Based on the method the server will the process the request.

### HTTP Methods [refer](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods)

The server can process following methods

* GET
* HEAD
* DELETE
* POST
* PUT

### HTTP Headers [refer](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers)

The following HTTP headres are handled by the server

* Server
* Accept-Ranges
* Date
* User-Agent
* Content-Language
* If-Modified-Since
* If-Unmodified-Since
* If-Range
* Range
* Last-Modified
* Content-Type
* Content-Length
* Location
* Connection
* Keep-Alive
* Cookie

### HTTP Status codes [refer](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)

The following status codes are implemented

* 200: 'OK',
* 201: 'Created',
* 202: 'Accepted',
* 204: 'No Content',
* 206: 'Partial Content',
* 304: 'Not Modified',
* 404: 'Not Found',
* 406: 'Not Acceptable',
* 412: 'Precondition Failed',
* 416: 'Range Not Satisfiable',
* 501: 'Not Implemented'

### HTTP Response [refer](https://www.tutorialspoint.com/http/http_responses.htm#:~:text=After%20receiving%20and%20interpreting%20a,end%20of%20the%20header%20fields)

After processing the client request, the server creates a HTTP response and sends it back to that specific client.
The HTTP response structure is same as of HTTP request except the first line is status line.


### Connection Request [refer](https://developer.mozilla.org/en-US/docs/Web/HTTP/Connection_management_in_HTTP_1.x)

The server can handle both the types of connection requests
* Persistent
* Non-Persistent

By default, the connection requests are non-persistent. To make them persistant, add `Connection : keep-alive` header to HTTP request headers.
You can also specify maximum number of request per connection and timeout in seconds for that specific connection by adding `Keep-Alive: timeout=5, max=10` header to HTTP request.

### Cookies [refer](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cookie)

The server generates cookie for every new `User-Agent`. The expiration period of the cookie generated is 1 day. Server sends the cookie back to client in HTTP response as `Cookie: name=value`.
The server stores all the cookies in `cookie.json` file.
For old User-Agent, server increments the cookie count sent by that User-Agent in request header. 

### Server Resources

All the server resources are in the `/resources` directory. For this resources clients can make requests to the server.
You can add/delete the resources on the server.

## Running Tests

Automated test scripts to test the specified functionalities can be found in the `/Test` directory. Before running any of the tests, first start the server.

### Automated Unit Tests

These tests ensure the conformance of the basic functionalities and the correctness of the responses. All the supported methods are tested.

#### To run unit test module for methods do the following:

```
cd Test
python3 methods.py <port_no>
```

#### To run tests for cookies:

```
cd Test
python3 cookies.py <port_no>
```


### Automated Stress Tests

These tests check if the server can handle a large scale pool of network requests in parallel and serve the reponses.

#### To run stress test module do the following:

```
cd Test
python3 stress.py <port_no> <no_of_clients>
```

Example:
```
python3 stress.py 12000 100
```
This will tries to send 100 parallel requests to the server listening on port 12000


## References

- [RFC2616](https://tools.ietf.org/html/rfc2616)
- [MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP)
