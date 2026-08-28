from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime

# data tracker with http link: ip / port / langage / browser

class MonHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/":  # if path is just /
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"message":"I got your data!"}')

        else:
            self.send_response(404)
            self.end_headers()

        with open("tracker_datas.txt", "a") as f:
            # client_address est un tuple (ip,port)
            f.write(f"connexion by IP:{self.client_address[0]} | Port:{self.client_address[1]} | at {datetime.now()}\n") 
            f.write(f"IP reel: {self.headers.get("X-Forwarded-For")}\n")
            f.write(f"navigateur reel: {self.headers.get("User-Agent")}\n")
            f.write(f"langue navigateur: {self.headers.get("Accept-Language")}\n\n")
            


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8000), MonHandler)  # tuple with ip/port to listen / handler with requests comes
    print("Serveur lancé sur https://localhost:8000")
    server.serve_forever() # loop infini du server

