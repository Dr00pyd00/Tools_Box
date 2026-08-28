# head, tail & navigation de flux — cheat sheet

---

## head — début d'un fichier

```bash
head fichier.txt              # 10 premières lignes (défaut)
head -n 20 fichier.txt        # 20 premières lignes
head -n -5 fichier.txt        # tout sauf les 5 dernières lignes
head -c 100 fichier.txt       # 100 premiers octets
```

---

## tail — fin d'un fichier

```bash
tail fichier.txt              # 10 dernières lignes (défaut)
tail -n 20 fichier.txt        # 20 dernières lignes
tail -n +5 fichier.txt        # à partir de la ligne 5 jusqu'à la fin
tail -f fichier.log           # suit le fichier en temps réel (logs live)
tail -f -n 50 fichier.log     # 50 dernières lignes + suivi live
```

---

## wc — compter

```bash
wc fichier.txt                # lignes, mots, octets
wc -l fichier.txt             # nombre de lignes uniquement
wc -w fichier.txt             # nombre de mots uniquement
wc -c fichier.txt             # nombre d'octets
wc -m fichier.txt             # nombre de caractères
cat fichier.txt | wc -l       # compter via pipe
```

---

## sort — trier

```bash
sort fichier.txt              # tri alphabétique
sort -r fichier.txt           # tri inverse
sort -n fichier.txt           # tri numérique
sort -u fichier.txt           # tri + supprime les doublons
sort -k 2 fichier.txt         # tri sur la 2ème colonne
sort -t: -k 3 -n /etc/passwd  # tri numérique sur 3ème champ séparé par :
```

---

## uniq — dédoublonner

```bash
uniq fichier.txt              # supprime les doublons consécutifs
uniq -c fichier.txt           # compte les occurrences
uniq -d fichier.txt           # affiche seulement les doublons
uniq -u fichier.txt           # affiche seulement les lignes uniques
sort fichier.txt | uniq -c | sort -rn   # fréquence de chaque ligne, triée
```

---

## cut — extraire des colonnes

```bash
cut -d: -f1 /etc/passwd       # 1er champ séparé par :  → usernames
cut -d: -f1,3 /etc/passwd     # 1er et 3ème champ
cut -c1-10 fichier.txt        # caractères 1 à 10 de chaque ligne
cut -d, -f2 data.csv          # 2ème colonne d'un CSV
```

---

## tr — remplacer / supprimer des caractères

```bash
echo "HELLO" | tr 'A-Z' 'a-z'        # majuscules → minuscules
echo "hello world" | tr ' ' '_'       # espaces → underscores
echo "aabbcc" | tr -s 'a-z'           # compresse les répétitions
cat fichier.txt | tr -d '\r'           # supprime les retours chariot Windows
```

---

## sed — éditer un flux

```bash
sed 's/ancien/nouveau/' fichier.txt       # remplace la 1ère occurrence par ligne
sed 's/ancien/nouveau/g' fichier.txt      # remplace toutes les occurrences
sed -n '5,10p' fichier.txt                # affiche les lignes 5 à 10
sed '/pattern/d' fichier.txt              # supprime les lignes qui matchent
sed -i 's/foo/bar/g' fichier.txt          # modifie le fichier directement
```

---

## awk — traitement de colonnes

```bash
awk '{print $1}' fichier.txt              # affiche la 1ère colonne
awk '{print $1, $3}' fichier.txt          # 1ère et 3ème colonne
awk -F: '{print $1}' /etc/passwd          # séparateur : → usernames
awk 'NR==5' fichier.txt                   # affiche la ligne 5
awk 'NR>=5 && NR<=10' fichier.txt         # lignes 5 à 10
awk '{sum += $1} END {print sum}' f.txt   # somme de la 1ère colonne
```

---

## combos utiles

```bash
# top 10 des mots de passe les plus fréquents dans rockyou
sort rockyou.txt | uniq -c | sort -rn | head -10

# usernames système avec un vrai shell
cut -d: -f1,7 /etc/passwd | grep -v "nologin\|false"

# compter les ports ouverts dans un scan nmap
grep "open" nmap_output.txt | wc -l

# extraire toutes les IPs d'un fichier log
grep -oE "[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}" fichier.log | sort -u

# voir les 20 dernières erreurs en live
tail -f app.log | grep "ERROR"

# lignes 50 à 100 d'un fichier
sed -n '50,100p' fichier.txt
# ou
awk 'NR>=50 && NR<=100' fichier.txt
```