# Hacking Éthique — Récap Leçon 1, 2 & 3

---

## 1. Le réseau

**Réseau** — des machines qui peuvent se parler entre elles.

**Adresse IP** — l'adresse unique de chaque machine sur un réseau.  
Format : `192.168.1.98` — 4 nombres entre 0 et 255.

---

## 2. IP Privée vs IP Publique

**IP Privée** — l'adresse de ta machine à l'intérieur de ton réseau local. Personne dehors la voit.  
Exemple : `192.168.1.98`

**IP Publique** — attribuée par ton fournisseur internet (SFR, Orange...) à ta box. C'est elle que le monde extérieur voit.

**NAT** *(Network Address Translation)* — mécanisme de ta box qui fait le lien entre IP privée et IP publique.

**IP dynamique** — change de temps en temps. Cas de la plupart des particuliers.

**IP statique** — ne change jamais. Utilisée par les entreprises qui hébergent des serveurs.

---

## 3. Les interfaces réseau

**Interface réseau** — un moyen pour ton PC de se connecter à un réseau.

| Préfixe | Type | Rôle |
|---|---|---|
| `lo` | Loopback | Pointe vers toi-même. Adresse toujours `127.0.0.1` = localhost |
| `wl` | Wireless | Carte WiFi |
| `en` | Ethernet | Prise filaire |
| `ww` | Wireless Wide Area | Module 4G/5G |
| `br` | Bridge | Pont virtuel (Docker etc) |

---

## 4. Le masque de sous-réseau

**`/24` Subnet mask** — les 24 premiers bits sont fixes = 254 machines utilisables.

`192.168.1.98/24` → toutes les machines de `192.168.1.0` à `192.168.1.255` sont sur le même réseau.

---

## 5. DHCP

**DHCP** *(Dynamic Host Configuration Protocol)* — service de ta box qui distribue automatiquement les adresses IP.

`valid_lft` *(Valid Lifetime)* — durée de vie de l'adresse en secondes.

---

## 6. La MAC Address

**MAC Address** *(Media Access Control Address)* — adresse physique unique gravée dans la carte réseau. Ne change jamais.

Format : `98:af:65:56:52:20` — 6 groupes en hexadécimal.

**Les 3 premiers groupes = le fabricant.**

Seules les **cartes réseau** ont une MAC — pas le CPU, la RAM, le disque dur.

**MAC Spoofing** — falsifier temporairement sa MAC via logiciel pour l'anonymat.

---

## 7. Les ports

**Port** — une "porte" numérotée sur une machine. 65535 ports par machine.

**Port ouvert** — un service écoute et attend des connexions.  
**Port fermé** — personne n'écoute, connexions rejetées.

| Port | Service |
|---|---|
| `22` | SSH — connexion à distance sécurisée |
| `53` | DNS — traduit les noms de domaine en IP |
| `80` | HTTP — web non chiffré |
| `443` | HTTPS — web chiffré |
| `5432` | PostgreSQL |
| `8000` | HTTP-alt (FastAPI, Django...) |
| `9050` | Tor |

---

## 8. Ports éphémères vs ports fixes

**Port fixe (serveur)** — écoute et attend. Exemple : uvicorn sur `8000`.

**Port éphémère (client)** *(Ephemeral Port)* — port aléatoire temporaire pour envoyer. Disparaît après la connexion.

```
Client : 192.168.1.85:52847  →→→  Serveur : 192.168.1.98:8000
         port éphémère                      port fixe
```

---

## 9. `0.0.0.0` vs `127.0.0.1`

| Adresse | Qui peut accéder |
|---|---|
| `127.0.0.1` | Que toi sur ton PC |
| `0.0.0.0` | Toi + tout le réseau local |

**Port Forwarding** — ouvrir la porte au monde extérieur via configuration de la box.

---

## 10. TCP *(Transmission Control Protocol)*

Protocole de transport **fiable** — créé en 1974 par Vint Cerf et Bob Kahn.

**3 garanties :**
- Livraison garantie — paquet perdu = renvoyé automatiquement
- Ordre garanti — chaque paquet a un numéro
- Vérification d'intégrité — données non corrompues

### Three-Way Handshake

```
Client          Serveur
  |                |
  |  ——SYN——>      |   demande de connexion
  |  <——SYN-ACK——  |   confirmation
  |  ——ACK——>      |   connexion établie
  |  === data ===  |
```

**SYN** *(Synchronize)* — demande de connexion  
**ACK** *(Acknowledge)* — confirmation de réception  
**RST** *(Reset)* — connexion refusée, port fermé  
**FIN** *(Finish)* — fermeture propre de la connexion

### Attaque SYN Flood

Envoyer des milliers de SYN sans jamais répondre → le serveur sature sa mémoire avec des connexions à moitié ouvertes → plus personne peut se connecter. C'est une attaque **DoS** *(Denial of Service)*.

---

## 11. UDP *(User Datagram Protocol)*

Protocole de transport **rapide mais sans garanties** — créé en même temps que TCP.

- Pas de handshake
- Pas de confirmation de réception
- Pas de remise en ordre
- Pas de renvoi si perdu

**"Fire and forget"** — t'envoies, t'oublies.

| | TCP | UDP |
|---|---|---|
| Fiabilité | ✅ Garanti | ❌ Pas garanti |
| Vitesse | Plus lent | Plus rapide |
| Handshake | ✅ Oui | ❌ Non |
| Usage | Web, emails, fichiers | Jeux, streaming, DNS |

### Packet Spoofing

UDP n'authentifie personne — n'importe qui peut envoyer des paquets en se faisant passer pour quelqu'un d'autre.

