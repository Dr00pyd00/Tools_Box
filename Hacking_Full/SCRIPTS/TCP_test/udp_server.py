import socket

# AF_INET : IPv4 / DGRAM: protocole UDP
server = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
server.bind(("0.0.0.0", 9001))

print("UDP en ecoute sur port 9001...")

while True:
    data, add = server.recvfrom(1024)
    print(f"UDP recu de {add}: {data.decode()}")
    server.sendto(b"message recu!", add)