document.addEventListener('DOMContentLoaded', () => {
    gsap.registerPlugin(Flip);

    let Clicks = 0;
    const cardImage = document.querySelector('.promotion-image'); // Target the card image
    const bg = document.getElementById('the-world-bg');

    if (!cardImage || !bg) return;

    // Handle both mouse and touch on the card image
    cardImage.addEventListener('pointerdown', handleInteraction);
    cardImage.style.cursor = 'pointer'; // Add pointer cursor to indicate it's clickable

    function handleInteraction(e) {
        e.preventDefault();
        Clicks++;

        // Get exact interaction point
        const rect = cardImage.getBoundingClientRect();
        const pos = {
            x: e.clientX,
            y: e.clientY
        };

        createFallingNumber(pos);

        if (Clicks >= 7) {
            activateEasterEgg();
        }
    }

    function activateEasterEgg() {
        bg.style.display = 'block';
        bg.muted = false;
        bg.style.opacity = '1';
        bg.load();
        bg.play().catch(e => console.error("Video play failed:", e));
        document.body.classList.add('the-world-active');

        bg.onended = () => {
            bg.style.opacity = '0';
            document.body.classList.remove('the-world-active');
            document.body.classList.add('time-resumes');
            setTimeout(() => window.location.href = '/ja', 1000);
        };
    }

    function createFallingNumber(pos) {
        const drop = document.createElement('div');
        drop.className = 'drop-one';
        drop.textContent = '1';

        // Position at exact touch point
        drop.style.position = 'fixed';
        drop.style.left = `${pos.x}px`;
        drop.style.top = `${pos.y}px`;
        drop.style.color = 'black';
        drop.style.zIndex = '10000';
        drop.style.pointerEvents = 'none';
        document.body.appendChild(drop);

        // YOUR ORIGINAL ANIMATION LOGIC
        const direction = Math.random() > 0.5 ? 1 : -1;
        const horizontalDistance = 100 + Math.random() * 100;
        const verticalBounceHeight = 40 + Math.random() * 30;

        const tl = gsap.timeline();
        tl.to(drop, {
            x: direction * horizontalDistance * 0.2,
            y: -verticalBounceHeight,
            rotation: direction * 90,
            duration: 0.4,
            ease: "sine.out"
        })
        .to(drop, {
            x: direction * horizontalDistance,
            y: window.innerHeight + 50,
            rotation: direction * 540,
            duration: 1.25,
            ease: "sine.in",
            onComplete: () => drop.remove()
        })
        .to(drop, {
            opacity: 0,
            duration: 0.5,
            ease: "power1.out"
        }, "-=0.5");
    }
});