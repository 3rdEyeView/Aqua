"""v3 rebuild: rewrites the services / process / work sections of src.html around all 34 web copies
(assets/p-*.jpg), adds Results, Equipment, a filterable gallery with lightbox, and a call-to-action band.
Run once on the v2 src.html:  python3 -I rebuild_v3.py   (then build.py, check.js)"""
import json, re, os
HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open('/tmp/dims.json'))
s = open(os.path.join(HERE, 'src.html'), encoding='utf8').read()

def rsub(pat, new, count=1):
    global s
    s, n = re.subn(pat, lambda m: new, s, count=count, flags=re.S)
    assert n == count, (pat[:60], n)

def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:70], s.count(a))
    s = s.replace(a, b)

def img(k, alt, lazy=True, cls=''):
    w, h = D[k]
    return f'<img{(" class=%r" % cls).replace(chr(39), chr(34)) if cls else ""} src="assets/p-{k}.jpg" alt="{alt}" width="{w}" height="{h}"{" loading=%slazy%s" % (chr(34), chr(34)) if lazy else ""}>'

# ---------------------------------------------------------------- services
SVC = [
 ('Commercial Grounds Maintenance', 'Scheduled mowing, edging, beds and seasonal cleanups that keep a business looking cared for.', '009',
  "Aerial view of a crew member mowing a dealership lawn, with the Comer's Landscaping box truck in the lot."),
 ('Residential Lawn Care', 'Regular mowing, trimming and clean edges, so the yard is ready whenever you are.', '034',
  'A Walker rider mower cutting stripes into a backyard lawn beside a fence and mulch beds.'),
 ('Installation of Decorative Rock', 'Sod, mulch, gravel and decorative rock installed for clean, low-upkeep beds and borders.', '028',
  'A river-rock bed with banana plants and purple flowers curving along a concrete pool deck.'),
 ('Hardscaping', 'Patios, walkways, walls and steps that give the yard structure and a place to gather.', '026c',
  'A round paver patio with a stacked-stone fire pit and a steel grate.'),
 ('Irrigation Installation &amp; Repair', 'New systems put in and existing ones repaired, so the lawn gets water where it needs it.', '020',
  'A white irrigation pipe laid in a trench across a front lawn.'),
 ('Landscape Design &amp; Lighting', 'Planting plans and low-voltage lighting that make the property work after dark too.', '021',
  'A curved paver patio with iron chairs overlooking a striped lawn and stone-edged planting beds.'),
 ('Erosion Control', 'Grading, walls, stone and groundcover to hold a slope and move water where it should go.', '017',
  'A long run of black silt fence on green T-posts along a roadside, with a skid steer in the distance.'),
]
items = []
for i, (t, d, k, alt) in enumerate(SVC):
    items.append(f'''      <div class="svc-item{' is-active' if i == 0 else ''}">
        <button class="svc-btn" type="button"><span class="n">0{i+1}</span><span class="t">{t}<small>{d}</small></span><span class="a" aria-hidden="true">→</span></button>
        <figure class="svc-fig">{img(k, alt)}<figcaption class="ai-chip">Comer's work</figcaption></figure>
      </div>''')
svc = f'''<section class="sec" id="services">
  <div class="wrap">
    <div class="svc-head">
      <div>
        <p class="eyebrow rv">Our Services</p>
        <h2 class="disp h2 rv">One crew for the <em>whole property</em></h2>
      </div>
      <p class="rv">Seven services, year-round, for homes and commercial sites across the Columbia area.</p>
    </div>
    <div class="svc" id="svc">
{chr(10).join(items)}
    </div>
    <p class="swipe" aria-hidden="true">Swipe for all seven →</p>
  </div>
</section>'''
rsub(r'<section class="sec" id="services">.*?</section>', svc)

