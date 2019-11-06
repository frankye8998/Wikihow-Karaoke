from os import listdir
from os.path import isfile, join
from random import shuffle
from http.server import BaseHTTPRequestHandler, HTTPServer
import time

HOST_NAME = '0.0.0.0'
PORT_NUMBER = 80
counter = 0
onlyfiles = [f for f in listdir('pics') if isfile(join('pics', f))]
shuffle(onlyfiles)

class MyHandler(BaseHTTPRequestHandler):
    def handle_http(self, status_code, path):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        content = '{"status": "GET"}'
        return bytes(content, 'UTF-8')

    def do_GET(self):
        global counter
        self.send_response(200)
        if counter == len(onlyfiles):
            self.send_header('Content-type', 'text/html')
            HTML = b'''<html><body><h3 style="text-align: center">Error: No more images!</h3></body></html'''
            self.wfile.write(HTML)
        else:
            self.send_header('Content-type', 'image/jpeg')
            self.end_headers()
            with open(f'./pics/{onlyfiles[counter]}', 'rb') as f:
                self.wfile.write(f.read())
            counter += 1
            print(counter)

if __name__ == '__main__':
    server_class = HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print(time.asctime(), 'Server Starts - %s:%s' % (HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    except StopIteration:
        print("Ran out of images!")
    httpd.server_close()
    print(time.asctime(), 'Server Stops - %s:%s' % (HOST_NAME, PORT_NUMBER))