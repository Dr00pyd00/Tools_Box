import random
import threading
import time

print("DEBUT")


num_of_t = 5
t_list = []

def display_t(num):
    time.sleep(random.randint(1,4))
    print(f"this is thread = {num}")



for n in range(num_of_t):
    t = threading.Thread(target=display_t, args=(n,))
    t_list.append(t)
    t.start()

for t in t_list:
    t.join()
   

print("FIN")