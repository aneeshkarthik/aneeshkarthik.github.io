#!/usr/bin/env python3
"""
Preview the site locally.

    ./serve

Then open http://localhost:8137 in your browser. Ctrl+C to stop.
Opening index.html directly as a file:// URL will not work — browsers block
local scripts that way — so use this instead.
"""

import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler

ROOT = os.path.dirname(os.path.abspath(__file__))
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8137


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def end_headers(self):
        # Never cache during development, so edits show up on refresh.
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, fmt, *args):
        pass  # keep the terminal quiet


if __name__ == "__main__":
    os.chdir(ROOT)
    server = HTTPServer(("127.0.0.1", PORT), Handler)
    print("Serving {} at http://localhost:{}".format(ROOT, PORT))
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
