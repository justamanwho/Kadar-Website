document.addEventListener('DOMContentLoaded', () => {
  const heading = document.querySelector('#hero-heading');
  if (!heading) return;

  const lines = heading.querySelectorAll('.line');
  if (!lines.length) return;

  const rand = (min, max) => Math.random() * (max - min) + min;
  let letterIndex = 0; // for stagger across all letters

  lines.forEach(line => {
    const raw = line.textContent.trim().replace(/\s+/g, ' ');
    line.textContent = ''; // keep the <span class="line">, empty its text

    raw.split(' ').forEach((word, wIdx) => {
      const wordWrap = document.createElement('span');
      wordWrap.className = 'word';
      wordWrap.style.display = 'inline-block';
      wordWrap.style.whiteSpace = 'nowrap';
      wordWrap.style.marginRight = '0.35em';

      [...word].forEach(ch => {
        const span = document.createElement('span');
        span.className = 'char';
        span.textContent = ch;

        span.style.setProperty('--tx', `${rand(-40, 40)}px`);
        span.style.setProperty('--ty', `${rand(-60, 60)}px`);
        span.style.setProperty('--rot', `${rand(-10, 10)}deg`);

        // slower overall effect; tweak 0.12 -> 0.15 to slow more
        span.style.animationDelay = (letterIndex * 0.12 + rand(0, 0.03)) + 's';
        letterIndex += 1;

        wordWrap.appendChild(span);
      });

      line.appendChild(wordWrap);
    });
  });
});
