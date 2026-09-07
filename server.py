import http.server
import socket
import socketserver
import json
import urllib.request
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PORT = 8000

def get_lan_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return '127.0.0.1'

class TeldaHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        if self.path.startswith('/api/scan'):
            try:
                content_len = int(self.headers.get('Content-Length', 0))
                post_body = self.rfile.read(content_len)
                req = urllib.request.Request(
                    'https://scanner.tradingview.com/egypt/scan',
                    data=post_body,
                    headers={'User-Agent': 'Mozilla/5.0', 'Content-Type': 'text/plain'},
                    method='POST'
                )
                with urllib.request.urlopen(req, timeout=10) as response:
                    res_body = response.read()
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json; charset=utf-8')
                    self.end_headers()
                    self.wfile.write(res_body)
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

def run_server():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    lan_ip = get_lan_ip()
    
    print("=" * 60)
    print("سيرفر محفظة تيلدا الذكي يعمل بنجاح!")
    print("=" * 60)
    print(f"الكمبيوتر: http://localhost:{PORT}")
    print(f"الموبايل:   http://{lan_ip}:{PORT}")
    print("=" * 60)
    print("اسعار البورصة المصرية ومساعد التداول مربوطان لحظيا ومباشرة.")
    print("=" * 60)
    sys.stdout.flush()

    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("0.0.0.0", PORT), TeldaHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nتم إيقاف السيرفر.")

if __name__ == '__main__':
    run_server()
