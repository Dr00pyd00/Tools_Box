

# SMB / Samba

- `SMB` **__Server_Message_Block__** = protocole de partage de fichiers en reseau
- `Samba` = application qui tourne pour recevoir les demande (avec le protocole)

### smbclient 

Outils pour faire les appels.

```bash
smbclient -L 192.168.78.129 -N

```
- `-L`: liste des partage disponible par la machine. Ce que le serveur samba
  expose.
-`-N`: filtre les elements qui ne demande pas de mdp.

### Config samba

```bash
/etc/samba

# smb.conf => configuration de ce que l'on veut exposer
```

### Mettre en partage un dossier via samba

Il faut aller dans **/etc/samba/smb.conf** et ajouter un block.


```
[nom_du_partage]
   path = /chemin/vers/dossier
   browseable = yes
   guest ok = yes
   read only = no
```

- `[nom_du_partage]` — le nom qui apparaît dans `smbclient -L`
- `path` — le vrai chemin sur le disque
- `browseable` — visible dans la liste ou non
- `guest ok` — accessible sans mot de passe
- `read only` — lecture seule ou écriture autorisée  


> par convention on met dans `/etc/samba/mon_dossier_partage`  
Il faut penser a chmod pour laisser les droits!


--- 

Les essentielles :

**Reconnaissance**
```bash
smbclient -L //IP -N          # lister les partages
enum4linux IP                  # énumération complète
```

**Connexion**
```bash
smbclient //IP/partage -N      # connexion anonyme
smbclient //IP/partage -U user # connexion avec user (demande mdp)
smbclient //IP/partage -U user%password  # connexion avec mdp direct
```

**Dans le shell SMB**
```
ls                  # lister les fichiers
cd dossier          # naviguer
get fichier         # télécharger un fichier
put fichier         # envoyer un fichier
more fichier        # lire un fichier
mkdir dossier       # créer un dossier
del fichier         # supprimer
lcd                 # voir où on est sur notre machine locale
help                # liste toutes les commandes
exit                # quitter
```


# smb.conf

Il y a deux blocks: 
- Global 
- Groupe de blocks pour chaque dossier/ objet partager




## Structure générale de `smb.conf`

Le fichier est divisé en **deux grandes parties** :

```
[global]        ← comportement général du serveur Samba
[nom_du_share]  ← définition de chaque dossier partagé
```

C'est exactement comme une config FastAPI : les settings globaux d'un côté, les routes/ressources de l'autre.

---

## Le bloc `[global]` — ce qui compte vraiment pour toi

Je vais ignorer tout ce qui est commenté (`;` ou `#`), parce que c'est juste de la doc inactive. Ce qui est **actif** dans ton `[global]` :

**Identification**
```ini
workgroup = WORKGROUP
server string = %h server (Samba, Ubuntu)
```
`workgroup` = le nom du groupe réseau Windows. `WORKGROUP` est la valeur par défaut, tu n'as pas besoin d'y toucher. `%h` est une variable Samba qui sera remplacée automatiquement par le hostname de ta machine.

**Logs**
```ini
log file = /var/log/samba/log.%m
max log size = 1000
logging = file
```
Un fichier de log par machine qui se connecte. `%m` = nom de la machine cliente. `1000` = taille max en kilo-octets (KiB).

**Authentification — la partie importante**
```ini
server role = standalone server
map to guest = bad user
usershare allow guests = yes
```

- `standalone server` : ton Samba fonctionne seul, pas dans un domaine Active Directory. C'est ce que tu veux pour un lab.
- `map to guest = bad user` : **si quelqu'un se connecte avec un utilisateur qui n'existe pas**, Samba le traite comme un invité anonyme. C'est ce qui va permettre à Metasploitable de se connecter sans mot de passe.
- `usershare allow guests = yes` : les shares créés avec `net usershare` peuvent être publics.

Les lignes `unix password sync`, `passwd program`, `pam password change` concernent la synchronisation des mots de passe Unix/Samba — tu peux les ignorer pour l'instant, elles ne bloquent rien.

---

## Ce que tu dois ajouter

Pour ton share `truc_a_partager`, tu ajoutes un bloc **en dessous** du `[global]`, après les blocs `[printers]` et `[print$]` :

```ini
[truc_a_partager]
   comment = Mon partage de test
   path = /home/kottak/truc_a_partager
   browseable = yes
   read only = no
   guest ok = yes
   create mask = 0755
   directory mask = 0755
```

**Explication ligne par ligne :**

