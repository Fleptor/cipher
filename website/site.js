/* Progressive enhancement for the project presentation. No analytics or network calls. */
(() => {
  const root = document.documentElement;
  const toggle = document.querySelector('.nav-toggle');
  const nav = document.querySelector('#site-nav');
  if (toggle && nav) {
    const closeMenu = () => {
      toggle.setAttribute('aria-expanded', 'false');
      nav.dataset.open = 'false';
    };
    toggle.hidden = false;
    toggle.addEventListener('click', () => {
      const open = toggle.getAttribute('aria-expanded') !== 'true';
      toggle.setAttribute('aria-expanded', String(open));
      nav.dataset.open = String(open);
    });
    nav.addEventListener('click', (event) => {
      if (event.target.closest('a')) closeMenu();
    });
    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') {
        closeMenu();
        toggle.focus();
      }
    });
    root.classList.add('js');
  }

  const panel = document.querySelector('.network-panel');
  const scenarios = {
    normal: {
      title: 'A familiar routine.',
      summary: 'The device stays close to its baseline. No incident is shown in this illustration.',
      announcement: 'Illustrative usual activity. The device stays close to its baseline, with no incident shown.',
      mark: '✓'
    },
    unusual: {
      title: 'A pattern breaks.',
      summary: 'Two signals change. An alert is raised; the device stays connected in monitor mode.',
      announcement: 'Illustrative unusual activity. Two signals change, raising an alert without automatic isolation in monitor mode.',
      mark: '!'
    }
  };
  document.querySelectorAll('[data-scenario-choice]').forEach((button) => {
    button.addEventListener('click', () => {
      const name = button.dataset.scenarioChoice;
      const scenario = scenarios[name];
      if (!panel || !scenario) return;
      panel.dataset.scenario = name;
      panel.querySelector('#scenario-title').textContent = scenario.title;
      panel.querySelector('#scenario-summary').textContent = scenario.summary;
      panel.querySelector('#scenario-announcement').textContent = scenario.announcement;
      panel.querySelector('.incident-mark').textContent = scenario.mark;
      panel.querySelectorAll('[data-scenario-choice]').forEach((choice) => {
        choice.setAttribute('aria-pressed', String(choice === button));
      });
    });
  });

  const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
  if ('IntersectionObserver' in window && !reducedMotion.matches) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('reveal');
        observer.unobserve(entry.target);
      });
    }, { threshold: .12 });
    document.querySelectorAll('.pipeline, .signal-board, .demo-figure, .status-grid, .resource-grid').forEach((item) => observer.observe(item));
  }
})();
