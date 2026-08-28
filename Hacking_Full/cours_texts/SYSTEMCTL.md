# systemctl — cheat sheet

> **system control** — gère les services et le système sur Linux moderne (systemd).
> Quasi universel sur Ubuntu, Debian, Kali, CentOS, Fedora...

---

## syntaxe de base

```bash
sudo systemctl [commande] [service]
```

---

## gestion des services

```bash
sudo systemctl start ssh          # démarrer un service
sudo systemctl stop ssh           # arrêter un service
sudo systemctl restart ssh        # arrêter puis redémarrer
sudo systemctl reload ssh         # recharger la config sans couper les connexions
sudo systemctl status ssh         # voir l'état détaillé du service
```

---

## démarrage automatique au boot

```bash
sudo systemctl enable ssh         # activer au démarrage
sudo systemctl disable ssh        # désactiver au démarrage
sudo systemctl enable --now ssh   # activer au boot ET démarrer maintenant
sudo systemctl disable --now ssh  # désactiver au boot ET arrêter maintenant
sudo systemctl is-enabled ssh     # vérifier si activé au boot
```

---

## informations sur un service

```bash
sudo systemctl status ssh         # état, PID, logs récents
sudo systemctl is-active ssh      # active / inactive
sudo systemctl is-failed ssh      # failed / active
systemctl show ssh                # toutes les propriétés du service
systemctl cat ssh                 # afficher le fichier unit du service
```

---

## lister les services

```bash
systemctl list-units              # tous les services actifs
systemctl list-units --type=service          # seulement les services
systemctl list-units --state=failed          # services en échec
systemctl list-unit-files                    # tous les services installés
systemctl list-unit-files --type=service     # avec leur état enable/disable
```

---

## gestion du système

```bash
sudo systemctl reboot             # redémarrer la machine
sudo systemctl poweroff           # éteindre
sudo systemctl halt               # arrêter sans couper l'alimentation
sudo systemctl suspend            # mettre en veille
```

---

## logs avec journalctl

`systemctl` s'utilise souvent avec `journalctl` pour voir les logs :

```bash
journalctl -u ssh                 # logs du service ssh
journalctl -u ssh -f              # logs en temps réel (comme tail -f)
journalctl -u ssh --since "1 hour ago"   # logs de la dernière heure
journalctl -u ssh -n 50           # 50 dernières lignes
journalctl -xe                    # logs système récents avec contexte
```

---

## services courants à connaître

| service | nom systemctl |
|---------|--------------|
| SSH | `ssh` ou `sshd` |
| Samba | `smbd` `nmbd` |
| Apache | `apache2` |
| Nginx | `nginx` |
| MySQL | `mysql` |
| PostgreSQL | `postgresql` |
| Docker | `docker` |
| Firewall | `ufw` |
| Cron | `cron` |

---

## exemples pratiques — sécurité

```bash
# vérifier si SSH tourne
sudo systemctl status ssh

# redémarrer après modification de sshd_config
sudo systemctl restart ssh

# redémarrer Samba après modification de smb.conf
sudo systemctl restart smbd nmbd

# voir si un service écoute bien après restart
ss -tlnp | grep ssh

# désactiver un service inutile (réduire surface d'attaque)
sudo systemctl disable --now cups    # imprimante — souvent inutile
sudo systemctl disable --now avahi-daemon  # mDNS — si pas nécessaire
```

---

## différence restart vs reload

| commande | comportement | quand l'utiliser |
|----------|-------------|-----------------|
| `restart` | coupe le service et le relance | modification config qui nécessite redémarrage complet |
| `reload` | recharge la config sans couper | modification config à chaud — connexions existantes maintenues |

SSH supporte `reload` — les connexions actives ne sont pas coupées.
Samba nécessite `restart` pour appliquer les changements de `smb.conf`.

---

## ancienne syntaxe — fonctionne encore

```bash
sudo service ssh restart          # équivalent de systemctl restart ssh
sudo service ssh status           # équivalent de systemctl status ssh
```

Compatible avec les vieux scripts et les systèmes sans systemd.




# service — commandes de base

> `service` est l'ancien système de gestion des services sur Linux.
> Utilisé sur les vieilles distros (Ubuntu < 15, Debian < 8, Metasploitable...).
> Les distros modernes utilisent `systemctl` à la place.

---

## Commandes de base

```bash
sudo service nom status     # affiche l'état du service
sudo service nom start      # démarre le service
sudo service nom stop       # arrête le service
sudo service nom restart    # redémarre le service
sudo service nom reload     # recharge la config sans redémarrer
```

---

## Exemples concrets

```bash
sudo service vsftpd status
sudo service vsftpd start
sudo service apache2 restart
sudo service ssh stop
sudo service samba restart
```

---

## service vs systemctl

| `service` | `systemctl` |
|---|---|
| vieilles distros | distros modernes |
| `service nom start` | `systemctl start nom` |
| `service nom stop` | `systemctl stop nom` |
| `service nom status` | `systemctl status nom` |
| `service nom restart` | `systemctl restart nom` |

Sur les distros modernes `service` existe encore mais redirige vers `systemctl` automatiquement.

---

## Lister les services qui tournent

```bash
# vieilles distros
service --status-all

# distros modernes
systemctl list-units --type=service --state=running
```

---

## Activer/désactiver au démarrage

```bash
# vieilles distros
update-rc.d nom enable    # démarre automatiquement au boot
update-rc.d nom disable   # ne démarre plus au boot

# distros modernes
systemctl enable nom
systemctl disable nom
```
