from concurrent.futures import ThreadPoolExecutor

import time 
from random import randint

urls = ["http://site1.com", "http://site2.com", "http://site3.com"]

def fake_dl(name, num):
    time.sleep(randint(0,4))
    print(f"id{num}  // dl of: {name} ")

futures_dict = {}
with ThreadPoolExecutor(max_workers=2) as executor:
    for i,v in enumerate(urls):
        f = executor.submit(fake_dl, v, i)
        futures_dict[f] = i


for k,v in futures_dict.items():
    if v == 1:
        print(f"index 1 donne: {k}")


