# Fiche mémo Redis

## Concepts de base

- Base de données **clé-valeur** en RAM (rapide, pas sur disque comme PostgreSQL)
- Une **clé** est toujours une string
- La **valeur** peut être de différents types : String, List, Hash, Set, Sorted Set
- Pas de tables, pas de schéma : toutes les clés vivent dans le même espace (DB 0 par défaut)
- Convention de nommage courante : `user:42:name` (séparateur `:`)

## Commandes générales

| Commande | Rôle |
|---|---|
| `PING` | teste la connexion, répond `PONG` |
| `TYPE cle` | affiche le type de la valeur stockée (string, list, hash, set, zset) |
| `KEYS *` | liste toutes les clés (à éviter en prod, coûteux) |
| `EXISTS cle` | vérifie si une clé existe (1 ou 0) |
| `DEL cle` | supprime une clé |
| `EXPIRE cle secondes` | pose un TTL (durée de vie) sur une clé |
| `TTL cle` | affiche le temps restant avant expiration |
| `FLUSHDB` | supprime **toutes** les clés de la base courante (attention) |

## String

| Commande | Rôle |
|---|---|
| `SET cle valeur` | crée ou **écrase** une clé (pas d'avertissement) |
| `GET cle` | récupère la valeur |
| `INCR cle` | incrémente une valeur numérique de 1 |
| `DECR cle` | décrémente une valeur numérique de 1 |

## List (liste ordonnée, doublons possibles)

| Commande | Rôle |
|---|---|
| `LPUSH cle valeur` | ajoute un élément **au début** (*Left PUSH*) |
| `RPUSH cle valeur` | ajoute un élément **à la fin** (*Right PUSH*) |
| `LRANGE cle debut fin` | lit une plage d'éléments (`0 -1` = tout, `-1` = dernier élément) |
| `LLEN cle` | longueur de la liste |
| `LPOP cle` | retire et retourne le premier élément |
| `RPOP cle` | retire et retourne le dernier élément |

## Pièges à retenir

- `SET` écrase silencieusement une valeur existante, sans erreur
- Une faute de frappe dans le nom d'une clé (`fruit` vs `fruits`) crée une **nouvelle clé indépendante** — Redis ne corrige rien
- Utiliser une commande d'un type sur une clé d'un autre type → erreur `WRONGTYPE`
- Toujours vérifier avec `TYPE cle` en cas de doute

## Hash (dictionnaire imbriqué : champ → valeur)

Représente un objet (ex: un utilisateur) sous une seule clé, avec plusieurs champs.

| Commande | Rôle |
|---|---|
| `HSET cle champ valeur` | crée/modifie un champ dans le hash |
| `HGET cle champ` | récupère la valeur d'un champ |
| `HGETALL cle` | récupère tous les champs et valeurs |
| `HDEL cle champ` | supprime un champ |
| `HEXISTS cle champ` | vérifie si un champ existe (1 ou 0) |
| `HKEYS cle` | liste tous les noms de champs |
| `HVALS cle` | liste toutes les valeurs |

Exemple : `HSET user:1 nom Luna age 25` puis `HGETALL user:1`

## Set (ensemble non-ordonné, valeurs uniques)

Pas de doublons, pas d'ordre garanti. Utile pour des tags, des relations, des tests d'appartenance rapides.

| Commande | Rôle |
|---|---|
| `SADD cle valeur` | ajoute un élément (ignoré si déjà présent) |
| `SMEMBERS cle` | liste tous les éléments |
| `SISMEMBER cle valeur` | vérifie si un élément est présent (1 ou 0) |
| `SREM cle valeur` | supprime un élément |
| `SCARD cle` | nombre d'éléments dans le set |
| `SINTER cle1 cle2` | intersection entre deux sets |
| `SUNION cle1 cle2` | union entre deux sets |
| `SDIFF cle1 cle2` | différence entre deux sets |

## Sorted Set / ZSet (ensemble ordonné par score)

Comme un Set, mais chaque élément a un **score** numérique qui définit son ordre. Utile pour des classements, des files priorisées, des timelines.

| Commande | Rôle |
|---|---|
| `ZADD cle score valeur` | ajoute un élément avec son score |
| `ZRANGE cle debut fin` | liste les éléments par ordre croissant de score |
| `ZREVRANGE cle debut fin` | liste les éléments par ordre décroissant |
| `ZSCORE cle valeur` | récupère le score d'un élément |
| `ZRANK cle valeur` | récupère le rang (position) d'un élément |
| `ZINCRBY cle increment valeur` | incrémente le score d'un élément |
| `ZREM cle valeur` | supprime un élément |

---
*Fiche vivante : à mettre à jour au fil de l'apprentissage*
