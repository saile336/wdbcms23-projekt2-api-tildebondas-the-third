import os
import psycopg
from psycopg.rows import dict_row
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)
app.config['JSON_AS_ASCII'] = False

load_dotenv()
db_url = os.environ.get("DB_URL")

# dict_row: få query-resultat som list of dicts
conn = psycopg.connect(db_url, row_factory=dict_row, autocommit=True)


@app.route("/")
def index():
    return {"message": "Use /todo for API endpoint"}


@app.route("/todo", methods=["GET", "POST"])
def get_todos():
    if request.method == 'GET':
        with conn.cursor() as cur:
            cur.execute(
                "SELECT todo.*, categories.category_name FROM todo INNER JOIN categories ON todo.category_id=categories.id")
            result = cur.fetchall()
        return {"ToDo": result}

    if request.method == 'POST':
        try:
            req_body = request.get_json()
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO todo (
                        user_id,
                        category_id,
                        title,
                        due_date
                    ) VALUES (
                        %s, %s, %s, %s
                    ) RETURNING id
                """, [
                    req_body['user_id'],
                    req_body['category_id'],
                    req_body['title'],
                    req_body['due_date'],
                ])
                return {"id": cur.fetchone()['id']}
        except Exception as e:
            print(repr(e))
            return {"ERROR": "Check logs for details"}, 400

    else:
        return {"Du använde metoden": request.method}


@app.route("/todo/<int:id>", methods=["PUT", "PATCH", "DELETE"])
def update_todo(id):
    if request.method == "PUT" or request.method == "PATCH":
        try:
            req_body = request.get_json()
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE todo
                    SET category_id = %s,
                        title = %s,
                        due_date = %s
                    WHERE id = %s;
                """, [
                    req_body['category_id'],
                    req_body['title'],
                    req_body['due_date'],
                    id,
                ])
                return {"updated todo id": id}

        except Exception as e:
            print(repr(e))
            return {"error": "check logs"}, 400

    if request.method == "DELETE":
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    DELETE FROM todo WHERE id = %s;
                """, [id])
                return {"deleted id": id}

        except Exception as e:
            print(repr(e))
            return {"ERROR, check logs for details"}, 400

    else:
        return {"Du använde metoden": request.method}


# Kom ihåg:
# - pip install -r requirements.txt
# - Kopiera/byt namn på .env-example ==> .env och sätt in en riktig DB_URL
# - Ändra portnummer nedan

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8322, debug=True)
