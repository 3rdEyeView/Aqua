# Updates post_content (the plain HTML copy Yoast/excerpts read) to match the published
# Elementor copy. Dry run unless --write. Elementor data is never sent.
import json, os, sys, urllib.request
auth = os.environ['AXIOM_ELEMENTOR_MCP_AUTH']
def call(pid, body=None):
    req = urllib.request.Request(f'https://axiomsystems.systems/wp-json/wp/v2/pages/{pid}?context=edit',
        data=json.dumps(body).encode() if body else None, method='POST' if body else 'GET',
        headers={'Authorization': 'Basic ' + auth, 'User-Agent': 'curl/8.5.0', 'Content-Type': 'application/json'})
    return json.load(urllib.request.urlopen(req))
from copy_spec import SPEC
NEW_OFFERS = """<h2>Google Review Requests</h2>
<p>Turn Great Service Into a Stronger Reputation.</p>
<p>Make it easier for customers to share their experience. Every Axiom website plan includes simple, automated Google review invitations to help your business build a stronger online reputation.</p>
<p>Neutral Google review invitations</p>
<p>Standardized email workflow or limited SMS</p>
<p>Available upon activation</p>
<a href="/pricing/">Explore Website Plans →</a>
<h2>Axiom Lead Automation</h2>
<p>+$349/month</p>
<p>Never Miss an Opportunity.</p>
<p>Your business doesn't stop when you're busy. Axiom Lead Automation responds to incoming inquiries, recovers missed calls, and automatically follows up with potential customers, helping you turn more opportunities into booked jobs.</p>
<p>Missed-call text-back</p>
<p>Instant lead response</p>
<p>Automated SMS &amp; email follow-up</p>
<p>Lead notifications</p>
<p>Lead nurturing</p>
<p>Basic CRM &amp; pipeline management</p>
<a href="/get-started/?plan=lead-automation">Add Lead Automation →</a>
<p>""" + SPEC[1074]['1a720fb3'][1] + """</p>
<h2>One Connected System. Built to Grow Your Business.</h2>
<p>""" + SPEC[1074]['4c7dd1a6'][1] + """</p>
<p>Axiom Growth: $599/month. """ + SPEC[1074]['52c6582f'][1] + """ Save $49/month.</p>
<a href="/get-started/?plan=growth">Grow My Business</a>
<p>Professional, conversion-focused website</p>
<p>Hosting &amp; ongoing management</p>
<p>Mobile-responsive design</p>
<p>Maintenance &amp; updates</p>
<p>On-page SEO fundamentals</p>
<p>FREE Google review requests</p>
<p>Instant inquiry acknowledgment</p>
<p>Axiom CRM</p>
<p>Missed-call text-back</p>
<p>Automated SMS &amp; email follow-up</p>
<p>Lead pipeline management</p>
<p>Appointment confirmations &amp; reminders</p>
<p>Estimate &amp; quote follow-up</p>
<p>Lead conversion tracking &amp; reporting</p>
<p>PREMIUM ADVERTISING · AXIOM MARKETING</p>
<h2>More Leads. Better Opportunities. Real Growth.</h2>
<p>""" + SPEC[1074]['2abec125'][1] + """</p>
<p>Starting at</p>
<p>$1,500</p>
<p>/month</p>
<p>Ad spend paid separately</p>
<p>Keep your existing website</p>
<a href="/get-started/?plan=marketing">Get More Leads</a>
<p>ACTIVELY MANAGED ADVERTISING</p>
<p>Google Ads strategy &amp; management</p>
<p>Continuous campaign monitoring &amp; optimization</p>
<p>Conversion-focused landing pages</p>
<p>Lead tracking &amp; performance reporting</p>
<p>AUTOMATION · AVAILABLE UPON ACTIVATION</p>
<p>Axiom CRM lead tracking</p>
<p>Automated lead follow-up</p>
<p>""" + SPEC[1074]['2e13ea5d'][1].replace('<strong>', '').replace('</strong>', '') + """</p>
<p>""" + SPEC[1074]['1ec7ff21'][1] + """</p>
<p>EVERY SERVICE</p>"""
MAP_OLD = """<p>Automated Google review requests</p>
<p>Free with every website plan</p>
<p>Missed-call text-back</p>
<p>Lead Response +$149/mo · Included with Growth</p>
<p>Lead nurturing &amp; follow-up</p>
<p>Follow-Up Automation +$199/mo · Included with Growth</p>
<p>Appointment reminders</p>
<p>Included with Growth</p>
<p>Axiom CRM</p>
<p>Included with Growth and Marketing</p>"""
MAP_NEW = """<p>Google review requests</p>
<p>Free with every website plan</p>
<p>Missed-call text-back &amp; lead follow-up</p>
<p>Lead Automation +$349/mo · Included with Growth</p>
<p>Appointment reminders</p>
<p>Included with Growth</p>
<p>Axiom CRM</p>
<p>Included with Lead Automation, Growth and Marketing</p>"""
def plain(s): return s.replace('<br>', ' ')
dry = '--write' not in sys.argv
for pid in (1074, 1068, 1085):
    page = call(pid); c = page['content']['raw']; orig = c; problems = []
    if pid == 1074:
        a = c.index('<h2>Google Review Requests</h2>'); b = c.index('<p>EVERY SERVICE</p>') + len('<p>EVERY SERVICE</p>')
        c = c[:a] + NEW_OFFERS + c[b:]
        if MAP_OLD not in c: problems.append('map')
        c = c.replace(MAP_OLD, MAP_NEW)
        for eid in ('4961b413', '3c6a6564'):
            o, n = SPEC[1074][eid]
            if eid == '3c6a6564':
                o2 = '<p>Campaign optimization</p>\n<p>Included with Marketing</p>'
                if o2 not in c: problems.append(eid)
                c = c.replace(o2, '<p>Ongoing campaign management</p>\n<p>Included with Marketing</p>')
            elif f'<p>{o}</p>' in c: c = c.replace(f'<p>{o}</p>', f'<p>{n}</p>')
            else: problems.append(eid)
    else:
        for eid, (o, n) in SPEC[pid].items():
            for oo in (o, o.replace("'", '&#8217;')):
                if f'>{oo}<' in c: c = c.replace(f'>{oo}<', f'>{n}<', 1); break
            else: problems.append(eid)
    left = [q for q in ['$149', '$199', '$647', '$48', 'Lead Response', 'Follow-Up Automation', 'each completed job'] if q in c]
    print(pid, 'problems', problems, 'old text left', left, 'changed', c != orig)
    if not dry and c != orig:
        r = call(pid, {'content': c})
        print('   written; elementor data unchanged:', r['meta']['_elementor_data'] == page['meta']['_elementor_data'], r['template'], r['status'])
