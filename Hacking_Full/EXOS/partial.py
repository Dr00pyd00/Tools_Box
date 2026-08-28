
# map

def double(n):
    return n * 2

res = map(double, [1,2,3,4,5,6,7,8,9])

print(list(res))

mots = ["bonjour", "monde", "python"]

def upp_words(word:str):
    return word.upper()

res2 = map(str.upper, mots)
print(list(res2))

