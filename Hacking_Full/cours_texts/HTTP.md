

---

## HTTP — comment ça marche

Le web c'est une conversation entre deux acteurs :

- **Client** — ton navigateur (ou curl, ou Burp Suite)
- **Serveur** — Apache, nginx... qui héberge le site

La conversation suit le protocole **HTTP** — **H**yper**T**ext **T**ransfer **P**rotocol.

---

### Une requête HTTP c'est quoi ?

Quand tu tapes `http://192.168.159.142` dans ton navigateur, il envoie ça au serveur :

```
GET / HTTP/1.1
Host: 192.168.159.142
User-Agent: Mozilla/5.0
Accept: text/html
```

Ligne par ligne :

- `GET` — la **méthode** — ce que tu veux faire
- `/` — le **chemin** — quelle page tu veux
- `HTTP/1.1` — la version du protocole
- `Host` — le domaine demandé
- `User-Agent` — qui fait la requête — navigateur, outil...
- `Accept` — quel type de contenu tu acceptes

---

### Les méthodes HTTP

| Méthode | Usage |
|---|---|
| `GET` | récupérer une page ou une ressource |
| `POST` | envoyer des données (formulaire, login) |
| `PUT` | créer ou remplacer une ressource |
| `DELETE` | supprimer une ressource |
| `PATCH` | modifier partiellement une ressource |

En hacking tu en utilises surtout deux — `GET` et `POST`.

---

### La réponse du serveur

Le serveur répond avec ça :

```
HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: 1234

<html>...</html>
```

- `200 OK` — le **code de statut** — tout s'est bien passé
- `Content-Type` — le type de contenu renvoyé
- Le corps — le HTML de la page

---

### Les codes de statut importants

| Code | Signification |
|---|---|
| `200` | OK — succès |
| `301` | Redirect permanent |
| `302` | Redirect temporaire |
| `400` | Bad Request — requête malformée |
| `401` | Unauthorized — pas authentifié |
| `403` | Forbidden — authentifié mais pas autorisé |
| `404` | Not Found — page inexistante |
| `500` | Internal Server Error — bug côté serveur |

En hacking les codes importants :
- `200` → la page existe
- `403` → la page existe mais t'as pas accès — intéressant
- `404` → n'existe pas
- `500` → t'as peut-être déclenché une erreur avec ton injection

---
### GET vs POST

Les deux envoient des données au serveur — mais pas de la même façon.

---

**GET — les données sont dans l'URL**

```
http://192.168.159.142/search.php?nom=luna&age=30
                                  ↑
                                  paramètres visibles dans l'URL
```

Le `?` sépare le path des paramètres. Chaque paramètre c'est `clé=valeur`, séparés par `&`.

La requête HTTP :
```
GET /search.php?nom=luna&age=30 HTTP/1.1
Host: 192.168.159.142
```

---

**POST — les données sont dans le corps de la requête**

```
http://192.168.159.142/login.php
```

La requête HTTP :
```
POST /login.php HTTP/1.1
Host: 192.168.159.142
Content-Type: application/x-www-form-urlencoded

username=luna&password=monmdp
```

Les données ne sont pas dans l'URL — elles sont dans le corps, après les headers.

---

**La différence en pratique :**

| | GET | POST |
|---|---|---|
| Données dans | l'URL | le corps |
| Visible dans | la barre d'adresse | invisible |
| Historique navigateur | oui | non |
| Usage | récupérer | envoyer/modifier |

---

**En hacking pourquoi c'est important :**

Les formulaires de login utilisent POST — tu vois pas le mot de passe dans l'URL.

Mais les paramètres GET sont directement manipulables dans l'URL :

```
http://site.com/page.php?id=1
```

Tu changes `id=1` en `id=2` — tu accèdes peut-être à une autre ressource. En SQL injection tu changes ça en :

```
http://site.com/page.php?id=1' OR '1'='1
```

C'est pour ça que GET est souvent plus vulnérable aux injections — les paramètres sont directement accessibles. 😄

---
Oui — exactement comme ça. La structure HTTP c'est :

```
MÉTHODE /path HTTP/version     ← ligne de requête
Header: valeur                 ← headers
Header: valeur
                               ← ligne vide obligatoire
corps de la requête            ← body
```

La **ligne vide** entre les headers et le body est obligatoire — c'est elle qui dit au serveur "les headers sont finis, ce qui suit c'est le body".

---

Donc une requête POST complète :

```
POST /login.php HTTP/1.1
Host: 192.168.159.142
Content-Type: application/x-www-form-urlencoded
Content-Length: 27

username=luna&password=monmdp
```

- `Content-Type` — dit au serveur comment interpréter le body
- `Content-Length` — **27** — le nombre de caractères dans le body
- ligne vide
- body

---

Tu peux voir ça en vrai avec curl :

**[Kali - terminal]**
```bash
curl -v -X POST http://192.168.159.142/dvwa/login.php \
  -d "username=admin&password=password"
```

