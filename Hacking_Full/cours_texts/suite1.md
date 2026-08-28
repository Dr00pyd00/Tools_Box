# Récap — Réseau & Hacking éthique

## Modèle OSI — les couches

Chaque couche ajoute un **header** au paquet. C'est le même bloc mémoire, lu différemment selon la couche.

```
Couche 7 — Application   → HTTP, DNS, FTP
Couche 6 — Présentation  → TLS, chiffrement
Couche 5 — Session       → gestion de connexion
Couche 4 — Transport     → TCP, UDP (ports)
Couche 3 — Réseau        → IP (routage)
Couche 2 — Liaison       → MAC, ARP (réseau local)
Couche 1 — Physique      → câbles, wifi, bits
```

En C, un paquet c'est juste une struct :

```c
struct paquet {
    eth_header  eth;    // couche 2
    ip_header   ip;     // couche 3
    tcp_header  tcp;    // couche 4
    char        data[]; // données
};
```

À l'envoi : couche 7 → couche 1 (on ajoute des headers)
À la réception : couche 1 → couche 7 (on retire des headers)

---

## Les headers en détail

### Header Ethernet (couche 2)
- MAC source → ton PC
- MAC destination → ton routeur (pas le serveur final !)
- Type → IPv4 ou IPv6

### Header IP (couche 3)
- IP source → ton PC
- IP destination → le serveur final (ne change jamais)
- TTL → décrémente à chaque saut, détruit à 0
- Protocole → TCP (6) ou UDP (17)

### Header TCP (couche 4)
- Port source → port éphémère de ton PC
- Port destination → 443 (HTTPS), 80 (HTTP), 22 (SSH)...
- Flags → SYN, ACK, RST, FIN
- Seq/Ack → numéros pour ordonner les paquets

---

## TCP Handshake

```
Ton PC          →  SYN          →  Serveur
Ton PC          ←  SYN + ACK   ←  Serveur
Ton PC          →  ACK          →  Serveur
                   connectés
```

Dans Wireshark : lignes consécutives avec flags SYN / SYN,ACK / ACK.

---

## MAC vs IP

| | IP | MAC |
|---|---|---|
| Rôle | Trouver la machine sur internet | Trouver la machine sur le réseau local |
| Portée | Mondiale | Réseau local uniquement |
| Changement | Attribuée par DHCP, peut changer | Gravée en usine, ne change pas |
| Format | 192.168.1.86 | f4:a4:75:eb:55:b4 |

La MAC change à chaque saut réseau. L'IP reste la même du début à la fin.

---

## ARP — Address Resolution Protocol

**Problème** : pour envoyer une frame Ethernet, j'ai besoin de la MAC de destination. Mais je ne connais que l'IP.

**Solution** : broadcast — envoyer un message à toutes les machines du réseau local.

```
Ton PC → (broadcast FF:FF:FF:FF:FF:FF) → "Qui a l'IP 192.168.1.50 ?"
Imprimante → (unicast vers ton PC)     → "C'est moi, ma MAC est AA:BB:CC:DD:EE:FF"
```

`FF:FF:FF:FF:FF:FF` = adresse MAC broadcast = tout le monde reçoit.

Ton PC garde la réponse dans le **cache ARP** :

```bash
arp -a  # affiche le cache ARP
```

**ARP scan** = répéter ARP sur toute la plage d'IPs pour découvrir les machines présentes.

---

## DNS — Domain Name System

Annuaire d'internet : transforme un nom en IP.

```
google.com → 142.251.47.78
```

**Hiérarchie de résolution** :

```
1. Cache local           → "je connais déjà ?"
2. Serveur DNS du FAI    → "tu connais google.com ?"
3. Serveur DNS racine    → "qui gère .com ?"
4. Serveur DNS .com      → "qui gère google.com ?"
5. Serveur DNS Google    → "voici l'IP : 142.251.47.78"
```

Port DNS : toujours **53**, UDP par défaut.

Requête `A` = IPv4, requête `AAAA` = IPv6.

```bash
nslookup google.com   # résolution DNS
```

---

## Outils vus

### traceroute
Affiche tous les routeurs entre ton PC et la destination.

```bash
traceroute google.com
```

Chaque ligne = un saut. `* * *` = routeur qui ne répond pas aux requêtes ICMP.

Le TTL décrémente à chaque saut — quand il atteint 0 le paquet est détruit.

### whois
Identifie le propriétaire d'une IP.

```bash
whois 209.85.250.94  # → Google LLC
```

### nmap
Scan réseau — découvrir les machines et leurs ports.

```bash
nmap -sn 192.168.1.0/24  # scan de machines sans scanner les ports
```

### Wireshark
Capture et analyse le trafic réseau en temps réel. Filtre utile :

```
dns   → affiche uniquement les requêtes DNS
tcp   → affiche uniquement le trafic TCP
```

### subprocess (Python)
Lancer des commandes shell depuis Python.

```python
import subprocess

res = subprocess.run(["whois", "209.85.250.94"], capture_output=True, text=True)
print(res.stdout)
```

---

## Méthodologie pentest réseau local

```
1. ARP scan        → quelles machines sont présentes ?
2. Port scan       → quels services tournent ?
3. Banner grabbing → quelle version du service ?
4. whois / DNS     → à qui appartient la cible ?
5. Exploitation    → y'a-t-il des vulnérabilités ?
```

Ton scanner de ports = étape 2. Scapy va permettre l'étape 1.

---

## Prochaine étape : Scapy

Scapy = bibliothèque Python pour fabriquer et envoyer des paquets réseau.

```python
from scapy.all import *

paquet = Ethernet() / IP() / TCP()  # empilement de couches
```

On va coder un ARP scan — découvrir toutes les machines d'un réseau local.
