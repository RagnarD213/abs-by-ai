"""One-shot local receiver: the Pexels search index gathered in the Browser pane is POSTed here and written to stock/pexels_index.md."""
import http.server, sys
OUT = "/Volumes/Extreme/_edit_work/ro08/stock/pexels_index.md"
class H(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0)); open(OUT, "wb").write(self.rfile.read(n))
        self.send_response(200); self.send_header("Access-Control-Allow-Origin", "*"); self.end_headers(); self.wfile.write(b"ok")
    def do_GET(self):
        self.send_response(200); self.send_header('Content-Type', 'text/html'); self.end_headers(); self.wfile.write(b'<html><body>recv</body></html>')
    def log_message(self, *a): pass
http.server.HTTPServer(("127.0.0.1", 8872), H).serve_forever()
