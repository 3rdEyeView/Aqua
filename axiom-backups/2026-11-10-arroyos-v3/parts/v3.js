/* ===== V3: view switch, scroll reveal, lead simulation. Self-contained: no fetch, no storage, no tracking. ===== */
(function(){
  var root=document.documentElement, body=document.body;
  function $(s,c){return (c||document).querySelector(s)} function $$(s,c){return Array.prototype.slice.call((c||document).querySelectorAll(s))}
  function clamp(x){return x<0?0:x>1?1:x} function seg(p,a,b){return clamp((p-a)/(b-a))} function ease(t){return t*t*(3-2*t)}

  /* ---------- view switch ---------- */
  var tabs=$$('.pbar button');
  function setView(v, keep){
    body.setAttribute('data-view', v);
    tabs.forEach(function(b){ b.setAttribute('aria-pressed', b.dataset.view===v); });
    try{ history.replaceState(null,'', v==='lead' ? '#lead-demo' : location.pathname+location.search); }catch(e){}
    if(!keep) window.scrollTo({top:0,left:0,behavior:'instant'});
    if(v==='home') { setMode(); }
  }
  tabs.forEach(function(b){ b.addEventListener('click', function(){ setView(b.dataset.view); }); });

  /* ---------- reveal ---------- */
  var rv=$('.rv'), bg=$('.rv__bg'), dim=$('.rv__dim'), intro=$('.rv__intro'), lines=$$('.rv__line'), cut=$('.rv__cut'), cutImg=$('.rv__cut img'), cutCap=$('.rv__cut figcaption'),
      proj=$('.rv__proj'), projImg=$('.rv__proj>img'), card=$('.rv__card'), pill=$('.rv__pill'), rail=$$('.rv__rail li'), toggle=$('.rv .vtoggle');
  var fxq=window.matchMedia('(min-width: 900px) and (min-height: 540px) and (prefers-reduced-motion: no-preference)');
  var rmq=window.matchMedia('(prefers-reduced-motion: reduce)');
  var fx=false, raf=0, scrubbed=[bg,dim,intro,cut,cutImg,cutCap,proj,projImg,card,pill,toggle].concat(lines);
  function setMode(){
    fx=fxq.matches;
    root.classList.toggle('fx', fx); root.classList.toggle('static', rmq.matches); root.classList.toggle('lite', !fx && !rmq.matches);
    if(!fx) scrubbed.forEach(function(el){ el.removeAttribute('style'); });
    tick();
  }
  function tick(){
    raf=0; if(!fx || body.getAttribute('data-view')!=='home') return;
    var r=rv.getBoundingClientRect(), W=window.innerWidth, H=window.innerHeight, p=clamp(-r.top/(r.height-H));
    /* 01 beginning: headline over the aerial, then it lifts away */
    var a=ease(seg(p,.05,.15));
    intro.style.opacity=1-a; intro.style.transform='translate3d(0,'+(-70*a)+'px,0)'; intro.style.visibility=a>=1?'hidden':'visible';
    /* footage holds, slow push-in, dims a little under the type */
    bg.style.transform='scale('+(1+.14*seg(p,0,.62))+')';
    dim.style.opacity=.34*seg(p,.12,.24);
    /* 02 reveal: three oversized lines cross the frame in alternating directions */
    lines.forEach(function(l,i){
      var t=seg(p,.13+.075*i,.47+.075*i), w=l.offsetWidth, dir=+l.dataset.dir;
      var x = dir>0 ? W - t*(W+w) : -w + t*(W+w);
      l.style.transform='translate3d('+x+'px,0,0)';
    });
    /* montage cut: another property opens from a centre slit */
    var c=ease(seg(p,.6,.7));
    cut.style.clipPath='inset(0 '+(50-50*c)+'% 0 '+(50-50*c)+'%)'; cut.style.visibility=c>0?'visible':'hidden';
    cutImg.style.transform='scale('+(1.22-.14*seg(p,.6,.8))+')';
    cutCap.style.opacity=seg(p,.66,.71)*(1-seg(p,.76,.8));
    /* 03 finish: close-up wipes up, settles from a tight crop, details arrive */
    var d=ease(seg(p,.76,.86));
    proj.style.clipPath='inset('+(100-100*d)+'% 0 0 0)'; proj.style.visibility=d>0?'visible':'hidden';
    projImg.style.transform='scale('+(1.34-.34*ease(seg(p,.76,.95)))+')';
    var e=ease(seg(p,.9,.985));
    card.style.opacity=e; card.style.transform='translate3d(0,'+(46*(1-e))+'px,0)';
    /* estimate button stays reachable between the two big ones */
    var pv=seg(p,.13,.17)*(1-seg(p,.88,.92));
    pill.style.opacity=pv; pill.style.visibility=pv>0?'visible':'hidden';
    toggle.style.opacity=1-seg(p,.55,.6); toggle.style.visibility=p>.6?'hidden':'visible';
    var stage=p<.12?0:p<.82?1:2; rail.forEach(function(li,i){ li.classList.toggle('is-on', i===stage); });
  }
  function onScroll(){ if(!raf) raf=requestAnimationFrame(tick); }
  window.addEventListener('scroll', onScroll, {passive:true}); window.addEventListener('resize', onScroll);
  [fxq,rmq].forEach(function(q){ (q.addEventListener?q.addEventListener.bind(q,'change'):q.addListener.bind(q))(setMode); });
  $$('.rv__rail button').forEach(function(b){ b.addEventListener('click', function(){
    var top=rv.getBoundingClientRect().top+window.scrollY, travel=rv.offsetHeight-window.innerHeight;
    window.scrollTo({top: top + (+b.dataset.to)*travel, behavior:'smooth'});
  }); });
  /* phones: one-shot enter transitions, no scroll scrubbing */
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(es){ es.forEach(function(en){ if(en.isIntersecting){ en.target.classList.add('in'); io.unobserve(en.target); } }); }, {threshold:.35});
    $$('.io').forEach(function(el){ io.observe(el); });
  } else $$('.io').forEach(function(el){ el.classList.add('in'); });

  /* ---------- lead simulation ---------- */
  var S, els={ clock:$('#ld-clock'), start:$('#ld-start'), s1:$('#ld-s1'), s2:$('#ld-s2'), s3a:$('#ld-s3a'), s3b:$('#ld-s3b'), reset:$('#ld-reset'),
    url:$('#ph-url'), ad:$('#ph-ad'), form:$('#ph-form'), inbox:$('#ph-inbox'), name:$('#ph-name'), msgs:$('#ph-msgs'),
    live:$('#crm-live'), empty:$('#crm-empty'), bodyEl:$('#crm-body'), lead:$('#crm-lead'), src:$('#crm-src'), auto:$('#crm-auto'), autoS:$('#auto-state'), autoN:$('#auto-next'), owner:$('#crm-owner'), tl:$('#crm-tl') };
  var SRC={ platform:'Google Ads', medium:'cpc', campaign:'Landscaping – Bradenton (sample)', keyword:'“landscaper near me”', click:'SAMPLE-GCLID-0142', page:'/estimate' };
  var defaults={}; $$('input,select', els.form).forEach(function(i){ defaults[i.name]= i.type==='checkbox' ? i.checked : i.value; });
  function el(tag, cls, text){ var n=document.createElement(tag); if(cls) n.className=cls; if(text!=null) n.textContent=text; return n; }
  function rows(dl, list){ dl.textContent=''; list.forEach(function(r){ var d=el('div'), dd=el('dd'); d.appendChild(el('dt',null,r[0])); if(r[2]){ dd.appendChild(el('span','tag tag--'+r[2], r[1])); } else dd.textContent=r[1]; d.appendChild(dd); dl.appendChild(d); }); }
  function ev(time, title, text, kind){ var li=el('li','ev is-new'+(kind?' ev--'+kind:'')); li.appendChild(el('time',null,time)); li.appendChild(el('b',null,title)); if(text) li.appendChild(el('p',null,text)); els.tl.insertBefore(li, els.tl.firstChild); }
  function msg(box, kind, head, when, text){ var m=el('div','msg is-new msg--'+kind), b=el('b'); b.appendChild(el('span',null,head)); b.appendChild(el('span',null,when)); m.appendChild(b); m.appendChild(document.createTextNode(text)); box.appendChild(m); m.scrollIntoView && 0; }
  function group(box, text){ box.appendChild(el('p','mgroup',text)); }
  function stage(key, label){
    $$('.col').forEach(function(c){ c.classList.toggle('is-on', c.dataset.stage===key); $('.slot',c).textContent=''; });
    var c=el('div','lcard is-new'); c.appendChild(el('b',null,S.lead.first+' '+S.lead.last)); c.appendChild(el('span',null,S.lead.service)); c.appendChild(document.createElement('br')); c.appendChild(el('i',null,'Google Ads'));
    $('.col[data-stage="'+key+'"] .slot').appendChild(c);
    S.stageLabel=label; els.live.textContent='Stage: '+label; renderLead();
  }
  function renderLead(){
    var L=S.lead;
    rows(els.lead, [['Name',L.first+' '+L.last],['Service',L.service],['Phone',L.phone],['Email',L.email],['SMS opt-in', L.sms?'Yes':'No', L.sms?'y':'n'],['Stage',S.stageLabel]]);
    rows(els.src, [['Platform',SRC.platform+' (simulated)'],['Medium',SRC.medium],['Campaign',SRC.campaign],['Keyword',SRC.keyword],['Click ID',SRC.click],['Landing page',SRC.page]]);
  }
  function clock(t){ S.clock=t; els.clock.textContent=t; }
  function auto(state, next, stopped){ els.autoS.textContent=state; els.autoN.textContent=next; els.auto.classList.toggle('is-stop', !!stopped); }
  function buttons(){
    var st=S.step;
    els.start.disabled = st!==0; els.s1.disabled = st!==1; els.s2.disabled = st!==2; els.s3a.disabled = els.s3b.disabled = !(st===2||st===3);
    els.start.classList.toggle('is-next', st===0); els.s1.classList.toggle('is-next', st===1); els.s2.classList.toggle('is-next', st===2);
    els.s3a.classList.toggle('is-next', st===3); els.s3b.classList.toggle('is-next', st===3); els.reset.classList.toggle('is-next', st===4);
    els.start.classList.toggle('is-done', st>0); els.s1.classList.toggle('is-done', st>1); els.s2.classList.toggle('is-done', S.followed);
    els.s3a.classList.toggle('is-done', S.outcome==='reply'); els.s3b.classList.toggle('is-done', S.outcome==='book');
    var bar=$('.ld__steps'), nx=$('.ld__step.is-next', bar); /* keep the next control in view on narrow screens */
    if(nx) bar.scrollLeft=Math.max(0, nx.offsetLeft - bar.offsetLeft - 12);
  }
  function reset(){
    S={ step:0, lead:null, followed:false, outcome:null, stageLabel:'' };
    $$('input,select', els.form).forEach(function(i){ if(i.type==='checkbox') i.checked=defaults[i.name]; else i.value=defaults[i.name]; });
    $$('.is-bad', els.form).forEach(function(f){ f.classList.remove('is-bad'); });
    els.ad.hidden=false; els.form.hidden=true; els.inbox.hidden=true; els.msgs.textContent=''; els.owner.textContent=''; els.tl.textContent='';
    els.url.textContent='Search results · sample';
    els.empty.hidden=false; els.bodyEl.hidden=true; els.live.textContent='Waiting for a visitor'; els.live.classList.remove('is-live');
    $$('.col').forEach(function(c){ c.classList.remove('is-on'); $('.slot',c).textContent=''; });
    clock('Tue · 10:41 AM'); buttons();
  }
  function startVisit(){
    if(S.step!==0) return; S.step=1;
    els.ad.hidden=true; els.form.hidden=false;
    els.url.textContent='arroyoslawncare.com/estimate?utm_source=google&utm_medium=cpc&gclid='+SRC.click;
    els.live.textContent='1 visitor on /estimate · source: Google Ads'; els.live.classList.add('is-live');
    buttons(); els.form.elements.first.focus({preventScroll:true});
  }
  function bad(i,on){ i.closest('.fld').classList.toggle('is-bad',on); return !on; }
  function submit(){
    if(S.step!==1) return;
    var f=els.form.elements, digits=f.phone.value.replace(/\D/g,'');
    var ok=[bad(f.first,!f.first.value.trim()), bad(f.last,!f.last.value.trim()), bad(f.phone,!(digits.length===10||(digits.length===11&&digits[0]==='1'))), bad(f.email,!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(f.email.value.trim()))].every(Boolean);
    if(!ok){ $('.is-bad .inp', els.form).focus(); return; }
    S.lead={ first:f.first.value.trim(), last:f.last.value.trim(), phone:f.phone.value.trim(), email:f.email.value.trim(), service:f.service.value, sms:f.sms.checked };
    var L=S.lead; S.step=2; clock('Tue · 10:42 AM');
    els.form.hidden=true; els.inbox.hidden=false; els.name.textContent=L.first;
    els.empty.hidden=true; els.bodyEl.hidden=false; els.live.textContent='New lead · just now'; els.live.classList.add('is-live');
    ev('Tue 10:41 AM','Ad click captured', SRC.platform+' (simulated) · '+SRC.campaign+' · keyword '+SRC.keyword+' · click ID '+SRC.click, 'mute');
    ev('Tue 10:42 AM','Estimate request submitted', L.service+' · from '+SRC.page);
    stage('new','New Lead');
    ev('Tue 10:42 AM','Lead entered the pipeline: New Lead','Contact created with the ad source attached.');
    ev('Tue 10:42 AM','Owner notified','Push and email to the owner with the lead’s details.');
    msg(els.owner,'push','New estimate request','10:42 AM', L.first+' '+L.last+' · '+L.service+' · '+L.phone+' · via Google Ads');
    ev('Tue 10:42 AM','Acknowledgment email sent','To '+L.email);
    group(els.msgs,'Tue 10:42 AM');
    msg(els.msgs,'email','Email · Arroyo’s Lawn Care','10:42 AM','Hi '+L.first+', thanks for reaching out. We got your request for '+L.service+' and will reply today to set up a walkthrough.');
    if(L.sms){ ev('Tue 10:42 AM','Acknowledgment text sent','To '+L.phone+' · lead opted in to texts');
      msg(els.msgs,'sms','Text · Arroyo’s Lawn Care','10:42 AM','Arroyo’s Lawn Care: got your estimate request, '+L.first+'. We’ll reach out today. Reply STOP to opt out.'); }
    else { ev('Tue 10:42 AM','Text not sent','No SMS opt-in on this lead. Email only.','mute');
      msg(els.msgs,'off','Text','—','No text sent: this lead did not opt in to SMS.'); }
    ev('Tue 10:42 AM','Follow-up scheduled','If there is no reply: follow-up 1 on Wed 9:00 AM.','warn');
    auto('Active · waiting for a reply','Next: follow-up 1 · Wed 9:00 AM');
    buttons(); if(window.innerWidth<1100) $('.crm').scrollIntoView({block:'start'});
  }
  function noReply(){
    if(S.step!==2) return; var L=S.lead; S.step=3; S.followed=true; clock('Wed · 9:00 AM');
    ev('Wed 9:00 AM','No reply yet','22 hours since the request. Demo clock advanced.','warn');
    stage('follow','Follow-Up');
    ev('Wed 9:00 AM','Scheduled follow-up 1 sent', L.sms ? 'Email and text to the homeowner.' : 'Email to the homeowner. No text: no SMS opt-in.');
    group(els.msgs,'Wed 9:00 AM');
    msg(els.msgs,'email','Email · Arroyo’s Lawn Care','9:00 AM','Hi '+L.first+', just checking in on your estimate request. Want to pick a time for a quick walkthrough?');
    if(L.sms) msg(els.msgs,'sms','Text · Arroyo’s Lawn Care','9:00 AM','Hi '+L.first+', still want an estimate for '+L.service+'? Reply here and we’ll set a time.');
    ev('Wed 9:00 AM','Owner task created','Call '+L.first+' '+L.last+': no reply yet.');
    msg(els.owner,'push','Task','9:00 AM','Call '+L.first+' '+L.last+' · no reply to the estimate acknowledgment yet');
    ev('Wed 9:00 AM','Next follow-up scheduled','Follow-up 2 on Fri 9:00 AM if there is still no reply.','warn');
    auto('Active · follow-up 1 sent','Next: follow-up 2 · Fri 9:00 AM');
    buttons();
  }
  function resolve(kind){
    if(!(S.step===2||S.step===3)) return; var L=S.lead, day=S.followed?'Wed':'Tue', hm=S.followed?'9:26 AM':'11:08 AM', t=day+' '+hm, via=L.sms?'text':'email';
    var pending=S.followed?'follow-up 2 (Fri 9:00 AM)':'follow-up 1 (Wed 9:00 AM)';
    S.step=4; S.outcome=kind; clock(day+' · '+hm); group(els.msgs,t);
    if(kind==='reply'){
      msg(els.msgs,'out','Homeowner · '+via,hm,'Yes, still interested. Can you come by Thursday?');
      ev(t,'Homeowner replied by '+via,'“Yes, still interested. Can you come by Thursday?”');
      stage('replied','Replied');
      ev(t,'Stage updated: Replied','Moved automatically when the reply came in.');
      msg(els.owner,'push','Reply from '+L.first,hm,'“Yes, still interested. Can you come by Thursday?” Tap to answer.');
    } else {
      msg(els.msgs,'out','Homeowner · booking link',hm,'Booked: property walkthrough, Thu 2:00 PM');
      ev(t,'Homeowner booked a walkthrough','Thu 2:00 PM · booked from the link in the follow-up.');
      stage('booked','Walkthrough Booked');
      ev(t,'Stage updated: Walkthrough Booked','Moved automatically when the booking came in.');
      ev(t,'Booking confirmation sent', L.sms?'Email and text to the homeowner.':'Email to the homeowner.');
      msg(els.msgs, L.sms?'sms':'email', (L.sms?'Text':'Email')+' · Arroyo’s Lawn Care',hm,'You’re booked for a property walkthrough on Thu at 2:00 PM. See you then.');
      msg(els.owner,'push','Walkthrough booked',hm,L.first+' '+L.last+' · Thu 2:00 PM · '+L.service);
    }
    ev(t,'Automated follow-up stopped','1 scheduled message cancelled: '+pending+'. Nothing else goes out automatically.','stop');
    auto('Stopped · homeowner '+(kind==='reply'?'replied':'booked'),'Cancelled: '+pending, true);
    buttons();
  }
  els.start.addEventListener('click', startVisit); $('#ph-start').addEventListener('click', startVisit);
  els.form.addEventListener('submit', function(e){ e.preventDefault(); submit(); });
  els.s1.addEventListener('click', submit); els.s2.addEventListener('click', noReply);
  els.s3a.addEventListener('click', function(){ resolve('reply'); }); els.s3b.addEventListener('click', function(){ resolve('book'); });
  els.reset.addEventListener('click', reset);

  reset(); setMode();
  setView(location.hash==='#lead-demo' ? 'lead' : 'home', true);
})();
