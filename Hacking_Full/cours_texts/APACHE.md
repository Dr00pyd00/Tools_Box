

# Apache2 — Fiche de référence

---

## C'est quoi Apache ?

Apache est un **logiciel serveur HTTP**. Il tourne en permanence sur une machine, écoute sur un port (80 par défaut), et répond aux requêtes HTTP.

Ce n'est pas un langage, pas un framework, pas un hébergeur. C'est un **programme** qui fait le lien entre le réseau et tes fichiers ou ton application.

```
Navigateur / curl
      │
      │  requête HTTP
      ▼
   Apache (port 80)
      │
      ├── fichiers statiques → lit /var/www/html/ et renvoie
      │
      └── reverse proxy → redirige vers Uvicorn/Werkzeug/Flask/FastAPI
```

---

## Apache vs Uvicorn/Werkzeug

| | Apache | Uvicorn / Werkzeug |
|---|---|---|
| Rôle | Serveur HTTP production | Serveur HTTP développement |
| Sert du Python | ❌ (via proxy seulement) | ✅ |
| Fichiers statiques | ✅ très efficace | ⚠️ lent |
| HTTPS | ✅ natif | ⚠️ compliqué |
| Trafic massif | ✅ | ❌ |
| Modèle | Multi-process | Async (Uvicorn) |

En production :
```
Internet → Apache (port 80/443) → Uvicorn (port 8000) → FastAPI/Flask
```

En développement :
```
curl → Werkzeug (port 5000) → Flask
```

---

## Architecture par modules

Apache de base est minimaliste. Tout se rajoute en **modules** (comme des plugins).

```
Apache core
   ├── mod_proxy       ← reverse proxy
   ├── mod_proxy_http  ← reverse proxy HTTP
   ├── mod_ssl         ← HTTPS / certificats
   ├── mod_rewrite     ← réécriture d'URLs
   ├── mod_php         ← exécuter du PHP
   └── mod_deflate     ← compression des réponses
```

Activer / désactiver un module :
```bash
sudo a2enmod nom_module     # enable  — active le module
sudo a2dismod nom_module    # disable — désactive le module
```

Voir les modules actifs :
```bash
ls /etc/apache2/mods-enabled/
```

---

## Architecture sites-available / sites-enabled

Apache peut héberger **plusieurs sites sur une seule machine** — c'est ce qu'on appelle les **Virtual Hosts**.

```
sites-available/    ← tous les sites configurés (actifs ou non)
sites-enabled/      ← liens symboliques vers les sites qui tournent
```

Activer / désactiver un site :
```bash
sudo a2ensite mon-site.conf     # active le site
sudo a2dissite mon-site.conf    # désactive le site
```

Comment Apache choisit quel site servir ? Il lit le header `Host` de la requête HTTP :
```
Host: site1.com   →  Apache sert le Virtual Host de site1.com
Host: site2.com   →  Apache sert le Virtual Host de site2.com
```

---

## Fichiers importants

```
/etc/apache2/
├── apache2.conf          ← config principale, inclut tout le reste
├── ports.conf            ← ports d'écoute (80, 443...)
├── mods-available/       ← tous les modules disponibles
├── mods-enabled/         ← modules actifs (liens symboliques)
├── sites-available/      ← tous les sites configurés
├── sites-enabled/        ← sites actifs (liens symboliques)
└── conf-available/       ← configs globales supplémentaires

/var/www/html/            ← document root par défaut (tes fichiers HTML)

/var/log/apache2/
├── access.log            ← toutes les requêtes reçues
└── error.log             ← les erreurs
```

---

## Document Root

Le dossier depuis lequel Apache sert les fichiers statiques.

Par défaut : `/var/www/html/`

- `var` = **variable** — données qui changent (convention Unix)
- `www` = convention historique (World Wide Web), pas réservé à Apache

Si Apache ne trouve pas de `index.html` dans le dossier → il affiche la liste des fichiers (**directory listing**). En prod c'est une vulnérabilité — on le désactive :

```apache
Options -Indexes    # interdit le listing → 403 Forbidden
Options Indexes     # autorise le listing  (dangereux)
```

---

## Commandes de base

```bash
sudo service apache2 start      # démarrer
sudo service apache2 stop       # arrêter
sudo service apache2 restart    # redémarrer (applique les configs)
sudo service apache2 reload     # recharger la config sans couper
sudo service apache2 status     # état du service

apache2 -v                      # version installée
sudo apache2ctl configtest      # vérifier la config avant restart
```

---

## Config Virtual Host — fichiers statiques

```apache
# /etc/apache2/sites-available/mon-site.conf

<VirtualHost *:80>
    ServerName mon-site.com
    DocumentRoot /var/www/mon-site/

    <Directory /var/www/mon-site/>
        Options -Indexes
        AllowOverride None
        Require all granted
    </Directory>
</VirtualHost>
```

