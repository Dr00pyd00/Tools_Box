from  concurrent.futures import ThreadPoolExecutor


def carre(n):
    return n * n

nums_list = [1,2,3,4,5]

with ThreadPoolExecutor(max_workers=3) as executor:
    res = executor.map(carre, nums_list)
    print(list(res))