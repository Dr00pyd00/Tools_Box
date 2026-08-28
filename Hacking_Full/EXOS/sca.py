from scapy.all import *


paquet = IP(dst="google.com") / TCP(dport=9999)
# paquet.show()

response = sr1(paquet, timeout=2)
# response.show()

# ARP().show()

# Ether  → qui envoie, qui reçoit (MACs)
# ARP    → la question "qui a cette IP ?"

mon_arp = Ether(dst="FF:FF:FF:FF:FF:FF") / ARP(pdst="172.27.240.1")

res, _ = srp(mon_arp, timeout=2, verbose=False)
print(res)