# ---------------------------------------------------------------- process
proc = f'''<section class="sec on-paper" id="process">
  <div class="wrap">
    <p class="eyebrow rv">How it works</p>
    <h2 class="disp h2 rv">Three words in the logo. <em>One plan</em> for your yard.</h2>
    <div class="proc-grid">
      <article class="proc rv">
        {img('006', 'A wide green lawn with curved mulch beds beside a white house.')}
        <div class="proc-in"><div class="num">01</div><h3>Design</h3><p>Tell us what you have in mind. We look at the site and lay out a plan and a quote.</p></div>
      </article>
      <article class="proc rv" style="--d:.12s">
        {img('037', 'A white irrigation pipe in a trench beside rolls of sod and bare graded soil.')}
        <div class="proc-in"><div class="num">02</div><h3>Install</h3><p>Grading, drainage, sod, rock, hardscape and irrigation, installed by the same company that planned it.</p></div>
      </article>
      <article class="proc rv" style="--d:.24s">
        {img('030', 'A freshly striped lawn curving toward a gravel drive and a line of trees.')}
        <div class="proc-in"><div class="num">03</div><h3>Maintain</h3><p>Reliable, year-round care for lawns and commercial grounds, so the work keeps its shape.</p></div>
      </article>
    </div>
  </div>
</section>'''
rsub(r'<section class="sec on-paper" id="process">.*?</section>', proc)

# ---------------------------------------------------------------- results (pairs)
def pair(n, title, sub, a, b):
    return f'''    <div class="pairrow rv">
      <div class="pairhd"><span class="pn">{n}</span><h3>{title}</h3><p>{sub}</p></div>
      <div class="pair">
        <figure>{img(a[0], a[1])}<figcaption><b>{a[2]}</b>{a[3]}</figcaption></figure>
        <figure>{img(b[0], b[1])}<figcaption><b>{b[2]}</b>{b[3]}</figcaption></figure>
      </div>
    </div>'''
results = f'''<section class="sec" id="results">
  <div class="wrap">
    <div class="svc-head">
      <div>
        <p class="eyebrow rv">Results</p>
        <h2 class="disp h2 rv">Bare ground to <em>finished work</em></h2>
      </div>
      <p class="rv">Three jobs from Comer's own photos, from the first pass to the result.</p>
    </div>
{pair('01', 'Roadside slope', 'Hydroseed goes down, then the bank holds.',
      ('001c', 'A roadside slope sprayed bright green with hydroseed beside a two-lane road.', 'Sprayed', 'Hydroseed day'),
      ('002', 'The same kind of roadside slope covered in thick grass beside a line of pines.', 'Grown in', 'Established cover'))}
{pair('02', 'Drainage crossing', 'A washed-out crossing, then pipe and stone.',
      ('010', 'A washed-out drainage crossing in woods with a corrugated pipe in muddy water.', 'Washed out', 'Pipe exposed, bank cut away'),
      ('011', 'A rebuilt crossing with a culvert pipe set in fresh gravel.', 'Rebuilt', 'Culvert set in gravel'))}
{pair('03', 'Backyard', 'Graded to bare soil, then a lawn that is kept.',
      ('039', 'A graded backyard of bare soil with tracked loader marks and a mini skid steer at the back fence.', 'Graded', 'Mini skid steer on site'),
      ('035', 'A mown striped backyard lawn with clean edges beside a brick walk and a string trimmer.', 'Finished', 'Edged and maintained'))}
  </div>
</section>'''

# ---------------------------------------------------------------- equipment
def eq(k, t, d, alt, d_=''):
    return f'''      <article class="eq rv"{d_}>
        {img(k, alt)}
        <div class="eq-in"><h3>{t}</h3><p>{d}</p></div>
      </article>'''
