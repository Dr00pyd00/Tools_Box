# dirb — commandes de base

> **dirb** = **Dir**ectory **B**ruter — outil de découverte de dossiers et fichiers sur un serveur web.
> Il teste des milliers de paths connus et affiche ceux qui existent.
> C'est le nmap du web — tu cartographies la surface d'attaque.

---

## Concept

```
dirb teste :
http://site.com/admin         → 200 ? existe
http://site.com/backup        → 404 ? n'existe pas
http://site.com/config        → 403 ? existe mais interdit
http://site.com/phpMyAdmin    → 200 ? existe
...
4612 paths testés en quelques secondes
```

---

## Commande de base

```bash
# [Kali - terminal]
dirb http://192.168.159.142
```

Utilise la wordlist par défaut : `/usr/share/dirb/wordlists/common.txt` — 4612 mots.

---

## Wordlists disponibles

```bash
ls /usr/share/dirb/wordlists/
```

| Wordlist | Taille | Usage |
|---|---|---|
| `common.txt` | 4 612 mots | scan rapide — défaut |
| `big.txt` | 20 469 mots | scan plus complet |
| `small.txt` | 959 mots | scan très rapide |
| `vulns/` | dossier | wordlists spécialisées (CGI, apache...) |

---

## Options utiles

```bash
dirb http://IP                                    # scan de base
dirb http://IP /usr/share/dirb/wordlists/big.txt  # wordlist plus grande
dirb http://IP -o resultats.txt                   # -o = output, sauvegarde les résultats
dirb http://IP -r                                 # -r = no recursive, ne rentre pas dans les sous-dossiers
dirb http://IP -z 100                             # -z = milliseconds, pause entre requêtes (discret)
dirb http://IP -a "Mozilla/5.0"                   # -a = user agent personnalisé
dirb http://IP -c "PHPSESSID=abc123"              # -c = cookie, scan en étant authentifié
dirb http://IP -X .php,.html,.txt                 # -X = extensions à tester
```

---

## Lire les résultats

```
+ http://site.com/admin     (CODE:200|SIZE:1234)   → existe, accessible
+ http://site.com/config    (CODE:403|SIZE:296)    → existe, accès interdit
==> DIRECTORY: http://site.com/backup/             → dossier trouvé, dirb va l'explorer
(!) WARNING: Directory IS LISTABLE                 → dossier ouvert, contenu visible
```

| Code | Signification | Intérêt |
|---|---|---|
| `200` | existe et accessible | ✓✓ très intéressant |
| `403` | existe mais interdit | ✓ intéressant — tenter de contourner |
| `301/302` | redirection | ✓ suivre la redirection |
| `404` | n'existe pas | ✗ ignorer |

---

## Directory IS LISTABLE — misconfiguration critique

```
(!) WARNING: Directory IS LISTABLE. No need to scan it.
```

Le dossier affiche son contenu comme un `ls` — sans authentification.
Tu peux voir et télécharger tous les fichiers dedans.

Exemple dangereux :
```
/backup/          → IS LISTABLE
  database.sql    → base de données complète téléchargeable
  config.php.bak  → fichier de config avec mots de passe
```

---

## Alternatives à dirb

| Outil | Particularité |
|---|---|
| `dirb` | simple, classique |
| `gobuster` | plus rapide, multithreadé |
| `ffuf` | très rapide, très flexible |
| `dirsearch` | plus moderne, Python |

```bash
# gobuster — alternative populaire
gobuster dir -u http://192.168.159.142 -w /usr/share/wordlists/dirb/common.txt

# ffuf — le plus rapide
ffuf -u http://192.168.159.142/FUZZ -w /usr/share/wordlists/dirb/common.txt
```

---

## Workflow pentest web

```
nmap -sV IP                → port 80 ouvert, Apache X.X
curl -I http://IP          → bannière serveur, headers
dirb http://IP             → cartographie des dossiers
                ↓
/phpMyAdmin  → tenter default credentials
/phpinfo.php → infos sur la config PHP
/backup/     → IS LISTABLE → chercher des fichiers sensibles
/admin/      → tenter de se connecter
```