| Ligne | Ce que ça fait |
|---|---|
| `[truc_a_partager]` | Le nom du share — c'est ce qui apparaît sur le réseau |
| `comment` | Description lisible par les clients |
| `path` | Le chemin **absolu** sur ton système vers le dossier à partager |
| `browseable = yes` | Le share est visible dans la liste des partages |
| `read only = no` | On peut écrire dedans (pas juste lire) |
| `guest ok = yes` | Pas besoin de mot de passe pour se connecter |
| `create mask = 0755` | Permissions des **fichiers** créés via Samba |
| `directory mask = 0755` | Permissions des **dossiers** créés via Samba |

---

## Avant de redémarrer Samba

Deux étapes importantes :

**1. Vérifier la syntaxe** — la commande magique que le fichier lui-même te conseille :
```bash
testparm
```
`testparm` = **test parameters** — il lit ton `smb.conf` et te dit s'il y a des erreurs. Aucune sortie d'erreur = tu es bon.

**2. S'assurer que le dossier existe vraiment** sur le système avec les bonnes permissions Unix :
```bash
ls -la /home/kottak/truc_a_partager
```

Si le dossier n'existe pas ou appartient à `root`, Samba ne pourra pas y accéder même avec une config parfaite — c'était probablement le problème la dernière fois.




# SAMBA — Guide de configuration

> Partage de dossiers sous Linux via le protocole SMB

---

## C'est quoi Samba ?

Samba est un service Linux qui permet de partager des dossiers sur un réseau en utilisant le protocole **SMB** (Server Message Block) — le même protocole utilisé par Windows.

Il fonctionne en deux parties :
- `smb.conf` — le fichier de configuration
- `smbd` — le service qui tourne en arrière-plan

> ⚠️ Toute modification de `smb.conf` nécessite un redémarrage : `sudo systemctl restart smbd`

---

## Structure de smb.conf

```ini
[global]           # paramètres qui s'appliquent à TOUT le serveur
   ...

[nom_du_share]     # définit UN dossier partagé
   path = /chemin/vers/le/dossier
   ...
```

---

## CAS 01 — Dossier public (accessible par tout le monde)

Tout utilisateur du réseau peut voir et écrire dans ce dossier, **sans mot de passe**.

### Étape 1 — Créer le dossier

```bash
mkdir -p ~/shares/public
chmod 777 ~/shares/public
# 777 = tout le monde peut lire, écrire, traverser
# nécessaire car Samba utilise le compte 'nobody' pour les guests
```

### Étape 2 — Configuration smb.conf

```ini
[global]
   map to guest = bad user    # connecte les anonymes en tant que guest
   guest account = nobody     # le compte Unix utilisé pour les guests

[public]
   path = /home/tonuser/shares/public
   browseable = yes           # visible dans smbclient -L
   read only = no             # lecture ET écriture autorisées
   guest ok = yes             # les guests peuvent entrer
   create mask = 0664         # permissions des fichiers créés
   directory mask = 0775      # permissions des dossiers créés
```

### Étape 3 — Redémarrer

```bash
sudo systemctl restart smbd
```

### Étape 4 — Tester depuis Kali

```bash
smbclient -L <IP_CIBLE> -N            # lister les shares disponibles
smbclient //<IP_CIBLE>/public -N      # se connecter sans mot de passe
smb: \> ls                            # lister le contenu
smb: \> put fichier.txt               # uploader un fichier
smb: \> get fichier.txt               # télécharger un fichier
```

### Explication des paramètres

| Paramètre | Valeur | Explication |
|---|---|---|
| `map to guest` | `bad user` | Redirige les connexions anonymes vers le compte guest |
| `guest account` | `nobody` | Compte Unix utilisé pour les accès anonymes |
| `guest ok` | `yes` | Ce share accepte les guests |
| `read only` | `no` | Écriture autorisée |
| `browseable` | `yes` | Share visible dans les listings réseau |
| `create mask` | `0664` | Permissions appliquées aux fichiers uploadés |
| `directory mask` | `0775` | Permissions appliquées aux dossiers créés |

> ⚠️ **`chmod 777` indispensable** : Samba accède au dossier avec le compte `nobody` pour les connexions anonymes. Si le dossier n'est pas en 777, `nobody` ne peut pas lire ou écrire dedans — même si `guest ok = yes`.
> Pour vérifier : `ls -ld ~/shares/public` → doit afficher `drwxrwxrwx`

---

## CAS 02 — Dossier privé (un utilisateur précis)

Seul un utilisateur authentifié avec son mot de passe peut accéder à ce dossier. **Aucun accès anonyme.**

### Étape 1 — Créer l'utilisateur Samba

> Samba a sa propre base de mots de passe, **séparée** de celle d'Ubuntu. L'utilisateur doit d'abord exister en tant que compte Linux, puis être enregistré dans Samba.

```bash
# S'il n'existe pas encore sur Linux :
sudo useradd -m -s /bin/bash alice

# L'enregistrer dans Samba et définir son mot de passe Samba :
sudo smbpasswd -a alice
# Samba demande de saisir un mot de passe deux fois

# Activer le compte s'il était désactivé :
sudo smbpasswd -e alice

# Voir les utilisateurs Samba enregistrés :
sudo pdbedit -L
```

