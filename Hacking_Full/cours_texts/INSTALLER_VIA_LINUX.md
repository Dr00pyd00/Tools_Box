# 📦 INSTALLATION DE LOGICIELS SUR LINUX (Ubuntu/Debian)

---

## Le concept de base

Sur Windows → tu télécharges un `.exe` et tu double-cliques.
Sur Ubuntu → tu as plusieurs systèmes selon d'où vient le logiciel.

---

## 1. APT — le gestionnaire de paquets principal

```bash
sudo apt install <nom_du_paquet>
```

`apt` = **Advanced Package Tool**
C'est le système officiel d'Ubuntu. Il va chercher les logiciels dans des **dépôts** (= serveurs officiels Ubuntu).

```bash
sudo apt update        # met à jour la liste des paquets disponibles
sudo apt upgrade       # met à jour tous les paquets installés
sudo apt install nmap  # installe nmap
sudo apt remove nmap   # désinstalle nmap
```

**Limites :** uniquement les logiciels présents dans les dépôts officiels Ubuntu.
Les logiciels propriétaires ou indépendants (Obsidian, Discord...) n'y sont pas.

---

## 2. DPKG — l'installateur de fichiers .deb

```bash
sudo dpkg -i fichier.deb
```

`dpkg` = **Debian Package**
C'est le système bas niveau qui installe un fichier `.deb` local.
Le `.deb` c'est l'équivalent Linux d'un `.exe` Windows — un fichier d'installation que tu télécharges toi-même depuis un site.

```bash
sudo dpkg -i obsidian-1.7.4.deb   # installe le .deb
sudo dpkg -r obsidian              # désinstalle
sudo dpkg -l                       # liste tous les paquets installés
```

**Quand l'utiliser :** quand un logiciel propose un `.deb` sur son site officiel
mais n'est pas dans les dépôts apt.

---

## 3. SNAP — paquets universels

```bash
sudo snap install <nom> --classic
```

`snap` = système de paquets créé par Canonical (l'éditeur d'Ubuntu).
Permet d'installer des apps qui ne sont pas dans apt, sans télécharger de `.deb`.
L'app tourne dans un environnement un peu isolé.

```bash
sudo snap install obsidian --classic
sudo snap remove obsidian
snap list                            # liste les snaps installés
```

`--classic` = donne à l'app un accès complet au système (fichiers, réseau...)
Sans `--classic`, l'app est sandboxée (= isolée, accès restreint).

**Moins propre que dpkg** — couche supplémentaire, parfois plus lent.

---

## 4. Depuis les sources — compilation manuelle

```bash
git clone https://github.com/projet/outil
cd outil
make
sudo make install
```

Tu récupères le code source et tu le **compiles toi-même**.
C'est le niveau le plus bas — tu contrôles tout, mais c'est plus complexe.
Utilisé pour des outils pas packagés du tout (certains outils hacking/CTF).

---

## Résumé — quoi utiliser quand ?

| Situation | Commande |
|---|---|
| Logiciel dans les dépôts Ubuntu | `sudo apt install` |
| Logiciel avec un `.deb` sur son site | `sudo dpkg -i fichier.deb` |
| Logiciel dispo sur Snap | `sudo snap install` |
| Logiciel que tu compiles | `make && sudo make install` |

---

## Analogie Windows → Linux

| Windows | Linux |
|---|---|
| `.exe` | `.deb` |
| double-clic pour installer | `sudo dpkg -i` |
| Microsoft Store | `apt` |
| winget | `apt` aussi |