equipment = f'''<section class="sec eq-sec" id="equipment">
  <div class="wrap">
    <div class="svc-head">
      <div>
        <p class="eyebrow rv">The equipment</p>
        <h2 class="disp h2 rv">Real machines for <em>real ground</em></h2>
      </div>
      <p class="rv">From residential beds to roadside right-of-way, the work calls for more than a push mower.</p>
    </div>
    <div class="eq-grid">
{eq('024', 'Truck &amp; trailer', "Comer's flatbed hauls a tracked skid steer from job to job.", "The white Comer's Landscaping flatbed truck towing a trailer with a CAT skid steer.")}
{eq('025', 'CAT 259D3', 'A tracked skid steer for grading, loading and attachments.', 'A yellow CAT 259D3 compact track loader parked on gravel.', ' style="--d:.1s"')}
{eq('015', 'Brush cutter', 'A mowing attachment for overgrown fields and highway right-of-way.', "The Comer's trailer and a CAT skid steer with a brush cutter beside a highway.", ' style="--d:.2s"')}
{eq('013', 'Compact excavator', 'For drainage pipe, culverts and cutting an access path.', 'A yellow compact excavator on a freshly graded path through woods.', ' style="--d:.3s"')}
    </div>
  </div>
</section>'''

# ---------------------------------------------------------------- gallery
G = [  # key, category, caption, alt, object-position
 ('003', 'drain', 'Basin, grown in', 'A stormwater basin covered in established grass.', '50% 50%'),
 ('019c', 'drain', 'Rip-rap and check dams', 'A new basin with rip-rap stone and erosion-control check dams.', '50% 50%'),
 ('016', 'drain', 'Silt fence trench', 'Posts set along a trench for silt fence beside a road, with a white pickup parked on the shoulder.', '50% 55%'),
 ('010', 'drain', 'Crossing, washed out', 'A washed-out drainage crossing in woods with a corrugated pipe.', '50% 70%'),
 ('011', 'drain', 'Crossing, rebuilt', 'A culvert pipe set in fresh gravel on a woodland crossing.', '50% 70%'),
 ('014', 'drain', 'Eroded bank', 'A cut-away bank above a drainage pipe in the woods.', '50% 60%'),
 ('018', 'drain', 'Site graded behind silt fence', 'A graded construction site with silt fence along the tree line.', '50% 60%'),
 ('017', 'drain', 'Silt fence along the road', 'A long run of black silt fence on green T-posts beside a roadside.', '50% 60%'),
 ('012', 'site', 'Drainage pipe going in', 'A compact excavator beside a length of corrugated drainage pipe.', '50% 70%'),
 ('039', 'site', 'Backyard graded', 'A graded backyard with tracked marks and a mini skid steer at the fence.', '50% 55%'),
 ('038', 'site', 'Pond edge, cleared', 'A cleared lot of bare soil beside a pond and a golf fairway.', '50% 50%'),
 ('023', 'site', 'Pond bank', 'A grassy pond bank with a wooden footbridge.', '50% 55%'),
 ('026', 'hard', 'Paver fire pit patio', 'A round paver patio with a stone fire pit in a backyard.', '50% 62%'),
 ('027', 'hard', 'Fire pit, close up', 'A stacked-stone fire pit ring with a steel grate and gravel base.', '50% 50%'),
 ('029', 'hard', 'Paver walkway', 'A long paver walkway running between two lawns.', '50% 50%'),
 ('028', 'hard', 'River rock by the pool', 'A river-rock border with banana plants along a pool deck.', '50% 50%'),
 ('021', 'hard', 'Paver patio and beds', 'A curved paver patio beside a striped lawn and stone-edged beds.', '50% 55%'),
 ('008', 'lawn', 'Mowing', 'A rider mower cutting a shaded lawn between a walk and mulch beds.', '60% 60%'),
 ('007', 'lawn', 'Backyard lawn', 'A large backyard lawn with curved mulch beds and a deck.', '50% 60%'),
 ('033', 'lawn', 'Backyard lawn', 'A green backyard lawn beside a house with a screened porch.', '50% 60%'),
 ('034', 'lawn', 'Walker mower at work', 'A rider mower leaving stripes on a backyard lawn.', '60% 55%'),
 ('035', 'lawn', 'Edged lawn', 'A neatly edged lawn beside a brick walk and driveway.', '50% 60%'),
 ('030', 'lawn', 'Striped lawn', 'A freshly striped lawn curving toward a gravel drive.', '50% 55%'),
 ('006', 'lawn', 'Lawn and beds', 'A wide green lawn with curved mulch beds beside a white house.', '50% 55%'),
 ('020', 'irr', 'Irrigation line', 'A white irrigation pipe laid in a trench across a front lawn.', '50% 55%'),
 ('037', 'irr', 'Irrigation and sod', 'A pipe in a trench beside rolls of sod and graded soil.', '50% 60%'),
 ('009', 'lawn', 'Commercial mowing', 'Aerial view of a crew member mowing a dealership lawn.', '60% 55%'),
 ('024', 'equip', 'Truck and trailer', "The Comer's Landscaping flatbed towing a skid steer on a trailer.", '30% 50%'),
 ('025', 'equip', 'CAT 259D3', 'A yellow CAT 259D3 compact track loader.', '50% 50%'),
 ('015', 'equip', 'Brush cutter on site', "The Comer's trailer and a skid steer with a brush cutter beside a highway.", '70% 55%'),
 ('013', 'equip', 'Compact excavator', 'A compact excavator on a graded path through woods.', '50% 50%'),
]
CATS = [('all', 'All'), ('drain', 'Drainage &amp; erosion'), ('site', 'Site work'), ('hard', 'Hardscape &amp; rock'),
        ('lawn', 'Lawns &amp; grounds'), ('irr', 'Irrigation &amp; sod'), ('equip', 'Equipment')]
