import http.server
import socketserver
import os
import argparse

WEBGL_BUILD_DIRECTORY = "."

class GzipHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        if self.path.endswith('.gz'):
            self.send_header('Content-Encoding', 'gzip')
            if self.path.endswith('.js.gz'):
                self.send_header('Content-Type', 'application/javascript')
            elif self.path.endswith('.data.gz'):
                self.send_header('Content-Type', 'application/octet-stream')
            elif self.path.endswith('.wasm.gz'):
                self.send_header('Content-Type', 'application/wasm')
            elif self.path.endswith('.json.gz'):
                self.send_header('Content-Type', 'application/json')
            self.path = self.path[:-3]
        super().end_headers()

    def do_GET(self):
        if self.path == "/":
            self.path = "/index.html"
        return super().do_GET()

os.chdir(WEBGL_BUILD_DIRECTORY)

parser = argparse.ArgumentParser(description="Serve Unity WebGL build over HTTP.")
parser.add_argument('--port', type=int, default=8080, help="Port to run the server on (default: 8080)")
args = parser.parse_args()

PORT = args.port

Handler = GzipHTTPRequestHandler
httpd = socketserver.TCPServer(("0.0.0.0", PORT), Handler)

print(f"Serving Unity WebGL on http://0.0.0.0:{PORT}")
httpd.serve_forever()
