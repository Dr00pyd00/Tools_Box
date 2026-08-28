#!/usr/bin/env python3

import time
import argparse
from scapy.all import *
from manuf import manuf

# parser:
my_parser = argparse.ArgumentParser(description="parser for arp scan")
my_parser.add_argument("-p", "--plage", type=str, help="plage to scan with masque you want ie: /16, /24 etc...")
my_parser.add_argument("-b", "--broadcast", type=str, help="what you want to broadcast?", default="ff:ff:ff:ff:ff:ff")
parser_args = my_parser.parse_args()

# variables:
plage = parser_args.plage
broadcast = parser_args.broadcast

# manuf setup:
mac_parser = manuf.MacParser()

# running time:
start = time.perf_counter()
print(f"Scanning plage <{plage}> with broadcast <{broadcast}> ...\n")

# on fait un paquet generqiue et scapy va faire tout via le masque /24
paquet = Ether(dst=broadcast) / ARP(pdst=plage)
responses, _ = srp(paquet, timeout=0.1, verbose=False)

# afficher resultats:
count = 0
for sended , received in responses:
    count += 1
    print(f"IP = {received.psrc} || MAC = {received.hwsrc} || manufactor = {mac_parser.get_manuf(received.hwsrc)}")


end = time.perf_counter()
print()
print(f"Scan finished in {end-start:.2f} seconds => {count} result(s) founds. ")
