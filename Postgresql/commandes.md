# Fiche mémo — Commandes internes psql

Les commandes internes de `psql` commencent toutes par `\`. Ce ne sont **pas** du SQL — pas besoin de `;` à la fin, elles sont interprétées directement par le client `psql`, pas envoyées au serveur.

## Connexion et contexte

| Commande | Rôle |
|---|---|
| `\c nom_base` | change de base de données courante (*connect*) |
| `\c nom_base utilisateur` | change de base **et** de rôle en même temps |
| `\conninfo` | affiche les infos de connexion actuelles (base, utilisateur, hôte, port) |
| `\q` | quitte psql |

## Lister les objets

| Commande | Rôle |
|---|---|
| `\l` | liste toutes les bases de données du serveur (*list*) |
| `\dt` | liste les tables du schéma courant (*display tables*) |
| `\dt+` | idem, avec taille et description en plus |
| `\d nom_table` | décrit une table : colonnes, types, contraintes, index |
| `\d+ nom_table` | idem, avec plus de détails (taille, stockage) |
| `\dn` | liste les schémas (*display namespaces*) |
| `\di` | liste les index |
| `\dv` | liste les vues |
| `\df` | liste les fonctions |
| `\du` | liste les rôles/utilisateurs, avec leurs attributs |
| `\dp` | liste les permissions sur les tables |

## Affichage des résultats

| Commande | Rôle |
|---|---|
| `\x` | bascule l'affichage en mode étendu (une colonne par ligne, utile pour les lignes larges) |
| `\x auto` | mode étendu automatique si la ligne est trop large pour le terminal |
| `\timing` | active/désactive l'affichage du temps d'exécution de chaque requête |

## Édition et fichiers

| Commande | Rôle |
|---|---|
| `\e` | ouvre la dernière commande dans un éditeur externe (`$EDITOR`) |
| `\i fichier.sql` | exécute un fichier `.sql` (*input*) |
| `\o fichier.txt` | redirige la sortie des prochaines requêtes vers un fichier |
| `\g` | ré-exécute la dernière commande |

## Aide

| Commande | Rôle |
|---|---|
| `\?` | liste toutes les commandes psql disponibles |
| `\h` | aide sur les commandes SQL (ex: `\h CREATE TABLE`) |

## Repères visuels du prompt

| Prompt | Signification |
|---|---|
| `nombase=>` | connecté normalement (rôle non-superuser) |
| `nombase=#` | connecté en tant que superuser |
| `nombase(>` | une instruction est ouverte (ex: parenthèse non fermée), en attente de la suite |
| `nombase-#` | une ligne SQL continue sur la suivante (pas encore de `;`) |
