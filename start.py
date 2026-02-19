mport http.server
import socketserver
import webbrowser
import os
import sys
import socket

def find_free_port(start=8000, end=8100):
    for port in range(start, end):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(('', port))
            s.close()
            return port
        except OSError:
            continue
    return None

class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()
    
    def log_message(self, format, *args):
        pass  # 静默日志

def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    port = find_free_port()
    if port is None:
        print("Error: No available port found.")
        sys.exit(1)
    
    print(f"Server running at http://localhost:{port}")
    print("Press Ctrl+C to stop.")
    
    webbrowser.open(f"http://localhost:{port}")
    
    socketserver.TCPServer.allow_reuse_address = True
    try:
        with socketserver.TCPServer(("", port), Handler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        sys.exit(0)

if __name__ == "__main__":
    main()
