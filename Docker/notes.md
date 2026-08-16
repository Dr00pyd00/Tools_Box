
# Docker

- `Image` = modele figee, la recette de cuisine ( classe )
- `Conteneur` = instance en cours d'execution, on peut en faire plusieurs. ( instance(s) ) 

> Les images sont telecharger via de registres ( DockerHub )

Voir si installer:
```bash 
docker --version
Docker version 29.1.3, build 29.1.3-0ubuntu4.1
```

- `dockerd` = daemon backend qui tourne en permanence
- `docker` = le CLI

### Voir les Images 
```bash 
docker images 
```

### Telecharger une image
```bash 
# exemple
docker pull redis 
```

### Voir les conteneurs qui tournent 
```bash 
docker ps

# ajouter -a : all = voir meme ceux qui sont stop
```

# Lancer a la main

Lancer en ligne de commande.   

```bash 
docker run --name redis-test -d -p 6380:6379 redis:latest
```

- `-d` = detach 

- `-p 6380:6379` : le conteneur est invisible pour l'hote, la on precise que quand on se connecte 
au port 6380 en fait ca appel docker qui va lier le tout au port du conteneur 6379.

### Checker les log si detacher:
```bash 
docker logs <nom-conteneur>

# ajouter flag -f : follow affiche les logs en continu
```

### Arreter un conteneur:
Il s'arrete mais n'est pas supprimer.

```bash 
docker stop <nom-conteneur>
```


### Supprimer un conteneur:
Un conteneur doit etre arreter pour etre supprimer.
```bash 
docker rm <nom-conteneur>
```


### Executer des trucs:

On peut executer sur un container en particulier .

```bash 
docker exec -it <nom-du-container> bash   # va lancer bash du container 

docker exec -it <nom-du-container> redis-cli GET name   # va lancer la commande du container 

```


# Network 

Voir tout les reseaux:
```bash 
docker network ls 
```













