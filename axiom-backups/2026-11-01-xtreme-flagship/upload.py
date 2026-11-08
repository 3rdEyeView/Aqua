# Uploads the new Xtreme portfolio images to the Axiom media library with alt text; writes media/ids.json
import json, os, urllib.request
auth = os.environ['AXIOM_ELEMENTOR_MCP_AUTH']
FILES = {
 'mobile': ('axiom-portfolio-xtreme-jet-ski-mobile.webp', 'Xtreme Jet Ski Watersports website – mobile',
   'Xtreme Jet Ski Watersports website on a phone: "Jet ski the Gulf. Land on an island." with Check Availability and Call buttons'),
 'desktop': ('axiom-portfolio-xtreme-jet-ski-desktop-2026-11.webp', 'Xtreme Jet Ski Watersports website – desktop (Nov 2026)',
   'Xtreme Jet Ski Watersports homepage in St. Petersburg, Florida, with guided Gulf tour headline and Check Availability and Call buttons'),
 'detail1': ('xtreme-detail-first-screen.webp', 'Xtreme website – first screen detail',
   'Detail of the Xtreme Jet Ski Watersports first screen: headline, tour description, Check Availability and Call buttons'),
 'detail2': ('xtreme-detail-tours.webp', 'Xtreme website – tours and pricing detail',
   'Detail of the Xtreme Jet Ski Watersports tour cards, each with its length, price and a Book button'),
}
ids = {}
for k, (fn, title, alt) in FILES.items():
    data = open('media/' + fn, 'rb').read()
    r = urllib.request.Request('https://axiomsystems.systems/wp-json/wp/v2/media', data=data, method='POST', headers={
        'Authorization': 'Basic ' + auth, 'User-Agent': 'curl/8.5.0', 'Content-Type': 'image/webp',
        'Content-Disposition': f'attachment; filename="{fn}"'})
    m = json.load(urllib.request.urlopen(r))
    r2 = urllib.request.Request(f'https://axiomsystems.systems/wp-json/wp/v2/media/{m["id"]}', data=json.dumps({'title': title, 'alt_text': alt}).encode(), method='POST',
        headers={'Authorization': 'Basic ' + auth, 'User-Agent': 'curl/8.5.0', 'Content-Type': 'application/json'})
    m2 = json.load(urllib.request.urlopen(r2))
    ids[k] = m2['id']; print(k, m2['id'], m2['source_url'], m2['media_details'].get('width'), m2['media_details'].get('height'))
json.dump(ids, open('media/ids.json', 'w'), indent=1)
