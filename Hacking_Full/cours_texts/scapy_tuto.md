# Scapy python

Scapy sert a creer des paquets **couche par couche**.

#### Syntaxe de base:

```python 
paquet = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst="192.168.1.1")
````
Le `/`emballe les couches.

--- 

### `Ether()`: couche 2 = Ethernet  

>Ethernet est le reseau LOCAL pour on utilise les MAC.
- `dst`: destination = la MAC a qui envoyer
- `"ff:ff:ff:ff:ff:ff"`: broadcast = envoie a tous

---

### `ARP()`: couche 2/3 = 
- `op` — **operation** — opération : le type de message ARP. Valeurs possibles : `who-has` (question) ou `is-at` (réponse)

- `hwsrc` — **hardware source** — adresse matérielle source : ta propre adresse MAC

- `psrc` — **protocol source** — adresse protocole source : ton propre adresse IP

---

tableau complet des champs ARP :

| Abréviation | Mot complet | Traduction |
|-------------|-------------|------------|
| `op` | operation | opération (question ou réponse) |
| `hwsrc` | hardware source | MAC source (la tienne) |
| `hwdst` | hardware destination | MAC destination (celle qu'on cherche) |
| `psrc` | protocol source | IP source (la tienne) |
| `pdst` | protocol destination | IP destination (celle qu'on cherche) |
| `hwtype` | hardware type | type matériel (Ethernet, WiFi...) |
| `ptype` | protocol type | type protocole (IPv4, IPv6...) |
| `hwlen` | hardware length | longueur de l'adresse MAC (6 octets) |
| `plen` | protocol length | longueur de l'adresse IP (4 octets) |


## Envoyer et recevoir

### Moyen 1:

```python
responses, _ = srp(paquet, timeout=0.2, verbose=False)

```

- `srp` — **send and received paquet** — envoyer ET recevoir paquet
- `timeout` — **timeout** — delai d'attente avant d'abandonner
- `verbose` — **details/ bavards** — False:  pas affichage automatique
- `_` = les paquets **sans** reponses ( on s'en fou)


Dans "reponses" ce sont des **Pairs**:
- `Sended` = le paquet que j'ai envoyer
- `Received` = le paquet recu en reponse

```python

for sended, received in responses:
    print(f"IP: {received.psrc} // MAC: {received.hwsrc}")

```


Bien sûr —

---

**Ce qu'on a fait avec Scapy**

Scapy c'est une bibliothèque Python qui te permet de **construire et envoyer des paquets réseau couche par couche** — là où `socket` te cachait tout ça.

---

**La syntaxe de base**

```python
paquet = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst="192.168.1.1")
```

Le `/` signifie "emballe dans" — tu empiles les couches comme dans le modèle OSI.

---

**Les deux couches qu'on utilise**

`Ether()` — couche 2, Ethernet
- `dst` — **destination** — destinataire : la MAC à qui envoyer physiquement
- `ff:ff:ff:ff:ff:ff` = broadcast = tout le monde sur le réseau local

`ARP()` — couche 2/3, protocole de résolution d'adresse
- `pdst` — **protocol destination** — IP destination : l'IP qu'on cherche
- Scapy remplit automatiquement `hwsrc` (**hardware source** — ta MAC) et `psrc` (**protocol source** — ton IP)

---

**Envoyer et recevoir**

```python
reponses, _ = srp(paquet, timeout=0.2, verbose=False)
```

- `srp` — **send receive packet** — envoyer/recevoir un paquet : envoie ET attend une réponse
- `timeout` — **timeout** — délai d'attente : secondes à attendre avant d'abandonner
- `verbose` — **verbose** — bavard : `False` = pas d'affichage automatique
- `_` = les paquets sans réponse — on s'en fout

---

**Lire la réponse**

```python
for sended, received in reponses:
    print(f"IP: {received.psrc} // MAC: {received.hwsrc}")
```

- `received.psrc` — **protocol source** — IP source : l'IP de la machine qui a répondu
- `received.hwsrc` — **hardware source** — MAC source : la MAC de la machine qui a répondu

---






Ethernet c'est la couche 2 — elle travaille uniquement avec des **adresses MAC**. Elle ne sait pas ce qu'est une IP.

Quand tu envoies un paquet sur ton réseau local, physiquement ce qui voyage sur le câble (ou le WiFi) c'est un **frame Ethernet** — et ce frame contient une MAC source et une MAC destination. Pas d'IP.

---

**Alors comment les IP et les MAC fonctionnent ensemble ?**

C'est exactement le rôle d'ARP —

> "J'ai une IP à contacter — mais j'ai besoin de sa MAC pour envoyer le frame Ethernet."

Le processus complet quand tu veux contacter `192.168.1.5` :

```
1. Ton OS regarde sa table ARP — est-ce que j'ai déjà la MAC de 192.168.1.5 ?
2. Non → envoie un ARP broadcast : "qui a 192.168.1.5 ?"
3. La machine répond : "c'est moi, ma MAC est aa:bb:cc:dd:ee:ff"
4. Maintenant ton OS peut construire le frame Ethernet avec cette MAC
5. Le paquet IP voyage dans le frame Ethernet
```

---

**Résumé visuel**

```
[ Frame Ethernet        ]
  MAC src → MAC dst
  [ Paquet IP           ]
    IP src → IP dst
    [ Données TCP/UDP   ]
```

Ethernet enveloppe IP. IP ne peut pas voyager sans Ethernet en dessous. Et Ethernet ne parle que MAC.

C'est pour ça qu'ARP existe — c'est le traducteur entre le monde IP et le monde MAC. 🤔




# MAC 

Les 3 premiers octets d'un MAC  = `OUI` : — **Organizationally Unique Identifier** —  identifiant unique organisationnel. Ils identifient le fabricant de la carte réseau.

Exemple:
```bash 
00:50:56:c0:00:08
└─────┘
  OUI = 00:50:56 = VMware
```
Il existe une base de données publique qui fait le lien OUI → fabricant.


--- 

### avoir le MAC  manufacturateur

On utilise "manuf" de python 

```bash
sudo pip install manuf --break-system-packages
```
- `--break-system-packages` = bypass la securité Linux qui tend a empecher de changer la version python

Ensuite on crée un objet :

```python
from manuf import manuf 

mac_parser = manuf.MacParser()

# puis on peut acceder grace a la MAC :
manufactor = mac_parser.get(MaMacAddresse)

```