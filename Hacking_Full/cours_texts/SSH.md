# ssh — cheat sheet

> **Secure Shell** — connexion sécurisée et chiffrée à une machine distante.

---

## connexion de base

```bash
ssh user@IP                        # connexion standard
ssh user@IP -p 2222                # port non standard
ssh -i ~/.ssh/id_rsa user@IP       # avec une clé privée spécifique
ssh -v user@IP                     # verbose — debug la connexion
ssh -X user@IP                     # forwarding X11 — interface graphique distante
```

---

## clés SSH

### générer une paire de clés

```bash
ssh-keygen                                    # génère id_rsa (défaut)
ssh-keygen -t ed25519                         # algo moderne recommandé
ssh-keygen -t rsa -b 4096                     # RSA 4096 bits
ssh-keygen -t ed25519 -C "mon@email.com"      # avec commentaire
ssh-keygen -f ~/.ssh/ma_cle                   # nom de fichier personnalisé
```

Génère deux fichiers :
- `~/.ssh/id_rsa` — clé **privée** — ne jamais partager
- `~/.ssh/id_rsa.pub` — clé **publique** — à déposer sur les serveurs

### déposer sa clé publique sur un serveur

```bash
ssh-copy-id user@IP                           # copie automatique
ssh-copy-id -i ~/.ssh/id_rsa.pub user@IP      # clé spécifique
```

Ajoute la clé dans `~/.ssh/authorized_keys` sur le serveur.

### manuellement

```bash
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
```

---

## fichiers importants

| fichier | rôle |
|---------|------|
| `~/.ssh/id_rsa` | clé privée — ne jamais partager |
| `~/.ssh/id_rsa.pub` | clé publique — à déposer sur les serveurs |
| `~/.ssh/authorized_keys` | clés autorisées à se connecter sur cette machine |
| `~/.ssh/known_hosts` | machines déjà connues — empreintes des serveurs |
| `~/.ssh/config` | config SSH par hôte |
| `/etc/ssh/sshd_config` | config du serveur SSH |

---

## config SSH par hôte (~/.ssh/config)

Évite de retaper les options à chaque fois :

```
Host monserveur
    HostName 192.168.1.10
    User kottak
    Port 2222
    IdentityFile ~/.ssh/id_rsa

Host github.com
    User git
    IdentityFile ~/.ssh/id_github
```

Utilisation :
```bash
ssh monserveur    # au lieu de ssh -p 2222 -i ~/.ssh/id_rsa kottak@192.168.1.10
```

---

## sécurisation du serveur SSH (/etc/ssh/sshd_config)

```ini
PermitRootLogin no              # interdire la connexion root directe
PasswordAuthentication no       # désactiver les mots de passe — clés uniquement
PubkeyAuthentication yes        # autoriser les clés
Port 2222                       # changer le port par défaut (obscurité)
MaxAuthTries 3                  # limiter les tentatives
AllowUsers kottak               # autoriser seulement certains users
LoginGraceTime 30               # timeout de connexion en secondes
```

Après modification :
```bash
sudo systemctl restart ssh
```

---

## transfert de fichiers

```bash
# copier un fichier local vers serveur
scp fichier.txt user@IP:/home/user/

# copier un fichier du serveur vers local
scp user@IP:/home/user/fichier.txt .

# copier un dossier entier
scp -r dossier/ user@IP:/home/user/

# avec rsync — plus efficace pour les gros transferts
rsync -avz dossier/ user@IP:/home/user/
```

---

## tunnels SSH

```bash
# tunnel local — accéder à un service distant via un port local
ssh -L 8080:localhost:80 user@IP
# → http://localhost:8080 accède au port 80 du serveur distant

# tunnel inverse — exposer un service local vers l'extérieur
ssh -R 9090:localhost:3000 user@IP
# → port 9090 du serveur distant accède à ton port 3000 local

# tunnel SOCKS — proxy pour tout le trafic
ssh -D 1080 user@IP
# → configure ton navigateur sur SOCKS5 localhost:1080
```

---

## commandes utiles

```bash
# vérifier si une clé est dans known_hosts
ssh-keygen -F 192.168.1.10

# supprimer une entrée de known_hosts (machine reinstallée)
ssh-keygen -R 192.168.1.10

# voir l'empreinte d'une clé publique
ssh-keygen -lf ~/.ssh/id_rsa.pub

# tester la connexion sans exécuter de commande
ssh -T git@github.com

# exécuter une commande distante sans shell interactif
ssh user@IP "ls /home"
ssh user@IP "cat /etc/passwd"
```

---

## intérêt offensif (pentest)

```bash
# brute force SSH avec hydra
hydra -l root -P rockyou.txt ssh://192.168.1.10

# si clé privée trouvée sur la cible
chmod 600 id_rsa_volée
ssh -i id_rsa_volée root@192.168.1.10

# voir les machines connues de la cible (mouvement latéral)
cat /home/user/.ssh/known_hosts
cat /root/.ssh/known_hosts

# voir qui peut se connecter sans mot de passe
cat /home/user/.ssh/authorized_keys
cat /root/.ssh/authorized_keys

# ajouter sa propre clé pour persistance (si accès root)
echo "ma_clé_publique" >> /root/.ssh/authorized_keys
```

---

## algorithmes — du plus ancien au plus sécurisé

| algo | flag | statut |
|------|------|--------|
| DSA | `-t dsa` | obsolète — ne plus utiliser |
| RSA 1024 | `-t rsa -b 1024` | faible — ne plus utiliser |
| RSA 2048 | `-t rsa -b 2048` | acceptable |
| RSA 4096 | `-t rsa -b 4096` | bien |
| ECDSA | `-t ecdsa` | bien |
| Ed25519 | `-t ed25519` | recommandé — rapide et sécurisé |