chips = ''.join(f'<button type="button" class="chip" data-f="{k}" aria-pressed="{"true" if k == "all" else "false"}">{n}</button>' for k, n in CATS)
tiles = []
for k, c, cap, alt, pos in G:
    w, h = D[k]
    tiles.append(f'''      <button type="button" class="gi" data-cat="{c}" data-src="assets/p-{k}.jpg" data-cap="{cap}" data-w="{w}" data-h="{h}" aria-label="Open photo: {cap}">
        <img src="assets/p-{k}.jpg" alt="{alt}" width="{w}" height="{h}" loading="lazy" style="object-position:{pos}"><span>{cap}</span>
      </button>''')
gallery = f'''<section class="sec on-paper" id="gallery">
  <div class="wrap">
    <div class="svc-head">
      <div>
        <p class="eyebrow rv">Our Work</p>
        <h2 class="disp h2 rv">Every kind of <em>job</em></h2>
      </div>
      <p class="rv">Photos from Comer's own jobs. Tap a photo to see it full size, or filter by the kind of work.</p>
    </div>
    <div class="chips rv" role="group" aria-label="Filter photos">{chips}</div>
    <p class="count" id="galCount" aria-live="polite"></p>
    <div class="gal" id="gal">
{chr(10).join(tiles)}
    </div>
    <div class="social rv">
      <a class="btn btn-dark" href="https://www.facebook.com/comerslandscaping" target="_blank" rel="noopener">More on Facebook</a>
      <a class="btn btn-ghost-dark" href="https://www.instagram.com/comerslandscapingllc/" target="_blank" rel="noopener">Instagram</a>
    </div>
  </div>
</section>'''

cta = f'''<section class="cta" aria-label="Call Comer's Landscaping">
  <picture><img src="assets/hero-grown.jpg" alt="" width="1920" height="1080" loading="lazy"></picture>
  <div class="wrap cta-in">
    <p class="eyebrow">Ready when you are</p>
    <h2 class="disp">When it comes to quality work, we are the first you should call.</h2>
    <div class="cta-row"><a class="btn btn-lime" href="tel:+18034228031">Call 803.422.8031</a><a class="btn btn-ghost" href="#quote">Request a Quote</a></div>
  </div>
</section>'''

rsub(r'<section class="sec" id="work">.*?</section>', results + '\n\n' + equipment + '\n\n' + gallery + '\n\n' + cta)