- `curl` — client HTTP en ligne de commande
- `-v` — **v**erbose — affiche la requête ET la réponse complètes
- `-X POST` — force la méthode POST
- `-d` — **d**ata — le body à envoyer



### Les headers HTTP

Les headers c'est des métadonnées — des informations supplémentaires que le client et le serveur s'échangent autour de la requête.

---

**Headers de requête — ce que le client envoie**

```
GET /dvwa/login.php HTTP/1.1
Host: 192.168.159.142
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)
Accept: text/html,application/xhtml+xml
Accept-Language: fr-FR,fr;q=0.9
Accept-Encoding: gzip, deflate
Connection: keep-alive
Cookie: security=low; PHPSESSID=abc123
```

| Header | Rôle |
|---|---|
| `Host` | domaine demandé — obligatoire |
| `User-Agent` | qui fait la requête — navigateur, curl, outil... |
| `Accept` | types de contenu acceptés |
| `Accept-Language` | langue préférée |
| `Cookie` | cookies stockés pour ce site |
| `Authorization` | token ou credentials |
| `Content-Type` | type du body — pour POST |
| `Content-Length` | taille du body en octets |

---

**Headers de réponse — ce que le serveur renvoie**

```
HTTP/1.1 200 OK
Server: Apache/2.2.8 (Ubuntu)
X-Powered-By: PHP/5.2.4-2ubuntu5.10
Set-Cookie: PHPSESSID=abc123; path=/
Content-Type: text/html; charset=utf-8
Content-Length: 1234
```

| Header | Rôle |
|---|---|
| `Server` | technologie du serveur |
| `X-Powered-By` | langage backend |
| `Set-Cookie` | crée un cookie dans le navigateur |
| `Content-Type` | type du contenu renvoyé |
| `Location` | URL de redirection (avec 301/302) |

---

**En hacking les headers sont une mine d'informations :**

```
Server: Apache/2.2.8 (Ubuntu)
X-Powered-By: PHP/5.2.4
```

T'as la version d'Apache et de PHP → searchsploit Apache 2.2.8 → exploits potentiels.

```bash
curl -I http://192.168.159.142
```

Ça affiche uniquement les headers de réponse — c'est souvent la première chose qu'un pentesteur fait sur un site web.

---



Oui — le header `Cookie` c'est une liste de paires `clé=valeur` séparées par `;` :

```
Cookie: security=low; PHPSESSID=abc123; theme=dark; user_id=42
```

Chaque paire c'est un cookie distinct. Le navigateur les envoie tous en une seule ligne dans le header `Cookie`.

---

Et dans l'autre sens — quand le serveur veut créer ou modifier un cookie, il utilise `Set-Cookie` dans sa réponse — un header par cookie :

```
Set-Cookie: PHPSESSID=abc123; path=/; HttpOnly
Set-Cookie: security=low; path=/
Set-Cookie: theme=dark; expires=...
```

---

Chaque cookie peut avoir des attributs supplémentaires :

| Attribut | Rôle |
|---|---|
| `path=/` | sur quels paths le cookie est envoyé |
| `expires=...` | quand le cookie expire |
| `HttpOnly` | JavaScript ne peut pas lire ce cookie |
| `Secure` | cookie envoyé uniquement en HTTPS |
| `SameSite` | protection contre certaines attaques |

---

**En hacking les cookies c'est crucial :**

Le cookie `PHPSESSID` c'est l'identifiant de session — si tu le voles tu peux te faire passer pour l'utilisateur sans connaître son mot de passe. C'est ce qu'on appelle le **session hijacking**.

Et `security=low` sur DVWA — c'est littéralement le niveau de sécurité de l'application stocké dans un cookie. Tu peux le modifier directement. 😄



### Les cookies

Un cookie c'est un petit fichier texte que le serveur demande au navigateur de stocker — et de renvoyer à chaque requête suivante.

---

**Pourquoi les cookies existent ?**

HTTP est un protocole **stateless** — sans mémoire. Chaque requête est indépendante, le serveur ne se souvient pas de toi.

Problème : si tu te connectes sur un site, la page suivante ne sait pas que t'es connectée.

Solution : le cookie. Le serveur te donne un identifiant, tu le renvoies à chaque requête, le serveur te reconnaît.

```
1. Tu envoies ton login/password
         ↓
2. Le serveur vérifie → OK
   Il crée une session en base
   Il t'envoie : Set-Cookie: PHPSESSID=abc123
         ↓
3. Ton navigateur stocke PHPSESSID=abc123
         ↓
4. Chaque requête suivante :
   Cookie: PHPSESSID=abc123
         ↓
5. Le serveur lit le cookie
   Trouve la session en base
   Sait que c'est toi → t'es connectée
```

---

**Les types de cookies**

