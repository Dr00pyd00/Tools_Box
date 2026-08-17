
# Postgresql


### Installation

```bash
sudo apt update
sudo apt install postgresql
```

Voir la version:
```bash 
psql --version
psql (PostgreSQL) 18.4 (Ubuntu 18.4-0ubuntu0.26.04.1)
```

Le daemon est : `postgresql@18-main`   ( le 18 est la version )     
Donc pour voir :
```bash 
sudo systemctl status postgresql@18-main
```

---

- **`psql`** : le client, installé, que tu vas utiliser pour te connecter et taper du SQL
- **`postgres`** (le daemon, `Main PID: 30470`) : le serveur, qui tourne déjà en arrière-plan via `systemd`, prêt à recevoir des connexions


### Lancement 

- Par defaut si on lance juste "psql", le server prend le nom de l'user courant.
- Automatiquement psql creer un user => `postgres` 


Donc pour commencer on utilise l'user special de posgresql: 

```bash 
sudo -u postgres psql 
```

- `sudo -u` = juste une commande linux qui change l'user pour cette ligne de commande only.
- `postgres` = le user special de base 


#### aparte claude gestion users:

```bash
kida@MSI:~/test_dock$ sudo -u postgres psql
[sudo: authenticate] Password:
psql (18.4 (Ubuntu 18.4-0ubuntu0.26.04.1))
Type "help" for help.

postgres=# \du
                             List of roles
 Role name |                         Attributes
-----------+------------------------------------------------------------
 postgres  | Superuser, Create role, Create DB, Replication, Bypass RLS
 ```

Exactement ce qu'on attendait : un seul rôle, `postgres`, avec tous les attributs maximaux (`Superuser`, `Create role`, `Create DB`, `Replication`, `Bypass RLS`).

**Petit décryptage de ces attributs**

- `Superuser` : contourne toutes les vérifications de permissions — équivalent de `root` mais à l'intérieur de PostgreSQL
- `Create role` : peut créer/supprimer d'autres rôles
- `Create DB` : peut créer/supprimer des bases de données
- `Replication` : peut être utilisé pour la réplication (copier les données vers un autre serveur PostgreSQL — pas utile pour toi maintenant)
- `Bypass RLS` : *Row Level Security* → contourne les restrictions de sécurité au niveau ligne (une fonctionnalité avancée de PostgreSQL, pas à connaître maintenant)

**Créons maintenant un rôle à ton nom**

Toujours dans le prompt `postgres=#`, tape ceci (c'est du **vrai SQL**, pas une commande `psql` cette fois — remarque : pas de `\`, et ça se termine par `;`) :

```sql
CREATE ROLE kida WITH LOGIN PASSWORD 'ton_mot_de_passe' CREATEDB;
```

- `CREATE ROLE kida` : crée un nouveau rôle nommé `kida`
- `WITH LOGIN` : autorise ce rôle à se **connecter** (par défaut, un rôle créé sans ça ne peut pas se connecter — utile pour des rôles "groupe" sans connexion directe)
- `PASSWORD 'ton_mot_de_passe'` : définit un mot de passe (choisis-en un simple pour l'instant, c'est local et pour apprendre)
- `CREATEDB` : donne à ce rôle le droit de créer ses propres bases de données
- `;` : le point-virgule termine une instruction SQL — **indispensable**, sans lui `psql` attend que tu continues à taper

Remplace `'ton_mot_de_passe'` par un mot de passe de ton choix, exécute, puis refais `\du` pour voir les deux rôles côte à côte.


## Premiere connexion


```bash 
psql -U kida -d postgres -h localhost  # force auth 

# plus simple si user existe sur la machine:
psql -d postgres

```

- `-U` = se connecter avec tel user
- `-d` = choisir sa db : "postgres" est la db creer par defaut 



### Creer un DB perso 

```bash
postgres=> CREATE DATABASE testdb;

# ensuite il faut se connecter a la db creer !
postgres=> \c testdb 
```