---

## 12. Les sockets

**Socket** — objet crée par l'OS qui représente un point de communication réseau.

```python
# TCP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# UDP
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
```

**`AF_INET`** *(Address Family Internet)* — utilise IPv4  
**`SOCK_STREAM`** *(Stream)* — TCP, flux continu et ordonné  
**`SOCK_DGRAM`** *(Datagram)* — UDP, paquets indépendants

### Méthodes TCP

| Méthode | Rôle |
|---|---|
| `bind((ip, port))` | Attacher le socket à une adresse et un port |
| `listen(5)` | Écouter — `5` = taille de la file d'attente |
| `accept()` | Accepter une connexion, retourne `(conn, addr)` |
| `recv(1024)` | Recevoir des bytes, `1024` = taille max du buffer |
| `send(b"data")` | Envoyer des bytes |
| `close()` | Fermer la connexion |
| `setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)` | Réutiliser un port même s'il est en cours de fermeture |

### Méthodes UDP

| Méthode | Rôle |
|---|---|
| `bind((ip, port))` | Attacher le socket |
| `recvfrom(1024)` | Recevoir bytes + adresse expéditeur |
| `sendto(b"data", addr)` | Envoyer vers une adresse précise |

---

## 13. La pile réseau

```
HTTP/HTTPS  — contenu, structure de la communication
      ↓
TLS  — chiffrement (HTTPS uniquement)
      ↓
TCP ou UDP  — transport
      ↓
IP  — adressage, trouver la bonne machine
      ↓
WiFi / Ethernet / Bluetooth  — transport physique
```

**HTTP** *(HyperText Transfer Protocol)* — protocole qui structure les requêtes et réponses web.  
**HTTPS** — HTTP + chiffrement TLS.  
**TLS** *(Transport Layer Security)* — chiffrement. Remplace l'ancien SSL *(Secure Sockets Layer)*.  
**HTTP/3** — nouvelle version qui tourne sur UDP + QUIC au lieu de TCP.

### Diffie-Hellman

Algorithme qui permet à deux machines de calculer une clé commune **sans jamais se l'envoyer**. C'est pour ça qu'intercepter une connexion HTTPS depuis le début ne suffit pas à déchiffrer.

---

## 14. WebSocket

Protocole qui tourne par dessus TCP permettant une communication **bidirectionnelle permanente**.

HTTP classique — le client demande, le serveur répond, terminé.  
WebSocket — le serveur peut envoyer des données **quand il veut** sans que le client demande.

Utilisé pour : chat temps réel, notifications live, jeux multijoueur.

---

## 15. DoS et DDoS

**DoS** *(Denial of Service)* — rendre un service inaccessible depuis **une seule machine**.  
**DDoS** *(Distributed Denial of Service)* — même attaque depuis **des milliers de machines simultanément**.  
**Botnet** — réseau de machines infectées utilisées pour des attaques DDoS à l'insu de leurs propriétaires.

---

## 16. La légalité en France

**Article 323-1 du Code Pénal** — interdit d'accéder à un système sans autorisation.

✅ Légal : ton propre réseau, VMs, TryHackMe, HackTheBox, VulnHub  
❌ Illégal : réseau d'autrui sans permission, collecte de données sans consentement (RGPD)

**RGPD** *(Règlement Général sur la Protection des Données)* — l'IP est une donnée personnelle, sa collecte doit être mentionnée.

En pentest professionnel → toujours un **contrat écrit** avant toute action.

---

## 17. Commandes vues

```bash
ip addr show                          # afficher toutes les interfaces réseau
ip addr show wlp0s20f3                # afficher une interface spécifique
curl ifconfig.me                      # afficher son IP publique
sudo apt install nmap                 # installer nmap
nmap -sn 192.168.1.0/24              # scanner les machines du réseau (ping)
sudo nmap -sn --send-ip 192.168.1.0/24  # scanner avec technique anti-Windows
sudo nmap -PS 192.168.1.0/24         # scanner avec TCP SYN
nmap 192.168.1.98                    # scanner les 1000 ports TCP d'une machine
ss -tlnp                             # ports TCP en écoute + programmes
ss -ulnap                            # ports UDP en écoute
ss -t                                # connexions TCP actives
nc 127.0.0.1 9000                    # connexion TCP avec netcat
nc -u 127.0.0.1 9001                 # connexion UDP avec netcat
kill -9 <PID>                        # forcer la fermeture d'un processus
ss -tlnp | grep 9000                 # filtrer les résultats sur le port 9000
```

---

## 18. Flags importants

| Commande | Flag | Nom complet | Rôle |
|---|---|---|---|
| `nmap` | `-sn` | Scan No port | Détecte machines sans scanner ports |
| `nmap` | `--send-ip` | Send IP | Paquets différents du ping classique |
| `nmap` | `-PS` | Ping Scan TCP SYN | Détection via TCP |
| `nmap` | `-sU` | Scan UDP | Scanner les ports UDP |
| `ss` | `-t` | TCP | Sockets TCP uniquement |
| `ss` | `-u` | UDP | Sockets UDP uniquement |
| `ss` | `-l` | Listening | Ports en écoute uniquement |
| `ss` | `-n` | Numeric | Numéros bruts sans traduction |
| `ss` | `-p` | Process | Programme associé à chaque port |
| `ss` | `-a` | All | Tous les sockets |
| `nc` | `-u` | UDP | Utiliser UDP au lieu de TCP |
| `kill` | `-9` | SIGKILL | Forcer fermeture immédiate |

---

*Prochaine leçon : DNS — comment google.com devient une adresse IP*
