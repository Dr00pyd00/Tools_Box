import subprocess


res = subprocess.run(["whois", "209.85.250.94"], capture_output=True, text=True)

print(res)


with open("toto.txt", "w") as f:
    f.write(res.stdout)