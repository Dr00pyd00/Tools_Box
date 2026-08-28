# 📡 Mémo — Commandes réseau Linux

---

## 1. Voir les ports occupés

```bash
sudo ss -tlnp
```

**Décortiqué mot par mot :**

| Morceau | Mot complet | Signification |
|--------|------------|---------------|
| `ss` | socket statistics | outil qui liste les connexions réseau actives sur ta machine |
| `-t` | TCP | affiche uniquement les connexions TCP (le protocole des serveurs web, API, etc.) |
| `-l` | listening | affiche uniquement les ports en **écoute** (ceux qui attendent des connexions) |
| `-n` | numeric | affiche les numéros de port tels quels, sans essayer de les convertir en noms |
| `-p` | process | affiche le **nom et le PID** du processus qui occupe chaque port |
| `sudo` | superuser do | lance la commande en tant qu'administrateur (nécessaire pour voir les PID) |

**Pour filtrer sur un port précis :**
```bash
sudo ss -tlnp | grep 8000
```
`grep 8000` — filtre les lignes qui contiennent "8000" dans le résultat.

**Ce que tu verras dans la sortie :**
```
State    Recv-Q   Send-Q   Local Address:Port   PID/Program
LISTEN   0        0        0.0.0.0:8000         12345/python3
```
→ Le PID ici c'est `12345` et le programme c'est `python3`

---

## 2. Libérer un port (tuer le processus qui l'occupe)

### Méthode A — en deux étapes (tu vois ce que tu tues)

```bash
# Étape 1 : trouver le PID
sudo ss -tlnp | grep 8000

# Étape 2 : tuer le processus
kill 12345
```

**`kill`** — envoie un signal d'arrêt au processus dont tu donnes le PID.

| Morceau | Mot complet | Signification |
|--------|------------|---------------|
| `kill` | kill | envoie un signal au processus (par défaut : SIGTERM = demande gentille de s'arrêter) |
| `12345` | — | le PID (Process ID = identifiant unique du processus) à arrêter |

Si le processus refuse de s'arrêter :
```bash
kill -9 12345
```
`-9` — envoie le signal **SIGKILL** = arrêt forcé immédiat, sans possibilité de refuser.

---

### Méthode B — en une seule commande (direct)

```bash
sudo fuser -k 8000/tcp
```

| Morceau | Mot complet | Signification |
|--------|------------|---------------|
| `fuser` | file user | trouve le processus qui utilise une ressource (fichier ou port) |
| `-k` | kill | tue directement le processus trouvé |
| `8000` | — | le numéro de port à libérer |
| `/tcp` | TCP | précise que c'est un port TCP (et non UDP) |

---

## 3. Voir son IP publique

```bash
curl ifconfig.me
```

| Morceau | Mot complet | Signification |
|--------|------------|---------------|
| `curl` | client URL | outil en ligne de commande pour faire des requêtes HTTP |
| `ifconfig.me` | — | site web qui te renvoie simplement ton IP publique (vue depuis internet) |

⚠️ Cette IP c'est celle de ta **box** (partagée avec tous les appareils de ton réseau), pas de ta machine.

---

## 4. Voir ses disques et partitions

```bash
lsblk -f
```

| Morceau | Mot complet | Signification |
|--------|------------|---------------|
| `lsblk` | list block devices | liste tous les périphériques de stockage (disques, partitions, clés USB) |
| `-f` | filesystem | affiche le type de système de fichiers de chaque partition |

**Ce qu'il faut chercher dans la sortie :**

| Type vu | Signification |
|--------|---------------|
| `ext4` | partition Linux normale, **non chiffrée** |
| `ntfs` | partition Windows |
| `vfat` | partition FAT32 (souvent la partition de boot EFI) |
| `crypto_LUKS` | partition Linux **chiffrée** avec LUKS ✅ |

---

## 5. Rappel — Le concept clé

> **Un port occupé = un processus qui tourne.**
> Tu ne "fermes" pas un port directement.
> Tu **tues le processus** → le port se libère automatiquement.

```
Port occupé
    ↓
sudo ss -tlnp | grep PORT   → trouve le PID
    ↓
kill PID                     → tue le processus
    ↓
Port libéré ✅
```

---

*Fiche construite le 02/04/2026 — session ngrok + réseau*
