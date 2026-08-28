# Flask — Fiche de référence
> Pour quelqu'un qui connaît FastAPI et Django

---

## Installation

```bash
pip install flask --break-system-packages
```

---

## Comparaison rapide Flask / FastAPI / Django

| | Flask | FastAPI | Django |
|---|---|---|---|
| Type | Micro-framework | Micro-framework async | Full-stack framework |
| Validation auto | ❌ manuelle | ✅ Pydantic | ✅ Forms/Serializers |
| Async natif | ❌ (possible mais bolted-on) | ✅ | ✅ (partiel) |
| ORM inclus | ❌ | ❌ | ✅ |
| Docs auto | ❌ | ✅ Swagger/ReDoc | ❌ |
| Verbosité | Très faible | Faible | Élevée |
| Serveur interne | Werkzeug | Uvicorn | Gunicorn |

---

## Structure minimale

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello"

app.run(host="0.0.0.0", port=5000)
```

- `Flask(__name__)` — crée l'app, `__name__` dit à Flask où chercher les fichiers
- `host="0.0.0.0"` — écoute sur toutes les interfaces (pas juste localhost)
- `port=5000` — port par défaut Flask

---

## Routes et méthodes HTTP

```python
# GET uniquement (défaut)
@app.route("/users", methods=["GET"])
def get_users():
    return jsonify([{"id": 1, "nom": "Luna"}])

# POST
@app.route("/users", methods=["POST"])
def create_user():
    body = request.get_json()
    return jsonify({"created": body}), 201

# Plusieurs méthodes sur une route
@app.route("/users", methods=["GET", "POST"])
def users():
    if request.method == "GET":
        return jsonify([])
    elif request.method == "POST":
        return jsonify({}), 201
```

**Comparaison FastAPI :**
```python
# FastAPI
@app.get("/users")          # méthode dans le décorateur
@app.post("/users")

# Flask
@app.route("/users", methods=["GET"])    # méthode en paramètre
@app.route("/users", methods=["POST"])
```

---

## Paramètres d'URL

```python
# /users/42
@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    return jsonify({"id": user_id})

# Convertisseurs disponibles
# <string:name>   — string (défaut)
# <int:id>        — entier
# <float:price>   — flottant
# <path:filepath> — string avec slashes
```

**Comparaison FastAPI :**
```python
# FastAPI — déclaré dans la signature de fonction
@app.get("/users/{user_id}")
def get_user(user_id: int):   # type hint = validation auto

# Flask — déclaré dans la route, pas de validation Pydantic
@app.route("/users/<int:user_id>")
def get_user(user_id):        # pas de type hint requis
```

---

## Query parameters

```python
# /search?q=luna&page=2
@app.route("/search", methods=["GET"])
def search():
    q = request.args.get("q", "")          # défaut ""
    page = request.args.get("page", 1, type=int)  # converti en int
    return jsonify({"q": q, "page": page})
```

- `request.args` — dict des query params
- `.get("key", default, type=)` — valeur par défaut + conversion de type

---

## L'objet `request`

Contient tout ce qui arrive dans la requête HTTP entrante.

```python
request.method          # "GET", "POST", "PUT"...
request.args            # query params (?page=2)
request.get_json()      # body JSON parsé en dict Python
request.get_json(force=True, silent=True)  # ignore Content-Type, pas d'erreur si vide
request.get_data(as_text=True)  # body brut en string
request.headers         # tous les headers de la requête
request.headers.get("Authorization")  # un header spécifique
request.remote_addr     # IP du client
request.form            # données de formulaire HTML
request.files           # fichiers uploadés
```

**Comparaison FastAPI :**
```python
# FastAPI — tout déclaré dans la signature
async def create(body: MonSchema, request: Request):
    ip = request.client.host

# Flask — tout dans l'objet global `request`
def create():
    body = request.get_json()
    ip = request.remote_addr
```

---

## Réponses

```python
from flask import jsonify, make_response

# Dict simple (Flask >= 2.2 convertit auto)
return {"message": "ok"}

# jsonify — explicite, garanti Content-Type: application/json
return jsonify({"message": "ok"})

# Avec status code
return jsonify({"message": "créé"}), 201

# Avec headers custom
response = make_response(jsonify({"message": "ok"}))
response.headers["X-Custom"] = "valeur"
return response
```

---

## Headers de réponse — modifier / cacher

```python
# Sur une route spécifique
@app.after_request
def modifier_headers(response):
    response.headers["Server"] = "Apache/2.4"   # masquer Werkzeug
    response.headers["X-Frame-Options"] = "DENY"
    return response
```

- `@app.after_request` — s'exécute après chaque requête, avant l'envoi

---

## Gestion des erreurs

```python
from flask import abort

# Déclencher une erreur HTTP
@app.route("/secret")
def secret():
    abort(403)   # comme raise HTTPException en FastAPI

# Handler d'erreur custom
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Route introuvable"}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({"error": "Erreur serveur"}), 500
```

**Comparaison FastAPI :**
```python
# FastAPI
raise HTTPException(status_code=404, detail="introuvable")

# Flask
abort(404)
```

---

## Blueprints — équivalent des routers FastAPI

```python
# users/routes.py
from flask import Blueprint, jsonify

users_bp = Blueprint("users", __name__, url_prefix="/users")

@users_bp.route("/", methods=["GET"])
def get_users():
    return jsonify([])

# main.py
from users.routes import users_bp
app.register_blueprint(users_bp)
```

**Comparaison FastAPI :**
```python
# FastAPI
router = APIRouter(prefix="/users")
app.include_router(router)

# Flask
users_bp = Blueprint("users", __name__, url_prefix="/users")
app.register_blueprint(users_bp)
```

---

## Mode debug

```python
app.run(debug=True)
# — recharge automatiquement à chaque modification du code
# — affiche les erreurs dans le navigateur
# — JAMAIS en production
```

---

## Variables d'environnement

```python
import os

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-only")
app.config["DATABASE_URL"] = os.getenv("DATABASE_URL")
```

---

## Ce que Flask ne fait PAS (contrairement à FastAPI/Django)

- ❌ Pas de validation automatique des données (pas de Pydantic intégré)
- ❌ Pas de docs Swagger auto
- ❌ Pas d'ORM intégré
- ❌ Pas d'async natif propre
- ❌ Pas de type hints requis

Flask te donne le strict minimum et te laisse choisir le reste.
C'est sa force pour comprendre HTTP — rien n'est caché.

---

## Werkzeug — la couche sous Flask

Flask est construit sur **Werkzeug** (allemand : "outil").
Werkzeug gère les connexions TCP, parse les requêtes HTTP brutes.
En production, on remplace Werkzeug par **Gunicorn** ou **Uvicorn**.

```
Ton code Flask
    └── Flask (routes, request, jsonify)
            └── Werkzeug (HTTP bas niveau)
                    └── Socket TCP
```