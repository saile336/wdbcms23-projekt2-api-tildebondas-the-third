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

conn = psycopg.connect(db_url, row_factory=dict_row, autocommit=True) #dict_row: få query-resultat som list of dicts

@app.route("/")
def index():
    return { "message": "Use /todo for API endpoint" }

@app.route("/todo", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
def get_todos():
    if request.method == 'GET':
        with conn.cursor() as cur:
            cur.execute("SELECT todo.*, categories.category_name FROM todo INNER JOIN categories on todo.category_id = categories.category_name ")
            result = cur.fetchall()
        return { "bookings": result }

    if request.method == 'POST':
        try:
            req_body = request.get_json()
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO hotel_booking (
                        room_id,
                        guest_id,
                        datefrom,
                        dateto, 
                        addinfo
                    ) VALUES (
                        %s, %s, %s, %s, %s
                    ) RETURNING id
                """, [
                req_body['room_id'], 
                req_body['guest_id'], 
                req_body['datefrom'], 
                req_body['dateto'],
                req_body['addinfo']
                ])
                return {"id": cur.fetchone()['id']}
        except Exception as e:
            print(repr(e))
            return { "ERROR, check logs for details" }, 400

    else:
        return { "Du använde metoden": request.method }


## Kom ihåg:
# - pip install -r requirements.txt
# - Kopiera/byt namn på .env-example ==> .env och sätt in en riktig DB_URL
# - Ändra portnummer nedan

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8322, debug=True)