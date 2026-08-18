
import os
import dotenv
import psycopg2

dotenv.load_dotenv()

print('DEBUT DU PROGRAMME')

conn = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        dbname=os.getenv("POSTGRES_DB"),
        )
print('conn reussi')


