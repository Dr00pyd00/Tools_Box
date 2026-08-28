# Nano — éditeur de texte terminal

Nano est l'éditeur le plus simple du terminal. Contrairement à vim, pas de modes à apprendre — tu ouvres et tu tapes directement.

---

## Ouvrir un fichier

```bash
nano fichier.txt          # ouvre ou crée le fichier
nano /etc/hosts           # chemin absolu
sudo nano /etc/hosts      # avec droits root si nécessaire
```

---

## Interface

```
  GNU nano 7.2          fichier.txt

[contenu du fichier ici]


^G Help    ^O Write Out  ^W Where Is  ^K Cut      ^T Execute   ^C Location
^X Exit    ^R Read File  ^\ Replace   ^U Paste     ^J Justify   ^/ Go To Line
```

`^` = touche `Ctrl`  
La barre du bas affiche tous les raccourcis disponibles en permanence.

---

## Raccourcis essentiels

| Raccourci | Action |
|-----------|--------|
| `Ctrl + O` | **O**utput — enregistrer le fichier |
| `Ctrl + X` | e**X**it — quitter (propose de sauvegarder si modifié) |
| `Ctrl + W` | **W**here — chercher un mot |
| `Ctrl + K` | **K**ut — couper la ligne entière |
| `Ctrl + U` | **U**npaste — coller la ligne coupée |
| `Ctrl + G` | **G**et help — aide complète |
| `Ctrl + C` | **C**ursor — affiche la position du curseur (ligne, colonne) |
| `Ctrl + /` | aller à une ligne précise |
| `Ctrl + A` | aller au début de la ligne |
| `Ctrl + E` | aller à la fin de la ligne |
| `Alt + U` | annuler (undo) |
| `Alt + E` | rétablir (redo) |

---

## Chercher et remplacer

```
Ctrl + W    → chercher
Ctrl + \    → chercher ET remplacer
```

Après `Ctrl + W` :
- `Entrée` pour chercher l'occurrence suivante
- `Ctrl + C` pour annuler la recherche

---

## Enregistrer

```
Ctrl + O → nano demande le nom du fichier → Entrée pour confirmer
```

Si le fichier existe déjà, il propose le même nom — appuie juste sur `Entrée`.

---

## Quitter

```
Ctrl + X
```

- Si le fichier n'a pas été modifié → quitte directement
- Si modifié → nano demande : `Save modified buffer?`
  - `Y` + `Entrée` → sauvegarde et quitte
  - `N` → quitte sans sauvegarder
  - `Ctrl + C` → annule, reste dans nano

---

## Options utiles à l'ouverture

```bash
nano -l fichier.txt       # affiche les numéros de ligne (-l = --linenumbers)
nano +42 fichier.txt      # ouvre directement à la ligne 42
nano -v fichier.txt       # mode lecture seule (-v = --view)
nano -m fichier.txt       # active la souris (-m = --mouse)
```

---

## En pentest

Nano est utile pour modifier rapidement des fichiers de config sur une cible :
```bash
nano /etc/hosts           # ajouter une entrée DNS locale
nano /etc/crontab         # lire/modifier les tâches planifiées (persistence)
nano ~/.bashrc            # modifier le shell d'un utilisateur
```

> Si nano n'est pas installé sur la cible, utilise `vi` ou `echo` pour écrire dans un fichier :
> ```bash
> echo "texte" >> fichier.txt
> ```