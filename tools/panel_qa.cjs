// Public-URL QA for .xj-panel tour cards (no cache-busting): direction, clipped prices/buttons, overflow; screenshots.
// Usage: NODE_EXTRA_CA_CERTS=/root/.ccr/ca-bundle.crt NODE_PATH=$(npm root -g) node tools/panel_qa.cjs <outDir> <widths> <url...>
const { chromium } = require('playwright'); const { execFileSync } = require('child_process'); const fs = require('fs');
function cf(u){const o=execFileSync('curl',['-sS','-L','-A','Mozilla/5.0 Chrome/128.0 XtremeAudit-Claude/1.0','-D','-',u],{maxBuffer:1<<26});let p=0,h=0;while(true){const e=o.indexOf(Buffer.from('\r\n\r\n'),p);if(e<0)break;if(!o.slice(p,e).toString().startsWith('HTTP/'))break;h=e+4;p=h;}const hd=o.slice(0,h).toString();const ct=(hd.match(/content-type:\s*([^\r\n]+)/gi)||[]).pop();return{body:o.slice(h),contentType:ct?ct.split(':').slice(1).join(':').trim():undefined};}
(async()=>{ const [out,wsArg,...urls]=process.argv.slice(2); const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
 for (const url of urls){ const slug=new URL(url).pathname.replace(/\//g,'')||'home';
 for (const w of wsArg.split(',').map(Number)){ const mob=w<768; const ua=mob?'Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1 XtremeAudit-Claude/1.0':'Mozilla/5.0 Chrome/128.0 XtremeAudit-Claude/1.0';
  const hp=`${out}/${slug}-${w}.html`; execFileSync('curl',['-sS','-A',ua,'-o',hp,url]); fs.writeFileSync(hp,fs.readFileSync(hp,'utf8').replace('<head>',`<head><base href="${url}">`));
  const ctx=await b.newContext({viewport:{width:w,height:900},isMobile:mob,hasTouch:w<1025,userAgent:ua});
  await ctx.route(/^https?:/,async r=>{const u=r.request().url(); if(!/xtremestpete\.com|waverez\.com|googleapis|gstatic/.test(u)){try{await r.fulfill({response:await r.fetch({timeout:20000})})}catch(e){await r.abort()}return;} try{const x=cf(u);await r.fulfill({status:200,body:x.body,contentType:x.contentType})}catch(e){await r.abort()}});
  const p=await ctx.newPage(); await p.goto('file://'+hp,{waitUntil:'domcontentloaded',timeout:60000}); await p.addStyleTag({content:'.cmplz-cookiebanner,.cmplz-soft-cookiewall{display:none!important}'}); if(process.env.NOBRIDGE) await p.evaluate(()=>{const b=document.getElementById('xj-cdn-bridge'); if(b) b.remove();}); // NOBRIDGE=1: test without the temporary CDN bridge await p.waitForTimeout(3000);
  const info=await p.evaluate(()=>{const ps=[...document.querySelectorAll('.xj-panel')]; return {overflow:document.documentElement.scrollWidth-innerWidth, panels:ps.map(c=>{const r=c.getBoundingClientRect(); const kids=[...c.querySelectorAll('p,a,h3,h2')].filter(k=>k.getBoundingClientRect().width>0);
     const clipped=kids.filter(k=>{const kr=k.getBoundingClientRect();return kr.right>r.right+1||kr.left<r.left-1}).map(k=>k.innerText.trim().slice(0,20));
     return {dir:getComputedStyle(c).flexDirection,w:Math.round(r.width),clipped,price:(kids.find(k=>/\$\d/.test(k.innerText))||{}).innerText}})}});
  const bad=info.panels.filter(x=>x.dir!=='column'||x.clipped.length);
  const first=await p.evaluate(()=>{const c=document.querySelector('.xj-panel'); let s=c; while(s.parentElement&&!s.parentElement.matches('.elementor[data-elementor-type="wp-page"]')) s=s.parentElement; const r=s.getBoundingClientRect(); return {x:0,y:r.top+scrollY,width:innerWidth,height:Math.min(r.height,4000)}});
  await p.screenshot({path:`${out}/public-${slug}-cards-${w}.png`,fullPage:true,clip:first});
  console.log(slug,w,'overflow',info.overflow,'panels',info.panels.length,'problems',JSON.stringify(bad),'prices',JSON.stringify(info.panels.map(x=>x.price).filter(Boolean)));
  await ctx.close(); } } await b.close(); })().catch(e=>{console.error(e);process.exit(1)});
