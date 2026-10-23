const { chromium } = require(require('child_process').execSync('npm root -g').toString().trim()+'/playwright');
const fs=require('fs');const SPKI=fs.readFileSync(process.argv[2],'utf8').match(/spki-list=([^']+)/)[1];
const URL='https://axiomsystems.systems/get-started/?plan=growth';
(async()=>{
const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome',args:['--ignore-certificate-errors-spki-list='+SPKI]});
const ctx=await b.newContext({viewport:{width:1280,height:900}});
const googleHits=[];
await ctx.route(/(google|googletagmanager|googleadservices|doubleclick|google-analytics)\./,r=>{googleHits.push(r.request().url().slice(0,90));r.abort();});
await ctx.route(u=>u.href.startsWith('https://axiomsystems.systems/get-started/'),async r=>{const res=await r.fetch();let body=await res.text();body=body.replace('"dest":""','"dest":"AW-0000000000\\/TEST"');r.fulfill({response:res,body});});
await ctx.addInitScript(()=>{window.__conv=[];const iv=setInterval(()=>{if(window.dataLayer&&!window.dataLayer.__w){window.dataLayer.__w=1;const op=window.dataLayer.push;window.dataLayer.push=function(){const a=arguments[0];if(a&&a[0]==='event'&&a[1]==='conversion')window.__conv.push(JSON.parse(JSON.stringify(a[2])));return op.apply(this,arguments);};}},5);});
async function fresh(){const p=await ctx.newPage();const log={ajax:[],check:[]};
 p.on('response',async r=>{const u=r.url();if(u.includes('action=grunion-contact-form')){let j=null;try{j=await r.json()}catch(e){}log.ajax.push({status:r.status(),success:j&&j.success,entry:j&&j.refreshArgs&&j.refreshArgs['contact-form-sent'],body:j});}
  if(u.includes('/axiom/v1/lead-check')){let j=null;try{j=await r.json()}catch(e){}log.check.push({status:r.status(),body:j});}});
 await p.goto(URL,{waitUntil:'load',timeout:90000});await p.waitForTimeout(1500);return {p,log};}
async function fill(p,email){const f=p.locator('.axgs form');
 await f.locator('[name$="-name"]').fill('Axiom tracking test');await f.locator('[name$="-businessname"]').fill('Axiom tracking test');
 await f.locator('[name$="-email"]').fill(email);await f.locator('[name$="-phone"]').fill('5555550100');
 await f.locator('textarea[name$="-tellusaboutyourbusiness"]').fill('Axiom tracking test: automated check of lead conversion tracking. Please ignore.');}
async function state(p){return p.evaluate(()=>({conversions:window.__conv,tracking:window.axiomLeadTracking,success:!!document.querySelector('.axgs .submission-success, .axgs .contact-form-submission')}));}
const out={};
{const {p,log}=await fresh();
 // Let the real submission reach the server, then mark the new entry as spam (what Akismet would do) before the page sees the reply.
 await p.route(/action=grunion-contact-form/,async r=>{const res=await r.fetch();const body=await res.json();const id=body&&body.refreshArgs&&body.refreshArgs['contact-form-sent'];
   if(id){const rr=await fetch('https://axiomsystems.systems/wp-json/wp/v2/feedback/'+id,{method:'POST',headers:{'Authorization':'Basic '+process.env.AXIOM_ELEMENTOR_MCP_AUTH,'Content-Type':'application/json','User-Agent':'curl/8.5.0'},body:JSON.stringify({status:'spam'})});out.markedSpam={id,status:(await rr.json()).status};}
   r.fulfill({response:res,body:JSON.stringify(body)});});
 await fill(p,'qa-test@example.com');await p.locator('.axgs form [name$="-name"]').fill('Axiom tracking test (spam simulation)');
 await p.locator('.axgs button[type=submit]').click();await p.waitForTimeout(9000);
 out.spam={...(await state(p)),ajax:log.ajax.map(a=>({status:a.status,success:a.success,entry:a.entry})),check:log.check};await p.close();}
out.googleRequestsBlocked=googleHits.length;out.googleSample=[...new Set(googleHits.map(u=>u.split('?')[0]))].slice(0,6);
console.log(JSON.stringify(out,null,1));await b.close();})();
