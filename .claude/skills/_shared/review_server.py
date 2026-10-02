#!/usr/bin/env python3
"""THE SERVER FOR EVERY LOCAL REVIEW PAGE. `python3 -m http.server` ignores Range requests, so Chrome cannot seek:
a click on a video's timeline does nothing and the clip keeps playing (Dan, 2026-10-02, Ad 13 round 2: "I'm not able
to click around to go backwards and forwards, which is essential"). This serves a folder with byte ranges (206), so
every player on a review page can be scrubbed.

  python3 review_server.py PORT [DIR]        (DIR defaults to the current folder; binds 127.0.0.1 only)
"""
import http.server
import os
import re
import socketserver
import sys


class Handler(http.server.SimpleHTTPRequestHandler):
    def send_head(self):
        rng = self.headers.get("Range")
        path = self.translate_path(self.path)
        m = re.match(r"bytes=(\d*)-(\d*)$", rng or "")
        if not m or os.path.isdir(path) or not os.path.isfile(path):
            return super().send_head()
        size = os.path.getsize(path)
        a, b = m.groups()
        if a == "":                                    # suffix range: the last N bytes
            start, end = max(0, size - int(b)), size - 1
        else:
            start, end = int(a), min(int(b) if b else size - 1, size - 1)
        if start >= size or start > end:
            self.send_response(416); self.send_header("Content-Range", f"bytes */{size}"); self.end_headers()
            return None
        f = open(path, "rb")
        f.seek(start)
        self._left = end - start + 1
        self.send_response(206)
        self.send_header("Content-Type", self.guess_type(path))
        self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        self.send_header("Content-Length", str(self._left))
        self.send_header("Last-Modified", self.date_time_string(os.path.getmtime(path)))
        self.end_headers()
        return f

    def end_headers(self):
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()

    def copyfile(self, source, outputfile):
        left = getattr(self, "_left", None)
        if left is None:
            return super().copyfile(source, outputfile)
        self._left = None
        try:
            while left > 0:
                buf = source.read(min(256 * 1024, left))
                if not buf:
                    break
                outputfile.write(buf); left -= len(buf)
        except (BrokenPipeError, ConnectionResetError):
            pass                                       # the browser dropped the request to seek elsewhere

    def log_message(self, *a):
        pass


class Server(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


if __name__ == "__main__":
    port = int(sys.argv[1])
    if len(sys.argv) > 2:
        os.chdir(sys.argv[2])
    Server(("127.0.0.1", port), Handler).serve_forever()
