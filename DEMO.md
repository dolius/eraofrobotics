# Demo walkthrough

## What this gives you
- a real PDF brief: `robotics-brief-real.pdf`
- a local site demo server on port 8000
- the lead capture server on port 8765
- a Safari Selenium walkthrough script with screenshots

## Run the local site server
```bash
cd /Users/demo/.openclaw/workspace/eraofrobotics
../.venv/bin/python -m http.server 8000
```

## Run the lead capture server
```bash
cd /Users/demo/.openclaw/workspace/eraofrobotics
../.venv/bin/python lead_capture_server.py
```

## Run the walkthrough
```bash
cd /Users/demo/.openclaw/workspace/eraofrobotics
../.venv/bin/python demo_walkthrough.py
```

## Safari note
If Safari remote automation is not enabled, open Safari and enable:
- Develop → Allow Remote Automation

## Output
Screenshots will be saved to:
- `demo-screens/`
