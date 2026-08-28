# méthode — rechercher dans la doc des outils

> Comment trouver le bon format, la bonne option, le bon mode quand tu bloques.

---

## réflexe 1 — chercher dans l'outil lui-même

### lister les formats/modes disponibles
```bash
john --list=formats                          # tous les formats john
john --list=formats | grep -i postgres       # filtrer sur un mot clé
john --list=formats | grep -i md5           # filtrer sur md5

hashcat --example-hashes                     # tous les modes hashcat avec exemples
hashcat --example-hashes | grep -i postgres  # filtrer
hashcat --example-hashes | grep -A 3 "m 10 " # voir le mode 10 avec 3 lignes après
```

### voir les détails d'un format
```bash
john --list=format-details --format=postgres  # détails + exemple de hash attendu
john --list=format-details --format=raw-md5
```

### voir l'aide d'une commande
```bash
john --help
john --help | grep format
hashcat --help | grep "\-m"
hydra --help
hydra -U smb                                  # aide spécifique à un module hydra
```

---

## réflexe 2 — identifier le format d'un hash

### par la longueur
| longueur | algorithme probable |
|----------|-------------------|
| 32 chars | MD5 |
| 40 chars | SHA1 |
| 56 chars | SHA224 |
| 64 chars | SHA256 |
| 96 chars | SHA384 |
| 128 chars | SHA512 |

### par le préfixe
| préfixe | algorithme |
|---------|-----------|
| `$1$` | MD5 Linux |
| `$2b$` | bcrypt |
| `$5$` | SHA-256 Linux |
| `$6$` | SHA-512 Linux |
| `$y$` | yescrypt |
| `md5` | PostgreSQL MD5 |
| `{SHA}` | SHA1 LDAP |

### outil automatique
```bash
hash-identifier                    # outil interactif — colle ton hash
hashid "5f4dcc3b5aa765d61d8327deb882cf99"  # identification directe
```

---

## réflexe 3 — chercher le bon mode hashcat

```bash
# chercher par nom
hashcat --example-hashes | grep -i "postgresql"
hashcat --example-hashes | grep -i "wordpress"
hashcat --example-hashes | grep -i "bcrypt"

# voir le mode ET l'exemple de hash
hashcat --example-hashes | grep -B 1 -A 4 "PostgreSQL"

# structure de la sortie :
# Hash mode #XXXX       ← le numéro de mode à utiliser avec -m
# Name: ...             ← nom de l'algorithme
# Example.Hash: ...     ← exemple du format exact attendu
```

---

## réflexe 4 — comprendre le format attendu

Toujours regarder l'exemple de hash avant de lancer :

```bash
john --list=format-details --format=MON_FORMAT
hashcat --example-hashes | grep -A 5 "MON_FORMAT"
```

L'exemple te dit exactement comment formater ton fichier.

---

## réflexe 5 — vérifier manuellement avant de lancer un outil

Pour les hashes simples — reconstruis le calcul à la main et compare :

```bash
# MD5 simple
echo -n "password" | md5sum

# MD5 avec sel (sel après)
echo -n "passwordmonsel" | md5sum

# MD5 avec sel (sel avant)
echo -n "monselpassword" | md5sum

# PostgreSQL : md5(password + username)
echo -n "postgrespostgres" | md5sum

# SHA1
echo -n "password" | sha1sum

# SHA256
echo -n "password" | sha256sum
```

Si le résultat correspond au hash cible → tu as trouvé le mot de passe sans lancer aucun outil.

---

## réflexe 6 — Google en dernier recours

Quand rien ne marche, cherche :

```
john the ripper postgresql md5 format example
hashcat mode postgresql shadow hash
crack md5(password+username) hashcat
```

Les sites utiles :
- `hashcat.net/wiki` — documentation officielle hashcat avec tous les modes
- `openwall.com/john` — documentation john
- `hashes.com` — identifier un hash en ligne
- Stack Overflow, GitHub issues

---

## exemple de session de debug — ce qu'on a fait

```
1. récupéré hash PostgreSQL : md53175bce1d3201d16594cebf9d7eb3f9d
2. identifié : 32 chars hex avec préfixe md5 → PostgreSQL MD5
3. cherché format john : john --list=formats | grep -i postgres → "postgres"
4. vu le format attendu : john --list=format-details --format=postgres
5. compris la formule : md5(password + username)
6. vérifié manuellement : echo -n "postgrespostgres" | md5sum → match !
7. trouvé sans outil de brute force
```

La vérification manuelle d'abord évite des heures de debug avec les mauvais modes.