# Builds the build-composition payload for the Pricing comparison table (written to ops/1068-compare.json).
import json
Y = '✓'; N = '—'
ROWS = [
    ('Professionally designed, mobile-responsive website', Y, Y),
    ('Hosting, SSL &amp; ongoing maintenance', Y, Y),
    ('Website updates &amp; technical support', 'Standard', 'Priority'),
    ('Foundational on-page SEO, contact forms &amp; lead capture', Y, Y),
    ('Google review requests, instant lead response &amp; missed-call text-back', Y, Y),
    ('GoHighLevel CRM &amp; lead management pipeline', N, Y),
    ('Advanced SMS &amp; email follow-up, scheduling, reminders &amp; nurturing', N, Y),
    ('Standardized business automations', 'Essential set', '7 in total'),
    ('Google Search Ads setup &amp; ongoing management', N, '1 standard program'),
    ('Monthly advertising &amp; lead performance reporting', N, Y),
    ('Setup fee', '$0', '$0'),
    ('First payment', 'First month at signup', 'First month at signup'),
    ('Google Ads advertising spend', 'Not applicable', 'Paid separately to Google'),
    ('SMS, call &amp; communication usage', 'May be billed separately', 'May be billed separately'),
    ('Commitment', 'Cancel anytime', '3-month minimum'),
]
ROW_BASE = "display: grid; grid-template-columns: 2fr 1fr 1fr; gap: 1rem; align-items: center; width: 100%; padding: 0.85rem 0; border-bottom: 1px solid #E2E7EE;"
ROW_MQ = " @media(--mobile){ grid-template-columns: 1.5fr 1fr 1fr; gap: 0.5rem; }"
ROW_CSS = ROW_BASE + ROW_MQ
SMALL = " @media(--mobile){ font-size: 0.8125rem; }"
CB = "font-family: var(--ax-body, Inter), sans-serif; font-size: 0.9375rem; line-height: 1.4; color: #0A1628; margin: 0;"
CELL = CB + SMALL
VAL = CB + " text-align: center; font-weight: 600;" + SMALL
GVAL = CB + " text-align: center; font-weight: 600; color: #1D6CE2;" + SMALL
HB = "font-family: var(--ax-display, Manrope), sans-serif; font-weight: 800; font-size: 1rem; text-align: center; color: #0A1628; margin: 0;"
HEAD = HB + SMALL
xml, cfg, style, classes = [], {}, {}, {}
def p(cid, text, css):
    xml.append(f'<e-paragraph configuration-id="{cid}"></e-paragraph>'); cfg[cid] = {'paragraph': text}; style[cid] = css
xml.append('<e-flexbox configuration-id="cmp">')
style['cmp'] = ("width: 100%; max-width: 62rem; display: flex; flex-direction: column; gap: 0.5rem; padding: 2rem; "
                "@media(--mobile){ padding: 1.25rem; }")
classes['cmp'] = ['ax-card']
p('cmp-k', 'Compare plans', ''); classes['cmp-k'] = ['ax-eyebrow']; del style['cmp-k']
xml.append('<e-heading configuration-id="cmp-h"></e-heading>'); cfg['cmp-h'] = {'title': 'What each plan includes', 'tag': 'h2'}
classes['cmp-h'] = ['ax-h3']
xml.append('<e-flexbox configuration-id="cmp-head">'); style['cmp-head'] = ROW_BASE + " border-bottom: 2px solid #0A1628;" + ROW_MQ
p('cmp-head-0', '&nbsp;', CELL); p('cmp-head-1', 'Essentials<br>$297/mo', HEAD); p('cmp-head-2', 'Growth<br>$597/mo', HB.replace('#0A1628', '#1D6CE2') + SMALL)
xml.append('</e-flexbox>')
for i, (label, e, g) in enumerate(ROWS):
    xml.append(f'<e-flexbox configuration-id="cmp-r{i}">'); style[f'cmp-r{i}'] = ROW_CSS
    p(f'cmp-r{i}-l', label, CELL); p(f'cmp-r{i}-e', e, VAL); p(f'cmp-r{i}-g', g, GVAL)
    xml.append('</e-flexbox>')
xml.append('<e-flexbox configuration-id="cmp-cta">')
style['cmp-cta'] = ("display: grid; grid-template-columns: 2fr 1fr 1fr; gap: 1rem; width: 100%; padding-block-start: 1.25rem; "
                    "@media(--mobile){ grid-template-columns: 1fr; gap: 0.75rem; }")
p('cmp-cta-0', 'Ready to start? Choose a plan and we will guide you through the next steps.', CELL)
for cid, text, plan, cls in (('cmp-cta-e', 'Get Started', 'essential', 'ax-btn-ghost'), ('cmp-cta-g', 'Get Started', 'growth', 'ax-btn')):
    xml.append(f'<e-button configuration-id="{cid}"></e-button>')
    cfg[cid] = {'text': text, 'link': {'destination': f'/get-started/?plan={plan}', 'isTargetBlank': False, 'tag': 'a'}}
    classes[cid] = [cls]; style[cid] = 'width: 100%; justify-content: center; text-align: center;'
xml.append('</e-flexbox>')
xml.append('</e-flexbox>')
out = {'xml_structure': ''.join(xml), 'element_config': cfg, 'style': style, 'classes': classes}
json.dump(out, open('ops/1068-compare.json', 'w'), indent=1, ensure_ascii=False)
print(json.dumps(out, ensure_ascii=False))
