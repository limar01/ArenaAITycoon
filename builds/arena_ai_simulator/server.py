#!/usr/bin/env python3
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler

DIR = os.path.expanduser("~/Projects/workspace/ArenaAITycoon/builds/arena_ai_simulator")
os.chdir(DIR)

class MyHandler(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        if path == "/" or path == "":
            path = "/index.html"
        return os.path.join(DIR, path.lstrip("/"))

if __name__ == "__main__":
    PORT = 8888
    server = HTTPServer(("0.0.0.0", PORT), MyHandler)
    print(f"Serving Castlevania on http://0.0.0.0:{PORT} from {DIR}")
    server.serve_forever()
