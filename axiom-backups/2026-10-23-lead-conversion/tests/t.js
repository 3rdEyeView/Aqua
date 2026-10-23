const vm=require('vm');const fs=require('fs');
const code=fs.readFileSync(process.argv[2],'utf8').replace(/^<script[^>]*>/,'').replace(/<\/script>$/,'');
function run(name, responses, countable){
  const gtagCalls=[], checks=[]; const store={};
  const fetch=async (u,o)=>{ if(String(u).includes('lead-check')){checks.push(JSON.parse(o.body).id); return {ok:true,json:async()=>({countable:countable(JSON.parse(o.body).id)})};}
    const r=responses.shift(); if(r==='throw') throw new Error('net'); return {ok:r.ok,clone(){return{json:async()=>r.body}},json:async()=>r.body}; };
  const w={fetch,gtag:(...a)=>gtagCalls.push(a),localStorage:{getItem:k=>store[k]||null,setItem:(k,v)=>store[k]=v}};
  w.window=w; vm.createContext(w); vm.runInContext(code,w);
  return {w,gtagCalls,checks,store};
}
(async()=>{
 const ok=id=>({ok:true,body:{success:true,refreshArgs:{'contact-form-sent':String(id)}}});
 const post=(w)=>w.fetch('https://x/wp-admin/admin-ajax.php?action=grunion-contact-form',{method:'POST'}).catch(()=>{});
 const tick=()=>new Promise(r=>setTimeout(r,20));
 let t=run('success',[ok(10)],id=>id===10); await post(t.w); await tick(); console.log('success        gtag calls:',t.gtagCalls.length, JSON.stringify(t.gtagCalls[0]));
 t=run('dup',[ok(10),ok(10)],id=>true); await post(t.w); await tick(); await post(t.w); await tick(); console.log('same entry x2  gtag calls:',t.gtagCalls.length,'skipped:',JSON.stringify(t.w.axiomLeadTracking.skipped));
 t=run('spam',[ok(11)],id=>false); await post(t.w); await tick(); console.log('spam           gtag calls:',t.gtagCalls.length,'checks:',t.checks);
 t=run('fail500',[{ok:false,body:{success:false,data:{error:'x'}}}],id=>true); await post(t.w); await tick(); console.log('server error   gtag calls:',t.gtagCalls.length,'checks:',t.checks.length);
 t=run('success:false',[{ok:true,body:{success:false,error:'invalid'}}],id=>true); await post(t.w); await tick(); console.log('success:false  gtag calls:',t.gtagCalls.length);
 t=run('network',['throw'],id=>true); await post(t.w); await tick(); console.log('network fail   gtag calls:',t.gtagCalls.length);
 t=run('other',[],id=>true); await t.w.fetch('https://x/other',{method:'POST'}).catch(()=>{}); await tick(); console.log('other request  gtag calls:',t.gtagCalls.length);
 t=run('persist',[ok(10)],id=>true); t.store['axiomLead:10']='1'; await post(t.w); await tick(); console.log('reload, seen   gtag calls:',t.gtagCalls.length);
})();
