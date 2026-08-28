from scapy.all import *
import time

addr_list = [f"192.168.159.{n}" for n in range(1,255)]


start_scan = time.perf_counter()
for addr_ip in addr_list:
    # creer paquet :
    paquet = Ether(dst="ff:ff:ff:ff:ff:ff") /  ARP(pdst=addr_ip)
    response_positive, _ = srp(paquet, timeout=0.2, verbose=False)
    if response_positive:
        for sended, received in response_positive:
            print(f"Ip: {received.psrc} // MAC: {received.hwsrc}")
    continue

end_scan = time.perf_counter()

print(f"total duration: {end_scan - start_scan:.2f} seconds")
