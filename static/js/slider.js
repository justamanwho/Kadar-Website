document.addEventListener("DOMContentLoaded", () => {
  let currentSlide = 0;

  const slidesContainer = document.querySelector(".slides");
  const slides = document.querySelectorAll(".slide");
  const dots = document.querySelectorAll(".dot");

  if (!slidesContainer || slides.length === 0 || dots.length === 0) {
    console.error("Slider: missing .slides/.slide/.dot in DOM");
    return;
  }

  const AUTOPLAY_MS = 7000;   // how long a slide stays visible
  const SLIDE_TRANSITION_MS = 600; // must match your CSS transition (.slides)

  function startKenBurns(slideEl) {
    // remove .ken from all slides
    slides.forEach(s => s.classList.remove("ken"));

    // Set alternating zoom origin for variety
    slideEl.style.transformOrigin = (currentSlide % 2 === 0) ? "left center" : "right center";

    // Force reflow so browser restarts the transition cleanly
    void slideEl.offsetWidth;

    // Now add ken for zoom-in
    slideEl.classList.add("ken");
  }

  function showSlide(index) {
    if (index < 0) index = slides.length - 1;
    if (index >= slides.length) index = 0;

    currentSlide = index;

    // Move slides container
    slidesContainer.style.transform = `translate3d(-${currentSlide * 100}%, 0, 0)`;

    // Update dots
    dots.forEach(d => d.classList.remove("active"));
    dots[currentSlide].classList.add("active");

    // Delay the zoom until after the horizontal slide finishes
    setTimeout(() => startKenBurns(slides[currentSlide]), SLIDE_TRANSITION_MS);
  }

  // Dot clicks
  dots.forEach((dot, idx) => dot.addEventListener("click", () => showSlide(idx)));

  // Initial setup
  showSlide(0);

  // Autoplay
  setInterval(() => showSlide(currentSlide + 1), AUTOPLAY_MS);
});
