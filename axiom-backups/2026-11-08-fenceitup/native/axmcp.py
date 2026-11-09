"""Minimal JSON-RPC client for the axiomsystems.systems Elementor MCP endpoint (same server/auth as the MCP tools)."""
import json, os, sys, urllib.request
URL = "https://axiomsystems.systems/wp-json/elementor/mcp/"
H = {"Authorization": "Basic " + os.environ["AXIOM_ELEMENTOR_MCP_AUTH"], "Content-Type": "application/json",
     "Accept": "application/json, text/event-stream", "User-Agent": "curl/8.5.0"}
SID = None
def rpc(method, params=None, _id=[0]):
    global SID
    _id[0] += 1
    body = {"jsonrpc": "2.0", "id": _id[0], "method": method}
    if params is not None: body["params"] = params
    h = dict(H)
    if SID: h["Mcp-Session-Id"] = SID
    r = urllib.request.urlopen(urllib.request.Request(URL, data=json.dumps(body).encode(), headers=h), timeout=300)
    SID = r.headers.get("Mcp-Session-Id") or SID
    raw = r.read().decode()
    if raw.startswith("event:") or "data:" in raw[:20]:
        raw = "\n".join(l[5:] for l in raw.splitlines() if l.startswith("data:"))
    return json.loads(raw) if raw.strip() else None
def init():
    rpc("initialize", {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "axiom-demo-build", "version": "1"}})
    try: rpc("notifications/initialized")
    except Exception: pass
def call(tool, args):
    r = rpc("tools/call", {"name": tool, "arguments": args})
    if "error" in r: return {"error": r["error"]}
    c = r["result"]
    txt = "".join(x.get("text", "") for x in c.get("content", []))
    try: return json.loads(txt)
    except Exception: return {"raw": txt, "isError": c.get("isError")}
if __name__ == "__main__":
    init()
    tools = rpc("tools/list")["result"]["tools"]
    print([t["name"] for t in tools][:80])
