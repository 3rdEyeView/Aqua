"""Thin wrapper over ../2026-11-08-arroyos/native/axmcp.py (adds the protocol-version header the endpoint now requires)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "2026-11-08-arroyos", "native"))
import axmcp
axmcp.H["MCP-Protocol-Version"] = "2025-06-18"
axmcp.init()
call, rpc = axmcp.call, axmcp.rpc
