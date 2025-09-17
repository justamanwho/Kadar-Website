document.addEventListener("DOMContentLoaded", () => {
  let currentSlide = 0;

  const slidesContainer = document.querySelector(".slides");
  const slides = document.querySelectorAll(".slide");
  const dots = document.querySelectorAll(".dot");

  if (!slidesContainer || slides.length === 0 || dots.length === 0) {
    console.error("Slider: missing .slides/.slide/.dot in DOM");
    return;
  }

  // (optional) keep this in sync with CSS transition duration
  const AUTOPLAY_MS = 7000;   // how long a slide stays visible
  const ZOOM_RESTART = () => { /* no-op; just for readability */ };

  function startKenBurns(imgEl){
    // remove .ken from all, then force-reflow and add to the active
    slides.forEach(s => s.classList.remove("ken"));

    // Alternate origin via inline style for more variety (overrides nth-child)
    imgEl.style.transformOrigin = (currentSlide % 2 === 0) ? "left center" : "right center";

    // Restart CSS transition cleanly:
    // 1) read a layout property to force reflow
    void imgEl.offsetWidth;
    // 2) add the class so the 6s transition plays every time
    imgEl.classList.add("ken");
  }

  function showSlide(index) {
    if (index < 0) index = slides.length - 1;
    if (index >= slides.length) index = 0;
    currentSlide = index;

    slidesContainer.style.transform = `translateX(-${currentSlide * 100}%)`;

    dots.forEach(d => d.classList.remove("active"));
    dots[currentSlide].classList.add("active");

    startKenBurns(slides[currentSlide]);
  }

  // dot clicks
  dots.forEach((dot, idx) => dot.addEventListener("click", () => showSlide(idx)));

  // initial
  showSlide(0);

  // autoplay
  setInterval(() => showSlide(currentSlide + 1), AUTOPLAY_MS);
});
