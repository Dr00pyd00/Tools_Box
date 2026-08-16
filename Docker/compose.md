
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




    
