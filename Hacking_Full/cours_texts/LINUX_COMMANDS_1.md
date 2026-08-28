# Commandes de reconnaissance Linux

> Contexte : énumération locale sur une cible ou sa propre machine. Toutes ces commandes lisent l'état du système sans modifier quoi que ce soit.

---

## `netstat` — état du réseau

Affiche les connexions réseau actives, les ports en écoute, les tables de routage.

```bash
netstat -tulnp
```

| Flag | Mot complet | Rôle |
|------|-------------|------|
| `-t` | TCP | affiche les connexions TCP |
| `-u` | UDP | affiche les connexions UDP |
| `-l` | listening | affiche uniquement les ports en écoute |
| `-n` | numeric | affiche les IPs et ports en chiffres (pas de résolution DNS) |
| `-p` | process | affiche le PID et le nom du processus associé |

> `netstat` est déprécié sur les systèmes récents — préférer `ss` qui est plus rapide et plus complet.

---

## `ss` — exploration des sockets

Remplaçant moderne de `netstat`. Plus rapide car il lit directement le kernel.

```bash
ss -tulnp
```

Les flags sont identiques à `netstat`. Exemple de sortie :

```
Netid  State   Local Address:Port   Process
tcp    LISTEN  0.0.0.0:22          sshd
tcp    LISTEN  127.0.0.1:5432      postgres
```

Utile en pentest pour repérer les services qui écoutent en local uniquement (non exposés réseau).

---

## `ps` — état des processus

Affiche les processus en cours d'exécution.

```bash
ps aux
```

| Flag | Mot complet | Rôle |
|------|-------------|------|
| `a` | all | affiche les processus de tous les utilisateurs |
| `u` | user | format lisible avec utilisateur et % CPU/RAM |
| `x` | without tty | inclut les processus sans terminal attaché (daemons) |

Combinaison utile en recon :

```bash
ps aux | grep root
```

Affiche tous les processus tournant en root — intéressant pour trouver des services privilégiés à cibler.

---

## `who` — utilisateurs connectés

Affiche les utilisateurs actuellement connectés à la machine.

```bash
who
```

Sortie typique :
```
luna     tty1         2024-01-15 09:32
root     pts/0        2024-01-15 10:11 (192.168.1.42)
```

`pts/0` — pseudo-terminal, connexion distante (SSH)  
`tty1` — terminal physique local

En pentest : révèle si d'autres sessions sont actives sur la cible.

---

## `env` — variables d'environnement

Affiche toutes les variables d'environnement du shell courant.

```bash
env
```

Intéressant en recon car les variables peuvent contenir :
- des credentials (`DB_PASSWORD`, `API_KEY`)
- des chemins sensibles (`PATH`, `HOME`)
- des infos sur l'application en cours

Filtrer une variable spécifique :

```bash
env | grep PATH
```

---

## `lsblk` — périphériques de stockage

**ls** + **blk** (block devices) — liste les disques et partitions.

```bash
lsblk
```

Sortie typique :
```
NAME   MAJ:MIN SIZE TYPE MOUNTPOINT
sda      8:0   50G  disk
├─sda1   8:1   49G  part /
└─sda2   8:2    1G  part [SWAP]
```

Utile pour repérer des partitions montées, des disques chiffrés, ou des volumes cachés.

---

## `lsusb` — périphériques USB

**ls** + **usb** — liste les périphériques connectés en USB.

```bash
lsusb
```

Moins utile en pentest remote, mais utile en forensics ou sur une machine physique pour identifier du matériel suspect (clé WiFi, dongle...).

---

## `lsof` — fichiers ouverts

**ls** + **of** (open files) — liste tous les fichiers ouverts par tous les processus. Sur Linux, tout est fichier : sockets, pipes, vrais fichiers.

```bash
lsof -i          # fichiers réseau (sockets)
lsof -i :80      # qui utilise le port 80
lsof -u root     # fichiers ouverts par root
lsof /etc/passwd # quel processus lit /etc/passwd
```

Très puissant en recon pour corréler processus ↔ fichiers ↔ connexions réseau.

---

## `lspci` — périphériques PCI

**ls** + **pci** — liste les périphériques connectés sur le bus PCI (carte réseau, GPU, contrôleurs...).

```bash
lspci
lspci -v         # verbose, détails complets
```

Utile pour identifier le matériel réseau exact (modèle de carte, drivers).

---

## Récapitulatif — usage pentest

| Commande | Ce qu'on cherche en recon |
|----------|--------------------------|
| `ss -tulnp` | services en écoute, ports internes cachés |
| `ps aux` | processus root, services vulnérables |
| `env` | credentials en clair, variables sensibles |
| `lsof -i` | connexions actives par processus |
| `who` | autres sessions actives |
| `lsblk` | partitions cachées, volumes chiffrés |