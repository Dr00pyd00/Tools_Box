

## Installation Docker — fiche de référence

**Prérequis :** Debian/Ubuntu/Kali, accès sudo.

```bash
# 1. Retirer d'anciennes versions si presentes
sudo apt-get remove docker docker-engine docker.io containerd runc 2>/dev/null

# 2. Prerequis
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg

# 3. Cle GPG officielle Docker
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# 4. Verifier le nom de code detecte AVANT d'ajouter le depot
. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}"
```

**→ regarde ce que la commande 4 affiche, puis choisis UNE des deux options ci-dessous.**

**Option A — Ubuntu/Debian standard** (le nom de code affiché existe sur https://download.docker.com/linux/ubuntu/dists/ ou /debian/dists/) :

```bash
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

**Option B — Kali** (rolling release, non reconnu par le dépôt Docker → forcer la base Debian) :

```bash
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
  bookworm stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

**5. Installer**

```bash
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

**6. Utiliser sans sudo**

```bash
sudo usermod -aG docker $USER
newgrp docker
```

**7. Vérifier**

```bash
sudo docker run hello-world
docker compose version
```

---

Garde cette fiche dans ton repo dotfiles — un `docs/docker-install.md`, par exemple. Tu la rejoueras probablement sur chaque nouvelle VM.
