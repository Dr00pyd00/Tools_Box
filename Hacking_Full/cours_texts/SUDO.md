# SUDO — Guide complet Linux

> Élévation de privilèges sous Linux

---

## C'est quoi sudo ?

`sudo` = **S**uper **U**ser **DO** — exécute une commande avec les droits d'un autre utilisateur (root par défaut).

Sans sudo, un user lambda ne peut pas toucher aux fichiers système, installer des paquets, ou modifier la config du système. Sudo est le **pont contrôlé** vers les privilèges root.

```bash
whoami          # kottak
sudo whoami     # root
```

---

## Comment sudo est accordé

### Méthode 1 — Le groupe `sudo`

Sur Ubuntu, tout membre du groupe `sudo` a les droits sudo automatiquement.

```bash
# Voir les groupes d'un user
groups alice

# Ajouter alice au groupe sudo
sudo usermod -aG sudo alice

# Vérifier
groups alice   # doit afficher "sudo" dans la liste
```

### Méthode 2 — Le fichier `/etc/sudoers`

C'est le fichier de configuration central de sudo. **Ne jamais l'éditer directement** — toujours passer par `visudo` qui vérifie la syntaxe avant de sauvegarder.

```bash
sudo visudo
```

---

## Syntaxe de /etc/sudoers

```
user    HOST=(USER:GROUP)   COMMANDES
```

| Champ | Signification |
|---|---|
| `user` | L'utilisateur concerné (ou `%groupe` pour un groupe) |
| `HOST` | Sur quelle machine la règle s'applique (`ALL` = partout) |
| `(USER:GROUP)` | En tant que quel user/groupe exécuter |
| `COMMANDES` | Quelles commandes sont autorisées |

---

## Exemples de règles sudoers

```bash
# kottak peut tout faire avec sudo (avec mot de passe)
kottak  ALL=(ALL:ALL) ALL

# kottak peut tout faire SANS mot de passe
kottak  ALL=(ALL) NOPASSWD: ALL

# alice peut UNIQUEMENT redémarrer apache
alice   ALL=(ALL) /usr/bin/systemctl restart apache2

# bob ne peut PAS utiliser sudo du tout (blacklist)
bob     ALL=(ALL) !ALL

# Tous les membres du groupe sudo peuvent tout faire
%sudo   ALL=(ALL:ALL) ALL

# www-data peut lire les logs sans mot de passe
www-data ALL=(ALL) NOPASSWD: /usr/bin/tail /var/log/*.log
```

---

## Commandes essentielles

```bash
# Voir ce que TON user peut faire avec sudo
sudo -l

# Exécuter une commande en root
sudo commande

# Ouvrir un shell root
sudo su
sudo -i
sudo bash

# Exécuter en tant qu'un autre user (pas root)
sudo -u alice commande

# Exécuter en tant qu'un autre user interactif
sudo -u alice -i

# Garder les variables d'environnement
sudo -E commande

# Éditer sudoers en sécurité
sudo visudo
```

---

## sudo -l — La commande clé en pentest

`sudo -l` liste exactement ce que ton user peut faire avec sudo. C'est **toujours** la première chose à taper quand tu obtiens un shell.

```bash
$ sudo -l

User kottak may run the following commands on kottak:
    (ALL : ALL) ALL
```

### Interprétation des outputs

```bash
# Peut tout faire avec mot de passe
(ALL : ALL) ALL

# Peut tout faire SANS mot de passe → escalade triviale
(ALL) NOPASSWD: ALL

# Peut uniquement cette commande
(ALL) /usr/bin/systemctl restart apache2

# Rien du tout → pas de sudo
User alice is not allowed to run sudo on this machine.
```

---

## Escalade de privilèges via sudo

### Cas 1 — NOPASSWD: ALL (trivial)

```bash
sudo whoami    # root
sudo su        # shell root direct
```

### Cas 2 — sudo sur un éditeur de texte

Si tu peux `sudo vim`, `sudo nano`, `sudo less` → tu peux devenir root depuis l'éditeur.

```bash
sudo vim /etc/hosts

# Dans vim, tape :
:!/bin/bash
# Tu obtiens un shell root
```

### Cas 3 — sudo sur un langage de script

```bash
# Si sudo python3 est autorisé :
sudo python3 -c "import os; os.system('/bin/bash')"

# Si sudo perl est autorisé :
sudo perl -e 'exec "/bin/bash"'
```

### Cas 4 — sudo sur find

```bash
sudo find / -name "*.txt" -exec /bin/bash \;
# bash s'exécute en root via find
```

> 💡 Le site **GTFOBins** (gtfobins.github.io) liste toutes les binaires Unix qui permettent une escalade de privilèges selon les droits sudo accordés.

---

## Création d'utilisateurs et gestion sudo

```bash
# Créer un user avec home directory
sudo adduser alice
# adduser est interactif, demande mot de passe etc.

# Créer un user sans home (service)
sudo useradd -r -s /bin/false www-data

# Donner sudo à un user existant
sudo usermod -aG sudo alice

# Retirer sudo à un user
sudo deluser alice sudo

# Voir tous les membres du groupe sudo
getent group sudo

# Voir les groupes d'un user
id alice
groups alice
```

---

## Différence adduser vs useradd

| | `adduser` | `useradd` |
|---|---|---|
| Type | Script interactif (Debian/Ubuntu) | Commande bas niveau POSIX |
| Home | Créé automatiquement | Pas créé par défaut (ajouter `-m`) |
| Mot de passe | Demandé pendant la création | Pas de mot de passe par défaut |
| Usage | Usage humain courant | Scripts, automatisation |

```bash
# useradd avec options pour créer un vrai user
sudo useradd -m -s /bin/bash -G sudo alice
#            │   │             │
#            │   │             └── ajouter au groupe sudo
#            │   └── shell par défaut
#            └── créer le home directory
```

---

## Vérifications utiles en pentest

```bash
# Qui suis-je et quels sont mes groupes
whoami
id

# Est-ce que j'ai sudo et pour quoi
sudo -l

# Qui a sudo sur cette machine
cat /etc/sudoers
getent group sudo

# Tous les users du système
cat /etc/passwd | cut -d: -f1

# Users avec un shell (users réels, pas services)
cat /etc/passwd | grep -v "nologin\|false" | cut -d: -f1

# Est-ce que je suis déjà root
[ $(id -u) -eq 0 ] && echo "ROOT" || echo "pas root"
```

---

## Récapitulatif — niveaux de privilèges

| Situation | Ce que tu peux faire |
|---|---|
| User sans sudo | Uniquement ses propres fichiers |
| User avec sudo (avec mdp) | Root si tu connais le mot de passe |
| User avec NOPASSWD sudo | Root instantanément |
| User avec sudo partiel | Escalade possible selon la commande (GTFOBins) |
| Déjà root | Tout |