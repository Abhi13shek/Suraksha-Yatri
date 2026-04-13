import os
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import qrcode
from werkzeug.utils import secure_filename
from flask_mysqldb import MySQL

app = Flask(__name__)
CORS(app)

# ---------------- MySQL Config ----------------
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Abhishek@13'
app.config['MYSQL_DB'] = 'tourist_Db'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# ---------------- Paths ----------------
BASE_DIR = app.root_path
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
QRCODE_DIR = os.path.join(BASE_DIR, "qrcodes")

os.makedirs(QRCODE_DIR, exist_ok=True)

# ---------- Ensure Table Exists ----------
def init_db():
    cur = mysql.connection.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tourists (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            phone VARCHAR(20) NOT NULL,
            aadhar VARCHAR(50) NOT NULL,
            emergency VARCHAR(20) NOT NULL,
            qr_filename VARCHAR(255) NOT NULL,
            created_at DATETIME NOT NULL
        )
    """)
    mysql.connection.commit()
    cur.close()

# call init_db *inside* application context
with app.app_context():
    init_db()

# ---------- Simple login ----------
USERS = {"admin": "1234"}

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password")
    if USERS.get(username) == password:
        return jsonify({"success": True})
    return jsonify({"success": False, "message": "Invalid credentials"}), 401

# # ---------- Register Tourist ----------

# @app.route("/register", methods=["POST"])
# def register():
#     data = request.get_json() or {}
#     name = data.get("name", "").strip()
#     phone = data.get("phone", "").strip()
#     aadhar = data.get("aadhar", "").strip()
#     emergency = data.get("emergency", "").strip()
#     print(name)
#     print(phone)
#     print(aadhar)
#     print(emergency)
#     if not all([name, phone, aadhar, emergency]):
#         return jsonify({"success": False, "message": "All fields required"}), 400

#     timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
#     raw_filename = f"{name}_{phone}_{timestamp}.png"
#     filename = secure_filename(raw_filename)
#     qr_path = os.path.join(QRCODE_DIR, filename)

#     qr_content = f"Name:{name};Phone:{phone};Aadhar:{aadhar};Emergency:{emergency}"
#     qrcode.make(qr_content).save(qr_path)
#     print(qr_path)

#     cur = mysql.connection.cursor()
#     cur.execute(
#         "INSERT INTO tourists (name, phone, aadhar, emergency, qr_filename, created_at) VALUES (%s, %s, %s, %s, %s, %s)",
#         (name, phone, aadhar, emergency, filename, datetime.utcnow())
#     )
#     mysql.connection.commit()
#     cur.close()

#     return jsonify({"success": True, "qr_filename": filename})
# -------------------------
# REGISTER ROUTE (already in your code)
# -------------------------
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    name = data.get("name", "").strip()
    phone = data.get("phone", "").strip()
    aadhar = data.get("aadhar", "").strip()
    emergency = data.get("emergency", "").strip()
    
    if not all([name, phone, aadhar, emergency]):
        return jsonify({"success": False, "message": "All fields required"}), 400

    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    raw_filename = f"{name}_{phone}_{timestamp}.png"
    filename = secure_filename(raw_filename)
    qr_path = os.path.join(QRCODE_DIR, filename)

    qr_content = f"Name:{name};Phone:{phone};Aadhar:{aadhar};Emergency:{emergency}"
    qrcode.make(qr_content).save(qr_path)

    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO tourists (name, phone, aadhar, emergency, qr_filename, created_at) VALUES (%s, %s, %s, %s, %s, %s)",
        (name, phone, aadhar, emergency, filename, datetime.utcnow())
    )
    mysql.connection.commit()
    cur.close()

    return jsonify({"success": True, "qr_filename": filename})


# -------------------------
# NEW: GET ALL TOURISTS (Step 3)
# -------------------------
# @app.route("/tourists", methods=["GET"])
# def get_tourists():
#     cur = mysql.connection.cursor()
#     cur.execute("SELECT id, name, phone, aadhar, emergency, qr_filename, created_at FROM tourists")
#     rows = cur.fetchall()
#     cur.close()

#     # Convert to list of dicts for JSON
#     tourists = []
#     for row in rows:
#         tourists.append({
#             "id": row[0],
#             "name": row[1],
#             "phone": row[2],
#             "aadhar": row[3],
#             "emergency": row[4],
#             "qr_filename": row[5],
#             "created_at": row[6].strftime("%Y-%m-%d %H:%M:%S")
#         })

#     return jsonify(tourists)
@app.route("/tourists", methods=["GET"])
def get_tourists():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password",
        database="your_db"
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tourists")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(rows)

# -------------------------
# RUN APP
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)

# ---------- List Tourists ----------
@app.route("/tourists", methods=["GET"])
def get_tourists():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, name, phone, aadhar, emergency, qr_filename, created_at FROM tourists ORDER BY id DESC")
    rows = cur.fetchall()
    cur.close()

    tourists = []
    for r in rows:
        # using DictCursor, r is a dict
        tourists.append({
            "id": r["id"], "name": r["name"], "phone": r["phone"],
            "aadhar": r["aadhar"], "emergency": r["emergency"],
            "qr_filename": r["qr_filename"], "created_at": r["created_at"].strftime("%Y-%m-%d %H:%M:%S")
        })
    return jsonify(tourists)

# ---------- Serve QR ----------
@app.route("/qrcode/<filename>")
def serve_qr(filename):
    return send_from_directory(QRCODE_DIR, filename)

# ---------- Serve Frontend ----------
@app.route("/")
def index():
    return send_from_directory(FRONTEND_DIR, "login.html")

@app.route("/dashboard")
def dashboard_page():
    return send_from_directory(FRONTEND_DIR, "dashboard.html")

if __name__ == "__main__":
    app.run(debug=True)
