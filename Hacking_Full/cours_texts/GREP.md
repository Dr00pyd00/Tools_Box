# grep — cheat sheet

> **Global Regular Expression Print** — cherche un pattern dans des fichiers ou des flux

---

## syntaxe

```bash
grep [flags] "pattern" [fichier(s)]
commande | grep [flags] "pattern"
```

---

## flags — affichage

| flag | nom | effet |
|------|-----|-------|
| `-n` | number | affiche le numéro de ligne devant chaque résultat |
| `-i` | ignore-case | insensible à la casse — "Error" = "error" = "ERROR" |
| `-v` | invert | affiche les lignes qui NE matchent PAS le pattern |
| `-c` | count | compte uniquement le nombre de lignes qui matchent |
| `-l` | list files | affiche seulement les noms de fichiers qui contiennent le pattern |
| `-L` | list no match | fichiers qui ne contiennent PAS le pattern |
| `-o` | only matching | affiche uniquement la partie qui matche, pas toute la ligne |
| `-q` | quiet | silencieux — retourne juste un code de sortie (0=trouvé, 1=pas trouvé) |

---

## flags — périmètre de recherche

| flag | nom | effet |
|------|-----|-------|
| `-r` | recursive | cherche dans tous les fichiers d'un dossier et sous-dossiers |
| `-R` | recursive+ | idem mais suit aussi les liens symboliques |
| `-w` | word | match le mot entier — "root" ne matche pas "rootkit" |
| `-x` | line | match la ligne entière exactement |
| `--include="*.py"` | filtre fichiers | cherche seulement dans certains types de fichiers |
| `--exclude="*.log"` | exclut fichiers | ignore certains types de fichiers |

---

## flags — contexte autour du match

| flag | nom | effet |
|------|-----|-------|
| `-A n` | after | affiche n lignes APRÈS chaque match |
| `-B n` | before | affiche n lignes AVANT chaque match |
| `-C n` | context | affiche n lignes avant ET après — équivalent de -A n -B n |

---

## flags — patterns avancés

| flag | nom | effet |
|------|-----|-------|
| `-e "pat"` | expression | multiple patterns — `grep -e "erreur" -e "warning"` |
| `-f fichier` | file | lit les patterns depuis un fichier, un par ligne |
| `-E` | extended regex | active les regex étendues — +, ?, \|, () sans échappement |
| `-P` | perl regex | regex Perl — \d, \w, \s, lookahead/lookbehind |
| `-F` | fixed string | pattern littéral, pas de regex — plus rapide sur gros fichiers |

---

## exemples pratiques — fichiers & logs

```bash
grep -n "password123" rockyou.txt       # numéro de ligne du mot
grep -c "ERROR" app.log                 # combien d'erreurs ?
grep -v "DEBUG" app.log                 # tout sauf les lignes DEBUG
grep -A 3 "Exception" app.log           # 3 lignes après chaque exception
grep -i "error" app.log                 # Error, ERROR, error...
grep -C 2 "CRITICAL" app.log            # 2 lignes avant et après
```

---

## exemples pratiques — sécurité & recon

```bash
grep -r "api_key" ~/projet/                      # cherche clés API dans le code
grep -r "password" . --include="*.env"           # mots de passe dans les .env
grep -w "root" /etc/passwd                       # ligne exacte de root
grep -E "LISTEN|ESTABLISHED" ss_output.txt       # filtre multi-états réseau
grep -o "[0-9]\{1,3\}\.[0-9]\{1,3\}" fichier     # extraire les IPs
grep -rn "TODO" . --include="*.py"               # tous les TODO avec numéro de ligne
```

---

## combos avec pipe — les plus utiles

```bash
# filtrer uniquement les ports ouverts
nmap 192.168.1.0/24 | grep -i "open"

# utilisateurs avec un vrai shell
cat /etc/passwd | grep -v "nologin" | grep -v "false"

# trouver les process python sans afficher grep lui-même
ps aux | grep -v grep | grep "python"

# tous les TODO Python sauf dans les tests
grep -r "TODO" . --include="*.py" | grep -v "test"

# compter le nombre total de lignes d'un fichier
grep -c "" fichier.txt
```

---

## regex de base utiles avec `-E`

| pattern | signification |
|---------|---------------|
| `.` | n'importe quel caractère |
| `*` | 0 ou plus du caractère précédent |
| `+` | 1 ou plus |
| `?` | 0 ou 1 |
| `^` | début de ligne |
| `$` | fin de ligne |
| `[abc]` | un caractère parmi a, b ou c |
| `[^abc]` | tout sauf a, b ou c |
| `a\|b` | a ou b |
| `\d` | chiffre (avec `-P`) |
| `\w` | caractère alphanumérique (avec `-P`) |
| `\s` | espace/tab (avec `-P`) |

---

## code de sortie — utile dans les scripts

```bash
# 0 = match trouvé, 1 = pas de match, 2 = erreur
grep -q "pattern" fichier && echo "trouvé" || echo "pas trouvé"

# dans un script
if grep -q "ERROR" app.log; then
    echo "des erreurs sont présentes"
fi
```