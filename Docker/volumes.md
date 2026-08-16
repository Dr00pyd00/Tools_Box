# Les volumes 

Sert a stocker en dehors du container les data.


### Creation
```bash 
# creation du volume: 
docker volume create redis-data

# checker le path par exemple:
docker volume inspect redis-data

```


### Lier avec container 
```bash 
docker run --name test-vol -v redis-data:/data -d redis:latest 
```

- `-v` = volume, attribuer un espace /volume
- `redis-data:/data` = endroit sur la machine:endroit dans le container


Donc ensuite on peut delete le container et rebrancher le volume a un nouveau container !



