from time import sleep
import redis

# On creer l'objet qui gere la connexion:
r = redis.Redis(
        host='localhost',
        port=6379,
        decode_responses=True,      # transforme direct les octets en string 
        )

r.flushdb() # reset total de la db ( ne pas faire en prod) 

# Basic:
# r.set('user:1:name', 'Luna')
# nom = r.get('user:1:name')
# print(nom)

# With expire
# r.set('name', 'lulu', ex= 1) 
# print(r.get('name'))
# sleep(2)
# print(r.get('name'))


# ====== Listes 
r.rpush('l1:emails', 'truc 1')
r.rpush('l1:emails', 'truc 2')
r.lpush('l1:emails', 'truc 3')

l = r.lrange('l1:emails', 0, -1)
print(l)

# ====== dict = hash
    # mapping pour pleins de champs en meme temps
r.hset('dict1', mapping={
    'date':'3232',
    'heure':'4h00',
    'statut':'dispo',
    }
       )

dispo = r.hgetall('dict1')
print(dispo)
    
    # avec un champ a la fois
r.hset('d2', 'name', 'koko')
r.hset('d2', 'age', '56')

data = r.hgetall('d2')
print(data)


# le expire pour les hash se met APRES 
r.expire('d2', 1)

sleep(2)
print(r.hgetall('d2'))




