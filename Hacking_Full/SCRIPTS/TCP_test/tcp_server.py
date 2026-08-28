import socket

# on met family et type de flux:
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind avec TUPLE addr + port:
server.bind(("0.0.0.0", 9000))

# file d'attente de 5 , un client par un est traiter si 6eme arrive dans la file la co est refusé.
server.listen(5)
print("Mon SERVER ecoute sur le port 9000...")

while True: # ecouter en boucle les clients

    # accept handshake
    # return 2 elements 
            # conn = socket du client : avec ca qu'on parle avec lui
            # addr = tup^le avec (IP et PORT) 
    conn, addr = server.accept()
    print(f"Connexion avec {addr}")

    while True: # boucloe pour recevoir plusieurs messages:

        # reception des bytes on precise combien au max:
        data = conn.recv(1024)

        # si jamais on recois plus rien : client deco, on ferme tout.
        if not data:
            print(f"Client {addr} deconnecté...")
            break

        # je print ce que je recois :
        print(f"Server a recu: {data.decode()}")

        # en retour je confirme ce que j'ai recu:
        conn.send(b"Message recu!")


    # fermeture du socket client:
    conn.close()
