# Message Board — 3-Tier Flask Application

A complete 3-tier architecture running entirely on your local machine:

```
Browser → Frontend (Flask :5000) → Backend API (Flask :5001) → SQLite DB
```

---

## Project Structure

```
message_board/
├── backend/
│   └── app.py              ← Tier 2: REST API (Flask, port 5001)
├── frontend/
│   ├── app.py              ← Tier 1: UI server (Flask, port 5000)
│   └── templates/
│       └── index.html      ← Jinja2 HTML template
├── database/
│   └── messages.db         ← Tier 3: SQLite file (auto-created on first run)
├── requirements.txt
├── start_backend.sh
├── start_frontend.sh
└── README.md
```

---

## Step-by-Step Setup & Run

### Step 1 — Install dependencies (run once)

```bash
cd message_board
pip install -r requirements.txt
```

Or install directly:

```bash
pip install flask flask-cors requests
```

---

### Step 2 — Start the Backend API (Terminal 1)

```bash
cd message_board/backend
python app.py
```

Expected output:
```
[DB] Initialised → /path/to/message_board/database/messages.db
[API] Backend running on http://localhost:5001
 * Running on http://0.0.0.0:5001
```

---

### Step 3 — Start the Frontend UI (Terminal 2)

Open a **new terminal window**, then:

```bash
cd message_board/frontend
python app.py
```

Expected output:
```
[UI]  Frontend running on http://localhost:5000
[UI]  Connecting to Backend API at http://localhost:5001/api
 * Running on http://0.0.0.0:5000
```

---

### Step 4 — Open the application

Navigate to: **http://localhost:5000**

---

## Testing

### Browser test
1. Open http://localhost:5000
2. Enter your name (optional) and a message
3. Click "→ Post Message"
4. Message appears in the feed instantly

### curl tests

**Post a message:**
```bash
curl -X POST http://localhost:5001/api/messages \
  -H "Content-Type: application/json" \
  -d '{"content": "Hello from curl!", "author": "Dev"}'
```

Expected response:
```json
{"id": 1, "content": "Hello from curl!", "author": "Dev", "created_at": "2025-01-01 12:00:00"}
```

**Get all messages:**
```bash
curl http://localhost:5001/api/messages
```

**Delete message #1:**
```bash
curl -X DELETE http://localhost:5001/api/messages/1
```

**Health check:**
```bash
curl http://localhost:5001/api/health
```

---

## Architecture — Data Flow

```
[Browser]
    |  HTTP form POST /post
    ↓
[Frontend: Flask :5000]  frontend/app.py
    |  requests.post("http://localhost:5001/api/messages", json={...})
    ↓
[Backend API: Flask :5001]  backend/app.py
    |  sqlite3.connect("database/messages.db")
    |  INSERT INTO messages ...
    ↓
[SQLite: database/messages.db]

Return path:
    ↑  rows as list of dicts
    ↑  JSON response 201 Created
    ↑  redirect to GET /
    ↑  requests.get("http://localhost:5001/api/messages")
    ↑  render_template("index.html", messages=[...])
    ↑  HTML page displayed in browser
```

**Key design decisions:**
- Frontend **never** imports sqlite3 — it only calls HTTP endpoints
- Backend **never** renders HTML — it only returns JSON
- SQLite file lives in `/database/` — separate from application code

---

## Common Errors & Fixes

### Error: `Address already in use` (port 5001 or 5000)

**Cause:** A previous Flask process is still running.

**Fix:**
```bash
# Find what's using the port
lsof -i :5001
lsof -i :5000

# Kill it (replace PID with the number shown)
kill -9 <PID>

# Or kill all python processes (careful on shared machines)
pkill -f "python app.py"
```

---

### Error: `ModuleNotFoundError: No module named 'flask'`

**Fix:**
```bash
pip install flask flask-cors requests

# If you have multiple Python versions:
python3 -m pip install flask flask-cors requests
```

---

### Error: Frontend shows "Cannot reach the backend API"

**Cause:** Backend isn't running, or is on the wrong port.

**Checklist:**
1. Is backend running? Check Terminal 1 for errors.
2. Test the backend directly: `curl http://localhost:5001/api/health`
3. Make sure backend started on port **5001** (not 5000).
4. Check `frontend/app.py` line: `API_BASE = "http://localhost:5001/api"` — must match.

---

### Error: `sqlite3.OperationalError: unable to open database file`

**Cause:** The `database/` directory doesn't exist.

**Fix:**
```bash
mkdir -p message_board/database
```
Then restart the backend — it will auto-create `messages.db`.

---

### Error: `flask_cors not found`

**Fix:**
```bash
pip install flask-cors
```

---

## API Reference

| Method | Endpoint | Body | Response |
|--------|----------|------|----------|
| GET | /api/health | — | `{"status":"ok"}` |
| GET | /api/messages | — | Array of message objects |
| POST | /api/messages | `{"content":"...", "author":"..."}` | Created message object |
| DELETE | /api/messages/:id | — | `{"deleted": id}` |
