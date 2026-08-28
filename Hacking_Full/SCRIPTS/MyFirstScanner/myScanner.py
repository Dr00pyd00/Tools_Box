import time
import argparse
import socket

from concurrent.futures import ThreadPoolExecutor, as_completed



# ==== PARSER 
parser = argparse.ArgumentParser(description="Scan Port flags")
parser.add_argument("-H", "--host", type=str, help="host to scan", default="localhost")
parser.add_argument("-s", "--start", type=int, help="starting num to scan host.", default=0)
parser.add_argument("-e", "--end", type=int, help="ending num to scan host.", default=60000)
parser_args = parser.parse_args()


# ==== FUNCTIONS 
def check_hostname(hostname:str)->str:
    try:
        host = socket.gethostbyname(hostname)
        return host
    except socket.gaierror as e:
        print(f"Error HostnameCheck: {e}")    
        

def scan_ports(host:str, port:int):
    # creation d'un socket :
    s = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    # ajout d'un timeout : si jamais il foire renvoi une erreur : socket.timeout
    s.settimeout(0.5)

    try:
        s.connect((host,port))
        return True
    except (socket.error, socket.timeout) as e:
        return False
    finally:
        s.close()



# ==== MAIN ===================================================

def main():

    start_time = time.perf_counter()

    p_start = parser_args.start 
    p_end = parser_args.end 
    s_host = check_hostname(parser_args.host)
    if s_host is None:
        print("Bad Host...")
        return

    print(f"Scanning Host: {s_host}")

    futures_dict = {}
    with ThreadPoolExecutor(max_workers=100) as executor:
        for port in range(p_start, p_end + 1):
            future = executor.submit(scan_ports, s_host, port)
            futures_dict[future] = port
        for future in as_completed(futures_dict):
            if future.result():
                print(f"Port {futures_dict[future]} is OPEN")

    end_time = time.perf_counter()
    duration = end_time - start_time
    print(f"Scan Finished! Ports scanned => {p_end - p_start} | Duration: {duration:.3f} seconds.")



if __name__=="__main__":
    main()