- `VirtualHost *:80` — écoute sur le port 80, toutes les interfaces
- `ServerName` — le domaine concerné
- `DocumentRoot` — dossier des fichiers à servir
- `Options -Indexes` — désactive le directory listing
- `Require all granted` — autorise tout le monde à accéder

---

## Config Virtual Host — Reverse Proxy (devant Flask/FastAPI)

```apache
# /etc/apache2/sites-available/flask-app.conf

<VirtualHost *:80>
    ProxyPass        /  http://127.0.0.1:5000/
    ProxyPassReverse /  http://127.0.0.1:5000/
</VirtualHost>
```

- `ProxyPass` — redirige les requêtes vers Flask sur le port 5000
- `ProxyPassReverse` — réécrit les headers de réponse pour que ce soit transparent

Modules nécessaires :
```bash
sudo a2enmod proxy proxy_http
```

---

## Headers révélateurs (en hacking)

```
Server: Apache/2.4.65 (Debian)
```

Ce header révèle la version exacte d'Apache et l'OS. Un attaquant cherche les CVE correspondantes. En prod on le masque :

```apache
# Dans apache2.conf
ServerTokens Prod        # affiche juste "Apache"
ServerSignature Off      # supprime la signature des pages d'erreur
```

---

## Page par défaut Apache

Quand Apache est installé et qu'aucun site n'est configuré, il affiche sa page par défaut depuis `/var/www/html/index.html`.

En hacking : voir cette page sur une cible = serveur mal configuré, potentiellement d'autres vulnérabilités.

---

## Les logs — yeux du hacker

```bash
sudo tail -f /var/log/apache2/access.log   # requêtes en temps réel
sudo tail -f /var/log/apache2/error.log    # erreurs en temps réel
```

Chaque ligne d'access.log :
```
192.168.1.1 - - [10/Apr/2026:14:18:00] "GET / HTTP/1.1" 200 10703
     │                    │                   │            │    │
     IP client            date/heure          requête    code  taille
```

En hacking : les logs d'Apache sur une cible révèlent qui a accédé à quoi et quand.



# Apache2 — Fiche complémentaire

---

## Virtual Hosts — comprendre vraiment

Un Virtual Host = un site. Apache peut en gérer plusieurs sur la même machine.
Il choisit lequel servir en lisant le header `Host:` de la requête HTTP.

### Deux types de Virtual Host — ne pas confondre

**Type 1 — Fichiers statiques** (HTML, CSS, images)
```apache
<VirtualHost *:80>
    ServerName mon-site.local
    DocumentRoot /var/www/mon-site/
</VirtualHost>
```
Apache lit les fichiers sur le disque et les envoie. Pas de Python, pas de logique.

**Type 2 — Reverse proxy** (devant Flask/FastAPI)
```apache
<VirtualHost *:80>
    ServerName mon-api.local
    ProxyPass / http://127.0.0.1:5000/
    ProxyPassReverse / http://127.0.0.1:5000/
</VirtualHost>
```
Apache ne touche pas au disque. Il reçoit la requête et la transmet à Flask/FastAPI.
C'est Flask qui génère la réponse — Apache est juste l'intermédiaire.

**Type 3 — Les deux ensemble** (frontend statique + backend API)
```apache
<VirtualHost *:80>
    ServerName mon-app.local

    # Frontend React/HTML — servi depuis le disque
    DocumentRoot /var/www/frontend/

    # Backend API — redirigé vers Flask
    ProxyPass /api http://127.0.0.1:5000/
    ProxyPassReverse /api http://127.0.0.1:5000/
</VirtualHost>
```
```
http://mon-app.local/           →  fichiers React dans /var/www/frontend/
http://mon-app.local/api/users  →  Flask port 5000
```

---

## ProxyPass — décortiqué

```apache
ProxyPass        /   http://127.0.0.1:5000/
ProxyPassReverse /   http://127.0.0.1:5000/
```

**`ProxyPass / http://127.0.0.1:5000/`**
```
ProxyPass   /        http://127.0.0.1:5000/
    │        │                │
    │        │                └── où envoyer (Flask sur port 5000)
    │        │
    │        └── quelles URLs intercepter
    │            "/" = TOUT (toutes les routes)
    │            "/api" = seulement les routes /api/*
    │
    └── directive Apache
```

Exemples :
```
ProxyPass / ...         →  /bonjour, /users, /data — TOUT redirigé
ProxyPass /api ...      →  seulement /api/*, le reste servi par Apache
```

**`ProxyPassReverse / http://127.0.0.1:5000/`**

Quand Flask envoie une redirection dans ses headers :
```
Location: http://127.0.0.1:5000/dashboard   ← Flask dit ça
```
Le client ne peut pas accéder à `127.0.0.1:5000` depuis l'extérieur.
`ProxyPassReverse` réécrit ce header automatiquement :
```
Location: http://mon-api.local/dashboard    ← le client voit ça
```
Toujours la même valeur que `ProxyPass`. Ils vont toujours en paire.

---

## Plusieurs sites en local — simuler des domaines

