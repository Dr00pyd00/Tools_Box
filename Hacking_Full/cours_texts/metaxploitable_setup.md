# MetaXploitable

C'est une VM expres faiblement securisé pour s'entrainer.  
Il faut pas creer une machine virtuelle mais juste l'installer.  

### pour la mettre en SSH

Disons qu'on prend Kali en tant que Client et on veut MetaX comme server:  

Ici on met 2 flags:
- `-o`: __overidde_config__ = on modifie le comportement a la volé 

```bash
# ssh -o OPTION=VALEUR
└─$ ssh -o HostKeyAlgorithms=+ssh-rsa -o PubkeyAcceptedAlgorithms=+ssh-rsa msfadmin@192.168.78.129

```

- `HostKeyAlgorithms=+ssh-rsa` : autorise ssh-rsa meme si normalement interdit,
  le "+" dit qu'on ajoute ca a la config de base. 


