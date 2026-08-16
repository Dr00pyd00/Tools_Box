
# Creation d'un mini ubuntu



## Creer container 

```bash 
docker run --name myubu -it ubuntu:latest
```

Ne pas oublier `-it`  sinon pas possibilite de console.   

=> Ducoup ca ouvre direct la console a la creation puis apres "exit" : 

```bash 
docker start -i myubu 
```

