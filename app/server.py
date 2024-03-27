from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
from database import Conn
from services import valida_dados
import json
import os

from signal import signal, SIGPIPE, SIG_DFL   
signal(SIGPIPE,SIG_DFL)

class RequestHandler(BaseHTTPRequestHandler):

    conn = Conn()
    
    def set_response(self, status_code, content_type = None, location = None, content=None):
        self.send_response(status_code)
        if content:
            self.send_header("Content-type", content_type)
        if location:
            self.send_header("Location", location)
        self.end_headers()
        if content:
            self.wfile.write(content.encode("utf-8"))

    def do_GET(self):
        if self.path.startswith('/pessoas'):
            if '?' in self.path:
                query = urllib.parse.urlparse(self.path).query
                term = urllib.parse.parse_qs(query).get('t')[0]
                try:
                    json = self.conn.search_by_term(term)
                    self.set_response(200, 'application/json', content=json)
                except Exception as err:
                    self.set_response(400)
            else:
                try:
                    uuid = self.path.split('/')[-1]
                    json = self.conn.search_by_uuid(uuid)
                    self.set_response(200, "application/json", content=json)
                except Exception as err:
                    self.set_response(400)
        elif self.path == '/contagem-pessoas':
            total_pessoas = self.conn.get_total_pessoas()
            self.set_response(200, 'text/plain', content=total_pessoas)
        else:
            self.set_response(404)

    def do_POST(self):
        if self.path == '/pessoas':
            content_length = int(self.headers['Content-Length'])
            post_data = json.loads(self.rfile.read(content_length))
            try:
                valida_dados(post_data)
                uuid = self.conn.insert(post_data)
                self.set_response(201, location=f'http://localhost:9999/pessoas/{uuid}')
            except Exception as err:
                self.set_response(err.args[0])
                

if __name__ == '__main__':
    server_adress = ('', int(os.environ['HTTP_PORT']))
    httpd = HTTPServer(server_adress, RequestHandler)
    print("Server starting")
    httpd.serve_forever()
