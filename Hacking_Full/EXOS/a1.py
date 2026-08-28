

import threading


num_list = [4,6,99,4343]
t_list = []

def task(n):
    print(f" task {n}")


for element in num_list:
    t = threading.Thread(target=task, args=(element,))
    t_list.append(t)
    t.start()

for t in t_list:
    t.join()

