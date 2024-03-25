from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from database import Conn
from services import valida_dados
import json

from signal import signal, SIGPIPE, SIG_DFL   
signal(SIGPIPE,SIG_DFL)

class RequestHandler(BaseHTTPRequestHandler):

    conn = Conn()
    
    def log_message(self, format, *args):
        print(*args)
    
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
        urlparsed = urlparse(self.path)
        path = urlparsed.path.split('/')
        query_url_parsed = urlparsed.query
        query = parse_qs(query_url_parsed)
        
        endpoint = path[1]
        
        match endpoint:
                
            case 'pessoas':
                if not query_url_parsed:
                    try:
                        uuid = path[2] 
                        json = self.conn.search_by_uuid(uuid)
                        self.set_response(200, "application/json", content=json)
                    except Exception as err:
                        self.set_response(400)
                else:
                    try:
                        term = query
                        json = self.conn.search_by_term(term['t'][0])
                        self.set_response(200, "application/json", content=json)
                    except Exception as err:
                        self.set_response(400)
                        
            case 'contagem-pessoas':
                total_pessoas = self.conn.get_total_pessoas()
                self.set_response(200, 'text/plain', content=total_pessoas)
                
            case _:
                self.set_response(404)
                
                
    def do_POST(self):
        path = urlparse(self.path).path
        content_type = self.headers.get_content_type()
        
        if path == '/pessoas' and content_type == 'application/json':
                length = int(self.headers.get('content-length'))
                content = json.loads(self.rfile.read(length))
                try:
                    valida_dados(content)
                    uuid = self.conn.insert(content)
                    self.set_response(201, location=f'http://localhost:9999/pessoas/{uuid}')
                except Exception as err:
                    self.set_response(err.args[0])

if __name__ == '__main__':
    server_adress = ('', 8080)
    httpd = HTTPServer(server_adress, RequestHandler)
    print("Server starting")
    httpd.serve_forever()
