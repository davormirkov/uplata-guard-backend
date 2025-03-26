from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

# Baza podataka setup
def init_db():
    conn = sqlite3.connect('uplate.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS uplate (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            korisnik TEXT,
            iznos TEXT,
            status TEXT DEFAULT 'pending',
            preuzeo TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route("/add_uplata", methods=["POST"])
def add_uplata():
    data = request.json
    conn = sqlite3.connect('uplate.db')
    c = conn.cursor()
    c.execute("INSERT INTO uplate (korisnik, iznos) VALUES (?, ?)", (data["korisnik"], data["iznos"]))
    conn.commit()
    conn.close()
    return jsonify({"message": "Uplata dodana"}), 201

@app.route("/get_uplate", methods=["GET"])
def get_uplate():
    conn = sqlite3.connect('uplate.db')
    c = conn.cursor()
    c.execute("SELECT id, korisnik, iznos, status, preuzeo FROM uplate")
    uplate = [{"id": row[0], "korisnik": row[1], "iznos": row[2], "status": row[3], "preuzeo": row[4]} for row in c.fetchall()]
    conn.close()
    return jsonify(uplate)

@app.route("/preuzmi_uplatu/<int:id>", methods=["POST"])
def preuzmi_uplatu(id):
    data = request.json
    conn = sqlite3.connect('uplate.db')
    c = conn.cursor()
    c.execute("UPDATE uplate SET status = 'in_progress', preuzeo = ? WHERE id = ? AND status = 'pending'", (data["preuzeo"], id))
    conn.commit()
    conn.close()
    return jsonify({"message": "Uplata preuzeta"}), 200

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
