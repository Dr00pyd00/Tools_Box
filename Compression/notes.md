
# Compression Linux 

## Compresser:

```bash 
tar  -czf   MonDossier.tar.gz    MonDossier 
```

- `tar` = outil d'archivage 
- `-c` = create 
- `-z` = utiliser gzip
- `-f` = file : donner le nom du fichier 

### Verifier contenu: 

```bash 
tar  -tzf  MonDossier.tar.gz 
```

- `-t` = list 

#### Exemple reel: 

```bash 
tar --exclude='.venv' \
    --exclude='__pycache__' \
    --exclude='.git' \
    --exclude='.env' \
    --exclude='*.pyc' \
    -czf mon-fastapi.tar.gz mon-fastapi/

``` 

> TOUJOURS mettre els excludes au debut !!

## Decompresser:

Dans dossier courant: 

```bash 
tar -xzf mon-fastapi.tar.gz
```

- `-x` = extract

Dans un dossier precis:

```bash
tar -xzf mon-fastapi.tar.gz -C ici 
```

- `-C` = change dir 


