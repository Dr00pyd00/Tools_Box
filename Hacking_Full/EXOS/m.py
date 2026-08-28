import os 
from multiprocessing import Process
import time

def child(truc, truc2):
    time.sleep(2)
    print(f"je suis l'enfanf mon pid = {os.getpid()}")
    print(f" mon truc:{truc} ")
    print(f" mon truc2:{truc2} ")

def parent():
    print(f"je suis le parent mon pid = {os.getpid()}")


p = Process(target=child, args=["KOKOKOKO", "P1P1P1"])
p.start()
parent()
# p.join()


print("programme FINI")