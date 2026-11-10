/* Reference copy: the existing looping drone hero, with working Pause / Play. */
(function(){
  var hero=document.getElementById('hero'); if(!hero) return; var v=hero.querySelector('video');
  var play=hero.querySelector('.e-background-video__play'), pause=hero.querySelector('.e-background-video__pause');
  function sync(){ play.style.display=v.paused?'flex':'none'; pause.style.display=v.paused?'none':'flex'; }
  pause.addEventListener('click', function(){ v.pause(); sync(); }); play.addEventListener('click', function(){ v.play(); sync(); });
  v.addEventListener('play', sync); v.addEventListener('pause', sync); sync();
})();
