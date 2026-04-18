"""
Backend API Layer — Flask REST service
Runs on: http://localhost:5001
Responsibilities:
  - Expose POST /api/messages  → save a message
  - Expose GET  /api/messages  → return all messages
  - Own the SQLite database connection
"""

import os
import sqlite3
from datetime import datetime, timezone
from flask import Flask, request, jsonify

app = Flask(__name__)

# In Docker: DB_PATH env var is "/database/messages.db" (mounted volume)
# Locally:   falls back to ../database/messages.db relative to this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH  = os.environ.get("DB_PATH", os.path.join(BASE_DIR, "..", "database", "messages.db"))


# ── DB helpers ─────────────────────────────────────────────────────────────────
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            content    TEXT    NOT NULL,
            author     TEXT    NOT NULL DEFAULT 'Anonymous',
            created_at TEXT    NOT NULL
        )
    """)
    conn.commit()
    conn.close()
    print(f"[DB] Initialised → {os.path.abspath(DB_PATH)}")


# ── Routes ─────────────────────────────────────────────────────────────────────
@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "message-board-api"}), 200


@app.route("/api/messages", methods=["POST"])
def create_message():
    data = request.get_json(silent=True)
    if not data or not data.get("content", "").strip():
        return jsonify({"error": "Field 'content' is required and cannot be blank."}), 400

    content    = data["content"].strip()
    author     = data.get("author", "Anonymous").strip() or "Anonymous"
    created_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

    conn = get_db()
    cursor = conn.execute(
        "INSERT INTO messages (content, author, created_at) VALUES (?, ?, ?)",
        (content, author, created_at),
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()

    print(f"[API] New message #{new_id} from '{author}': {content[:60]}")
    return jsonify({
        "id":         new_id,
        "content":    content,
        "author":     author,
        "created_at": created_at,
    }), 201


@app.route("/api/messages", methods=["GET"])
def get_messages():
    conn = get_db()
    rows = conn.execute(
        "SELECT id, content, author, created_at FROM messages ORDER BY id DESC"
    ).fetchall()
    conn.close()
    messages = [dict(row) for row in rows]
    print(f"[API] Returning {len(messages)} messages")
    return jsonify(messages), 200


@app.route("/api/messages/<int:message_id>", methods=["DELETE"])
def delete_message(message_id):
    conn = get_db()
    cursor = conn.execute("DELETE FROM messages WHERE id = ?", (message_id,))
    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        return jsonify({"error": f"Message #{message_id} not found."}), 404

    print(f"[API] Deleted message #{message_id}")
    return jsonify({"deleted": message_id}), 200


# ── Entry point ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    init_db()
    print("[API] Backend running on http://localhost:5001")
    app.run(host="0.0.0.0", port=5001, debug=True, use_reloader=False)
