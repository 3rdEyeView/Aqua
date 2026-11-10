/* Axiom lead walkthrough (simulation). Mounted only when the URL ends in #lead-demo; lives in a shadow root, so its
   styles and markup never touch the page. No form element, no links, no network calls, no dataLayer or tracking calls. */
(function(){
  var HASH='#lead-demo', root=document.documentElement, host=null, title=document.title, paused=[];
  function build(){
    host=document.createElement('div'); host.id='axl-lead-demo';
    var sh=host.attachShadow({mode:'open'});
    sh.appendChild(document.getElementById('axl-lead-tpl').content.cloneNode(true));
    document.body.appendChild(host);
    var ov=sh.querySelector('.ov');
    /* demo interactions stop here: page-level listeners (analytics, chat, form capture) never get them */
    ['click','dblclick','mousedown','mouseup','pointerdown','pointerup','touchstart','touchend','keydown','keyup','keypress','input','change','submit','focusin','focusout'].forEach(function(t){
      ov.addEventListener(t, function(e){ e.stopPropagation(); });
    });
    sh.querySelector('#axl-close').addEventListener('click', function(){
      try{ history.replaceState(null,'',location.pathname+location.search); }catch(e){ location.hash=''; }
      sync();
    });
    initDemo(sh);
  }
  function sync(){
    var on=location.hash===HASH;
    if(on && !host) build();
    if(host) host.hidden=!on;
    root.classList.toggle('axl-lead-open', on);
    if(on){ document.title='Lead walkthrough (simulation) · Axiom'; paused=[]; Array.prototype.forEach.call(document.querySelectorAll('video'), function(v){ if(!v.paused){ paused.push(v); try{v.pause();}catch(e){} } }); }
    else { document.title=title; paused.forEach(function(v){ try{ var p=v.play(); if(p&&p.catch) p.catch(function(){}); }catch(e){} }); paused=[]; }
  }
  window.addEventListener('hashchange', sync);

  function initDemo(sh){
    function $(s,c){return (c||sh).querySelector(s)} function $$(s,c){return Array.prototype.slice.call((c||sh).querySelectorAll(s))}
/*__LEAD_JS__*/
    reset();
  }
  sync();
})();
