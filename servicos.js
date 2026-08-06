/* ========================================
   SAVYLLA ADRYAN - Página de Serviços
   ========================================

   Script próprio, separado do script.js do portfólio: aquele arquivo assume a
   existência do grid de projetos, do modal e do lightbox, e quebraria aqui na
   primeira chamada a um elemento que não existe. Esta página só precisa do
   header, do overlay de navegação e da revelação dos blocos ao rolar.
   ---------------------------------------- */

// ----------------------------------------
// Header scroll (throttled com rAF)
// ----------------------------------------
const header = document.getElementById('header');
let scrollTicking = false;
window.addEventListener('scroll', () => {
  if (!scrollTicking) {
    requestAnimationFrame(() => {
      if (header) header.classList.toggle('scrolled', window.scrollY > 80);
      scrollTicking = false;
    });
    scrollTicking = true;
  }
}, { passive: true });

// ----------------------------------------
// Fullscreen nav overlay
// Mesmo comportamento do index.html — os dois gatilhos (burger no mobile,
// rótulo lateral no desktop) controlam o mesmo overlay e precisam refletir o
// estado para leitores de tela.
// ----------------------------------------
const sideMenu = document.getElementById('sideMenu');
const navOverlay = document.getElementById('navOverlay');
const burgerBtn = document.getElementById('burgerBtn');

function setNavState(isOpen) {
  navOverlay.classList.toggle('active', isOpen);
  burgerBtn.classList.toggle('active', isOpen);
  document.body.classList.toggle('nav-open', isOpen);
  navOverlay.setAttribute('aria-hidden', String(!isOpen));
  [burgerBtn, sideMenu].forEach(btn => {
    btn.setAttribute('aria-expanded', String(isOpen));
    btn.setAttribute('aria-label', isOpen ? 'Fechar menu de navegação' : 'Abrir menu de navegação');
  });
  // Com o overlay aberto o burger some acima de 768px; sem trocar este rótulo o
  // desktop ficaria sem nenhuma saída visível.
  sideMenu.textContent = isOpen ? 'FECHAR' : 'MENU';
  document.body.style.overflow = isOpen ? 'hidden' : '';
}

function toggleNav() {
  setNavState(!navOverlay.classList.contains('active'));
}

function closeNav() {
  const focoDentro = navOverlay.contains(document.activeElement);
  setNavState(false);
  if (focoDentro) {
    const gatilho = burgerBtn.offsetParent !== null ? burgerBtn : sideMenu;
    gatilho.focus({ preventScroll: true });
  }
}

sideMenu.addEventListener('click', toggleNav);
burgerBtn.addEventListener('click', toggleNav);

document.addEventListener('keydown', e => {
  if (e.key === 'Escape' && navOverlay.classList.contains('active')) closeNav();
});

// Clique fora dos links fecha; nos links, deixa a navegação seguir (todos
// apontam para index.html, então não há preventDefault aqui).
navOverlay.addEventListener('click', e => {
  if (!e.target.closest('.nav-overlay__link')) closeNav();
});

// ----------------------------------------
// Reveal dos blocos ao rolar
// ----------------------------------------
const revelaveis = document.querySelectorAll('[data-revelar]');
if (revelaveis.length) {
  const prefereSemMovimento = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (prefereSemMovimento) {
    revelaveis.forEach(el => el.classList.add('revelado'));
  } else {
    const obs = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('revelado');
          obs.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -10% 0px', threshold: 0.1 });
    revelaveis.forEach(el => obs.observe(el));
  }
}
