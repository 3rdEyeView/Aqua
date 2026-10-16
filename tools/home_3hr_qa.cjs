// Public-URL QA for the homepage tour section (no cache-busting): images loaded, prices, booking buttons
// open the WaveRez lightframe for product 5919 in place, overflow, header height, JS errors.
// Usage: NODE_EXTRA_CA_CERTS=/root/.ccr/ca-bundle.crt NODE_PATH=$(npm root -g) node tools/home_3hr_qa.cjs <outDir> [widths]
const { chromium } = require('playwright'); const { execFileSync } = require('child_process'); const fs = require('fs');
function cf(u){const o=execFileSync('curl',['-sS','-L','-A','Mozilla/5.0 Chrome/128.0 XtremeAudit-Claude/1.0','-D','-',u],{maxBuffer:1<<26});let p=0,h=0;while(true){const e=o.indexOf(Buffer.from('\r\n\r\n'),p);if(e<0)break;if(!o.slice(p,e).toString().startsWith('HTTP/'))break;h=e+4;p=h;}const hd=o.slice(0,h).toString();const ct=(hd.match(/content-type:\s*([^\r\n]+)/gi)||[]).pop();return{body:o.slice(h),contentType:ct?ct.split(':').slice(1).join(':').trim():undefined};}
(async()=>{ const out=process.argv[2]; const ws=(process.argv[3]||'1440,1024,768,430,375').split(',').map(Number); const url='https://xtremestpete.com/';
 const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
 for (const w of ws){ const mob=w<768; const ua=mob?'Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1 XtremeAudit-Claude/1.0':'Mozilla/5.0 Chrome/128.0 XtremeAudit-Claude/1.0';
  const hp=`${out}/home-${w}.html`; execFileSync('curl',['-sS','-A',ua,'-o',hp,url]); fs.writeFileSync(hp,fs.readFileSync(hp,'utf8').replace('<head>',`<head><base href="${url}">`));
  const ctx=await b.newContext({viewport:{width:w,height:900},isMobile:mob,hasTouch:w<1025,userAgent:ua});
  await ctx.route(/^https?:/,async r=>{const u=r.request().url(); if(!/xtremestpete\.com|waverez\.com|googleapis|gstatic/.test(u)){try{await r.fulfill({response:await r.fetch({timeout:20000})})}catch(e){await r.abort()}return;} try{const x=cf(u);await r.fulfill({status:200,body:x.body,contentType:x.contentType})}catch(e){await r.abort()}});
  const p=await ctx.newPage(); const errs=[]; p.on('pageerror',e=>errs.push(e.message.slice(0,120)));
  await p.goto('file://'+hp,{waitUntil:'domcontentloaded',timeout:60000}); await p.addStyleTag({content:'.cmplz-cookiebanner,.cmplz-soft-cookiewall{display:none!important}'});
  await p.evaluate(async()=>{document.querySelectorAll('img[loading="lazy"]').forEach(i=>{i.loading='eager'});for(let y=0;y<document.body.scrollHeight;y+=500){scrollTo(0,y);await new Promise(r=>setTimeout(r,80))}scrollTo(0,0)});
  await p.waitForFunction(()=>[...document.querySelectorAll('.elementor-element-119cd4b5 img')].every(i=>i.complete),null,{timeout:30000}).catch(()=>{});
  await p.waitForTimeout(1500);
  const info=await p.evaluate(()=>{const sec=document.querySelector('.elementor-element-119cd4b5'); const q=id=>document.querySelector(`[data-interaction-id="${id}"],[data-id="${id}"]`);
    const imgs=[...sec.querySelectorAll('img')].map(i=>({ok:i.naturalWidth>0,w:Math.round(i.getBoundingClientRect().width),h:Math.round(i.getBoundingClientRect().height)}));
    const card=q('50e56cec'), r=card.getBoundingClientRect(); const media=q('7d496de').getBoundingClientRect();
    const hdr=document.querySelector('.elementor-27'); return {overflow:document.documentElement.scrollWidth-innerWidth, header:Math.round(hdr.getBoundingClientRect().height),
     imgs, card:{w:Math.round(r.width),h:Math.round(r.height),dir:getComputedStyle(card).flexDirection,media:[Math.round(media.width),Math.round(media.height)]},
     prices:[...sec.querySelectorAll('p')].map(x=>x.innerText.trim()).filter(t=>/^\$|^From \$/.test(t)),
     buttons:[...sec.querySelectorAll('a')].map(a=>a.innerText.trim().replace(/\s+/g,' ')+' -> '+a.getAttribute('href').replace('https://reservations.waverez.com',''))}});
  await p.evaluate(()=>document.querySelector('.elementor-element-119cd4b5').scrollIntoView()); await p.waitForTimeout(500);
  const box=await p.evaluate(()=>{const r=document.querySelector('.elementor-element-119cd4b5').getBoundingClientRect();return {x:0,y:r.top+scrollY-16,width:innerWidth,height:r.height+32}});
  await p.screenshot({path:`${out}/public-home-tours-${w}.png`,fullPage:true,clip:box});
  const lf=[];
  for (const id of ['4e3b4a54','2ed69dc']) { const a=p.locator(`[data-interaction-id="${id}"], [data-id="${id}"]`).first(); await a.scrollIntoViewIfNeeded(); await a.click({noWaitAfter:true}); await p.waitForTimeout(3000);
    const src=await p.$$eval('.waverez_popup iframe',f=>f.map(x=>x.src)); lf.push(id+': '+(src.pop()||'NO LIGHTFRAME')+' stayed='+p.url().startsWith('file://'));
    if(id==='2ed69dc') await p.screenshot({path:`${out}/public-home-3hr-lightframe-${w}.png`});
    await p.evaluate(()=>{const c=document.querySelector('.waverez_popup');if(c){c.innerHTML='';c.className='waverez_popup';c.removeAttribute('style')}document.body.style.overflow=''}); await p.waitForTimeout(300); }
  console.log(w, JSON.stringify(info)); console.log('   lightframe:', lf.join(' | '), '| jsErrors:', errs.length, errs.slice(0,3).join(' / '));
  await ctx.close(); } await b.close(); })().catch(e=>{console.error(e);process.exit(1)});
