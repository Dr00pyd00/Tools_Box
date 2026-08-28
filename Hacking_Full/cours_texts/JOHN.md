# john the ripper — cheat sheet

> Outil de crackage de mots de passe. Supporte des centaines de formats de hash.

---

## syntaxe de base

```bash
john [options] fichier_hash
```

---

## modes de crackage

| mode | commande | description |
|------|----------|-------------|
| wordlist | `john --wordlist=rockyou.txt hash.txt` | teste chaque mot de la liste |
| wordlist + rules | `john --wordlist=rockyou.txt --rules hash.txt` | applique des mutations (password → P@ssw0rd) |
| incremental | `john --incremental hash.txt` | brute force pur — teste toutes les combinaisons |
| single | `john --single hash.txt` | utilise le username et des variations simples |
| sans option | `john hash.txt` | essaie tous les modes automatiquement |

---

## formats de hash courants

| format | flag | exemple |
|--------|------|---------|
| MD5 Linux `$1$` | auto-détecté | `/etc/shadow` vieux systèmes |
| SHA-512 Linux `$6$` | auto-détecté | `/etc/shadow` systèmes modernes |
| bcrypt `$2b$` | auto-détecté | applications web |
| yescrypt `$y$` | auto-détecté | Ubuntu récent |
| NTLM | `--format=nt` | Windows |
| MD5 raw | `--format=raw-md5` | hash MD5 seul sans sel |
| SHA1 raw | `--format=raw-sha1` | hash SHA1 seul |
| zip | `--format=pkzip` | archives zip protégées |

```bash
john --list=formats          # lister tous les formats supportés
john --format=raw-md5 hash.txt   # forcer un format spécifique
```

---

## wordlists

```bash
john --wordlist=/usr/share/wordlists/rockyou.txt hash.txt
john --wordlist=passwords.txt hash.txt
```

Wordlists disponibles sur Kali :
- `/usr/share/wordlists/rockyou.txt` — 14 millions de mots de passe réels
- `/usr/share/wordlists/fasttrack.txt` — mots de passe courants, rapide
- `/usr/share/seclists/` — collections variées

---

## rules — mutations automatiques

```bash
john --wordlist=rockyou.txt --rules hash.txt
```

Les rules appliquent des transformations automatiques sur chaque mot :
- `password` → `Password`, `PASSWORD`, `p@ssword`, `password123`
- Très utile quand le mot de passe de base est dans la liste mais modifié

```bash
john --rules=jumbo --wordlist=rockyou.txt hash.txt    # rules plus agressives
```

---

## afficher les résultats

```bash
john --show hash.txt              # affiche les mots de passe trouvés
john --show --format=raw-md5 hash.txt   # préciser le format si nécessaire
```

John stocke les résultats dans `~/.john/john.pot` — même après fermeture du terminal.

---

## gestion des sessions

```bash
john --session=nom_session hash.txt        # nommer une session
john --restore=nom_session                 # reprendre une session interrompue
john --restore                             # reprendre la dernière session
```

Utile pour les crackages longs — tu peux interrompre avec Ctrl+C et reprendre plus tard.

---

## fichiers importants

| fichier | contenu |
|---------|---------|
| `~/.john/john.pot` | mots de passe déjà crackés — john ne les reteste pas |
| `~/.john/john.log` | logs détaillés |
| `~/.john/john.rec` | fichier de reprise de session |

```bash
cat ~/.john/john.pot        # voir tous les mots de passe trouvés
rm ~/.john/john.pot         # effacer le cache pour retester
```

---

## préparer les fichiers hash

```bash
# depuis /etc/shadow directement
john --wordlist=rockyou.txt /etc/shadow

# extraire seulement certains utilisateurs
grep "msfadmin\|user\|postgres" /etc/shadow > hashes.txt
john --wordlist=rockyou.txt hashes.txt

# hash seul sans format shadow
echo "5f4dcc3b5aa765d61d8327deb882cf99" > md5.txt
john --format=raw-md5 --wordlist=rockyou.txt md5.txt
```

---

## combiner avec unshadow

Sur une machine cible où tu as accès aux deux fichiers :

```bash
unshadow /etc/passwd /etc/shadow > combined.txt
john --wordlist=rockyou.txt combined.txt
```

`unshadow` combine `passwd` et `shadow` pour que john ait toutes les infos nécessaires.

---

## exemples complets

```bash
# cracker des hashes MD5 Linux avec rockyou
john --wordlist=/usr/share/wordlists/rockyou.txt hashes_metas.txt

# même chose avec mutations
john --wordlist=/usr/share/wordlists/rockyou.txt --rules hashes_metas.txt

# voir les résultats
john --show hashes_metas.txt

# cracker un hash NTLM Windows
echo "aad3b435b51404eeaad3b435b51404ee:8846f7eaee8fb117ad06bdd830b7586c" > ntlm.txt
john --format=nt --wordlist=rockyou.txt ntlm.txt

# brute force pur sur un hash court
john --incremental --format=raw-md5 hash.txt
```

---

## john vs hashcat

| | john | hashcat |
|--|------|---------|
| facilité | plus simple | plus complexe |
| GPU | limité | optimisé GPU |
| vitesse | plus lent | beaucoup plus rapide |
| auto-détection format | oui | non — il faut `-m` |
| usage typique | pentest rapide | crackage intensif |

Pour du crackage rapide sur le terrain → **john**
Pour du crackage sérieux avec GPU → **hashcat**