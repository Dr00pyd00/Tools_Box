
from concurrent.futures import ThreadPoolExecutor


num_list = [4,6,99,4343]
t_list = []

def task(n):
    print(f" task {n}")


with ThreadPoolExecutor(max_workers=3) as executor:
    executor.map(task, num_list)