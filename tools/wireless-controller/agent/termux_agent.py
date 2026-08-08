"""
Simple Termux-compatible Python agent for the Wireless Controller.

Usage (on device):
- Install Termux or a Linux environment with Python 3
- pip install requests
- Edit SERVER_URL and REGISTER_SECRET or pass via env
- Run: python3 termux_agent.py

The agent will register (first run), store credentials in agent_config.json, then poll the server for commands
and execute only a small whitelist of safe commands. Results are posted back to the server.
"""

import os
import sys
import time
import json
import requests
import subprocess
from pathlib import Path

CONFIG_FILE = Path.home() / '.mira_agent_config.json'
SERVER_URL = os.environ.get('MIRA_SERVER', 'http://YOUR_SERVER:5000')
REGISTER_SECRET = os.environ.get('MIRA_REGISTER_SECRET', 'register-secret')
DEVICE_NAME = os.environ.get('MIRA_DEVICE_NAME', None) or subprocess.getoutput('hostname')
POLL_INTERVAL = int(os.environ.get('MIRA_POLL_INTERVAL', '5'))

# Whitelisted commands - only these can be executed by the agent
WHITELIST = [
    'uptime',
    'uname -a',
    'hostname',
    'whoami',
    'df -h',
    'ip addr',
    'ping -c 3 8.8.8.8'
]


def save_config(conf):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(conf, f)


def load_config():
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return None


def register():
    url = SERVER_URL.rstrip('/') + '/api/register'
    payload = {'name': DEVICE_NAME, 'register_secret': REGISTER_SECRET}
    print('Registering with server...', url)
    r = requests.post(url, json=payload, timeout=10)
    if r.status_code == 200:
        data = r.json()
        conf = {'device_id': data['device_id'], 'api_key': data['api_key'], 'server': SERVER_URL}
        save_config(conf)
        print('Registered:', conf['device_id'])
        return conf
    else:
        print('Registration failed:', r.status_code, r.text)
        return None


def poll_and_run(conf):
    url = conf['server'].rstrip('/') + '/api/poll'
    payload = {'device_id': conf['device_id'], 'api_key': conf['api_key']}
    try:
        r = requests.post(url, json=payload, timeout=15)
    except Exception as e:
        print('Poll error', e)
        return
    if r.status_code != 200:
        print('Poll failed', r.status_code, r.text)
        return
    data = r.json()
    cmd = data.get('command')
    if cmd:
        cmd = cmd.strip()
        print('Received command:', cmd)
        # check whitelist
        allowed = any(cmd == w or cmd.startswith(w + ' ') for w in WHITELIST)
        if not allowed:
            result = 'Command not allowed'
        else:
            try:
                completed = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
                result = 'OUT:\n' + completed.stdout + '\nERR:\n' + completed.stderr
            except Exception as e:
                result = f'Execution error: {e}'
        # send result
        send_result(conf, result)


def send_result(conf, result):
    url = conf['server'].rstrip('/') + '/api/result'
    payload = {'device_id': conf['device_id'], 'api_key': conf['api_key'], 'result': result}
    try:
        r = requests.post(url, json=payload, timeout=15)
        if r.status_code == 200:
            print('Result sent')
        else:
            print('Result send failed', r.status_code, r.text)
    except Exception as e:
        print('Result send error', e)


def main():
    conf = load_config()
    if not conf:
        conf = register()
        if not conf:
            print('Could not register. Exiting.')
            sys.exit(1)
    print('Starting poll loop. Server:', conf['server'])
    while True:
        try:
            poll_and_run(conf)
        except Exception as e:
            print('Loop error', e)
        time.sleep(POLL_INTERVAL)

if __name__ == '__main__':
    main()
