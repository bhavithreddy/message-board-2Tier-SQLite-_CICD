"""
Frontend Layer — Flask UI server
Runs on: http://localhost:5000
Responsibilities:
  - Serve the HTML page (Jinja2 template)
  - Proxy user actions to the Backend API (port 5001)
  - Never touch the database directly
"""

import os
import requests
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "dev-secret-key-change-in-production"

# In Docker: API_BASE env var is injected as "http://backend:5001/api"
# Locally:   falls back to "http://localhost:5001/api"
API_BASE = os.environ.get("API_BASE", "http://localhost:5001/api")


# ── Routes ─────────────────────────────────────────────────────────────────────
@app.route("/", methods=["GET"])
def index():
    """Fetch all messages from the API and render the board."""
    messages = []
    error    = None

    try:
        resp = requests.get(f"{API_BASE}/messages", timeout=5)
        resp.raise_for_status()
        messages = resp.json()
    except requests.exceptions.ConnectionError:
        error = "⚠️  Cannot reach the backend API. Make sure backend/app.py is running on port 5001."
    except requests.exceptions.Timeout:
        error = "⚠️  Backend API timed out. Please try again."
    except Exception as exc:
        error = f"⚠️  Unexpected error: {exc}"

    return render_template("index.html", messages=messages, error=error)


@app.route("/post", methods=["POST"])
def post_message():
    """Forward the form data to the backend API, then redirect home."""
    content = request.form.get("content", "").strip()
    author  = request.form.get("author",  "").strip() or "Anonymous"

    if not content:
        flash("Message cannot be empty!", "error")
        return redirect(url_for("index"))

    try:
        resp = requests.post(
            f"{API_BASE}/messages",
            json={"content": content, "author": author},
            timeout=5,
        )
        if resp.status_code == 201:
            flash("Message posted!", "success")
        else:
            flash(f"API error: {resp.json().get('error', 'Unknown error')}", "error")
    except requests.exceptions.ConnectionError:
        flash("Cannot reach the backend API. Is it running?", "error")

    return redirect(url_for("index"))


@app.route("/delete/<int:message_id>", methods=["POST"])
def delete_message(message_id):
    """Ask the backend to delete a message."""
    try:
        resp = requests.delete(f"{API_BASE}/messages/{message_id}", timeout=5)
        if resp.status_code == 200:
            flash(f"Message #{message_id} deleted.", "success")
        else:
            flash(f"Could not delete: {resp.json().get('error')}", "error")
    except requests.exceptions.ConnectionError:
        flash("Cannot reach the backend API.", "error")

    return redirect(url_for("index"))


# ── Entry point ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"[UI]  Frontend running on http://localhost:5000")
    print(f"[UI]  Connecting to Backend API at {API_BASE}")
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
