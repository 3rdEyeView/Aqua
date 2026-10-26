# Snapshot of all snippets and of each public page's scripts/forms/tracking: snapshot.py <dir>
import json, os, re, sys, time, urllib.request
auth = os.environ['AXIOM_ELEMENTOR_MCP_AUTH']; out = sys.argv[1]; os.makedirs(out, exist_ok=True)
A = {'Authorization': 'Basic ' + auth, 'User-Agent': 'curl/8.5.0'}
def get(p): return json.load(urllib.request.urlopen(urllib.request.Request('https://axiomsystems.systems/wp-json/' + p + ('&' if '?' in p else '?') + 'nc=%d' % time.time(), headers=A)))
lst = get('angie/v1/snippets'); json.dump(lst, open(f'{out}/snippets-list.json', 'w'), indent=1)
for s in lst['snippets']:
    json.dump(get(f"angie/v1/snippets/{s['id']}/files?include_content=true"), open(f"{out}/snippet-{s['id']}.json", 'w'), indent=1)
pages = {}
for u in ['/', '/pricing/', '/add-ons/', '/faq/', '/get-started/', '/get-started/?plan=lead-automation', '/how-it-works/', '/our-work/']:
    h = urllib.request.urlopen(urllib.request.Request('https://axiomsystems.systems' + u + ('&' if '?' in u else '?') + 'nc=%d' % time.time(), headers={'User-Agent': 'Mozilla/5.0'})).read().decode()
    f = h[h.find('<form'):h.find('</form>')] if '<form' in h else ''
    pages[u] = {
        'script_srcs': [re.sub(r'([?&](ver|nc)=[^&"]*)', '', x) for x in re.findall(r'<script[^>]*src="([^"]+)"', h)],
        'gtag_config': re.findall(r'gtag\("config", "([A-Z0-9-]+)"', h),
        'lead_send_to': re.findall(r'"dest":"([^"]+)"', h),
        'form_inputs': re.findall(r"name='([^']+)'", f),
        'plan_label': re.findall(r'axgs-plan"><span>Interested in</span>([^<]+)', h),
        'tel_links': len(re.findall(r'href="tel:\+17275917527"', h)),
        'nav_links': re.findall(r'<a[^>]+href="(/[a-z-]*/?)"', h)[:20],
        'leadconnector_widget_tags': len(re.findall(r'widgets\.leadconnectorhq\.com/loader\.js', h)),
        'widget_ids': re.findall(r'data-widget-id="([a-z0-9]+)"', h),
    }
json.dump(pages, open(f'{out}/pages.json', 'w'), indent=1)
st = get('axiom/v1/crm-sync')['settings']
json.dump({k: st[k] for k in ('mode', 'pipeline_id', 'field_map', 'test_emails')}, open(f'{out}/crm-sync-settings.json', 'w'), indent=1)
fp = get('axiom/v1/form-protection'); json.dump({k: fp[k] for k in ('mode', 'site_key_set', 'secret_set')}, open(f'{out}/form-protection.json', 'w'), indent=1)
print('snippets', [s['id'] for s in lst['snippets']], '| widget tags per page', {u: p['leadconnector_widget_tags'] for u, p in pages.items()}, '| crm', st['mode'], '| fp', fp['mode'], fp['site_key_set'])
