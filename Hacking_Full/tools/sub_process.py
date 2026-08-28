import subprocess 

# dans res: on met la commande dans une list, on capture et met en texte

res = subprocess.run(["ls","-l","-a"], capture_output=True, text=True)

# res: est un objet subprocess 
# res.stdout : ce que verrais la console
# il existe stderr par exemple aussi

print(res.stdout)

# je peux mettre tout dans un fichier text:

with open("subprocess.txt", "w") as f:
    f.write(res.stdout)

