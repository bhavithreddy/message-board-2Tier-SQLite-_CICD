# Message Board — 3-Tier Flask Application

A complete 3-tier architecture running entirely on your local machine:

```
Br

## Projectowser → Frontend (Flask :5000) → Backend API (Flask :5001) → SQLite DB
```

--- Structure

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







<img width="1525" height="892" alt="Screenshot 2026-04-18 220717" src="https://github.com/user-attachments/assets/7063f829-3853-4950-8a45-f6e47b82341d" />
<img width="847" height="563" alt="Screenshot 2026-04-18 221706" src="https://github.com/user-attachments/assets/26cb315a-9fb2-4cc2-b686-c1941a914116" />
<img width="792" height="412" alt="Screenshot 2026-04-18 221559" src="https://github.com/user-attachments/assets/bea4de7c-ae73-45e6-bb80-f2a3a9cf9e84" />
<img width="1297" height="296" alt="Screenshot 2026-04-18 220800" src="https://github.com/user-attachments/assets/e5351ca0-8b7e-4622-a87d-177b6dbb72af" />



