import socket
from functools import partial
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse


# ========== PARSER 
parser = argparse.ArgumentParser(description="Port Scanner")
parser.add_argument("-H", "--host", help="Host to scan")
parser.add_argument("-s", "--start", type=int, help="num to start port scan")
parser.add_argument("-e", "--end", type=int,  help="num to end port scan")
cli_args = parser.parse_args()


def main():
    # user_host_input = input("Enter host:")
    # user_port_start_input = int(input("Enter start port to analyze:"))
    # user_port_end_input = int(input("Enter end port :"))
    user_port_start_input = cli_args.start
    user_port_end_input = cli_args.end
    cli_host = cli_args.host


    # host = test_hostname(name=user_host_input)

    print(f"Scanning {cli_host} ports ...")

    # while(count <= user_port_end_input):
    # for port in range(user_port_start_input, user_port_end_input+1):
    #     if scan_port_localhost( port=port):
    #         print(f"port {port} is OPEN.")

    # avec thread truc
    # with ThreadPoolExecutor(max_workers=100) as executor:
    #     res =  executor.map(scan_port_localhost, range(user_port_start_input, user_port_end_input +1) )
    #     list_res = list(res)
    #     for index, port_bool in enumerate(list_res):
    #         if port_bool:
    #             print(f"port {index+user_port_start_input}")


    futures = {}
    with ThreadPoolExecutor(max_workers=100) as executor:
        for port in range(user_port_start_input, user_port_end_input +1):
            future = executor.submit(scan_port_localhost, port)
            futures[future] = port
    
        for future in as_completed(futures):
            port = futures[future]
            if future.result():
                print(f"port = {port} is OPEN.")
                    


def test_hostname(name)->str:
    try:
        host = socket.gethostbyname(name)
        return host

    except socket.gaierror as e:
        print(f"error test_hostname: {e}")
    

def scan_port( port:int, host:str,)->bool:
    # creer mon socket : 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5) # met en place une erreur socket.timeout si jamais ca rate
    try:
        s.connect((host,port))
        return True
    
    except (socket.error, socket.timeout) as e:
        return False
    finally:
        s.close()

scan_port_localhost = partial(scan_port, host=cli_args.host)

# ============== go 

if __name__ == "__main__":
    main()
