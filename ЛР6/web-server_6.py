import http.server
import socketserver

PORT = 80
DIRECTORY = "/Desktop/university"

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = 'index.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

Handler = MyHandler
Handler.directory = DIRECTORY

# Create an HTTP server instead of a TCP server
httpd = socketserver.TCPServer(("", PORT), Handler)
httpd.allow_reuse_address = True

# Set up the HTTP headers
httpd.server_name = "My Server"
httpd.server_version = "1.0"
httpd.headers = {
    'Content-Type': 'text/html; charset=utf-8',
    'Cache-Control': 'no-cache'
}

print(f"Serving at port {PORT}")
httpd.serve_forever()
