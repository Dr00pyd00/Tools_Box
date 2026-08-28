# Burp Suite — guide de base

> Burp Suite est un **proxy HTTP** — il se place entre ton navigateur et le serveur.
> Tout le trafic HTTP passe par lui — tu peux l'intercepter, le modifier, le rejouer.
> C'est l'outil numéro 1 du hacking web.

---

## Concept — comment ça marche

```
Navigateur → Burp Suite → Serveur web
            ↑
            tu interceptes ici
            tu modifies les requêtes
            tu les analyses
```

Sans Burp :
```
Navigateur ──────────────────► Serveur
```

Avec Burp :
```
Navigateur ──► Burp (port 8080) ──► Serveur
```

---

## Lancer Burp Suite

```bash
# [Kali - terminal]
burpsuite &
```

- `&` — lance en arrière-plan pour garder le terminal libre

Ou depuis le menu Kali : Applications → Web Application Analysis → burpsuite

---

## Configuration du proxy navigateur

Burp écoute sur `127.0.0.1:8080` par défaut.
Tu dois dire à ton navigateur d'utiliser ce proxy.

**Dans Firefox :**
```
Paramètres → Réseau → Paramètres de connexion
→ Configuration manuelle du proxy
→ HTTP : 127.0.0.1  Port : 8080
→ Cocher "Utiliser ce proxy pour tous les protocoles"
```

**Ou avec FoxyProxy** (extension Firefox recommandée) :
- Installe FoxyProxy
- Ajoute un profil : `127.0.0.1:8080`
- Active/désactive en un clic

---

## Les onglets principaux

### Proxy
L'onglet central — intercepte les requêtes.

```
Proxy → Intercept → bouton "Intercept is on/off"
```

- **Intercept ON** → chaque requête est bloquée, tu peux la modifier avant de l'envoyer
- **Intercept OFF** → les requêtes passent sans être bloquées (mode observation)

### HTTP History
```
Proxy → HTTP History
```
Liste de toutes les requêtes qui ont transitié par Burp.
Tu peux cliquer sur chacune pour voir le détail requête/réponse.

### Repeater
Tu envoies une requête dans le Repeater pour la rejouer autant de fois que tu veux avec des modifications.

```
Clic droit sur une requête → Send to Repeater
```

Ensuite dans Repeater :
- Tu modifies la requête
- Tu cliques "Send"
- Tu vois la réponse
- Tu recommences

C'est là que tu fais tes tests d'injection manuellement.

### Intruder
Automatise des requêtes avec des payloads variables — équivalent de Hydra mais pour HTTP.

```
Clic droit sur une requête → Send to Intruder
```

Tu marques les paramètres à fuzzer avec `§` :
```
username=§admin§&password=§password§
```

Tu choisis une wordlist → Burp teste toutes les combinaisons.

### Scanner (version Pro uniquement)
Scan automatique de vulnérabilités — pas disponible en version Community gratuite.

---

## Workflow type en pentest web

```
1. Lancer Burp Suite
2. Configurer le proxy dans Firefox
3. Naviguer sur le site cible
4. Observer le HTTP History — comprendre la structure
5. Identifier les requêtes intéressantes (login, recherche, paramètres)
6. Send to Repeater → tester manuellement
7. Send to Intruder → automatiser si nécessaire
```

---

## Intercepter et modifier une requête

1. Intercept ON
2. Dans Firefox, clique sur un bouton ou soumets un formulaire
3. La requête apparaît dans Burp — elle est bloquée
4. Tu la modifies directement
5. Tu cliques "Forward" pour l'envoyer au serveur
6. Ou "Drop" pour l'annuler

---

## Certificat HTTPS

Pour intercepter le trafic HTTPS, Burp génère son propre certificat.
Il faut l'installer dans Firefox :

```
1. Firefox configuré sur le proxy Burp
2. Aller sur http://burpsuite (ou http://burp)
3. Télécharger le certificat CA
4. Firefox → Paramètres → Confidentialité → Certificats → Importer
```

---

## Raccourcis utiles

| Action | Raccourci |
|---|---|
| Forward la requête | `Ctrl+F` |
| Drop la requête | `Ctrl+D` |
| Envoyer au Repeater | `Ctrl+R` |
| Envoyer à l'Intruder | `Ctrl+I` |

---

## Burp vs curl

| | curl | Burp Suite |
|---|---|---|
| Usage | requêtes manuelles scriptées | interception visuelle |
| Modifier à la volée | non | oui |
| Voir l'historique | non | oui |
| Automatisation | scripts bash | Intruder |
| Interface | terminal | graphique |

En pratique tu utilises les deux — curl pour scripter, Burp pour explorer et tester manuellement.