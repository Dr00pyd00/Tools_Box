
import os 
import time 
from random import randint

from multiprocessing import Process

# os.getpid() ! avoir le pid du process courant

# on doit creer une fonction pour la passer dans un fork
# et on passe les args dans une LIST 

# join sert a WAIT:
    # ca dit : .join -> ici on attend que tout le fork se finnisse puis on continue le main


def child_func(arg1, arg2):
    time.sleep(randint(1,5))
    print(f"Hello from child! mon pid={os.getpid()}")
    print(f"arg1 = {arg1}, arg2 = {arg2}")

def parent_func():
    print(f"Je suis le PARENT ! mon pid={os.getpid()}")


p = Process(target=child_func, args=["ARGUMENT UN", 9898989898])
p.start()
p.join()

parent_func()

