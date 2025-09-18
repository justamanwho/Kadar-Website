document.addEventListener('DOMContentLoaded', () => {
  const track = document.querySelector('.truck-track');
  const truck = document.querySelector('.truck');
  if (!track || !truck) return;

  // margins so the truck doesn't touch edges
  const SIDE_MARGIN_PX = 8;

  let vw = 0, carW = 0, maxX = 0, ticking = false;

  function clamp(n,min,max){ return Math.max(min, Math.min(max, n)); }

  function measure(){
    vw   = window.innerWidth;
    carW = truck.clientWidth || 0;
    maxX = Math.max(0, vw - carW - SIDE_MARGIN_PX*2);
  }

  function getGlobalProgress(){
    const doc   = document.documentElement;
    const body  = document.body;
    const scrollTop = window.pageYOffset || doc.scrollTop || body.scrollTop || 0;
    const docHeight = Math.max(
      body.scrollHeight, doc.scrollHeight,
      body.offsetHeight, doc.offsetHeight,
      body.clientHeight, doc.clientHeight
    );
    const winH = window.innerHeight || doc.clientHeight;
    const scrollable = Math.max(1, docHeight - winH); // avoid divide by zero
    return clamp(scrollTop / scrollable, 0, 1);
  }

  function render(){
    ticking = false;
    const p = getGlobalProgress();
    const x = Math.round(p * maxX) + SIDE_MARGIN_PX;
    // Keep compatibility with optional bobbing animation via CSS var:
    truck.style.setProperty('--carX', x + 'px');
    // If you prefer no bobbing, uncomment:
    // truck.style.transform = `translateX(${x}px)`;
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

  // enable optional bobbing:
  truck.classList.add('bob');

  measure();
  render();
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onResize);
});
