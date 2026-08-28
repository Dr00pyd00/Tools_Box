
# enum4linux

Lander le scan:
```bash 
enum4linux 192.168.78.129
```

## Output sections

### lancement

```bash
]
└─$ enum4linux 192.168.78.129
Starting enum4linux v0.9.1 ( http://labs.portcullis.co.uk/application/enum4linux/ ) on Sat Apr  4 08:16:26 2026
```
---

### 1. Target Information

```bash
 =========================================( Target Information )=========================================                                                                             
                                                                                             
Target ........... 192.168.78.129                                                            
RID Range ........ 500-550,1000-1050
Username ......... ''
Password ......... ''
Known Usernames .. administrator, guest, krbtgt, domain admins, root, bin, none

```

`RID`: **relativeIDentifier** = numero unique de chaque utilisateur/groupe sur la machine.  
`enum4linux`: va scanner 2 plages:
- `500-550`: plage reservée aux comptes systeme (pas les users normaux) window/samba : 500=**Administrator**  | 501=**Guest**  (toujours)
- `1000-1050`: plage des comptes utilisateurs normaux creer sur la machine => `uid`=1000 -> premier vrai utilisateur humain.
---

Tentative de coonection avec identifiants **vides**:
```bash
Username ......... ''
Password ......... ''
```

Liste de noms que enum4linux tentera en priorité lors de l'énumération — ce sont des noms universellement communs sur Windows et Linux. krbtgt est spécifique à Active Directory (Kerberos). Il les teste pour voir lesquels existent réellement sur la cible:
```bash
Known Usernames .. administrator, guest, krbtgt, domain admins, root, bin, none
```

---

### 2. Enumerating Workgroup/Domain

```bash

 ===========================( Enumerating Workgroup/Domain on 192.168.78.129 )===========================                                                                                                            
                                                            
[+] Got domain/workgroup name: WORKGROUP                                                     
```



**Workgroup** = **groupe de travail** — un regroupement logique de machines sur un réseau local.

Il y a deux modes possibles :

