#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import os
import re
import sqlite3
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / 'data' / 'leads.sqlite3'
BRIEF_PATH = ROOT / 'robotics-brief.html'
THANK_YOU_PATH = ROOT / 'brief-unlocked.html'
PREMIUM_PATH = ROOT / 'premium-robotics-brief.html'
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def ensure_db() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            '''
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL UNIQUE,
                source TEXT,
                persona TEXT,
                interest TEXT,
                stage TEXT,
                created_at TEXT NOT NULL,
                ip_address TEXT,
                user_agent TEXT
            )
            '''
        )
        columns = [row[1] for row in conn.execute("PRAGMA table_info(leads)").fetchall()]
        for name in ('persona', 'interest', 'stage'):
            if name not in columns:
                conn.execute(f'ALTER TABLE leads ADD COLUMN {name} TEXT')
        conn.commit()


def save_lead(email: str, source: str, persona: str, interest: str, stage: str, ip: str | None, user_agent: str | None) -> tuple[bool, str]:
    created_at = datetime.now(timezone.utc).isoformat()
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute(
                'INSERT INTO leads (email, source, persona, interest, stage, created_at, ip_address, user_agent) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                (email.lower(), source, persona, interest, stage, created_at, ip, user_agent),
            )
            conn.commit()
        return True, 'saved'
    except sqlite3.IntegrityError:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute(
                'UPDATE leads SET source=?, persona=?, interest=?, stage=?, ip_address=?, user_agent=? WHERE email=?',
                (source, persona, interest, stage, ip, user_agent, email.lower()),
            )
            conn.commit()
        return True, 'updated'


def export_csv() -> str:
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute('SELECT email, source, persona, interest, stage, created_at FROM leads ORDER BY id DESC').fetchall()
    out = []
    out.append(['email', 'source', 'persona', 'interest', 'stage', 'created_at'])
    out.extend(rows)
    from io import StringIO
    buf = StringIO()
    writer = csv.writer(buf)
    writer.writerows(out)
    return buf.getvalue()


class Handler(BaseHTTPRequestHandler):
    def _send_json(self, payload: dict, status: int = 200) -> None:
        raw = json.dumps(payload).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(raw)))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(raw)

    def _send_file(self, path: Path, content_type: str) -> None:
        if not path.exists():
            self.send_error(404, 'File not found')
            return
        raw = path.read_bytes()
        self.send_response(200)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def _redirect(self, location: str) -> None:
        self.send_response(303)
        self.send_header('Location', location)
        self.end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == '/health':
            self._send_json({'ok': True, 'db': str(DB_PATH)})
            return
        if parsed.path == '/download/robotics-brief':
            self._send_file(BRIEF_PATH, 'text/html; charset=utf-8')
            return
        if parsed.path == '/thank-you':
            self._send_file(THANK_YOU_PATH, 'text/html; charset=utf-8')
            return
        if parsed.path == '/premium-offer':
            self._send_file(PREMIUM_PATH, 'text/html; charset=utf-8')
            return
        if parsed.path == '/leads':
            with sqlite3.connect(DB_PATH) as conn:
                rows = conn.execute('SELECT email, source, persona, interest, stage, created_at FROM leads ORDER BY id DESC LIMIT 200').fetchall()
            self._send_json({'count': len(rows), 'leads': rows})
            return
        if parsed.path == '/leads.csv':
            raw = export_csv().encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/csv; charset=utf-8')
            self.send_header('Content-Length', str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)
            return
        self.send_error(404, 'Not found')

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path != '/capture':
            self.send_error(404, 'Not found')
            return

        content_length = int(self.headers.get('Content-Length', '0'))
        raw = self.rfile.read(content_length).decode('utf-8')
        content_type = self.headers.get('Content-Type', '')
        wants_json = 'application/json' in content_type

        if wants_json:
            payload = json.loads(raw or '{}')
        else:
            payload = {k: v[0] for k, v in parse_qs(raw).items()}

        email = (payload.get('email') or '').strip()
        source = (payload.get('source') or 'robotics-brief-download').strip()
        persona = (payload.get('persona') or 'general').strip()
        interest = (payload.get('interest') or 'robotics-brief').strip()
        stage = (payload.get('stage') or 'brief-captured').strip()

        if not EMAIL_RE.match(email):
            if wants_json:
                self._send_json({'ok': False, 'error': 'invalid_email'}, status=400)
            else:
                self._redirect('/thank-you?error=invalid_email')
            return

        ok, state = save_lead(
            email=email,
            source=source,
            persona=persona,
            interest=interest,
            stage=stage,
            ip=self.client_address[0] if self.client_address else None,
            user_agent=self.headers.get('User-Agent'),
        )
        if not ok:
            if wants_json:
                self._send_json({'ok': False, 'error': 'save_failed'}, status=500)
            else:
                self._redirect('/thank-you?error=save_failed')
            return

        if wants_json:
            self._send_json({
                'ok': True,
                'state': state,
                'downloadUrl': '/download/robotics-brief',
                'thankYouUrl': '/thank-you',
                'premiumUrl': '/premium-offer'
            })
        else:
            self._redirect('/thank-you')


def main() -> None:
    ensure_db()
    host = os.environ.get('LEAD_CAPTURE_HOST', '127.0.0.1')
    port = int(os.environ.get('LEAD_CAPTURE_PORT', '8765'))
    server = ThreadingHTTPServer((host, port), Handler)
    print(f'Lead capture server listening on http://{host}:{port}')
    server.serve_forever()


if __name__ == '__main__':
    main()
