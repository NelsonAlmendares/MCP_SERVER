# Oracle Development MCP — Phase 1

MCP server for internal Oracle development diagnostics. **No Oracle connection in Phase 1.**
The demo tool returns explicitly simulated data.

## Prerequisites
- Python 3.11 or newer
- Linux internal server
- Outbound package access to a trusted Python package index, or a reviewed internal mirror

## Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[dev]'
cp .env.example .env
python -m pytest -q
python -m oracle_development_mcp.server
```

The Streamable HTTP MCP endpoint defaults to `http://127.0.0.1:8000/mcp`.
Do not treat `/mcp` as a normal REST GET endpoint; use an MCP-aware client.

## Inspect
From the server or through a secured SSH tunnel:
```bash
npx @modelcontextprotocol/inspector
```
In the Inspector select Streamable HTTP, set URL to
`http://127.0.0.1:8000/mcp`, connect, list tools and invoke:
- `estado_servidor` (no arguments)
- `listar_objetos_invalidos_demo` with `{ "esquema": "DEV" }`

## Internal server deployment
1. Review the code and dependencies and install under `/opt/oracle-development-mcp`.
2. Create an unprivileged `oracle-mcp` service account.
3. Install dependencies in `/opt/oracle-development-mcp/.venv`.
4. Put config values in `/etc/oracle-development-mcp/environment` (systemd `KEY=value` format).
5. Install `deploy/oracle-development-mcp.service` under `/etc/systemd/system/`.
6. Have an administrator review permissions and run `systemctl daemon-reload`, then `systemctl enable --now oracle-development-mcp`.
7. Check `journalctl -u oracle-development-mcp -n 100 --no-pager`.

**Do not expose port 8000 externally.** The server binds to loopback by design.
A remote ChatGPT connection requires a separately designed authenticated HTTPS
entry point or supported secure tunnel, origin checks, authorization, and auditing.
The included service is not a production-ready internet-facing deployment.

## Phase 1 acceptance criteria
- Unit tests pass.
- MCP Inspector lists two tools.
- Status reports `oracle_connected=false` and `read_only=true`.
- Demo result clearly identifies simulated data.
- Requests for `SYS`, `PROD`, and cross-environment UAT are rejected.
- No Oracle DDL, DML or COMMIT is performed.