**Cookie de session** — temporaire, disparaît à la fermeture du navigateur :
```
Set-Cookie: PHPSESSID=abc123
```
Pas de date d'expiration → cookie de session.

**Cookie persistant** — stocké sur le disque, survit à la fermeture :
```
Set-Cookie: remember_me=xyz; expires=Thu, 01 Jan 2027 00:00:00 GMT
```

---

**Où sont stockés les cookies ?**

Dans ton navigateur — chaque navigateur a sa propre base. Sur Firefox tu peux les voir dans :

`F12 → Storage → Cookies`

---

**En hacking — ce qu'on peut faire avec les cookies**

**1. Vol de cookie — Session Hijacking**

Si tu récupères le `PHPSESSID` de quelqu'un tu peux te faire passer pour lui :

```bash
curl -b "PHPSESSID=abc123" http://site.com/dashboard
```

Le serveur voit le bon cookie → pense que c'est l'utilisateur légitime.

Comment voler un cookie ? Via **XSS** — on y reviendra.

**2. Modifier un cookie**

Sur DVWA le niveau de sécurité est dans un cookie :
```
Cookie: security=low
```

Tu le changes en `security=impossible` — ou l'inverse selon ce que tu veux faire.

**3. Analyser les cookies**

Un cookie mal protégé peut contenir des infos sensibles :
```
Cookie: user=admin; role=user
```

Tu changes `role=user` en `role=admin` → peut-être que le serveur te donne des droits admin. C'est ce qu'on appelle **cookie tampering**.

---

**Les protections côté serveur**

| Attribut | Protection |
|---|---|
| `HttpOnly` | JavaScript ne peut pas lire le cookie — protège contre XSS |
| `Secure` | envoyé uniquement en HTTPS — protège contre l'écoute réseau |
| `SameSite=Strict` | protège contre CSRF |

---

### Sessions et authentification

---

**C'est quoi une session ?**

La session c'est ce que le serveur stocke de son côté — l'équivalent serveur du cookie.

```
Côté client (navigateur)     Côté serveur
Cookie: PHPSESSID=abc123  ←→  session_abc123 = {user: "admin", role: "admin", logged: true}
```

Le cookie c'est juste une clé — la vraie information est sur le serveur.

---

**Le flux d'authentification complet**

```
1. Tu envoies POST /login.php
   username=admin&password=password
         ↓
2. Serveur vérifie en base de données
   SELECT * FROM users WHERE username='admin'
   Compare le hash du password
         ↓
3. Si OK → serveur crée une session
   $_SESSION['user'] = 'admin'
   $_SESSION['logged'] = true
   Génère un identifiant unique : abc123
         ↓
4. Serveur répond :
   HTTP/1.1 302 Found
   Location: /dashboard.php
   Set-Cookie: PHPSESSID=abc123
         ↓
5. Navigateur stocke le cookie
   Suit la redirection vers /dashboard.php
   Cookie: PHPSESSID=abc123
         ↓
6. Serveur reçoit la requête
   Lit PHPSESSID=abc123
   Trouve la session → user=admin, logged=true
   Affiche le dashboard
```

---

**Où sont stockées les sessions côté serveur ?**

Ça dépend du langage et de la config :

| Stockage | Exemple |
|---|---|
| Fichiers | `/tmp/sess_abc123` sur le disque |
| Base de données | table `sessions` |
| Redis | en mémoire, rapide |
| Mémoire | perdu au redémarrage |

Sur Metasploitable/PHP les sessions sont dans `/tmp` — tu peux les lire si t'as un shell root. 😄

---

**En hacking — attaques sur les sessions**

**1. Session fixation**

Tu forces la victime à utiliser un PHPSESSID que tu connais déjà :

```
http://site.com/login.php?PHPSESSID=abc123
```

Si le serveur accepte ça et ne régénère pas le cookie après login → t'as accès à sa session.

**2. Session hijacking**

Tu voles le cookie via XSS ou écoute réseau → tu te connectes avec.

**3. Weak session ID**

Si le PHPSESSID est prévisible — `1`, `2`, `3`... — tu peux deviner les sessions d'autres utilisateurs.

Un bon PHPSESSID c'est aléatoire et long :
```
PHPSESSID=a3f8b2c9d1e4f7a0b5c8d2e6f9a1b4c7
```

---

**JWT — JSON Web Token**

Les API modernes n'utilisent pas PHPSESSID — elles utilisent des **JWT**.

T'as déjà vu ça dans tes projets FastAPI. Un JWT c'est un token signé qui contient les infos de l'utilisateur :

```
eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiYWRtaW4ifQ.signature
       ↑                      ↑                    ↑
     header               payload               signature
```

Le payload est encodé en base64 — pas chiffré. Tu peux le décoder :

```bash
echo "eyJ1c2VyIjoiYWRtaW4ifQ" | base64 -d
# {"user":"admin"}
```

Si la signature est mal vérifiée → tu modifies le payload → tu te fais passer pour admin.

---

