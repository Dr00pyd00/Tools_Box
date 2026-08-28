from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import random

mots = ["python", "linux", "hacking", "thread", "socket"]

def compter_lettres(mot):
    time.sleep(random.uniform(0.5, 2))
    return len(mot)


with ThreadPoolExecutor(max_workers=3) as executor:
    futures = {executor.submit(compter_lettres, mot): mot for mot in mots}

    for f in as_completed(futures):
        mot = futures[f]
        nb = f.result()
        print(f"{mot} fait {nb} lettres")



