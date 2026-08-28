
# Creation + gestion de clés SSh

### Generer une clé en specifiant son utilité

```bash
ssh-keygen -t ed25519 -C "maKeyMachin" -f ~/.ssh/id_ed25519_github
```
- `-t` -> type algo
- `-C` -> commentaire (nom ou mail par exemple)
- `-f` -> file: nom du fichier de la clé



### Config de SSH

> ATTENTION: ce fichierest obligatoire sinon shh ne saura pas quelle clé utiliser pour tel ou tel app!

Dans ~/.ssh/config:

```bash

# Host: nom du server auquelle la regle s'applique
# HostName: addresse reelle du server (souvent la meme que host)
# User: utilisateur SSH github -> toujours "git"
# IdentityFile: chemin vers la clé privée

Host github.com 
        HostName github.com
        User git 
        IdentityFile ~/.ssh/id_ed25519_github
```


