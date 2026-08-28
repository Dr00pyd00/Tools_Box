# Infos système — mémoire, disque, RAM

---

## `df -h` — espace disque par partition

**df** = **d**isk **f**ree — **-h** = **h**uman readable

```bash
df -h
```

Sortie typique :
```
Filesystem      Size  Used Avail Use% Mounted on
udev            7.8G     0  7.8G   0% /dev
tmpfs           1.6G  1.2M  1.6G   1% /run
/dev/sda1        49G   18G   29G  38% /
tmpfs           7.8G  312M  7.5G   4% /dev/shm
/dev/sda2       512M   6M   506M   2% /boot
```

| Colonne | Signification |
|---------|---------------|
| `Filesystem` | le périphérique ou système de fichiers |
| `Size` | taille totale de la partition |
| `Used` | espace utilisé |
| `Avail` | espace disponible |
| `Use%` | pourcentage utilisé — si > 90% c'est critique |
| `Mounted on` | où la partition est montée dans l'arborescence |

`/dev/sda1` monté sur `/` — c'est ta partition principale (racine du système)  
`tmpfs` — partition temporaire en RAM, disparaît au reboot  
`/dev/shm` — **sh**ared **m**emory, mémoire partagée entre processus

---

## `du -sh` — taille des dossiers

**du** = **d**isk **u**sage — **-s** = **s**ummary — **-h** = **h**uman readable

```bash
du -sh *           # taille de chaque élément dans le dossier courant
du -sh /var/log    # taille d'un dossier précis
du -sh /* 2>/dev/null   # taille de chaque dossier racine
```

Sortie de `du -sh *` :
```
4.0K    Bureau
128M    Documents
2.3G    Téléchargements
840M    HACKING
12K     script.py
```

`2>/dev/null` — redirige les erreurs "permission denied" vers le néant pour ne pas polluer la sortie

---

## `free -h` — état de la RAM

```bash
free -h
```

Sortie typique :
```
               total        used        free      shared  buff/cache   available
Mem:            15Gi        8Gi        2Gi       312Mi        4Gi        6Gi
Swap:            2Gi          0         2Gi
```

| Colonne | Signification |
|---------|---------------|
| `total` | RAM physique totale installée |
| `used` | RAM utilisée par les processus |
| `free` | RAM complètement libre (souvent faible, c'est normal) |
| `shared` | RAM partagée entre processus |
| `buff/cache` | RAM utilisée par le kernel comme cache disque |
| `available` | RAM réellement disponible pour un nouveau processus |

**Piège courant** : `free` faible ne veut pas dire problème. Linux utilise le RAM libre comme cache disque (`buff/cache`) pour accélérer les accès. Ce cache est libéré automatiquement si un processus en a besoin. La colonne à surveiller c'est `available`.

`Swap` — mémoire virtuelle sur disque. Si `used` en swap est élevé, ta RAM est saturée et le système rame.

---

## `lsblk` — vue des disques et partitions

**lsblk** = **l**i**s**t **bl**oc**k** devices

```bash
lsblk
```

Sortie typique :
```
NAME   MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
sda      8:0    0   50G  0 disk
├─sda1   8:1    0   49G  0 part /
└─sda2   8:2    0    1G  0 part [SWAP]
sr0     11:0    1 1024M  0 rom
```

| Colonne | Signification |
|---------|---------------|
| `NAME` | nom du périphérique |
| `RM` | **r**e**m**ovable — 1 si amovible (clé USB) |
| `SIZE` | taille |
| `RO` | **r**ead **o**nly — 1 si lecture seule |
| `TYPE` | disk / part / rom |
| `MOUNTPOINT` | où c'est monté |

`sda` — premier disque SATA (**s**erial **a**ta **d**isk **a**)  
`sda1`, `sda2` — partitions de ce disque  
`sr0` — lecteur CD/DVD

---

## `cat /proc/cpuinfo` — détails CPU

```bash
cat /proc/cpuinfo | grep "model name" | head -1
nproc
lscpu | grep -E "CPU|Core|Thread|MHz"
```

Sortie de `lscpu` filtrée :
```
CPU(s):                  8
Thread(s) per core:      2
Core(s) per socket:      4
CPU MHz:                 2400.000
CPU max MHz:             4500.000
```

`nproc` — retourne juste le nombre de coeurs disponibles, utile pour les scripts

---

## `uname -a` — infos kernel et système

```bash
uname -a
```

Sortie typique :
```
Linux kali 6.1.0-kali9-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.27-1kali1 x86_64 GNU/Linux
```

| Champ | Valeur | Signification |
|-------|--------|---------------|
| `Linux` | Linux | nom du kernel |
| `kali` | kali | hostname de la machine |
| `6.1.0-kali9-amd64` | — | version précise du kernel |
| `x86_64` | — | architecture 64 bits |
| `GNU/Linux` | — | OS complet |

En pentest : la version du kernel est la première chose à noter — elle permet de chercher des exploits de privilege escalation.

---

## `cat /etc/os-release` — version de la distro

```bash
cat /etc/os-release
```

Sortie typique :
```
NAME="Kali GNU/Linux"
VERSION="2023.4"
ID=kali
VERSION_ID="2023.4"
PRETTY_NAME="Kali GNU/Linux 2023.4"
```

---

## `top` / `htop` — vue temps réel

```bash
top     # intégré partout
htop    # plus lisible, navigation à la souris
```

Sortie `top` :
```
top - 10:42:01 up 2:13,  1 user,  load average: 0.52, 0.58, 0.62
Tasks: 214 total,   1 running, 213 sleeping
%Cpu(s):  5.2 us,  1.3 sy,  0.0 ni, 92.8 id
MiB Mem :  15258.4 total,   2048.1 free,   8192.3 used,   5018.0 buff/cache
MiB Swap:   2048.0 total,   2048.0 free,      0.0 used.   6800.1 avail Mem

  PID USER      PR  NI    VIRT    RES  %CPU  %MEM  COMMAND
 1200 cyanure   20   0  512Mi   128Mi   5.2   0.8  firefox-esr
  842 root      20   0  256Mi    64Mi   0.3   0.4  Xorg
```

| Colonne | Signification |
|---------|---------------|
| `PID` | **P**rocess **ID** |
| `PR` | **pr**iorité kernel |
| `NI` | **ni**ce value — priorité utilisateur |
| `VIRT` | mémoire **virt**uelle totale allouée |
| `RES` | mémoire **rés**idente réellement en RAM |
| `%CPU` | pourcentage CPU utilisé |
| `%MEM` | pourcentage RAM utilisé |

`load average: 0.52, 0.58, 0.62` — charge moyenne sur 1min, 5min, 15min. Sur un CPU 4 coeurs, une charge de 4.0 = 100% occupé.

`id` dans `%Cpu` = **id**le = pourcentage de temps où le CPU ne fait rien. 92.8% idle = machine quasi au repos.

Quitter `top` : `q`