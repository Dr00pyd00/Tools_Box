# `find` et `which` — localiser des fichiers et commandes

---

## `which` — trouver l'emplacement d'une commande

`which` cherche dans le `PATH` et retourne le chemin absolu d'une commande exécutable.

```bash
which python3
which nc
which wget
which curl
```

Sorties typiques :
```
/usr/bin/python3
/usr/bin/nc
/usr/bin/wget
/usr/bin/curl
```

Si la commande n'existe pas :
```bash
which netcat
# pas de sortie — commande introuvable dans le PATH
```

**En pentest** — vérifier ce qui est disponible sur une cible après intrusion :
```bash
which python3 perl ruby nc wget curl gcc
```
Chaque outil présent est un vecteur potentiel — téléchargement de fichiers, reverse shell, compilation d'exploit.

---

## `find` — chercher des fichiers sur le système

`find` est beaucoup plus puissant que `which` — il cherche partout, pas seulement dans le PATH, et avec des critères précis.

### Syntaxe de base

```bash
find [où chercher] [critères] [action]
```

---

### Chercher par nom

```bash
find / -name "passwd"           # cherche "passwd" partout depuis la racine
find /etc -name "*.conf"        # tous les .conf dans /etc
find . -name "*.py"             # tous les .py dans le dossier courant
find / -name "flag.txt"         # chercher un flag HTB
```

`-name` — sensible à la casse  
`-iname` — **i**nsensitive, ignore la casse (`-iname "readme*"` trouve README.txt et readme.txt)

---

### Chercher par type

```bash
find / -type f -name "*.txt"    # uniquement les fichiers (-type f = file)
find / -type d -name "backup"   # uniquement les dossiers (-type d = directory)
find / -type l                  # uniquement les liens symboliques (-type l = link)
```

---

### Chercher par propriétaire

```bash
find / -user root               # fichiers appartenant à root
find / -user cyanure            # fichiers appartenant à cyanure
find / -group sudo              # fichiers appartenant au groupe sudo
```

---

### Chercher par permissions

```bash
find / -perm 777                # fichiers avec permissions rwxrwxrwx exactement
find / -perm -4000              # fichiers avec le bit SUID activé
find / -perm -2000              # fichiers avec le bit SGID activé
find / -perm -o+w               # fichiers modifiables par tout le monde
```

**SUID** — **S**et **U**ser **ID** — le fichier s'exécute avec les droits de son propriétaire (souvent root) peu importe qui le lance. En pentest c'est une des premières choses à chercher pour le privilege escalation :
```bash
find / -perm -4000 -type f 2>/dev/null
```

---

### Chercher par taille

```bash
find / -size +100M              # fichiers de plus de 100 Mo
find / -size -10k               # fichiers de moins de 10 Ko
find / -size 1337c              # fichiers de exactement 1337 octets (c = bytes)
```

`k` = kilo-octets, `M` = méga-octets, `G` = giga-octets, `c` = octets bruts

---

### Chercher par date

```bash
find / -mtime -7                # modifiés il y a moins de 7 jours
find / -mtime +30               # modifiés il y a plus de 30 jours
find / -newer /etc/passwd       # modifiés plus récemment que /etc/passwd
```

`-mtime` — **m**odification **time**  
`-atime` — **a**ccess **time** (dernier accès en lecture)  
`-ctime` — **c**hange **time** (changement de métadonnées)

---

### Combiner les critères

```bash
find / -type f -user root -perm -4000 2>/dev/null
# fichiers, appartenant à root, avec SUID, sans afficher les erreurs
```

`2>/dev/null` — redirige les erreurs "Permission denied" vers le néant pour une sortie propre

---

### Actions sur les résultats

```bash
find / -name "*.log" -delete              # supprimer tous les .log trouvés
find / -name "*.py" -exec cat {} \;       # afficher le contenu de chaque .py trouvé
find / -name "*.conf" -exec grep -l "password" {} \;  # chercher "password" dans les .conf
```

`-exec` — exécute une commande sur chaque résultat  
`{}` — représente le fichier trouvé  
`\;` — termine la commande `-exec`

---

## Récapitulatif — usage pentest

| Commande | Objectif |
|----------|----------|
| `which python3 nc wget curl` | outils dispo sur la cible |
| `find / -perm -4000 -type f 2>/dev/null` | binaires SUID → privilege escalation |
| `find / -user root -writable 2>/dev/null` | fichiers root modifiables |
| `find / -name "*.conf" 2>/dev/null` | fichiers de config (credentials) |
| `find / -name "flag*" 2>/dev/null` | flags HTB |
| `find / -mtime -1 2>/dev/null` | fichiers modifiés récemment |


---

## `locate` — chercher vite dans une base de données

`locate` ne parcourt pas le disque en temps réel comme `find` — il interroge une base de données pré-indexée. Résultat : **beaucoup plus rapide**, mais potentiellement **pas à jour**.

```bash
locate passwd
locate "*.conf"
locate flag.txt
```

### Mettre à jour la base de données

```bash
sudo updatedb
```

`updatedb` — **update** **d**ata**b**ase — reconstruit l'index en parcourant le disque. À faire si un fichier récent n'apparaît pas dans les résultats.

### Options utiles

```bash
locate -i readme        # -i = insensible à la casse
locate -c passwd        # -c = --count, affiche juste le nombre de résultats
locate -l 5 "*.py"     # -l = --limit, affiche seulement 5 résultats
```

### `find` vs `locate` — quand utiliser lequel

| | `find` | `locate` |
|--|--------|----------|
| Vitesse | Lent (parcourt le disque) | Rapide (base de données) |
| Résultats | Toujours à jour | Peut être obsolète |
| Critères | Permissions, taille, date, owner... | Nom uniquement |
| Disponible sur cible | Presque toujours | Pas toujours installé |

**En pentest** : `locate` est utile sur ta propre machine Kali pour trouver des wordlists, des scripts, des exploits rapidement. Sur une cible, `find` est plus fiable car `locate` n'est souvent pas installé et sa base peut être vide.

```bash
locate wordlist         # trouver les wordlists sur ton Kali
locate exploit          # trouver des exploits locaux
locate rockyou          # trouver rockyou.txt
```