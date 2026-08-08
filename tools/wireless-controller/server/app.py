"""
Simple Flask server for authorized remote-management (agent-based) - basic proof-of-concept.

Features:
- Agent registration (secret-based)
- Admin UI (basic auth) to view devices and send whitelisted commands
- Agent polling endpoint to receive a command
- Agent result upload endpoint

Security notes (important):
- Use HTTPS in production (reverse proxy with TLS)
- Use strong ADMIN_USER/ADMIN_PASS and AGENT_REGISTER_SECRET
- Agents receive an api_key on registration; store it on the agent side securely
- This project is intended for devices you own and manage
"""

from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, Response
from functools import wraps
import os
import sqlite3
import secrets
import time
from datetime import datetime
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, '..', '.env'))

DB_PATH = os.environ.get('DATABASE', os.path.join(BASE_DIR, 'devices.db'))
ADMIN_USER = os.environ.get('ADMIN_USER', 'admin')
ADMIN_PASS = os.environ.get('ADMIN_PASS', 'password')
AGENT_REGISTER_SECRET = os.environ.get('AGENT_REGISTER_SECRET', 'register-secret')

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'dev-secret')

# DB helpers
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS devices (
        id TEXT PRIMARY KEY,
        name TEXT,
        api_key TEXT,
        last_seen INTEGER,
        last_result TEXT,
        pending_command TEXT
    )''')
    conn.commit()
    conn.close()

def get_db_conn():
    return sqlite3.connect(DB_PATH)

# Admin basic auth
def check_auth(username, password):
    return username == ADMIN_USER and password == ADMIN_PASS

def authenticate():
    return Response('Authentication required', 401, {'WWW-Authenticate': 'Basic realm="Login"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@app.route('/')
@requires_auth
def index():
    conn = get_db_conn()
    c = conn.cursor()
    c.execute('SELECT id, name, api_key, last_seen, last_result, pending_command FROM devices')
    rows = c.fetchall()
    devices = []
    for r in rows:
        devices.append({
            'id': r[0],
            'name': r[1],
            'api_key': r[2],
            'last_seen': datetime.fromtimestamp(r[3]).isoformat() if r[3] else None,
            'last_result': r[4],
            'pending_command': r[5]
        })
    conn.close()
    return render_template('index.html', devices=devices)

@app.route('/send_command', methods=['POST'])
@requires_auth
def send_command():
    device_id = request.form.get('device_id')
    command = request.form.get('command')
    # only allow short commands - server does no execution
    if not device_id or not command:
        flash('Missing device or command')
        return redirect(url_for('index'))
    # store pending command
    conn = get_db_conn()
    c = conn.cursor()
    c.execute('UPDATE devices SET pending_command = ? WHERE id = ?', (command, device_id))
    conn.commit()
    conn.close()
    flash('Command queued')
    return redirect(url_for('index'))

@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.get_json(force=True)
    name = data.get('name')
    secret = data.get('register_secret')
    if secret != AGENT_REGISTER_SECRET:
        return jsonify({'error': 'invalid register secret'}), 403
    device_id = secrets.token_hex(8)
    api_key = secrets.token_hex(20)
    now = int(time.time())
    conn = get_db_conn()
    c = conn.cursor()
    c.execute('INSERT INTO devices (id, name, api_key, last_seen) VALUES (?, ?, ?, ?)', (device_id, name, api_key, now))
    conn.commit()
    conn.close()
    print(f"Registered device {name} -> {device_id}")
    return jsonify({'device_id': device_id, 'api_key': api_key})

@app.route('/api/poll', methods=['POST'])
def api_poll():
    data = request.get_json(force=True)
    device_id = data.get('device_id')
    api_key = data.get('api_key')
    if not device_id or not api_key:
        return jsonify({'error': 'missing credentials'}), 400
    conn = get_db_conn()
    c = conn.cursor()
    c.execute('SELECT api_key, pending_command FROM devices WHERE id = ?', (device_id,))
    row = c.fetchone()
    if not row or row[0] != api_key:
        conn.close()
        return jsonify({'error': 'unauthorized'}), 403
    pending = row[1]
    # clear pending command when returning it
    c.execute('UPDATE devices SET pending_command = NULL, last_seen = ? WHERE id = ?', (int(time.time()), device_id))
    conn.commit()
    conn.close()
    if pending:
        return jsonify({'command': pending})
    else:
        return jsonify({'command': None})

@app.route('/api/result', methods=['POST'])
def api_result():
    data = request.get_json(force=True)
    device_id = data.get('device_id')
    api_key = data.get('api_key')
    result = data.get('result')
    if not device_id or not api_key:
        return jsonify({'error': 'missing credentials'}), 400
    conn = get_db_conn()
    c = conn.cursor()
    c.execute('SELECT api_key FROM devices WHERE id = ?', (device_id,))
    row = c.fetchone()
    if not row or row[0] != api_key:
        conn.close()
        return jsonify({'error': 'unauthorized'}), 403
    c.execute('UPDATE devices SET last_result = ?, last_seen = ? WHERE id = ?', (result, int(time.time()), device_id))
    conn.commit()
    conn.close()
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    init_db()
    host = os.environ.get('SERVER_HOST', '0.0.0.0')
    port = int(os.environ.get('SERVER_PORT', '5000'))
    app.run(host=host, port=port)
