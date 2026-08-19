# Fiche Emmet — abréviations HTML

Contexte : `nvim-emmet` + `emmet_language_server` (LSP). Tape l'abréviation en mode insertion dans un fichier `.html`, puis déclenche la complétion (`Ctrl-Space` ou ton raccourci `cmp`) pour l'expand.

## Structure de base

| Abréviation | Résultat |
|---|---|
| `!` | Boilerplate HTML5 complet |
| `html:5` | Équivalent explicite de `!` |
| `div` | `<div></div>` |
| `p` | `<p></p>` |

## Opérateurs de structure

| Symbole | Rôle | Exemple | Résultat |
|---|---|---|---|
| `>` | enfant (descendant) | `div>ul>li` | `<li>` imbriqué dans `<ul>` imbriqué dans `<div>` |
| `+` | frère (sibling) | `header+main+footer` | trois balises au même niveau, l'une après l'autre |
| `*` | multiplication | `li*3` | trois `<li></li>` |
| `()` | groupement | `(header>nav)+main+footer` | groupe une structure imbriquée comme un seul bloc frère |

## Attributs rapides

| Symbole | Rôle | Exemple | Résultat |
|---|---|---|---|
| `.` | classe | `div.container` | `<div class="container"></div>` |
| `#` | id | `div#header` | `<div id="header"></div>` |
| `{}` | texte interne | `a{Lien}` | `<a>Lien</a>` |
| `$` | numérotation auto (avec `*`) | `li.item$*3` | `item1`, `item2`, `item3` |

## Exemple combiné

```
nav>ul>li.nav-item$*3>a.nav-link{Lien $}
```

Génère une nav avec 3 liens numérotés, texte inclus.

## Pour aller plus loin (non couvert ici)

- Attributs custom : `input[type=text name=username]`
- Texte de remplissage : `lorem50`
- Voir la doc officielle : https://docs.emmet.io/cheat-sheet/
