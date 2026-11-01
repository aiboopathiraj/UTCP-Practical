# UTCP-Practical
latest tool calling structure to latest way of tool calling

**Execution Steps**

1) create venv - mac

```bash
uv venv .
source bin/activate
```
create .env - include your GOOGLE_API_KEY

2) run tool fastapi server :

```bash
granian --interface asgi tool:app --port 8000
```

3) run main server

```bash
granian --interface asgi main:app --port 8001
```
