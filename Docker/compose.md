
# Docker Compose 


Construction de containers groupes grace a `docker-compose`.    

> Il faut un file **docker-compose.yml** 
Se sert du dossier courant pour tout ( nommage etc ) 

### Le file 

En `yaml` : le identations comptes 

Ultra basic:
```yaml
services:                       # 1er identation : les differents services donc containers qu'on veut
    mon_redis:                  # 2eme : nom du container 
        image: redis:latest     # 3eme : image a utiliser 

```



### Gestion

#### Lancement 

Va chercher dans le dir le file `docker-compose.yml` et l'execute donc creer les choses.
```bash 
docker compose up ( -d )  # on peut detacher
```


#### Arreter 

```bash 
docker compose stop
```

#### Relancer 

```bash 
docker compose start 
```

#### Arreter ET supprimer 

```bash 
docker compose down ( -v ) 
```

- `-v` = ATTENTION si on met ca supprime aussi les volumes !!!

# Commandes 


**Cycle de vie principal**

```bash
docker compose up              # build (si besoin) + crée + démarre tous les services, reste attaché (logs en direct)
docker compose up -d           # pareil, mais en arrière-plan (detached), rend la main direct
docker compose up -d --build   # force la RECONSTRUCTION de l'image avant de démarrer (utile après avoir modifié Dockerfile/code)
```

**Arrêter / relancer sans supprimer**

```bash
docker compose stop            # arrête les containers, mais les GARDE (comme docker stop)
docker compose start           # relance des containers déjà existants, arrêtés (pas de -d possible, inutile ici)
```

**Supprimer complètement**

```bash
docker compose down            # arrête ET supprime les containers + le réseau créé (mais PAS les volumes)
docker compose down -v         # pareil + supprime aussi les volumes (utile si tu changes des identifiants Postgres par ex.)
```

**Inspecter l'état**

```bash
docker compose ps              # liste les containers du projet courant, avec leur statut (Up, Exited, healthy...)
```

**Exécuter une commande dans un container déjà en cours**

```bash
docker compose exec <service> <commande>   # ex: docker compose exec app python3 py/main.py gerard
```

**Point commun important à tous ces éléments**

Toutes ces commandes lisent le `docker-compose.yml` du **dossier courant** — donc il faut être dans le bon dossier (pas besoin de connaître un nom de container généré comme `exemple-app-1`, Compose s'en charge via le nom du **service**, genre `app` ou `db`).





