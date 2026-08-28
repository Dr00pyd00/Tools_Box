# mysql — navigation cheat sheet

> Commandes pour se déplacer et explorer une base MySQL/MariaDB.

---

## connexion

```bash
mysql -h IP -u root --skip-ssl          # sans mot de passe
mysql -h IP -u user -p --skip-ssl       # avec mot de passe (demandé après)
mysql -h IP -u user -pmotdepasse        # mot de passe inline (pas d'espace après -p)
mysql -h IP -u root -p mabase          # connexion directe à une base
```

---

## navigation — les essentiels

```sql
SHOW DATABASES;                  -- lister toutes les bases
USE nom_database;                -- sélectionner une base
SHOW TABLES;                     -- lister les tables de la base courante
DESCRIBE nom_table;              -- voir la structure d'une table (colonnes, types)
DESC nom_table;                  -- raccourci de DESCRIBE
SELECT DATABASE();               -- voir dans quelle base on est
SELECT USER();                   -- voir quel user on est
SELECT VERSION();                -- version du serveur
```

---

## lire les données

```sql
SELECT * FROM nom_table;                        -- tout le contenu
SELECT * FROM nom_table LIMIT 10;               -- 10 premières lignes
SELECT colonne1, colonne2 FROM nom_table;       -- colonnes spécifiques
SELECT * FROM nom_table WHERE colonne='valeur'; -- avec filtre
SELECT COUNT(*) FROM nom_table;                 -- compter les lignes
```

---

## informations système

```sql
SHOW DATABASES;                              -- toutes les bases
SHOW TABLES;                                 -- tables de la base courante
SHOW TABLES FROM nom_database;               -- tables d'une autre base
SHOW COLUMNS FROM nom_table;                 -- colonnes d'une table
SHOW GRANTS FOR 'root'@'localhost';          -- droits d'un utilisateur
SELECT * FROM mysql.user;                    -- tous les utilisateurs MySQL
SELECT host, user, password FROM mysql.user; -- users et leurs hash de mdp
```

---

## commandes client (commencent par \)

```
\q    quitter
\h    aide
\s    statut de la connexion
\u    changer de base (équivalent de USE)
\!    exécuter une commande shell
\G    afficher le résultat verticalement (plus lisible)
```

---

## exemple de session complète

```sql
-- 1. lister les bases
SHOW DATABASES;

-- 2. sélectionner une base
USE dvwa;

-- 3. voir les tables
SHOW TABLES;

-- 4. voir la structure d'une table
DESCRIBE users;

-- 5. lire le contenu
SELECT * FROM users;

-- 6. chercher des mots de passe
SELECT user, password FROM users;
```

---

## différences PostgreSQL vs MySQL

| action | MySQL | PostgreSQL |
|--------|-------|-----------|
| lister les bases | `SHOW DATABASES;` | `\l` |
| sélectionner une base | `USE nom;` | `\c nom` |
| lister les tables | `SHOW TABLES;` | `\dt` |
| décrire une table | `DESCRIBE table;` | `\d table` |
| quitter | `\q` ou `exit` | `\q` |