#!/usr/bin/env python3
"""Restore Axiom Systems pages from this backup.

Usage:  AXIOM_ELEMENTOR_MCP_AUTH=<base64 user:app-password> python3 restore.py 1068 [1074 ...]

For each page ID it writes the saved Elementor data, page settings and
template back through the WordPress REST API. Afterwards, regenerate CSS
(Elementor > Tools > Regenerate Files & Data) or re-publish the page in
Elementor, and clear the Kinsta cache. Snippets: paste snippets/<id>-main.php
back into the matching Angie snippet (or use angie-update-snippet-files).
"""
import json, os, sys, urllib.request
BASE = 'https://axiomsystems.systems/wp-json/wp/v2/pages/'
here = os.path.dirname(os.path.abspath(__file__))
auth = os.environ['AXIOM_ELEMENTOR_MCP_AUTH']
for pid in sys.argv[1:]:
    b = json.load(open(os.path.join(here, 'pages', f'{pid}.json')))
    m = b['meta']
    body = {'template': b['template'], 'status': b['status'],
            'meta': {k: m[k] for k in ('_elementor_edit_mode', '_elementor_template_type', '_elementor_data', '_elementor_page_settings')}}
    req = urllib.request.Request(BASE + pid, json.dumps(body).encode(), method='POST',
                                 headers={'Authorization': 'Basic ' + auth, 'Content-Type': 'application/json', 'User-Agent': 'curl/8.5.0'})
    d = json.load(urllib.request.urlopen(req, timeout=120))
    ok = d['meta']['_elementor_data'] == m['_elementor_data']
    print(pid, d['slug'], d['status'], d['template'], 'restored' if ok else 'MISMATCH')
