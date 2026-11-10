/* V4 hero sequence: real drone footage -> AI-generated transition -> real project photo, then it starts over.
   The label always says which of the three is on screen. Reduced motion: no video, the real project photo is shown. */
(function(){
  var hero=document.getElementById('hero'); if(!hero) return;
  var v=hero.querySelector('video'), chip=hero.querySelector('.v4-chip'), txt=chip.querySelector('span');
  var AI_START=7.04, HOLD=6500, timer=0;
  var LABEL={ drone:'Arroyo’s own drone footage', ai:'AI-generated transition', photo:'Real Arroyo project · Bottle Palms & Ti Plants' };
  function label(k){ if(chip.dataset.kind!==k){ chip.dataset.kind=k; txt.textContent=LABEL[k]; } hero.classList.toggle('v4-late', k!=='drone'); }
  function restart(){ clearTimeout(timer); v.currentTime=0; var p=v.play(); if(p&&p.catch) p.catch(function(){}); setTimeout(function(){ hero.classList.remove('v4-settled'); }, 120); label('drone'); }
  if(window.matchMedia('(prefers-reduced-motion: reduce)').matches){ v.removeAttribute('src'); v.load(); hero.classList.add('v4-settled'); label('photo'); return; }
  v.muted=true; v.loop=false;
  v.addEventListener('timeupdate', function(){ if(!hero.classList.contains('v4-settled')) label(v.currentTime>=AI_START?'ai':'drone'); });
  v.addEventListener('ended', function(){ hero.classList.add('v4-settled'); label('photo'); timer=setTimeout(restart, HOLD); });
  hero.querySelector('.e-background-video__pause').addEventListener('click', function(){ clearTimeout(timer); v.pause(); hero.classList.add('v4-paused'); });
  hero.querySelector('.e-background-video__play').addEventListener('click', function(){ hero.classList.remove('v4-paused'); if(v.ended||hero.classList.contains('v4-settled')) restart(); else v.play(); });
  label('drone'); var p=v.play(); if(p&&p.catch) p.catch(function(){});
})();
