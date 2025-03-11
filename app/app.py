from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

# Retrieve PostgreSQL connection info from environment variables (set via ConfigMap/Secret)
DB_HOST = os.environ.get("POSTGRES_HOST", "localhost")
DB_PORT = os.environ.get("POSTGRES_PORT", "5432")
DB_USER = os.environ.get("POSTGRES_USER", "postgres")
DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "postgres")
DB_NAME = os.environ.get("POSTGRES_DB", "postgres")

@app.route("/")
def index():
    return "Hello from Flask in Kubernetes!"

@app.route("/db-test")
def db_test():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            dbname=DB_NAME
        )
        cur = conn.cursor()
        cur.execute("SELECT version();")
        version = cur.fetchone()
        cur.close()
        conn.close()
        return jsonify({"postgres_version": version})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
