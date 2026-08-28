# Variables Linux — commandes de base

---

## Deux types de variables

**Variables locales** — existent uniquement dans le terminal courant.
**Variables d'environnement** — héritées par tous les programmes lancés depuis ce terminal.

---

## Créer et lire une variable

```bash
# Créer une variable locale
MA_VAR="bonjour"

# Lire une variable — toujours avec $ devant
echo $MA_VAR         # affiche : bonjour
echo ${MA_VAR}       # idem, syntaxe plus explicite

# Transformer en variable d'environnement
export MA_VAR="bonjour"
```

---

## Variables d'environnement importantes

```bash
echo $HOME        # ton dossier home — /home/cyanure
echo $USER        # ton username — cyanure
echo $SHELL       # ton shell — /bin/zsh ou /bin/bash
echo $PATH        # liste des dossiers où Linux cherche les programmes
echo $PWD         # dossier courant (même que pwd)
echo $HISTFILE    # fichier historique des commandes
echo $HISTSIZE    # nombre de commandes gardées en mémoire
```

---

## Afficher toutes les variables d'environnement

```bash
env               # liste toutes les variables d'environnement
printenv          # idem
printenv HOME     # affiche une variable précise
```

---

## PATH — la variable la plus importante

```bash
echo $PATH
# /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
```

Quand tu tapes `nmap`, Linux cherche le programme dans chaque dossier du PATH dans l'ordre. Si `nmap` est dans `/usr/bin` → trouvé → exécuté.

```bash
# Ajouter un dossier au PATH
export PATH=$PATH:/mon/dossier

# Voir où est un programme
which nmap        # /usr/bin/nmap
```

---

## Variables et historique

```bash
echo $HISTFILE      # où est sauvegardé l'historique
echo $HISTSIZE      # combien de commandes en mémoire

# Désactiver l'historique pour la session (anti-forensique)
export HISTFILE=/dev/null
```

---

## Bash vs Zsh

| | Bash | Zsh (Kali par défaut) |
|---|---|---|
| Historique | `~/.bash_history` | `~/.zsh_history` |
| Config | `~/.bashrc` | `~/.zshrc` |
| Variables | identiques | identiques |

---

## Astuces

```bash
# Variable dans une commande
IP="192.168.159.142"
nmap $IP              # équivalent à nmap 192.168.159.142

# Très utile en hacking — définir la cible une fois
CIBLE="192.168.159.142"
nmap $CIBLE
hydra -l admin -P rockyou.txt ssh://$CIBLE
smbclient //$CIBLE/tmp -N
```

---

## Variables système utiles

```bash
echo $HOSTNAME      # nom de la machine
echo $OSTYPE        # type d'OS — linux-gnu, darwin...
echo $TERM          # type de terminal — xterm-256color...
echo $LANG          # langue du système — fr_FR.UTF-8...
echo $EDITOR        # éditeur par défaut — nano, vim...
echo $DISPLAY       # écran X11 — utile pour les GUI
echo $EUID          # Effective User ID — 0 = root
echo $UID           # User ID de l'utilisateur réel
echo $PPID          # PID du processus parent
echo $?             # code de retour de la dernière commande
echo $$             # PID du shell courant
```

---

## $? — le code de retour

```bash
ls /tmp
echo $?       # 0 = succès

ls /dossier_inexistant
echo $?       # 1 ou 2 = erreur
```

- `0` → la commande a réussi
- autre que `0` → la commande a échoué

Très utile dans les scripts pour vérifier si une commande a marché.

---

## $EUID — suis-je root ?

```bash
echo $EUID    # 0 = root, autre = utilisateur normal
```

Dans un script :
```bash
if [ $EUID -eq 0 ]; then
    echo "je suis root"
else
    echo "je suis pas root"
fi
```

---

## Variables réseau utiles en hacking

```bash
# Définir ses variables de session une fois
export LHOST="192.168.159.141"   # ton IP Kali
export LPORT="4444"              # ton port d'écoute
export CIBLE="192.168.159.142"   # IP Metasploitable

# Les utiliser partout
nmap -sV $CIBLE
nc -lvp $LPORT
smbclient //$CIBLE/tmp -N
```

---

## Variables spéciales en bash/zsh

```bash
$0      # nom du script ou shell en cours
$1 $2   # arguments passés à un script ($1 = premier, $2 = deuxième...)
$#      # nombre d'arguments passés au script
$@      # tous les arguments
$!      # PID du dernier processus lancé en arrière-plan
```

Exemple dans un script :
```bash
#!/bin/bash
# ./mon_scan.sh 192.168.1.1
echo "Je scanne : $1"
nmap -sV $1
```