En local tu n'as que `localhost`. Pour simuler plusieurs domaines, tu modifies `/etc/hosts` :

```bash
sudo nano /etc/hosts
```

```
127.0.0.1   flask-app.local
127.0.0.1   blog.local
127.0.0.1   boutique.local
```

`/etc/hosts` = le DNS de ta machine. Il est consulté **avant** les vrais serveurs DNS.
Ça ne fonctionne que sur ta machine — les autres machines du réseau ne le voient pas.

Ensuite chaque Virtual Host a son `ServerName` :
```apache
# sites-available/flask-app.conf
<VirtualHost *:80>
    ServerName flask-app.local
    ProxyPass / http://127.0.0.1:5000/
    ProxyPassReverse / http://127.0.0.1:5000/
</VirtualHost>

# sites-available/blog.conf
<VirtualHost *:80>
    ServerName blog.local
    ProxyPass / http://127.0.0.1:5001/
    ProxyPassReverse / http://127.0.0.1:5001/
</VirtualHost>
```

Apache lit le header `Host:` et sert le bon Virtual Host :
```
curl http://flask-app.local  →  Host: flask-app.local  →  Flask port 5000
curl http://blog.local       →  Host: blog.local        →  Flask port 5001
```

---

## ServerName — d'où ça vient ?

En production = un **nom de domaine** acheté chez un registrar (OVH, Gandi...).
```
luna-api.com  →  DNS  →  ton IP publique  →  Apache  →  Flask
```

En local = ce que tu mets dans `/etc/hosts`. Tu inventes le nom.

ServerName n'a **rien à voir** avec ton code Flask/FastAPI. Les deux ne se connaissent pas.

---

## Logs — comprendre les fichiers

```
/var/log/apache2/
├── access.log              ← requêtes du site par défaut (000-default.conf)
├── error.log               ← erreurs Apache
└── other_vhosts_access.log ← requêtes des Virtual Hosts sans CustomLog défini
```

**Pourquoi `other_vhosts_access.log` ?**

Si ton Virtual Host n'a pas de `CustomLog` explicite, Apache logue dans `other_vhosts_access.log` au lieu de `access.log`.

Format de `other_vhosts_access.log` :
```
flask-app.local:80 127.0.0.1 - - [10/Apr/2026] "GET /bonjour HTTP/1.1" 200 43
      │                │                              │                   │
   VirtualHost       IP client                     requête             code
```

Pour logger dans `access.log` depuis un Virtual Host, ajoute `CustomLog` :
```apache
<VirtualHost *:80>
    ServerName flask-app.local
    ProxyPass / http://127.0.0.1:5000/
    ProxyPassReverse / http://127.0.0.1:5000/
    CustomLog ${APACHE_LOG_DIR}/access.log combined
    ErrorLog ${APACHE_LOG_DIR}/error.log
</VirtualHost>
```
- `CustomLog` — définit où écrire les logs d'accès
- `${APACHE_LOG_DIR}` — variable Apache = `/var/log/apache2/`
- `combined` — format de log standard (IP, date, requête, code, taille, user-agent)
- `ErrorLog` — où écrire les erreurs

---

## Workflow complet — créer un nouveau site

```bash
# 1. Créer le fichier de config
sudo nano /etc/apache2/sites-available/mon-site.conf

# 2. Activer le site
sudo a2ensite mon-site.conf

# 3. Vérifier la config avant de redémarrer
sudo apache2ctl configtest

# 4. Redémarrer Apache
sudo service apache2 restart

# 5. Ajouter le domaine local si besoin
sudo nano /etc/hosts
# ajouter : 127.0.0.1   mon-site.local
```

---

## Architecture complète — frontend + backend + Apache

```
Navigateur / curl
      │
      ▼
Apache (port 80)         ← reçoit tout
      │
      ├── GET /           →  /var/www/frontend/index.html  (React)
      ├── GET /style.css  →  /var/www/frontend/style.css   (statique)
      │
      └── GET /api/*      →  ProxyPass → Werkzeug/Uvicorn (port 5000/8000)
                                              │
                                          Flask/FastAPI
                                              │
                                          PostgreSQL
```

---

## En hacking — ce qu'Apache révèle

```bash
curl -v http://cible.com
```

Headers dangereux à chercher :
```
Server: Apache/2.4.65 (Debian)    ← version exacte + OS → chercher CVEs
X-Powered-By: PHP/7.4.0           ← version PHP → chercher CVEs PHP
```

Comportements révélateurs :
```
http://cible.com/           →  page Apache par défaut  = serveur mal configuré
http://cible.com/uploads/   →  liste de fichiers        = directory listing activé
http://cible.com/admin/     →  200 OK                   = dossier admin accessible
http://cible.com/.env       →  200 OK                   = fichier de config exposé ⚠️
```

Masquer les infos en prod :
```apache
# Dans /etc/apache2/apache2.conf
ServerTokens Prod        # affiche juste "Apache" sans version
ServerSignature Off      # supprime la signature sur les pages d'erreur
```