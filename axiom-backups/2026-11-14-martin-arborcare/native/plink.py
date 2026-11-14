"""Prints a fresh signed Elementor preview URL for page 2057 (links expire after ~10 minutes)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import axmcp as mcp
mcp.init(); print(mcp.call("elementor-create-preview-link", {"post_id": int(os.environ.get("MA_PID", "2057"))})["url"])