**Mode Workgroup** (ce qu'on voit ici) — chaque machine gère ses propres utilisateurs localement. Pas de serveur central. C'est la config typique d'un réseau domestique ou d'une petite structure. `WORKGROUP` est le nom par défaut sur Windows et Samba quand rien n'a été configuré.

**Mode Domain** (Active Directory) — il y a un serveur central (contrôleur de domaine) qui gère tous les utilisateurs et toutes les machines. C'est la config typique en entreprise. Le nom serait quelque chose comme `CONTOSO` ou `MONENTREPRISE`.

Pour un attaquant la différence est importante — en mode Domain, compromettre le contrôleur de domaine donne accès à **toutes** les machines du réseau d'un coup. En mode Workgroup, chaque machine est indépendante. 

---


### 3. Nbtstat Information 

```bash
                                                                                          
 ===============================( Nbtstat Information for 192.168.78.129 )===============================                                                                                 
                                                                                             
Looking up status of 192.168.78.129                                                          
        METASPLOITABLE  <00> -         B <ACTIVE>  Workstation Service
        METASPLOITABLE  <03> -         B <ACTIVE>  Messenger Service
        METASPLOITABLE  <20> -         B <ACTIVE>  File Server Service
        ..__MSBROWSE__. <01> - <GROUP> B <ACTIVE>  Master Browser
        WORKGROUP       <00> - <GROUP> B <ACTIVE>  Domain/Workgroup Name
        WORKGROUP       <1d> -         B <ACTIVE>  Master Browser
        WORKGROUP       <1e> - <GROUP> B <ACTIVE>  Browser Service Elections

        MAC Address = 00-00-00-00-00-00

```


**NBT** = **N**et**B**IOS over **T**CP/IP — un ancien protocole Microsoft de nommage réseau, qui permet aux machines de s'annoncer et de se trouver sur un réseau local. Precède le DNS — avant le DNS c'était lui qui résolvait les noms de machines.

---

Chaque ligne suit ce format :
```
NOM  <CODE>  -  [GROUP]  B  <ACTIVE>  Description
```

- **NOM** = nom NetBIOS de la machine ou du groupe
- **`<CODE>`** = type de service en hexadécimal
- **GROUP** = appartient à un groupe (plusieurs machines) sinon c'est unique
- **B** = **B**roadcast — mode de diffusion sur le réseau local
- **ACTIVE** = service actuellement en cours d'exécution

---

Ligne par ligne :

```
METASPLOITABLE  <00>  Workstation Service
```
La machine est joignable sur le réseau. C'est le service de base — annonce son existence.

```
METASPLOITABLE  <03>  Messenger Service
```
Ancien service de messagerie réseau Windows (le `net send` de Windows XP). Inutile aujourd'hui mais toujours actif ici.

```
METASPLOITABLE  <20>  File Server Service
```
**Le plus important.** `<20>` = serveur de fichiers SMB actif. Confirme qu'on peut s'y connecter pour partager des fichiers.

```
..__MSBROWSE__.  <01>  Master Browser
```
**Master Browser** = la machine qui tient à jour la liste de toutes les machines du réseau local. C'est elle que les autres interrogent pour savoir qui est connecté. Ici Metasploitable joue ce rôle.

```
WORKGROUP  <00>  Domain/Workgroup Name
```
Annonce le nom du groupe de travail auquel appartient la machine.

```
WORKGROUP  <1d>  Master Browser
```
Confirme que Metasploitable est le Master Browser du workgroup WORKGROUP.

```
WORKGROUP  <1e>  Browser Service Elections
```
Service qui gère les **élections** — quand plusieurs machines sont sur le réseau, elles négocient entre elles laquelle sera le Master Browser. C'est automatique.

```
MAC Address = 00-00-00-00-00-00
```
Adresse MAC nulle — signe que c'est une machine **virtualisée**. VMware masque la vraie adresse MAC dans les réponses NetBIOS. 😄

---

### 4. Session Check

```bash

 ==================================( Session Check on 192.168.78.129 )==================================                                                                                  
                                                                                             
                                                                                             
[+] Server 192.168.78.129 allows sessions using username '', password ''         
```

```
Server allows sessions using username '', password ''
```

**C'est le test le plus important de tout enum4linux.**

Enum4linux tente une connexion avec username vide et password vide — c'est ce qu'on appelle une **null session** (session nulle).

Deux résultats possibles :

**`[+]` = succès** (ce qu'on voit ici) — la machine accepte les connexions anonymes. Tous les blocs suivants — users, groupes, partages, politique de mots de passe — deviennent accessibles. C'est la porte d'entrée de tout.

**`[-]` = échec** — la machine refuse les null sessions. Enum4linux s'arrête pratiquement là, peu d'infos récupérables.

Sur une machine bien configurée en production cette ligne serait `[-]`. Sur Metasploitable c'est volontairement `[+]` — c'est une des failles de base de la machine. 😄

---

### 5. Getting domain SID 


```bash
                                                                                        
 ===============================( Getting domain SID for 192.168.78.129 )===============================                                                                                  
                                                                                             
Domain Name: WORKGROUP                                                                       
Domain Sid: (NULL SID)

[+] Can't determine if host is part of domain or part of a workgroup                         
                                                                                
```


```
Domain Name: WORKGROUP
Domain Sid: (NULL SID)
Can't determine if host is part of domain or part of a workgroup
```

**SID** = **S**ecurity **Id**entifier — identifiant unique cryptographique attribué à chaque domaine Windows/Samba. Il ressemble à ça :

```
S-1-5-21-1042354039-2475377354-766472396
```

On le verra dans le bloc RID Cycling plus tard.

---

Ici `NULL SID` = Samba n'a pas de vrai domaine configuré. C'est cohérent avec `WORKGROUP` — pas de domaine Active Directory, donc pas de SID de domaine propre.

---

`Can't determine if host is part of domain or part of a workgroup` — enum4linux est un peu perdu parce que normalement :

- **Workgroup** → pas de SID
- **Domain** → SID présent

Mais Samba en mode workgroup peut quand même générer un SID local — donc enum4linux ne sait pas trop comment classifier ça. C'est une limitation de l'outil, pas un problème réel. 😄

---

### 6. OS information 

```bash
                                                                                       
 ==================================( OS information on 192.168.78.129 )==================================                                                                                 
                                                                                             
                                                                                             
[E] Can't get OS info with smbclient                                                         
                                                                                             
                                                                                             
[+] Got OS info for 192.168.78.129 from srvinfo:                                             
        METASPLOITABLE Wk Sv PrQ Unx NT SNT metasploitable server (Samba 3.0.20-Debian)      
        platform_id     :       500
        os version      :       4.9
        server type     :       0x9a03


```


```
[E] Can't get OS info with smbclient
```
Enum4linux a d'abord essayé de récupérer les infos OS via `smbclient` — ça a échoué. Probablement une incompatibilité de protocole entre la version moderne de smbclient sur Kali et le vieux Samba 3.0.20 sur Metasploitable.

---

```
[+] Got OS info for 192.168.78.129 from srvinfo:
```
Plan B — il utilise `rpcclient` avec la commande `srvinfo` (**srv**er **info**rmation) à la place. Ça a marché.

---

```
METASPLOITABLE Wk Sv PrQ Unx NT SNT metasploitable server (Samba 3.0.20-Debian)
```

Le nom de la machine suivi de flags abrégés qui décrivent ses capacités :
- `Wk` = **W**or**k**station — peut agir comme poste de travail
- `Sv` = **S**er**v**er — peut agir comme serveur
- `PrQ` = **Pr**int **Q**ueue — gère une file d'impression
- `Unx` = **Un**i**x** — c'est un système Linux/Unix
- `NT` = compatible protocole **NT** (protocole SMB Microsoft)
- `SNT` = **S**amba **NT** server

Et la partie la plus importante : **`Samba 3.0.20-Debian`** — version exacte. En vrai pentest tu cherches immédiatement `CVE Samba 3.0.20` — cette version a un exploit public dans Metasploit. 🎯

---

```
platform_id : 500
os version  : 4.9
server type : 0x9a03
```

- `platform_id 500` = code Microsoft pour "c'est un serveur Unix/Linux"
- `os version 4.9` = version du kernel Linux telle que rapportée par Samba — approximative, pas fiable
- `server type 0x9a03` = valeur hexadécimale qui encode les mêmes flags que `Wk Sv PrQ Unx NT SNT` ci-dessus, mais en binaire pour les machines 😄


---

### 7. Users

```bash

 ======================================( Users on 192.168.78.129 )======================================                                                                                  
                                                                                             
index: 0x1 RID: 0x3f2 acb: 0x00000011 Account: games    Name: games     Desc: (null)         
index: 0x2 RID: 0x1f5 acb: 0x00000011 Account: nobody   Name: nobody    Desc: (null)
index: 0x3 RID: 0x4ba acb: 0x00000011 Account: bind     Name: (null)    Desc: (null)
index: 0x4 RID: 0x402 acb: 0x00000011 Account: proxy    Name: proxy     Desc: (null)
index: 0x5 RID: 0x4b4 acb: 0x00000011 Account: syslog   Name: (null)    Desc: (null)
index: 0x6 RID: 0xbba acb: 0x00000010 Account: user     Name: just a user,111,, Desc: (null)
index: 0x7 RID: 0x42a acb: 0x00000011 Account: www-data Name: www-data  Desc: (null)
index: 0x8 RID: 0x3e8 acb: 0x00000011 Account: root     Name: root      Desc: (null)
index: 0x9 RID: 0x3fa acb: 0x00000011 Account: news     Name: news      Desc: (null)
index: 0xa RID: 0x4c0 acb: 0x00000011 Account: postgres Name: PostgreSQL administrator,,,   Desc: (null)
index: 0xb RID: 0x3ec acb: 0x00000011 Account: bin      Name: bin       Desc: (null)
index: 0xc RID: 0x3f8 acb: 0x00000011 Account: mail     Name: mail      Desc: (null)
index: 0xd RID: 0x4c6 acb: 0x00000011 Account: distccd  Name: (null)    Desc: (null)
index: 0xe RID: 0x4ca acb: 0x00000011 Account: proftpd  Name: (null)    Desc: (null)
index: 0xf RID: 0x4b2 acb: 0x00000011 Account: dhcp     Name: (null)    Desc: (null)
index: 0x10 RID: 0x3ea acb: 0x00000011 Account: daemon  Name: daemon    Desc: (null)
index: 0x11 RID: 0x4b8 acb: 0x00000011 Account: sshd    Name: (null)    Desc: (null)
index: 0x12 RID: 0x3f4 acb: 0x00000011 Account: man     Name: man       Desc: (null)
index: 0x13 RID: 0x3f6 acb: 0x00000011 Account: lp      Name: lp        Desc: (null)
index: 0x14 RID: 0x4c2 acb: 0x00000011 Account: mysql   Name: MySQL Server,,,   Desc: (null)
index: 0x15 RID: 0x43a acb: 0x00000011 Account: gnats   Name: Gnats Bug-Reporting System (admin)     Desc: (null)
index: 0x16 RID: 0x4b0 acb: 0x00000011 Account: libuuid Name: (null)    Desc: (null)
index: 0x17 RID: 0x42c acb: 0x00000011 Account: backup  Name: backup    Desc: (null)
index: 0x18 RID: 0xbb8 acb: 0x00000010 Account: msfadmin        Name: msfadmin,,,       Desc: (null)
index: 0x19 RID: 0x4c8 acb: 0x00000011 Account: telnetd Name: (null)    Desc: (null)
index: 0x1a RID: 0x3ee acb: 0x00000011 Account: sys     Name: sys       Desc: (null)
index: 0x1b RID: 0x4b6 acb: 0x00000011 Account: klog    Name: (null)    Desc: (null)
index: 0x1c RID: 0x4bc acb: 0x00000011 Account: postfix Name: (null)    Desc: (null)
index: 0x1d RID: 0xbbc acb: 0x00000011 Account: service Name: ,,,       Desc: (null)
index: 0x1e RID: 0x434 acb: 0x00000011 Account: list    Name: Mailing List Manager      Desc: (null)
index: 0x1f RID: 0x436 acb: 0x00000011 Account: irc     Name: ircd      Desc: (null)
index: 0x20 RID: 0x4be acb: 0x00000011 Account: ftp     Name: (null)    Desc: (null)
index: 0x21 RID: 0x4c4 acb: 0x00000011 Account: tomcat55        Name: (null)    Desc: (null)
index: 0x22 RID: 0x3f0 acb: 0x00000011 Account: sync    Name: sync      Desc: (null)
index: 0x23 RID: 0x3fc acb: 0x00000011 Account: uucp    Name: uucp      Desc: (null)

user:[games] rid:[0x3f2]
user:[nobody] rid:[0x1f5]
user:[bind] rid:[0x4ba]
user:[proxy] rid:[0x402]
user:[syslog] rid:[0x4b4]
user:[user] rid:[0xbba]
user:[www-data] rid:[0x42a]
user:[root] rid:[0x3e8]
user:[news] rid:[0x3fa]
user:[postgres] rid:[0x4c0]
user:[bin] rid:[0x3ec]
user:[mail] rid:[0x3f8]
user:[distccd] rid:[0x4c6]
user:[proftpd] rid:[0x4ca]
user:[dhcp] rid:[0x4b2]
user:[daemon] rid:[0x3ea]
user:[sshd] rid:[0x4b8]
user:[man] rid:[0x3f4]
user:[lp] rid:[0x3f6]
user:[mysql] rid:[0x4c2]
user:[gnats] rid:[0x43a]
user:[libuuid] rid:[0x4b0]
user:[backup] rid:[0x42c]
user:[msfadmin] rid:[0xbb8]
user:[telnetd] rid:[0x4c8]
user:[sys] rid:[0x3ee]
user:[klog] rid:[0x4b6]
user:[postfix] rid:[0x4bc]
user:[service] rid:[0xbbc]
user:[list] rid:[0x434]
user:[irc] rid:[0x436]
user:[ftp] rid:[0x4be]
user:[tomcat55] rid:[0x4c4]
user:[sync] rid:[0x3f0]
user:[uucp] rid:[0x3fc]

```

**Vue détaillée — chaque champ expliqué**

```
index: 0x1 RID: 0x3f2 acb: 0x00000011 Account: games  Name: games  Desc: (null)
```

- `index` = numéro d'ordre dans la liste retournée par Samba — pas important
- `RID` = **R**elative **ID**entifier — identifiant numérique unique de l'utilisateur en hexadécimal. `0x3f2` = 1010 en décimal
- `acb` = **A**ccount **C**ontrol **B**its — flags qui décrivent l'état du compte
- `Account` = le nom de login
- `Name` = le nom complet affiché (peut être vide)
- `Desc` = description du compte

---

**ACB — les deux valeurs qu'on voit ici :**

`0x00000011` = compte **désactivé** — compte système, pas de login possible. C'est le cas de la grande majorité : `games`, `nobody`, `root`, `bin`, `www-data`, `postgres`, `mysql`...

`0x00000010` = compte **actif** — peut se connecter. Seulement **deux** comptes dans toute la liste :
- `user` (RID `0xbba`) — Name: `just a user,111,,`
- `msfadmin` (RID `0xbb8`) — Name: `msfadmin,,,`

Ce sont les **deux seules cibles valides** pour une attaque brute force SSH ou SMB.

---

**Vue condensée — pourquoi elle existe :**

```
user:[games] rid:[0x3f2]
user:[msfadmin] rid:[0xbb8]
```

C'est la même liste mais sans les détails `acb`, `Name`, `Desc`. Enum4linux l'affiche en double parce qu'elle vient d'une **deuxième requête** différente — la vue détaillée vient de `querydispinfo`, la vue condensée vient de `enumdomusers`. Deux méthodes d'énumération, même résultat — si l'une échoue l'autre peut réussir.

Format pratique pour scripter — tu peux parser `user:[xxx]` facilement pour extraire juste les noms. 😄


---

### 8. Share Enumeration

```bash

 ================================( Share Enumeration on 192.168.78.129 )================================                                                                                  
                                                                                             
                                                                                             
        Sharename       Type      Comment
        ---------       ----      -------
        print$          Disk      Printer Drivers
        tmp             Disk      oh noes!
        opt             Disk      
        IPC$            IPC       IPC Service (metasploitable server (Samba 3.0.20-Debian))
        ADMIN$          IPC       IPC Service (metasploitable server (Samba 3.0.20-Debian))
Reconnecting with SMB1 for workgroup listing.

        Server               Comment
        ---------            -------

        Workgroup            Master
        ---------            -------
        WORKGROUP            METASPLOITABLE

[+] Attempting to map shares on 192.168.78.129                                               
                                                                                             
//192.168.78.129/print$ Mapping: DENIED Listing: N/A Writing: N/A                            
//192.168.78.129/tmp    Mapping: OK Listing: OK Writing: N/A
//192.168.78.129/opt    Mapping: DENIED Listing: N/A Writing: N/A

[E] Can't understand response:                                                               
                                                                                             
NT_STATUS_NETWORK_ACCESS_DENIED listing \*                                                   
//192.168.78.129/IPC$   Mapping: N/A Listing: N/A Writing: N/A
//192.168.78.129/ADMIN$ Mapping: DENIED Listing: N/A Writing: N/A

```

**Tableau des partages — chaque colonne :**

```
Sharename    Type    Comment
print$       Disk    Printer Drivers
tmp          Disk    oh noes!
opt          Disk    
IPC$         IPC     IPC Service (metasploitable server (Samba 3.0.20-Debian))
ADMIN$       IPC     IPC Service (metasploitable server (Samba 3.0.20-Debian))
```

- `Sharename` = nom du partage — ce qu'on tape dans `smbclient //IP/nom`
- `Type` = `Disk` = partage de fichiers / `IPC` = canal de communication interne (pas de fichiers)
- `Comment` = description libre configurée dans `smb.conf`

Le `$` à la fin d'un nom = partage **caché** — n'apparaît pas dans l'explorateur Windows, mais existe quand même. On peut s'y connecter si on connaît le nom.

`oh noes!` sur `tmp` = quelqu'un savait que c'était une faille et a laissé ce message ironique dans le `comment` de `smb.conf`. 😄

---

**Les cinq partages un par un :**

`print$` = partage standard Samba qui contient les drivers d'imprimantes. Présent par défaut sur toute installation Samba.

`tmp` = le dossier `/tmp` de la machine partagé anonymement. `/tmp` est public par définition sur Linux — `chmod 777` par défaut. Vecteur d'attaque direct.

`opt` = le dossier `/opt` partagé. `/opt` c'est là où s'installent les logiciels tiers sur Linux.

`IPC$` = **I**nter**P**rocess **C**ommunication — canal spécial utilisé par Samba pour les communications internes. C'est via `IPC$` qu'enum4linux récupère toutes les infos : users, groupes, politique de mots de passe. Pas un vrai partage de fichiers — on ne peut pas y naviguer.

`ADMIN$` = partage administratif qui pointe vers le dossier système. Sur Windows c'est `C:\Windows`. Toujours présent, normalement réservé aux admins.

---

**`Reconnecting with SMB1 for workgroup listing`**

Enum4linux se reconnecte en forçant le protocole **SMB1** — l'ancienne version de SMB — pour récupérer la liste des machines du workgroup. SMB1 est désactivé sur les systèmes modernes pour des raisons de sécurité (c'est lui qu'exploitait WannaCry), mais Metasploitable le supporte encore.

```
Workgroup      Master
WORKGROUP      METASPLOITABLE
```
Confirme que `METASPLOITABLE` est le **Master Browser** du workgroup — c'est elle qui tient la liste des machines du réseau.

---

**Test d'accès sur chaque partage :**

- `Mapping` = peut-on **se connecter** au partage
- `Listing` = peut-on **lister** les fichiers dedans
- `Writing` = peut-on **écrire** dedans

```
print$   Mapping: DENIED              → bloqué dès la connexion
tmp      Mapping: OK  Listing: OK     → accessible et navigable ✅
opt      Mapping: DENIED              → bloqué
IPC$     Mapping: N/A                 → pas un vrai partage, pas de test possible
ADMIN$   Mapping: DENIED              → bloqué
```

`tmp` est le seul partage accessible anonymement. `Writing: N/A` ne veut pas dire qu'on ne peut pas écrire — ça veut dire qu'enum4linux n'a pas testé l'écriture. On sait d'expérience qu'on peut y faire `put` car `/tmp` est `777`. 😄


### 9.  Password Policy Information

```bash

 ===========================( Password Policy Information for 192.168.78.129 )===========================                                                                                 
                                                                                             
Password:                                                                                    


[+] Attaching to 192.168.78.129 using a NULL share

[+] Trying protocol 139/SMB...

[+] Found domain(s):

        [+] METASPLOITABLE
        [+] Builtin

[+] Password Info for Domain: METASPLOITABLE

        [+] Minimum password length: 5
        [+] Password history length: None
        [+] Maximum password age: Not Set
        [+] Password Complexity Flags: 000000

                [+] Domain Refuse Password Change: 0
                [+] Domain Password Store Cleartext: 0
                [+] Domain Password Lockout Admins: 0
                [+] Domain Password No Clear Change: 0
                [+] Domain Password No Anon Change: 0
                [+] Domain Password Complex: 0

        [+] Minimum password age: None
        [+] Reset Account Lockout Counter: 30 minutes 
        [+] Locked Account Duration: 30 minutes 
        [+] Account Lockout Threshold: None
        [+] Forced Log off Time: Not Set



[+] Retieved partial password policy with rpcclient:                                         
                                                                                             
                                                                                             
Password Complexity: Disabled                                                                
Minimum Password Length: 0

```

**Comment enum4linux récupère ces infos :**

```
Password:
[+] Attaching to 192.168.78.129 using a NULL share
[+] Trying protocol 139/SMB...
```

`Password:` — c'est enum4linux qui pose la question à Samba, pas à toi. Il tente une connexion null session via le port **139** (**NetBIOS over TCP**) — l'ancien port SMB, avant que le 445 existe. Metasploitable supporte les deux.

`NULL share` = connexion anonyme sans identifiants, exactement comme le Session Check vu plus tôt.

---

**Les domaines trouvés :**

```
[+] Found domain(s):
    [+] METASPLOITABLE
    [+] Builtin
```

`METASPLOITABLE` = le domaine local de la machine — là où vivent les vrais utilisateurs.

`Builtin` = domaine réservé aux groupes système prédéfinis par Windows/Samba (`Administrators`, `Users`, `Guests`...). Présent sur toute installation, c'est automatique.

---

**La politique de mots de passe — ligne par ligne :**

```
Minimum password length: 5
```
Mots de passe de minimum 5 caractères. Très court — `admin`, `12345` sont valides. Facilite le brute force.

```
Password history length: None
```
Pas d'historique — on peut réutiliser le même mot de passe indéfiniment. Un utilisateur peut changer son mdp et remettre le même juste après.

```
Maximum password age: Not Set
```
Pas d'expiration — les mots de passe ne forcent jamais un changement. Un mdp faible peut rester en place des années.

```
Password Complexity Flags: 000000
```
Six flags tous à zéro — aucune règle de complexité. Chaque flag correspond à une contrainte :
- majuscules requises → 0
- chiffres requis → 0
- caractères spéciaux requis → 0
- etc.

```
Domain Refuse Password Change: 0
```
La machine accepte les changements de mot de passe à distance via SMB.

```
Domain Password Store Cleartext: 0
```
Les mots de passe ne sont **pas** stockés en clair — ils sont hashés. `0` = bonne pratique respectée ici.

```
Domain Password Lockout Admins: 0
```
Les admins peuvent aussi être verrouillés — pas de protection spéciale pour eux.

```
Domain Password No Clear Change: 0
```
Autorise les changements de mdp via protocoles non chiffrés.

```
Domain Password No Anon Change: 0
```
**Important** — autorise les changements de mdp anonymement. N'importe qui peut tenter de changer un mot de passe sans être authentifié.

```
Domain Password Complex: 0
```
Confirme — complexité désactivée.

---

```
Minimum password age: None
Reset Account Lockout Counter: 30 minutes
Locked Account Duration: 30 minutes
Account Lockout Threshold: None
Forced Log off Time: Not Set
```

`Minimum password age: None` = on peut changer son mdp autant de fois qu'on veut sans délai.

`Reset Account Lockout Counter: 30 minutes` = si des tentatives ratées ont été comptées, le compteur se remet à zéro après 30 minutes.

`Locked Account Duration: 30 minutes` = si un compte est verrouillé, il se déverrouille après 30 minutes.

`Account Lockout Threshold: None` = **le plus critique** — pas de seuil de verrouillage défini. Les deux lignes au-dessus parlent de verrouillage mais celui-ci dit que le verrouillage ne se déclenche jamais. On peut tenter **infiniment** de mots de passe sans jamais bloquer le compte. Brute force sans limite. 🎯

`Forced Log off Time: Not Set` = pas de déconnexion forcée après un certain temps.

---

```
Password Complexity: Disabled
Minimum Password Length: 0
```

Récupéré via `rpcclient` — une deuxième méthode de vérification. Et là `Minimum Password Length: 0` — encore plus permissif que les `5` d'avant. Un mot de passe **vide** est techniquement accepté. 😄



### 10. Groups

```bash


 ======================================( Groups on 192.168.78.129 )======================================                                                                                 
                                                                                             
                                                                                             
[+] Getting builtin groups:                                                                  
                                                                                             
                                                                                             
[+]  Getting builtin group memberships:                                                      
                                                                                             
                                                                                             
[+]  Getting local groups:                                                                   
                                                                                             
                                                                                             
[+]  Getting local group memberships:                                                        
                                                                                             
                                                                                             
[+]  Getting domain groups:                                                                  
                                                                                             
                                                                                             
[+]  Getting domain group memberships:                                                       
                                                                         
```


```
[+] Getting builtin groups:
[+] Getting builtin group memberships:
[+] Getting local groups:
[+] Getting local group memberships:
[+] Getting domain groups:
[+] Getting domain group memberships:
```

Enum4linux tente de récupérer trois catégories de groupes :

**Builtin groups** = groupes prédéfinis par Samba/Windows — `Administrators`, `Users`, `Guests`, `Backup Operators`... Ils existent sur toute installation automatiquement.

**Local groups** = groupes créés manuellement sur cette machine — par exemple `sambashare`, `admin` qu'on avait vus dans le `id` de msfadmin.

**Domain groups** = groupes du domaine — `Domain Admins`, `Domain Users`... On les verra dans le bloc RID Cycling juste après.

---

**Pourquoi tout est vide ici ?**

Samba 3.0.20 dans cette configuration ne retourne pas les groupes via cette méthode d'interrogation. Ce n'est pas qu'il n'y a pas de groupes — c'est que cette version répond pas correctement à ces requêtes spécifiques.

Ce n'est pas un échec total — les groupes apparaîtront quand même dans le bloc **RID Cycling** qui suit, via une méthode différente. 😄



### 11.  Users

```bash
                                                                                      
                                                                                             
 =================( Users on 192.168.78.129 via RID cycling (RIDS: 500-550,1000-1050) )=================                                                                                  
                                                                                             
                                                                                             
[I] Found new SID:                                                                           
S-1-5-21-1042354039-2475377354-766472396                                                     

[+] Enumerating users using SID S-1-5-21-1042354039-2475377354-766472396 and logon username '', password ''                                                                               
                                                                                             
S-1-5-21-1042354039-2475377354-766472396-500 METASPLOITABLE\Administrator (Local User)       
S-1-5-21-1042354039-2475377354-766472396-501 METASPLOITABLE\nobody (Local User)
S-1-5-21-1042354039-2475377354-766472396-512 METASPLOITABLE\Domain Admins (Domain Group)
S-1-5-21-1042354039-2475377354-766472396-513 METASPLOITABLE\Domain Users (Domain Group)
S-1-5-21-1042354039-2475377354-766472396-514 METASPLOITABLE\Domain Guests (Domain Group)
S-1-5-21-1042354039-2475377354-766472396-1000 METASPLOITABLE\root (Local User)
S-1-5-21-1042354039-2475377354-766472396-1001 METASPLOITABLE\root (Domain Group)
S-1-5-21-1042354039-2475377354-766472396-1002 METASPLOITABLE\daemon (Local User)
S-1-5-21-1042354039-2475377354-766472396-1003 METASPLOITABLE\daemon (Domain Group)
S-1-5-21-1042354039-2475377354-766472396-1004 METASPLOITABLE\bin (Local User)
S-1-5-21-1042354039-2475377354-766472396-1005 METASPLOITABLE\bin (Domain Group)
S-1-5-21-1042354039-2475377354-766472396-1006 METASPLOITABLE\sys (Local User)
S-1-5-21-1042354039-2475377354-766472396-1007 METASPLOITABLE\sys (Domain Group)
S-1-5-21-1042354039-2475377354-766472396-1008 METASPLOITABLE\sync (Local User)
S-1-5-21-1042354039-2475377354-766472396-1009 METASPLOITABLE\adm (Domain Group)
S-1-5-21-1042354039-2475377354-766472396-1010 METASPLOITABLE\games (Local User)
S-1-5-21-1042354039-2475377354-766472396-1011 METASPLOITABLE\tty (Domain Group)
S-1-5-21-1042354039-2475377354-766472396-1012 METASPLOITABLE\man (Local User)
S-1-5-21-1042354039-2475377354-766472396-1013 METASPLOITABLE\disk (Domain Group)
S-1-5-21-1042354039-2475377354-766472396-1014 METASPLOITABLE\lp (Local User)
S-1-5-21-1042354039-2475377354-766472396-1015 METASPLOITABLE\lp (Domain Group)
S-1-5-21-1042354039-2475377354-766472396-1016 METASPLOITABLE\mail (Local User)
S-1-5-21-1042354039-2475377354-766472396-1017 METASPLOITABLE\mail (Domain Group)
S-1-5-21-1042354039-2475377354-766472396-1018 METASPLOITABLE\news (Local User)
S-1-5-21-1042354039-2475377354-766472396-1019 METASPLOITABLE\news (Domain Group)
S-1-5-21-1042354039-2475377354-766472396-1020 METASPLOITABLE\uucp (Local User)
S-1-5-21-1042354039-2475377354-766472396-1021 METASPLOITABLE\uucp (Domain Group)
S-1-5-21-1042354039-2475377354-766472396-1025 METASPLOITABLE\man (Domain Group)
S-1-5-21-1042354039-2475377354-766472396-1026 METASPLOITABLE\proxy (Local User)
S-1-5-21-1042354039-2475377354-766472396-1027 METASPLOITABLE\proxy (Domain Group)
S-1-5-21-1042354039-2475377354-766472396-1031 METASPLOITABLE\kmem (Domain Group)
S-1-5-21-1042354039-2475377354-766472396-1041 METASPLOITABLE\dialout (Domain Group)
S-1-5-21-1042354039-2475377354-766472396-1043 METASPLOITABLE\fax (Domain Group)
S-1-5-21-1042354039-2475377354-766472396-1045 METASPLOITABLE\voice (Domain Group)
S-1-5-21-1042354039-2475377354-766472396-1049 METASPLOITABLE\cdrom (Domain Group)

```

**C'est quoi le RID Cycling ?**

La technique consiste à envoyer des requêtes à Samba en incrémentant le RID un par un :
- "Qui est le RID 500 ?" → `Administrator`
- "Qui est le RID 501 ?" → `nobody`
- "Qui est le RID 502 ?" → rien
- "Qui est le RID 503 ?" → rien
- ...jusqu'à 550, puis 1000 à 1050

Pour chaque RID qui existe, Samba répond avec le nom. Pour ceux qui n'existent pas, il ne répond pas. C'est une méthode différente de l'énumération classique du bloc Users — elle permet de trouver des comptes qui n'auraient pas été retournés par `querydispinfo`.

---

**Le SID :**

```
S-1-5-21-1042354039-2475377354-766472396
```

Structure d'un SID complet :
- `S` = **S**ecurity identifier — préfixe fixe
- `1` = version du format SID — toujours 1
- `5` = autorité = Microsoft
- `21` = machine ou domaine ordinaire (pas un compte builtin)
- `1042354039-2475377354-766472396` = trois nombres générés aléatoirement à l'installation — identifient cette machine de manière unique dans le monde

Pour obtenir le SID complet d'un utilisateur on ajoute son RID à la fin :
```
S-1-5-21-1042354039-2475377354-766472396-1000  →  root
```

---

**Les RIDs fixes — conventions universelles :**

```
-500  Administrator   → toujours, sur toute machine Windows/Samba
-501  nobody/Guest    → toujours
-512  Domain Admins   → toujours
-513  Domain Users    → toujours
-514  Domain Guests   → toujours
```

Ces RIDs sont **gravés dans la spec Microsoft** — ils ne changent jamais. Un attaquant qui trouve le SID d'une machine peut immédiatement cibler `SID-500` pour atteindre l'Administrator, même sans connaître le nom exact du compte. 🎯

---

**RIDs 1000+ — comptes normaux :**

```
-1000  root          (Local User)
-1002  daemon        (Local User)
-1004  bin           (Local User)
-1006  sys           (Local User)
-1008  sync          (Local User)
-1010  games         (Local User)
-1012  man           (Local User)
-1014  lp            (Local User)
-1016  mail          (Local User)
-1018  news          (Local User)
-1020  uucp          (Local User)
-1026  proxy         (Local User)
```

Les RIDs pairs = utilisateurs (`Local User`).
Les RIDs impairs = leur groupe associé (`Domain Group`).

Samba mappe les `uid` Linux vers des RIDs en ajoutant un offset. C'est pour ça qu'on voit les mêmes noms en double — une fois comme utilisateur, une fois comme groupe.

---

**`Local User` vs `Domain Group` — pourquoi les deux ?**

Sur Linux chaque utilisateur a un groupe principal du même nom — par exemple `root` l'utilisateur appartient au groupe `root`. Samba expose les deux séparément :
- `Local User` = le compte utilisateur
- `Domain Group` = le groupe Linux associé

C'est une particularité de comment Samba traduit les concepts Linux vers les concepts Windows/SMB. 😄

---

**Les RIDs manquants — ce qu'on n'a pas trouvé :**

Entre 1000 et 1050 il y a des trous — `1022`, `1023`, `1024` par exemple n'apparaissent pas. Soit ces RIDs n'existent pas, soit ils dépassent la plage scannée. C'est pour ça qu'on peut élargir avec `-R 1000-2000` pour être exhaustif.



---


### 12. Getting printer info

```bash 

 ==============================( Getting printer info for 192.168.78.129 )==============================                                                                                  
                                                                                             
No printers returned.                                                                        


enum4linux complete on Sat Apr  4 08:23:31 2026


```

```
No printers returned.
enum4linux complete on Sat Apr  4 08:23:31 2026
```

**Printer info** — enum4linux interroge Samba pour lister les imprimantes partagées sur la machine. Sur un réseau d'entreprise Windows c'est utile — les imprimantes partagées peuvent révéler des infos sur l'infrastructure (noms de départements, étages, sites...).

Ici `No printers returned` = aucune imprimante configurée sur Metasploitable. Normal pour un serveur Linux de lab.

---

`enum4linux complete` + timestamp = fin du scan. La session a duré **7 minutes** (08:16:26 → 08:23:31) pour extraire toutes ces informations **anonymement**, sans aucun mot de passe.

---

**Bilan offensif de toute la session enum4linux :**

Ce qu'un attaquant retient après ce scan :
- **Cibles brute force** : `msfadmin` et `user` — les deux seuls comptes actifs
- **Vecteur SMB** : partage `tmp` accessible anonymement en lecture
- **Version vulnérable** : Samba 3.0.20 → CVE à chercher
- **Brute force sans limite** : pas de lockout, complexité nulle, longueur minimale nulle
- **SID de la machine** : `S-1-5-21-1042354039-2475377354-766472396` → peut cibler `SID-500` directement

Tout ça avec une seule commande. 😄




# proteger samba: 

dans /etc/samba/smb.conf :

```bash
map to guest = never
restrict anonymous = 2
usershare allow guests = no
```