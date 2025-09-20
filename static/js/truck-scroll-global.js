document.addEventListener('DOMContentLoaded', () => {
  const track = document.querySelector('.truck-track');
  const truck = document.querySelector('.truck');
  if (!track || !truck) return;

  const SIDE_MARGIN_PX = 8;   // keep a bit of space from edges
  let trackW = 0, carW = 0, maxX = 0, ticking = false;

  function clamp(n, min, max){ return Math.max(min, Math.min(max, n)); }

  function measure(){
    trackW = track.clientWidth || window.innerWidth;
    carW   = truck.clientWidth || 0;
    // shave 1px to defeat sub-pixel overshoot on some devices
    maxX   = Math.max(0, trackW - carW - SIDE_MARGIN_PX*2 - 1);
  }

  function getGlobalProgress(){
    const doc = document.documentElement, body = document.body;
    const y   = window.pageYOffset || doc.scrollTop || body.scrollTop || 0;
    const h   = Math.max(
      body.scrollHeight, doc.scrollHeight,
      body.offsetHeight, doc.offsetHeight,
      body.clientHeight, doc.clientHeight
    );
    const winH = window.innerHeight || doc.clientHeight;
    const scrollable = Math.max(1, h - winH);
    return clamp(y / scrollable, 0, 1);
  }

  function render(){
    ticking = false;
    const p = getGlobalProgress();
    const x = Math.floor(p * maxX) + SIDE_MARGIN_PX; // floor avoids 0.5px bleed
    truck.style.setProperty('--carX', x + 'px');
  }

  function onScroll(){
    if (!ticking){
      ticking = true;
      requestAnimationFrame(render);
    }
  }

  function onResize(){
    measure();
    render();
  }

  // init
  measure();
  render();
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onResize);
});
