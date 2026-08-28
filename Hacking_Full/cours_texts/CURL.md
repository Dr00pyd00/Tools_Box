# curl — commandes de base

> **curl** = **C**lient **URL** — outil en ligne de commande pour faire des requêtes HTTP (et autres protocoles).
> C'est le navigateur web du terminal — il envoie des requêtes et affiche les réponses.

---

## Requêtes de base

```bash
curl http://192.168.159.142                    # GET sur la page d'accueil
curl http://192.168.159.142/dvwa/login.php     # GET sur un path précis
curl -v http://192.168.159.142                 # -v = verbose, affiche requête + réponse complètes
curl -s http://192.168.159.142                 # -s = silent, cache les infos de progression
curl -o fichier.html http://192.168.159.142    # -o = output, sauvegarde dans un fichier
```

---

## Voir les headers

```bash
curl -I http://192.168.159.142        # -I = headers uniquement, pas le body
curl -v http://192.168.159.142        # -v = tout afficher — requête et réponse
```

Avec `-v` tu vois :
- `>` = ce que curl envoie
- `<` = ce que le serveur répond

---

## Méthodes HTTP

```bash
curl -X GET http://site.com/page          # GET (défaut)
curl -X POST http://site.com/login        # POST
curl -X PUT http://site.com/resource      # PUT
curl -X DELETE http://site.com/resource   # DELETE
curl -X PATCH http://site.com/resource    # PATCH
```

---

## Envoyer des données POST

```bash
# Formulaire classique (application/x-www-form-urlencoded)
curl -X POST http://192.168.159.142/dvwa/login.php \
  -d "username=admin&password=password"

# JSON
curl -X POST http://site.com/api/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "password"}'
```

---

## Headers personnalisés

```bash
curl -H "Content-Type: application/json" http://site.com
curl -H "Authorization: Bearer token123" http://site.com
curl -H "User-Agent: Mozilla/5.0" http://site.com   # se faire passer pour un navigateur
```

- `-H` = **H**eader — ajoute un header à la requête

---

## Cookies

```bash
# Envoyer un cookie
curl -b "session=abc123" http://site.com

# Sauvegarder les cookies reçus dans un fichier
curl -c cookies.txt http://site.com/login

# Réutiliser les cookies sauvegardés
curl -b cookies.txt http://site.com/dashboard
```

- `-b` = **b**rowser cookies — envoie des cookies
- `-c` = **c**ookie jar — sauvegarde les cookies reçus

---

## Suivre les redirections

```bash
curl -L http://site.com     # -L = Location, suit les redirections 301/302
```

Sans `-L` curl s'arrête à la redirection et affiche juste le header `Location`.

---

## Authentification

```bash
curl -u admin:password http://site.com          # Basic Auth
curl -u admin http://site.com                   # demande le mot de passe interactivement
```

---

## curl en hacking

```bash
# Tester si une page existe
curl -s -o /dev/null -w "%{http_code}" http://192.168.159.142/admin
# affiche juste le code HTTP : 200, 403, 404...

# Voir la bannière du serveur web
curl -I http://192.168.159.142
# cherche : Server: Apache/2.2.8

# Tester une injection dans un paramètre GET
curl "http://192.168.159.142/page.php?id=1'"

# Envoyer un formulaire de login et voir la réponse
curl -v -X POST http://192.168.159.142/dvwa/login.php \
  -d "username=admin&password=password" \
  -L
```

---

## Afficher uniquement le code HTTP

```bash
curl -s -o /dev/null -w "%{http_code}\n" http://site.com/path
```

- `-s` — silent
- `-o /dev/null` — jette le body
- `-w "%{http_code}"` — **w**rite-out — affiche le code HTTP

Utile pour scripter — tester des dizaines d'URLs rapidement.

---

## curl vs navigateur

| | Navigateur | curl |
|---|---|---|
| Interface | graphique | terminal |
| JavaScript | exécuté | ignoré |
| Usage hacking | voir le rendu | voir la requête brute |
| Cookies | automatiques | manuels avec -b/-c |

En hacking curl est plus utile que le navigateur pour voir exactement ce qui circule sur le réseau — sans l'interprétation du JavaScript.