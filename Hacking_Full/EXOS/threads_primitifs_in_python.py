import threading
import random
import time


def display_data(index):
    time.sleep(random.randint(1,3))
    print(f"salut c'est le THREAD:{index}")

nb_of_t = 6
list_of_threads = []

for i in range(nb_of_t):
    # on creer des threads lié a une func avec args
    # args : DOIT etre un tuple ou une list 
    t = threading.Thread(target=display_data, args=(i,))
    # commencer le thread
    t.start()

    # on ajoute TOUT les threads a une liste car on a besoin
    # de tout les WAIT a la fin 
    # DOIS le faire a la fin dans une autre boucle for
    list_of_threads.append(t)

print("Salut AVANT les join() !!")

for t in list_of_threads:
    t.join()


print("salut APRES les join()")
    
