document.addEventListener('DOMContentLoaded', () => {
  const lightbox = GLightbox({
    selector: 'a.gallery__item',
    touchNavigation: true,
    loop: true,
    plyr: { css: false, js: false }, // we only show images
  });
});
