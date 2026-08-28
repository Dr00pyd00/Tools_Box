from scapy.all import * 
import time

from manuf import manuf

# mon objet manuf:
p = manuf.MacParser()

start = time.perf_counter()

paquet = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst="192.168.159.0/24")

responses, _ = srp(paquet, timeout=2, verbose=False)

for s, r in responses:
    print(f"IP = {r.psrc} || MAC = {r.hwsrc}")
    fabricant = p.get_manuf(r.hwsrc)
    print(f"fabricant=> {fabricant}")

end = time.perf_counter()

print(f"programme fini en {end - start:.2f} secondes")
