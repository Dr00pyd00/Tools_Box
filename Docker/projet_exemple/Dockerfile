
# prend une image d'OS
FROM python:3.12-alpine
# creer un dir racine ou tout commence 
WORKDIR /app
# copy [ machine ] vers [ container ] 
COPY . .
# execute la commande pendant le build de l'image: install les dependances dans l'image elle meme 
RUN pip install -r requirements.txt
# lance la cmd au start du container
CMD ["python3","main.py"]

