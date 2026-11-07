from http.server import BaseHTTPRequestHandler
import urllib.request
import urllib.error
import json

VPS_TARGET = "http://180.93.195.52:8080"

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self._forward_request("GET")

    def do_POST(self):
        self._forward_request("POST")

    def _forward_request(self, method):
        target_url = VPS_TARGET + self.path
        body = None
        if method == "POST":
            content_length = int(self.headers.get("Content-Length", 0))
            if content_length > 0:
                body = self.rfile.read(content_length)

        req = urllib.request.Request(target_url, data=body, method=method)
        req.add_header("Content-Type", self.headers.get("Content-Type", "application/json"))

        try:
            with urllib.request.urlopen(req, timeout=12) as resp:
                data = resp.read()
                self.send_response(resp.status)
                self.send_header("Content-Type", "application/json")
                self.send_header("X-Shield-Proxy", "Vercel-GitHub-Gateway")
                self.end_headers()
                self.wfile.write(data)
        except urllib.error.HTTPError as e:
            err_data = e.read()
            self.send_response(e.code)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(err_data)
        except Exception:
            self.send_response(502)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"ok": False, "error": "Máy chủ bản quyền tạm thời gián đoạn"}).encode("utf-8"))
