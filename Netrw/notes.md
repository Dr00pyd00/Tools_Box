
# Navigation VIM via Netrw

**Navigation**

| Commande | Action |
|---|---|
| Entrée | ouvrir le fichier / entrer dans le dossier |
| `-` | remonter au dossier parent |
| `u` | revenir en arrière dans l'historique de navigation |
| `gh` | afficher / masquer les fichiers cachés (ceux qui commencent par `.`) |

**Édition**

| Commande | Action |
|---|---|
| `%` | créer un nouveau fichier |
| `d` | créer un nouveau dossier |
| `R` | renommer le fichier/dossier sous le curseur |
| `mf` | marquer un fichier (sélection multiple) |
| `mm` | déplacer les fichiers marqués vers le dossier courant |
| `mc` | copier les fichiers marqués vers le dossier courant |

**Suppression**

| Commande | Action |
|---|---|
| `D` | supprimer le fichier/dossier sous le curseur (confirmation demandée) |

**Ouverture dans un split** (pratique pour comparer deux fichiers)

| Commande | Action |
|---|---|
| `v` | ouvrir dans un split vertical |
| `o` | ouvrir dans un split horizontal |
| `t` | ouvrir dans un nouvel onglet |

**Lancer netrw**

```
:Explore    -- :Ex, dans la fenêtre courante
:Vexplore   -- :Vex, split vertical
:Sexplore   -- split horizontal
```

Le réflexe à garder en tête : `mf` marque, la commande suivante (`mm` ou `mc`) agit sur tout ce qui est marqué. C'est ce qui permet de déplacer plusieurs fichiers d'un coup — la seule partie un peu moins intuitive du lot.

