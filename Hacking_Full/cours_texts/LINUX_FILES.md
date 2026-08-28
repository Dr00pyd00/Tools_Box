# fichiers & dossiers importants Linux — cheat sheet hacking

---

## utilisateurs & authentification

| chemin | contenu | intérêt offensif |
|--------|---------|-----------------|
| `/etc/passwd` | liste de tous les utilisateurs, uid, gid, shell | énumération des users, trouver les comptes avec un vrai shell |
| `/etc/shadow` | mots de passe hashés — lisible seulement par root | récupérer les hashes pour crackage offline |
| `/etc/group` | liste des groupes et leurs membres | trouver qui est dans sudo, admin, docker... |
| `/etc/sudoers` | qui peut faire quoi avec sudo | trouver des chemins d'escalade de privilèges |
| `/etc/sudoers.d/` | configs sudo supplémentaires | idem |

---

## dossiers personnels

| chemin | contenu | intérêt offensif |
|--------|---------|-----------------|
| `/root/` | home de root | clés SSH, scripts, notes d'admin, historique |
| `/home/<user>/` | home de chaque utilisateur | fichiers perso, clés SSH, configs, historique |
| `/home/<user>/.ssh/` | clés SSH de l'utilisateur | `id_rsa` = clé privée SSH — accès direct à d'autres machines |
| `/home/<user>/.bash_history` | historique des commandes | mots de passe tapés en clair, commandes révélatrices |
| `/home/<user>/.bashrc` | config bash | alias, variables d'environnement avec credentials |

---

## configuration système

| chemin | contenu | intérêt offensif |
|--------|---------|-----------------|
| `/etc/hosts` | résolution DNS locale | cartographie réseau interne |
| `/etc/hostname` | nom de la machine | identification |
| `/etc/os-release` | version de l'OS | chercher des CVE adaptés |
| `/etc/crontab` | tâches planifiées système | escalade de privilèges via cron mal configuré |
| `/etc/cron.d/` | crons supplémentaires | idem |
| `/var/spool/cron/crontabs/` | crons par utilisateur | idem |

---

## réseau

| chemin | contenu | intérêt offensif |
|--------|---------|-----------------|
| `/etc/network/interfaces` | config réseau | cartographie, autres interfaces |
| `/etc/resolv.conf` | serveurs DNS configurés | infrastructure DNS interne |
| `/etc/hosts.allow` | connexions autorisées (TCP wrappers) | comprendre les restrictions réseau |
| `/etc/hosts.deny` | connexions refusées | idem |
| `/proc/net/tcp` | connexions TCP actives | voir les connexions en cours |

---

## services & applications

| chemin | contenu | intérêt offensif |
|--------|---------|-----------------|
| `/etc/ssh/sshd_config` | config SSH | `PermitRootLogin`, auth par clé/password |
| `/etc/apache2/` | config Apache | virtual hosts, répertoires exposés |
| `/etc/nginx/` | config Nginx | idem |
| `/etc/mysql/` | config MySQL | credentials, accès réseau |
| `/var/www/html/` | racine web Apache | fichiers sources, configs avec credentials |
| `/var/www/` | racine web générale | idem |

---

## logs — traces & informations

| chemin | contenu | intérêt offensif |
|--------|---------|-----------------|
| `/var/log/auth.log` | tentatives d'authentification | voir les connexions SSH, sudo, su |
| `/var/log/syslog` | logs système généraux | activité de la machine |
| `/var/log/apache2/access.log` | requêtes HTTP Apache | historique des accès web |
| `/var/log/apache2/error.log` | erreurs Apache | infos sur l'appli web |
| `/var/log/mysql/` | logs MySQL | requêtes, erreurs |

---

## fichiers sensibles courants

| chemin | contenu | intérêt offensif |
|--------|---------|-----------------|
| `/root/.ssh/id_rsa` | clé privée SSH de root | connexion SSH directe sans mot de passe |
| `/root/.ssh/authorized_keys` | clés autorisées à se connecter en root | ajouter sa propre clé pour persistance |
| `~/.ssh/known_hosts` | machines connues via SSH | cartographie du réseau interne |
| `/tmp/` | fichiers temporaires | souvent writable par tous — utile pour déposer des fichiers |
| `/var/tmp/` | idem mais persistant | idem |
| `/.env` ou `.env` | variables d'environnement appli | credentials base de données, API keys |
| `wp-config.php` | config WordPress | credentials MySQL en clair |
| `config.php` | config applis PHP génériques | credentials en clair |

---

## escalade de privilèges — fichiers clés

| chemin / commande | pourquoi |
|-------------------|---------|
| `find / -perm -4000 2>/dev/null` | fichiers SUID — s'exécutent en tant que owner (souvent root) |
| `find / -writable 2>/dev/null` | fichiers modifiables par l'utilisateur courant |
| `/etc/passwd` writable | si writable, on peut ajouter un user root directement |
| `/etc/crontab` writable | remplacer un script exécuté par root |
| `sudo -l` | lister ce que l'utilisateur peut faire en sudo |

---

## commandes utiles en post-exploitation

```bash
whoami                          # qui suis-je ?
id                              # uid, gid, groupes
uname -a                        # version kernel — chercher CVE
cat /etc/os-release             # version OS
cat /etc/passwd | grep "/bin/bash"   # users avec un vrai shell
cat /etc/shadow                 # hashes des mots de passe (root requis)
ls -la /root/                   # contenu du home root
ls -la /home/                   # tous les homes
find / -name "*.env" 2>/dev/null     # chercher des .env
find / -name "config.php" 2>/dev/null # chercher des configs
sudo -l                         # droits sudo de l'utilisateur courant
crontab -l                      # crons de l'utilisateur courant
cat /etc/crontab                # crons système
```