# ---------------------------------------------------------------- nav, drawer, footer
NAV_OLD = '<a href="#about">About</a><a href="#services">Services</a><a href="#process">Process</a><a href="#work">Our Work</a>'
NAV_NEW = '<a href="#about">About</a><a href="#services">Services</a><a href="#results">Results</a><a href="#equipment">Equipment</a><a href="#gallery">Our Work</a>'
assert s.count(NAV_OLD)==3, s.count(NAV_OLD)
s = s.replace(NAV_OLD, NAV_NEW)  # header nav, drawer and footer
rep('.drawer a{font-family:var(--disp);text-transform:uppercase;font-size:40px;line-height:1.25;', '.drawer a{font-family:var(--disp);text-transform:uppercase;font-size:34px;line-height:1.22;')

# ---------------------------------------------------------------- css
CSS = '''
[hidden]{display:none!important}
.btn-ghost-dark{border-color:rgba(16,22,15,.5);color:var(--text);background:transparent}
.btn-ghost-dark:hover{border-color:var(--text);background:rgba(16,22,15,.06)}
/* results */
.pairrow{display:grid;grid-template-columns:minmax(180px,.34fr) 1fr;gap:clamp(18px,3vw,44px);align-items:center;padding:clamp(18px,2.4vw,34px) 0;border-top:1px solid var(--line)}
.pairrow:last-child{border-bottom:1px solid var(--line)}
.pairhd .pn{font:700 13px/1 var(--body);letter-spacing:.14em;color:var(--lime)}
.pairhd h3{font-family:var(--disp);font-weight:400;text-transform:uppercase;font-size:clamp(30px,3.4vw,50px);line-height:1;margin-top:10px}
.pairhd p{color:rgba(255,255,255,.72);margin-top:10px;max-width:16em}
.pairrow .pair img{aspect-ratio:4/3;object-position:50% 60%}
/* equipment */
.eq-sec{background:var(--panel)}
.eq-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:clamp(12px,1.6vw,22px)}
.eq{position:relative;border-radius:20px;overflow:hidden;background:#000;aspect-ratio:3/4;display:flex;align-items:flex-end;isolation:isolate}
.eq img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:-2;transition:transform 1.2s cubic-bezier(.2,.7,.2,1)}
.eq:hover img{transform:scale(1.06)}
.eq::after{content:"";position:absolute;inset:0;z-index:-1;background:linear-gradient(0deg,rgba(0,0,0,.92) 0,rgba(0,0,0,.4) 46%,rgba(0,0,0,0) 78%)}
.eq-in{padding:18px}
.eq h3{font-family:var(--disp);font-weight:400;text-transform:uppercase;font-size:clamp(26px,2.4vw,34px);line-height:1;color:var(--lime)}
.eq p{font-size:14.5px;line-height:1.45;margin-top:8px;color:rgba(255,255,255,.86)}
/* gallery */
.chips{display:flex;flex-wrap:wrap;gap:8px}
.chip{min-height:44px;padding:0 18px;border-radius:999px;border:1.5px solid rgba(16,22,15,.28);background:transparent;color:var(--text);font:800 13px/1 var(--body);letter-spacing:.06em;text-transform:uppercase;cursor:pointer;transition:background .2s,color .2s,border-color .2s}
.chip:hover{border-color:var(--text)}
.chip[aria-pressed="true"]{background:var(--ink);border-color:var(--ink);color:#fff}
.count{margin:14px 0 0;font:700 13px/1 var(--body);letter-spacing:.1em;text-transform:uppercase;color:var(--mute)}
.on-paper .gal{margin-top:16px}
.gal{display:grid;grid-template-columns:repeat(4,1fr);gap:clamp(8px,1.2vw,16px)}
.gi{all:unset;box-sizing:border-box;cursor:zoom-in;position:relative;display:block;border-radius:16px;overflow:hidden;background:#111;aspect-ratio:1;isolation:isolate}
.gi:focus-visible{outline:3px solid var(--green);outline-offset:3px}
.gi img{width:100%;height:100%;aspect-ratio:auto;object-fit:cover;transition:transform 1s cubic-bezier(.2,.7,.2,1)}
.gi:hover img{transform:scale(1.06)}
.gi span{position:absolute;inset:auto 0 0 0;padding:34px 12px 11px;background:linear-gradient(0deg,rgba(0,0,0,.82),rgba(0,0,0,0));color:#fff;font:700 13px/1.25 var(--body);opacity:0;transform:translateY(6px);transition:opacity .3s,transform .3s}
.gi:hover span,.gi:focus-visible span{opacity:1;transform:none}
.on-paper .social{margin-top:30px}
/* lightbox */
.lb{position:fixed;inset:0;z-index:80;background:rgba(3,6,4,.94);display:none;align-items:center;justify-content:center;padding:clamp(12px,3vw,40px)}
.lb.is-open{display:flex}
.lb figure{margin:0;display:grid;gap:12px;justify-items:center;max-width:min(1100px,100%)}
.lb img{max-width:100%;max-height:calc(100vh - 150px);max-height:calc(100svh - 150px);width:auto;height:auto;border-radius:12px;box-shadow:0 30px 90px rgba(0,0,0,.6)}
.lb figcaption{font:700 15px/1.3 var(--body);color:#fff;text-align:center}
.lb figcaption small{display:block;margin-top:4px;font-weight:600;color:rgba(255,255,255,.6)}
.lb button{position:absolute;width:52px;height:52px;border-radius:50%;border:1px solid rgba(255,255,255,.35);background:rgba(0,0,0,.5);color:#fff;font-size:22px;cursor:pointer;display:grid;place-items:center}
.lb button:hover{background:var(--lime);color:#0a1005;border-color:var(--lime)}
.lb .lb-x{top:14px;right:14px}.lb .lb-p{left:14px;top:50%;margin-top:-26px}.lb .lb-n{right:14px;top:50%;margin-top:-26px}
/* cta */
.cta{position:relative;isolation:isolate;overflow:hidden;padding:clamp(80px,11vw,150px) 0;text-align:left}
.cta picture,.cta img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:-2}
.cta::after{content:"";position:absolute;inset:0;z-index:-1;background:linear-gradient(90deg,rgba(0,0,0,.86) 0,rgba(0,0,0,.6) 55%,rgba(0,0,0,.3) 100%)}
.cta h2{font-size:clamp(40px,6vw,88px);max-width:12em;margin-top:16px}
.cta-row{display:flex;flex-wrap:wrap;gap:12px;margin-top:28px}
@media (max-width:980px){
  .pairrow{grid-template-columns:1fr}
  .pairhd p{max-width:none}
  .eq-grid{grid-template-columns:repeat(2,1fr)}
  .gal{grid-template-columns:repeat(3,1fr)}
  .chips{flex-wrap:nowrap;overflow-x:auto;margin-inline:calc(-1*var(--gut));padding:0 var(--gut) 6px;scrollbar-width:none}
  .chips::-webkit-scrollbar{display:none}
  .chip{flex:none}
}
@media (max-width:640px){
  .gal{grid-template-columns:repeat(2,1fr)}
  .eq{aspect-ratio:4/5}
  .eq p{font-size:13.5px}
  .gi span{opacity:1;transform:none;font-size:12px;padding:26px 9px 8px}
  .lb button{width:46px;height:46px}
  .cta::after{background:linear-gradient(0deg,rgba(0,0,0,.9) 0,rgba(0,0,0,.6) 100%)}
  .cta-row .btn{flex:1 1 100%}
}
'''
rep('/* quote */', CSS + '/* quote */')
rep('.pair img{width:100%;aspect-ratio:4/5;object-fit:cover;object-position:50% 90%}', '.pair img{width:100%;aspect-ratio:4/5;object-fit:cover;object-position:50% 90%}\n.pair figcaption small{font-weight:600;opacity:.8}')
# the old .gal/.gi rules from v2 are overridden by the later block; drop their duplicates to keep one source of truth
rsub(r'\.gal\{display:grid;grid-template-columns:repeat\(4,1fr\);gap:clamp\(10px,1\.5vw,20px\);margin-top:clamp\(10px,1\.5vw,20px\)\}\n\.gi img\{[^\n]*\n\.gi:hover img\{[^\n]*\n#work \.social\{[^\n]*\n@media \(max-width:980px\)\{\.gal\{[^\n]*\n', '')
rsub(r'\.pair figure,\.gi\{', '.pair figure{')
rep('.pair figcaption,.gi figcaption{', '.pair figcaption{')