> ℹ️ **Deux mots de passe distincts** : Linux et Samba ont des bases séparées. `smbpasswd -a alice` définit le mot de passe **Samba** uniquement — pas celui du login Linux. Si tu changes le mot de passe Linux d'alice, ça ne change pas son mot de passe Samba.

### Étape 2 — Créer le dossier

```bash
mkdir -p ~/shares/prive
sudo chown alice:alice ~/shares/prive   # alice devient propriétaire
chmod 750 ~/shares/prive
# 750 = owner: rwx | group: r-x | others: ---
```

### Étape 3 — Configuration smb.conf

```ini
[global]
   # Pas de map to guest = bad user ici
   # Les anonymes seront refusés par défaut

[prive]
   path = /home/alice/shares/prive
   browseable = yes
   read only = no
   guest ok = no              # guests refusés
   valid users = alice        # SEUL alice peut entrer
   create mask = 0640
   directory mask = 0750
```

### Étape 4 — Redémarrer et tester

```bash
sudo systemctl restart smbd

# Connexion avec mot de passe depuis Kali :
smbclient //<IP_CIBLE>/prive -U alice
# Samba demande le mot de passe Samba d'alice
```

### Plusieurs utilisateurs autorisés

```ini
valid users = alice bob        # alice ET bob peuvent accéder
valid users = @mon_groupe      # tous les membres du groupe Linux 'mon_groupe'
```

```bash
# Créer un groupe et y ajouter un utilisateur :
sudo groupadd mon_groupe
sudo usermod -aG mon_groupe alice
```

---

## CAS 03 — Tout bloquer (zéro accès)

Aucun accès anonyme sur tout le serveur. Les shares ne sont pas visibles sans authentification.

### Configuration smb.conf

```ini
[global]
   map to guest = never        # connexions anonymes REFUSÉES
   restrict anonymous = 2      # bloque même la liste des shares sans auth

[prive]
   path = /home/kottak/shares/prive
   browseable = no             # invisible dans smbclient -L
   read only = yes             # lecture seule
   guest ok = no               # guests refusés
   valid users = kottak        # seul kottak peut entrer
```

### Permissions dossier

```bash
chmod 700 ~/shares/prive
# 700 = owner: rwx | group: --- | others: ---
# Seul le propriétaire peut accéder. Personne d'autre.
```

### Vérifier que c'est bien bloqué

```bash
smbclient -L <IP_CIBLE> -N
# Résultat attendu : NT_STATUS_ACCESS_DENIED
# ou : session setup failed: NT_STATUS_LOGON_FAILURE

# La connexion avec le bon user doit fonctionner :
smbclient //<IP_CIBLE>/prive -U kottak
```

### Explication des paramètres

| Paramètre | Valeur | Explication |
|---|---|---|
| `map to guest` | `never` | Refuse toutes les connexions sans authentification |
| `restrict anonymous` | `2` | Bloque même la liste des shares pour les anonymes |
| `browseable` | `no` | Le share n'apparaît pas dans `smbclient -L` |
| `read only` | `yes` | Écriture impossible |
| `guest ok` | `no` | Les guests sont refusés |
| `valid users` | `kottak` | Seul cet utilisateur est autorisé |

---

## Récapitulatif des trois cas

| Paramètre | CAS 01 Public | CAS 02 User précis | CAS 03 Tout bloqué |
|---|---|---|---|
| `map to guest` | `bad user` | absent | `never` |
| `guest account` | `nobody` | absent | absent |
| `guest ok` | `yes` | `no` | `no` |
| `read only` | `no` | `no` | `yes` |
| `browseable` | `yes` | `yes` | `no` |
| `valid users` | absent | `alice` | `kottak` |
| `restrict anonymous` | absent | absent | `2` |
| `chmod dossier` | `777` | `750` | `700` |

---

## Commandes utiles

```bash
# Vérifier la config sans redémarrer
testparm

# Redémarrer le service
sudo systemctl restart smbd

# Voir les utilisateurs Samba enregistrés
sudo pdbedit -L

# Ajouter un utilisateur Samba
sudo smbpasswd -a alice

# Activer un compte Samba désactivé
sudo smbpasswd -e alice

# Changer le mot de passe Samba d'un user
sudo smbpasswd alice

# Supprimer un utilisateur Samba
sudo smbpasswd -x alice

# Voir les connexions actives
sudo smbstatus

# Lister les shares disponibles depuis Kali (anonyme)
smbclient -L <IP> -N

# Se connecter à un share avec un user
smbclient //<IP>/nom_share -U alice

# Vérifier les permissions d'un dossier
ls -ld ~/shares/mondossier
```