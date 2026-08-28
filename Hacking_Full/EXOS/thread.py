import threading
import time

threads = []

def tache(num:int):
    time.sleep(num + 2)
    print(f"tache du thread {num}")



for i in range(3):
    t = threading.Thread(target=tache, args=(i+1,))
    threads.append(t)
    t.start()

# for thread in threads:
#     thread.join()

print("HELLO")