# ---------------------------------------------------------------- js
JS = '''
  /* gallery: filter chips + lightbox */
  var tiles=$$('.gi'), chips=$$('.chip'), cnt=$('#galCount'), cur=-1, vis=[];
  function applyFilter(f){
    chips.forEach(function(c){c.setAttribute('aria-pressed', c.getAttribute('data-f')===f)});
    tiles.forEach(function(t){ t.hidden = !(f==='all' || t.getAttribute('data-cat')===f); });
    vis=tiles.filter(function(t){return !t.hidden});
    cnt.textContent = vis.length+' photo'+(vis.length===1?'':'s');
  }
  chips.forEach(function(c){c.addEventListener('click', function(){applyFilter(c.getAttribute('data-f'))})});
  applyFilter('all');
  var lb=d.createElement('div'); lb.className='lb'; lb.setAttribute('role','dialog'); lb.setAttribute('aria-modal','true'); lb.setAttribute('aria-label','Photo viewer');
  lb.innerHTML='<button type="button" class="lb-x" aria-label="Close">✕</button><button type="button" class="lb-p" aria-label="Previous photo">←</button><figure><img alt=""><figcaption></figcaption></figure><button type="button" class="lb-n" aria-label="Next photo">→</button>';
  d.body.appendChild(lb);
  var lbi=$('img',lb), lbc=$('figcaption',lb), opener=null;
  function show(i){
    cur=(i+vis.length)%vis.length; var t=vis[cur], im=$('img',t);
    lbi.src=t.getAttribute('data-src'); lbi.alt=im.alt; lbc.textContent=t.getAttribute('data-cap');
    var s=d.createElement('small'); s.textContent=(cur+1)+' of '+vis.length; lbc.appendChild(s);
  }
  function openLb(t){ opener=t; lb.classList.add('is-open'); d.body.style.overflow='hidden'; show(vis.indexOf(t)); $('.lb-x',lb).focus(); }
  function closeLb(){ lb.classList.remove('is-open'); d.body.style.overflow=''; if(opener) opener.focus(); }
  tiles.forEach(function(t){t.addEventListener('click', function(){openLb(t)})});
  $('.lb-x',lb).addEventListener('click', closeLb); $('.lb-p',lb).addEventListener('click', function(){show(cur-1)}); $('.lb-n',lb).addEventListener('click', function(){show(cur+1)});
  lb.addEventListener('click', function(e){ if(e.target===lb) closeLb(); });
  d.addEventListener('keydown', function(e){
    if(!lb.classList.contains('is-open')) return;
    if(e.key==='Escape') closeLb(); else if(e.key==='ArrowLeft') show(cur-1); else if(e.key==='ArrowRight') show(cur+1);
    else if(e.key==='Tab'){ var b=$$('button',lb), f=b[0], l=b[b.length-1]; if(e.shiftKey && d.activeElement===f){e.preventDefault(); l.focus();} else if(!e.shiftKey && d.activeElement===l){e.preventDefault(); f.focus();} }
  });
  var tx=null; lb.addEventListener('touchstart', function(e){tx=e.touches[0].clientX},{passive:true});
  lb.addEventListener('touchend', function(e){ if(tx===null) return; var dx=e.changedTouches[0].clientX-tx; tx=null; if(Math.abs(dx)>50) show(cur+(dx<0?1:-1)); },{passive:true});

'''
rep('  onScroll();\n})();', JS + '  onScroll();\n})();')

# footer notice + ribbon already say photos are Comer's own; keep as is
open(os.path.join(HERE, 'src.html'), 'w', encoding='utf8').write(s)
print('ok', len(s) // 1024, 'KB source;', len(re.findall(r'assets/p-[\w]+\.jpg', s)), 'photo refs')
