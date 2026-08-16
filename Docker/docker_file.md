
# Dockerfile 

Sert a creer une image personaliser , c'est une recette de cuisine.  
Le file s'appelle `Dockerfile`.

### Exemple:

Ecrire de la recette:
```dockerfile
FROM ubuntu:latest
RUN apt update && apt install -y python3 curl
CMD ["bash"]
```

Lancer la creation avec la recette:
```bash 
docker build -t nom-image .
```

- `-t` = tag : donc nom de l'image

Cherche le `Dockerfile` dans le dossier courant.



