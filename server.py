from http.server import BaseHTTPRequestHandler,HTTPServer
from socketserver import ThreadingMixIn
import threading
import argparse
import re
import cgi
from model import *

#creating a class for handling simple HTTP POST requests
class HTTPRequestHandler(BaseHTTPRequestHandler):
	
	def do_POST(self):
		'''
		handles POST request. Since we could not implement the client side,
		just prints the response instead of sending it to client
		'''

		if None != re.search('/predict_dropout', self.path):
			ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
			
			myresponse = 200
      
			if ctype == 'application/json':
				#JSON received, send to model  
				data = self.headers.get('data')
				
				model = Modeller()
				my_response = model.predict(data)
				print(my_response)

			else:
				#if something other than JSON is received, do nothing
				data={}

			self.send_response(200)# ok
			self.end_headers()
    
		else:
			self.send_response(403)
			self.send_header('Content-Type', 'application/json')
			self.end_headers()
			return

#allowing threads to prevent overload.
#this was copied.
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
  allow_reuse_address = True

  def shutdown(self):
    self.socket.close()
    HTTPServer.shutdown(self)

class SimpleHttpServer():
  def __init__(self, ip, port):
    self.server = ThreadedHTTPServer((ip,port), HTTPRequestHandler)

  def start(self):
    self.server_thread = threading.Thread(target=self.server.serve_forever)
    self.server_thread.daemon = True
    self.server_thread.start()

  def waitForThread(self):
    self.server_thread.join()

  def addRecord(self, recordID, jsonEncodedRecord):
    LocalData.records[recordID] = jsonEncodedRecord

  def stop(self):
    self.server.shutdown()
    self.waitForThread()

if __name__=='__main__':
  parser = argparse.ArgumentParser(description='HTTP Server')
  parser.add_argument('port', type=int, help='Listening port for HTTP Server')
  parser.add_argument('ip', help='HTTP Server IP')
  args = parser.parse_args()

  server = SimpleHttpServer(args.ip, args.port)
  print ('HTTP Server Running...........')
  server.start()
  server.waitForThread()
