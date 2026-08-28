# WireGuard — concepts et commandes de base

> WireGuard est un protocole VPN moderne — rapide, simple, open source.
> Crée un tunnel chiffré entre deux machines, même derrière NAT.
> Intégré dans le kernel Linux depuis 2020.

---

## Concept — comment ça marche

```
Machine A (toi)          Machine B (ami)
10.0.0.1/24    ←tunnel chiffré→    10.0.0.2/24
192.168.1.x                        192.168.2.x
(IP privée)                        (IP privée)
```

WireGuard crée une interface réseau virtuelle `wg0` sur chaque machine.
Les deux machines se voient comme si elles étaient sur le même réseau local —
peu importe où elles sont dans le monde.

---

## Clés cryptographiques

WireGuard utilise de la **cryptographie asymétrique** — comme SSH.

Chaque machine génère une paire de clés :
- **Clé privée** — secrète, ne part jamais
- **Clé publique** — partagée avec les autres

```bash
# Générer une paire de clés
wg genkey | tee privatekey | wg pubkey > publickey

cat privatekey    # ta clé privée — garde-la secrète
cat publickey     # ta clé publique — partage-la
```

---

## Installation

```bash
# [Kali / Ubuntu - terminal]
sudo apt install wireguard -y
```

---

## Configuration — deux rôles

### Serveur (celui qui a une IP publique)

```ini
# /etc/wireguard/wg0.conf

[Interface]
Address = 10.0.0.1/24          # IP virtuelle du serveur
ListenPort = 51820             # port d'écoute UDP
PrivateKey = CLE_PRIVEE_SERVEUR

# Pour chaque client :
[Peer]
PublicKey = CLE_PUBLIQUE_CLIENT
AllowedIPs = 10.0.0.2/32      # IP virtuelle autorisée pour ce client
```

### Client (derrière NAT)

```ini
# /etc/wireguard/wg0.conf

[Interface]
Address = 10.0.0.2/24          # IP virtuelle du client
PrivateKey = CLE_PRIVEE_CLIENT

[Peer]
PublicKey = CLE_PUBLIQUE_SERVEUR
Endpoint = IP_PUBLIQUE_SERVEUR:51820   # où se connecter
AllowedIPs = 10.0.0.0/24              # trafic à router dans le tunnel
PersistentKeepalive = 25              # maintient la connexion derrière NAT
```

---

## Commandes de base

```bash
# Démarrer l'interface WireGuard
sudo wg-quick up wg0

# Arrêter l'interface
sudo wg-quick down wg0

# Voir l'état de la connexion
sudo wg show

# Activer au démarrage
sudo systemctl enable wg-quick@wg0
```

---

## Ce que wg show affiche

```
interface: wg0
  public key: abc123...
  private key: (hidden)
  listening port: 51820

peer: xyz789...
  endpoint: 82.64.x.x:51820
  allowed ips: 10.0.0.2/32
  latest handshake: 5 seconds ago
  transfer: 1.23 MiB received, 456 KiB sent
```

- `latest handshake` — dernière fois que les deux machines ont communiqué
- `transfer` — données échangées

---

## WireGuard vs autres VPN

| | WireGuard | OpenVPN | IPsec |
|---|---|---|---|
| Lignes de code | ~4 000 | ~600 000 | complexe |
| Vitesse | très rapide | moyen | rapide |
| Config | simple | complexe | très complexe |
| Audit sécurité | facile | difficile | difficile |
| Port | UDP 51820 | UDP/TCP 1194 | UDP 500 |

WireGuard est plus simple et plus rapide — c'est pour ça qu'il est devenu la référence.

---

## Alternative sans config — Tailscale

Tailscale utilise WireGuard sous le capot mais sans configuration manuelle :

```bash
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up
```

T'installes sur les deux machines, vous vous connectez avec le même compte
→ réseau virtuel automatique, même derrière NAT.

Gratuit pour usage personnel, 100 appareils max.

---

## En hacking

WireGuard peut être utilisé pour du **pivot réseau** — une technique avancée :

```
Machine compromise ──WireGuard──► ton Kali
        ↓
Réseau interne accessible
```

Si tu compromets une machine derrière NAT, tu peux installer WireGuard dessus
et accéder au réseau interne depuis l'extérieur.
C'est un niveau avancé — OSCP et au-delà.