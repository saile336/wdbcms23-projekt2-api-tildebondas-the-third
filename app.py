import os, psycopg
from psycopg.rows import dict_row
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app) 
app.config['JSON_AS_ASCII'] = False

load_dotenv()
db_url = os.environ.get("DB_URL")

@app.route("/")
def index():
    return { "message": "Hello" }


## Kom ihåg:
# - pip install -r requirements.txt
# - Kopiera/byt namn på .env-example ==> .env och sätt in en riktig DB_URL
# - Ändra portnummer nedan

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)