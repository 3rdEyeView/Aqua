"""Prints a fresh signed Elementor preview URL for page 2118 (links expire after ~10 minutes)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import axmcp as mcp
mcp.init(); print(mcp.call("elementor-create-preview-link", {"post_id": int(os.environ.get("MP_PID", "2118"))})["url"])
