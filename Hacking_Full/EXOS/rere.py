from scapy.all import *
import time

ip_list = [f"192.168.159.{n}" for n in range(1,255)]


start = time.perf_counter()

for ip_addr in ip_list:

    paquet = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip_addr)

    responses, _ = srp(paquet, timeout=0.1, verbose=False)
    for sended, received in responses:
        print(f"IP = {received.psrc} || MAC = {received.hwsrc}")

end = time.perf_counter()

print(f"programme fini en {end-start:.2f} seconds")

