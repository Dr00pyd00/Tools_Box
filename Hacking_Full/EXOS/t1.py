from concurrent.futures import ThreadPoolExecutor

def dire_bonjour(nom):
    print(f"Bonjour {nom}")

noms = ["harry","hermione","ron","draco"]

with ThreadPoolExecutor(max_workers=2) as executor:
    executor.map(dire_bonjour, noms)
