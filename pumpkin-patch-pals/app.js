/* Pumpkin Patch Pals - fall & Halloween classroom games (PreK-2).
   Works offline. Art lives in art.js (shared with the printable PDF set). */
(() => {
  'use strict';

  // ---------------------------------------------------------------- utilities
  const $ = (sel, el = document) => el.querySelector(sel);
  const app = $('#app');
  const rand = (n) => Math.floor(Math.random() * n);
  const pick = (arr) => arr[rand(arr.length)];
  const shuffle = (arr) => { const a = arr.slice(); for (let i = a.length - 1; i > 0; i--) { const j = rand(i + 1); [a[i], a[j]] = [a[j], a[i]]; } return a; };
  const sample = (arr, n) => shuffle(arr).slice(0, n);
  const art = (key, cls = 'art') => `<span class="${cls}" aria-hidden="true">${(window.ART[key] || {}).svg || ''}</span>`;
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const wait = (ms) => new Promise((r) => setTimeout(r, ms));
  const alive = (el) => document.body.contains(el); // false once the child has left the activity

  const store = {
    get(k, d) { try { const v = localStorage.getItem('ppp-' + k); return v === null ? d : JSON.parse(v); } catch (e) { return d; } },
    set(k, v) { try { localStorage.setItem('ppp-' + k, JSON.stringify(v)); } catch (e) { /* private mode */ } },
  };
  const settings = { sound: store.get('sound', true), voice: store.get('voice', true) };
  let stars = store.get('stars', 0);

  // ---------------------------------------------------------------- sound + voice
  let actx = null;
  function tone(freq, start, dur, type = 'triangle', vol = 0.18) {
    if (!settings.sound) return;
    try {
      actx = actx || new (window.AudioContext || window.webkitAudioContext)();
      const t = actx.currentTime + start;
      const o = actx.createOscillator(); const g = actx.createGain();
      o.type = type; o.frequency.setValueAtTime(freq, t);
      g.gain.setValueAtTime(0.0001, t); g.gain.exponentialRampToValueAtTime(vol, t + 0.02);
      g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
      o.connect(g).connect(actx.destination); o.start(t); o.stop(t + dur + 0.05);
    } catch (e) { /* audio unavailable */ }
  }
  const sfx = {
    tap: () => tone(660, 0, 0.08, 'sine', 0.08),
    right: () => { tone(523, 0, 0.16); tone(659, 0.1, 0.16); tone(784, 0.2, 0.3); },
    wrong: () => { tone(330, 0, 0.18, 'sine', 0.12); tone(262, 0.14, 0.25, 'sine', 0.1); },
    win: () => [523, 659, 784, 1047, 784, 1047].forEach((f, i) => tone(f, i * 0.12, 0.22)),
    roll: () => { for (let i = 0; i < 6; i++) tone(200 + rand(400), i * 0.07, 0.05, 'square', 0.05); },
    flip: () => tone(880, 0, 0.06, 'sine', 0.06),
  };
  // Voice: every line the app speaks is pre-recorded with a natural female neural voice (voice.js).
  // If a clip is missing, or voice.js has not loaded yet, the best female device voice reads it instead.
  const voiceEl = new Audio();
  voiceEl.preload = 'auto';
  let voiceQueue = [];
  let voiceGen = 0;
  const voiceMisses = (window.__voiceMisses = []);
  const FEMALE_VOICES = [/ava.*natural/i, /jenny.*natural/i, /aria.*natural/i, /emma.*natural/i, /michelle.*natural/i,
    /google us english/i, /samantha/i, /\bava\b/i, /allison/i, /susan/i, /zira/i, /karen/i, /moira/i, /tessa/i,
    /serena/i, /victoria/i, /female/i];
  function femaleVoice() {
    const vs = speechSynthesis.getVoices().filter((v) => /^en/i.test(v.lang));
    for (const re of FEMALE_VOICES) { const v = vs.find((x) => re.test(x.name)); if (v) return v; }
    return vs.find((v) => /en.US/i.test(v.lang)) || vs[0];
  }
  function deviceSay(text, done) {
    if (!('speechSynthesis' in window)) return done();
    try {
      const u = new SpeechSynthesisUtterance(text);
      u.rate = 0.95; u.pitch = 1.05;
      const v = femaleVoice(); if (v) u.voice = v;
      u.onend = done; u.onerror = done;
      speechSynthesis.speak(u);
    } catch (e) { done(); }
  }
  function playNext(gen) {
    if (gen !== voiceGen) return;
    const text = voiceQueue.shift();
    if (text === undefined) return;
    const next = () => playNext(gen);
    const clip = window.VOICE && window.VOICE[text];
    if (clip) {
      voiceEl.src = clip;
      voiceEl.onended = next;
      const p = voiceEl.play();
      if (p && p.catch) p.catch(() => { if (gen === voiceGen) deviceSay(text, next); });
    } else {
      voiceMisses.push(text);
      deviceSay(text, next);
    }
  }
  function stopVoice() {
    voiceGen += 1;
    voiceQueue = [];
    voiceEl.onended = null;
    try { voiceEl.pause(); } catch (e) { /* not playing */ }
    if ('speechSynthesis' in window) speechSynthesis.cancel();
  }
  function say(parts) {
    stopVoice();
    if (!settings.voice) return;
    voiceQueue = [].concat(parts);
    playNext(voiceGen);
  }

  // ---------------------------------------------------------------- rewards
  function addStar() {
    stars += 1; store.set('stars', stars);
    $('#starCount').textContent = stars;
    const s = $('.stars'); s.classList.remove('pop'); void s.offsetWidth; s.classList.add('pop');
  }
  function confetti(n = 18) {
    const box = $('#confetti');
    const keys = ['maple', 'leaf', 'oak', 'star', 'mini', 'candy-corn', 'acorn'];
    for (let i = 0; i < n; i++) {
      const d = document.createElement('div');
      d.className = 'bit';
      d.innerHTML = art(pick(keys));
      d.style.left = rand(100) + 'vw';
      d.style.animationDuration = (1.8 + Math.random() * 1.6) + 's';
      d.style.animationDelay = (Math.random() * 0.4) + 's';
      box.appendChild(d);
      setTimeout(() => d.remove(), 4200);
    }
  }
  const PRAISE = ['Great job!', 'You got it!', 'Pumpkin-tastic!', 'Awesome!', 'Way to go!', 'Super!', 'Spook-tacular!', 'Fantastic!'];
  const TRY = ['Try again!', 'Almost! Try again.', 'Keep trying!', 'Oops, try another one!'];

  // ---------------------------------------------------------------- activities list
  const ACTIVITIES = [
    { id: 'decorate', title: 'Decorate a Pumpkin', icon: 'jack', tag: 'art', label: 'Art', run: runDecorate },
    { id: 'roll', title: "Roll a Jack-o'-Lantern", icon: 'jack-glow', tag: 'math', label: 'Dice', run: runRoll },
    { id: 'count', title: 'Count the Pumpkins', icon: 'mini', tag: 'math', label: 'Counting', run: () => quiz(countRounds, 'Count the Pumpkins', ['1-10', '1-20']) },
    { id: 'tenframe', title: 'Ten Frame Fill', icon: 'seed', tag: 'math', label: 'Ten frames', run: runTenFrame },
    { id: 'add', title: 'Pumpkin Addition', icon: 'pie', tag: 'math', label: 'Adding', run: () => quiz(addRounds, 'Pumpkin Addition', ['to 5', 'to 10']) },
    { id: 'pattern', title: 'What Comes Next?', icon: 'candy-corn', tag: 'math', label: 'Patterns', run: () => quiz(patternRounds, 'What Comes Next?', ['AB', 'Mixed']) },
    { id: 'letters', title: 'Letter Match', icon: 'maple', tag: 'literacy', label: 'ABC', run: () => quiz(letterRounds, 'Letter Match', ['A-M', 'N-Z']) },
    { id: 'sounds', title: 'Beginning Sounds', icon: 'bat', tag: 'literacy', label: 'Phonics', run: () => quiz(soundRounds, 'Beginning Sounds') },
    { id: 'rhyme', title: 'Rhyme Time', icon: 'cat', tag: 'literacy', label: 'Rhyming', run: () => quiz(rhymeRounds, 'Rhyme Time') },
    { id: 'spell', title: 'Spell It!', icon: 'web', tag: 'literacy', label: 'CVC words', run: runSpell },
    { id: 'lifecycle', title: 'Pumpkin Life Cycle', icon: 'sprout', tag: 'science', label: 'Science', run: runLifeCycle },
    { id: 'memory', title: 'Fall Memory Match', icon: 'owl', tag: 'math', label: 'Memory', run: runMemory },
    { id: 'feelings', title: 'Feelings Check-In', icon: 'feel-happy', tag: 'sel', label: 'Feelings', run: runFeelings },
  ];

  // ---------------------------------------------------------------- home
  function home() {
    stopVoice();
    const filt = store.get('filter', 'all');
    const tags = [['all', 'All'], ['math', 'Math'], ['literacy', 'Literacy'], ['science', 'Science'], ['art', 'Art'], ['sel', 'Feelings']];
    app.innerHTML = `
      <section class="hero">
        <h1>Pumpkin Patch Pals</h1>
        <p>Pick a fall game to play!</p>
      </section>
      <div class="filters" role="toolbar" aria-label="Filter games">
        ${tags.map(([k, t]) => `<button class="chip" data-f="${k}" aria-pressed="${k === filt}">${t}</button>`).join('')}
      </div>
      <div class="grid">
        ${ACTIVITIES.filter((a) => filt === 'all' || a.tag === filt).map((a) => `
          <button class="tile" data-id="${a.id}">
            ${art(a.icon)}
            <h2>${esc(a.title)}</h2>
            <span class="tag ${a.tag === 'art' ? 'tag-art' : a.tag}">${a.label}</span>
          </button>`).join('')}
      </div>
      <p class="footer-note">Works offline • Great on interactive whiteboards, tablets and Chromebooks • Voice: Kokoro (Apache 2.0) • © Pumpkin Patch Pals</p>`;
    app.querySelectorAll('.chip').forEach((b) => b.onclick = () => { store.set('filter', b.dataset.f); sfx.tap(); home(); });
    app.querySelectorAll('.tile').forEach((b) => b.onclick = () => { sfx.tap(); go(b.dataset.id); });
  }

  function go(id) {
    const a = ACTIVITIES.find((x) => x.id === id);
    if (!a) return home();
    if (location.hash !== '#' + id) history.pushState(null, '', '#' + id);
    a.run();
    app.focus({ preventScroll: true });
    window.scrollTo(0, 0);
  }

  function frame(title, { levels = null, level = 0, onLevel = null } = {}) {
    app.innerHTML = `
      <div class="panel">
        <div class="act-head no-print">
          <button class="back" id="backBtn">← Games</button>
          <h1>${esc(title)}</h1>
          ${levels ? `<div class="levels" role="group" aria-label="Level">${levels.map((l, i) => `<button data-l="${i}" aria-pressed="${i === level}">${esc(l)}</button>`).join('')}</div>` : ''}
        </div>
        <div id="body"></div>
      </div>`;
    $('#backBtn').onclick = () => { sfx.tap(); history.pushState(null, '', '#'); home(); };
    if (levels) app.querySelectorAll('.levels button').forEach((b) => b.onclick = () => { sfx.tap(); onLevel(+b.dataset.l); });
    return $('#body');
  }

  function celebrate(body, again) {
    sfx.win(); confetti(40);
    body.innerHTML = `
      <div class="celebrate">
        ${art('jack-glow')}
        <h2>You did it!</h2>
        <p>You earned ${ROUNDS} stars!</p>
        <div class="row"><button class="big-btn" id="again">Play again</button><button class="big-btn alt" id="homeAgain">More games</button></div>
      </div>`;
    say('You did it! Great work!');
    $('#again').onclick = again;
    $('#homeAgain').onclick = () => { history.pushState(null, '', '#'); home(); };
  }

  // ---------------------------------------------------------------- quiz engine
  const ROUNDS = 5;
  function quiz(makeRound, title, levels = null) {
    let level = store.get('lvl-' + title, 0);
    if (!levels) level = 0;
    const start = () => {
      const body = frame(title, { levels, level, onLevel: (l) => { level = l; store.set('lvl-' + title, l); start(); } });
      let n = 0;
      let last = null;
      const next = () => {
        if (n >= ROUNDS) return celebrate(body, start);
        let r;
        do { r = makeRound(level); } while (last && r.key && r.key === last && Math.random() < 0.9);
        last = r.key;
        body.innerHTML = `
          <div class="progress" aria-label="Progress">${Array.from({ length: ROUNDS }, (_, i) => `<span class="${i < n ? 'done' : ''}">${window.ART.star.svg}</span>`).join('')}</div>
          <div class="prompt"><button class="say" aria-label="Hear it again">🔊</button><span>${r.prompt}</span></div>
          <div class="stage">${r.stage || ''}</div>
          <div class="choices">${r.choices.map((c, i) => `<button class="choice ${c.cls || ''}" data-i="${i}" aria-label="${esc(c.label)}">${c.html}</button>`).join('')}</div>
          <div class="feedback" aria-live="polite"></div>`;
        const speak = () => say(r.speak || r.prompt.replace(/<[^>]+>/g, ''));
        $('.say', body).onclick = speak;
        speak();
        let done = false;
        body.querySelectorAll('.choice').forEach((b) => b.onclick = async () => {
          if (done) return;
          const c = r.choices[+b.dataset.i];
          const fb = $('.feedback', body);
          if (c.correct) {
            done = true;
            b.classList.add('right'); sfx.right(); confetti(); addStar();
            fb.className = 'feedback'; fb.textContent = pick(PRAISE);
            say(r.after || fb.textContent);
            n += 1;
            await wait(1500);
            if (alive(body)) next();
          } else {
            b.classList.remove('wrong'); void b.offsetWidth; b.classList.add('wrong');
            sfx.wrong();
            fb.className = 'feedback try'; fb.textContent = pick(TRY);
            setTimeout(() => b.classList.add('wrong-done'), 400);
          }
        });
      };
      next();
    };
    start();
  }

  function numberChoices(ans, lo, hi, k = 3) {
    const set = new Set([ans]);
    while (set.size < k) {
      const d = ans + (rand(2) ? 1 : -1) * (1 + rand(3));
      if (d >= lo && d <= hi) set.add(d);
    }
    return shuffle([...set]).map((v) => ({ html: String(v), label: String(v), correct: v === ans }));
  }

  // ---------------------------------------------------------------- counting
  function countRounds(level) {
    const max = level ? 20 : 10;
    const n = 1 + rand(max);
    const icon = pick(['mini', 'mini', 'apple', 'acorn', 'ghost', 'maple']);
    const names = { mini: 'pumpkins', apple: 'apples', acorn: 'acorns', ghost: 'ghosts', maple: 'leaves' };
    const cells = n > 10 ? 20 : 10;
    const spots = new Set(sample([...Array(cells).keys()], n));
    const field = Array.from({ length: cells }, (_, i) => art(icon, spots.has(i) ? 'art' : 'art hide')).join('');
    return {
      key: n, prompt: `How many ${names[icon]}?`,
      stage: `<div class="count-field ${cells > 10 ? 'wide' : ''}">${field}</div>`,
      choices: numberChoices(n, 1, max),
      after: `Yes! ${n}!`,
    };
  }

  // ---------------------------------------------------------------- addition
  function addRounds(level) {
    const max = level ? 10 : 5;
    const a = 1 + rand(max - 1);
    const b = 1 + rand(max - a);
    const g = (k) => `<div class="group">${Array.from({ length: k }, () => art('mini')).join('')}</div>`;
    return {
      key: a * 100 + b, prompt: `${a} + ${b} = ?`, speak: `What is ${a} plus ${b}?`,
      stage: `<div class="sum">${g(a)}<span class="op">+</span>${g(b)}</div>`,
      choices: numberChoices(a + b, 1, 10),
      after: `${a} plus ${b} equals ${a + b}!`,
    };
  }

  // ---------------------------------------------------------------- patterns
  const PAT_PICS = ['mini', 'maple', 'acorn', 'apple', 'ghost', 'bat', 'candy-corn', 'moon', 'owl', 'star'];
  function patternRounds(level) {
    const shapes = level ? pick(['AB', 'AAB', 'ABB', 'ABC', 'AABB']) : 'AB';
    const letters = [...new Set(shapes)];
    const pics = sample(PAT_PICS, letters.length + 1);
    const map = Object.fromEntries(letters.map((l, i) => [l, pics[i]]));
    const len = Math.max(6, shapes.length * 2 + 1);
    const seq = Array.from({ length: len }, (_, i) => map[shapes[i % shapes.length]]);
    const ans = seq.pop();
    const opts = shuffle([...new Set([ans, ...Object.values(map), pics[pics.length - 1]])]).slice(0, 3);
    if (!opts.includes(ans)) opts[0] = ans;
    return {
      key: shapes + pics.join(), prompt: 'What comes next?',
      stage: `<div class="pattern">${seq.map((p) => `<div class="cell">${art(p)}</div>`).join('')}<div class="cell q">?</div></div>`,
      choices: shuffle(opts).map((p) => ({ html: art(p), label: p, correct: p === ans })),
    };
  }

  // ---------------------------------------------------------------- letters
  function letterRounds(level) {
    const pool = level ? 'NOPQRSTUVWXYZ' : 'ABCDEFGHIJKLM';
    const L = pick([...pool]);
    const others = sample([...'abcdefghijklmnopqrstuvwxyz'].filter((c) => c !== L.toLowerCase()), 2);
    return {
      key: L, prompt: `Find the lowercase <b>${L.toLowerCase()}</b>`, speak: `Find the lowercase letter that matches capital ${L}.`,
      stage: `<div class="letter-pumpkin">${art('pumpkin-plain')}<b>${L}</b></div>`,
      choices: shuffle([L.toLowerCase(), ...others]).map((c) => ({ html: c, label: c, cls: 'letter', correct: c === L.toLowerCase() })),
      after: `Yes! Capital ${L} and lowercase ${L.toLowerCase()}!`,
    };
  }

  // ---------------------------------------------------------------- beginning sounds
  const SOUND_WORDS = [['bat', 'b', 'bat'], ['cat', 'c', 'cat'], ['ghost', 'g', 'ghost'], ['hat', 'h', 'hat'],
    ['maple', 'l', 'leaf'], ['moon', 'm', 'moon'], ['owl', 'o', 'owl'], ['pumpkin', 'p', 'pumpkin'], ['star', 's', 'star'],
    ['web', 'w', 'web'], ['apple', 'a', 'apple'], ['rake', 'r', 'rake'], ['corn', 'c', 'corn'], ['mug', 'm', 'mug'],
    ['bee', 'b', 'bee'], ['tree', 't', 'tree'], ['bug', 'b', 'bug'], ['spider', 's', 'spider'], ['cake', 'c', 'cake'],
    ['broom', 'b', 'broom'], ['mushroom', 'm', 'mushroom'], ['pie', 'p', 'pie'], ['car', 'c', 'car']];
  function soundRounds() {
    const [pic, letter, word] = pick(SOUND_WORDS);
    const others = sample([...'bcdfghlmnprstw'].filter((c) => c !== letter), 2);
    return {
      key: word, prompt: `What sound does <b>${word}</b> start with?`, speak: `${word}. What sound does ${word} start with?`,
      stage: `<div class="pic-big">${art(pic)}</div>`,
      choices: shuffle([letter, ...others]).map((c) => ({ html: c, label: c, cls: 'letter', correct: c === letter })),
      after: `Yes! The word ${word} starts with ${letter}!`,
    };
  }

  // ---------------------------------------------------------------- rhyming
  const RHYME = [['at', [['cat', 'cat'], ['hat', 'hat'], ['bat', 'bat']]], ['oon', [['moon', 'moon'], ['spoon', 'spoon']]],
    ['ar', [['star', 'star'], ['car', 'car']]], ['ake', [['rake', 'rake'], ['cake', 'cake']]],
    ['ee', [['bee', 'bee'], ['tree', 'tree']]], ['ug', [['bug', 'bug'], ['mug', 'mug']]]];
  function rhymeRounds() {
    const gi = rand(RHYME.length);
    const [a, b] = sample(RHYME[gi][1], 2);
    const others = sample(RHYME.filter((_, i) => i !== gi), 2).map((g) => pick(g[1]));
    return {
      key: a[1], prompt: `What rhymes with <b>${a[1]}</b>?`, speak: `What rhymes with ${a[1]}?`,
      stage: `<div class="pic-big">${art(a[0])}</div>`,
      choices: shuffle([b, ...others]).map((w) => ({ html: art(w[0]), label: w[1], correct: w === b })),
      after: `Yes! ${a[1]} and ${b[1]} rhyme!`,
    };
  }

  // ---------------------------------------------------------------- ten frame
  function runTenFrame() {
    const start = () => {
      const body = frame('Ten Frame Fill');
      let n = 0;
      const next = () => {
        if (n >= ROUNDS) return celebrate(body, start);
        const target = 1 + rand(10);
        const filled = Array(10).fill(false);
        body.innerHTML = `
          <div class="progress">${Array.from({ length: ROUNDS }, (_, i) => `<span class="${i < n ? 'done' : ''}">${window.ART.star.svg}</span>`).join('')}</div>
          <div class="prompt"><button class="say" aria-label="Hear it again">🔊</button><span>Put <b>${target}</b> pumpkins in the ten frame.</span></div>
          <div class="row" style="gap:28px">
            <div class="target">${art('mini')}<span>${target}</span></div>
            <div class="tenframe">${filled.map((_, i) => `<button data-i="${i}" aria-label="box ${i + 1}"></button>`).join('')}</div>
          </div>
          <div class="row" style="margin-top:18px"><button class="big-btn green" id="check">Check</button><button class="big-btn alt" id="clear">Clear</button></div>
          <div class="feedback" aria-live="polite"></div>`;
        const speak = () => say(tenPrompt(target));
        $('.say', body).onclick = speak; speak();
        body.querySelectorAll('.tenframe button').forEach((b) => b.onclick = () => {
          const i = +b.dataset.i; filled[i] = !filled[i];
          b.innerHTML = filled[i] ? art('mini') : '';
          sfx.tap();
        });
        $('#clear').onclick = () => { filled.fill(false); body.querySelectorAll('.tenframe button').forEach((b) => b.innerHTML = ''); };
        $('#check').onclick = async () => {
          const c = filled.filter(Boolean).length;
          const fb = $('.feedback', body);
          if (c === target) {
            sfx.right(); confetti(); addStar();
            fb.className = 'feedback'; fb.textContent = `${pick(PRAISE)} ${target} pumpkins!`;
            say(tenYes(target));
            n += 1; await wait(1900); if (alive(body)) next();
          } else {
            sfx.wrong();
            fb.className = 'feedback try';
            fb.textContent = tenFix(c, target);
            say(fb.textContent);
          }
        };
      };
      next();
    };
    start();
  }

  // ---------------------------------------------------------------- spell CVC
  const CVC = [['cat', 'cat'], ['bat', 'bat'], ['hat', 'hat'], ['bug', 'bug'], ['mug', 'mug'], ['web', 'web']];
  function runSpell() {
    const start = () => {
      const body = frame('Spell It!');
      let n = 0; let last = null;
      const next = () => {
        if (n >= ROUNDS) return celebrate(body, start);
        let w; do { w = pick(CVC); } while (w === last); last = w;
        const word = w[1];
        const extra = sample([...'abcdefghilmnoprstuw'].filter((c) => !word.includes(c)), 2);
        const tiles = shuffle([...word, ...extra]);
        let typed = [];
        body.innerHTML = `
          <div class="progress">${Array.from({ length: ROUNDS }, (_, i) => `<span class="${i < n ? 'done' : ''}">${window.ART.star.svg}</span>`).join('')}</div>
          <div class="prompt"><button class="say" aria-label="Hear it again">🔊</button><span>Spell the word!</span></div>
          <div class="stage"><div class="pic-big">${art(w[0])}</div></div>
          <div class="slots">${[...word].map(() => '<div class="slot"></div>').join('')}</div>
          <div class="tiles">${tiles.map((t, i) => `<button class="tilebtn" data-i="${i}">${t}</button>`).join('')}</div>
          <div class="row" style="margin-top:14px"><button class="big-btn alt" id="undo">⌫ Undo</button></div>
          <div class="feedback" aria-live="polite"></div>`;
        const speak = () => say(`Spell ${word}. ${[...word].join(', ')}.`);
        $('.say', body).onclick = speak; say(`Spell ${word}.`);
        const slots = body.querySelectorAll('.slot');
        const render = () => slots.forEach((s, i) => { s.textContent = typed[i] ? typed[i].ch : ''; s.classList.toggle('filled', !!typed[i]); });
        body.querySelectorAll('.tilebtn').forEach((b) => b.onclick = async () => {
          if (typed.length >= word.length) return;
          typed.push({ ch: b.textContent, b }); b.disabled = true; sfx.tap(); say(b.textContent); render();
          if (typed.length === word.length) {
            const fb = $('.feedback', body);
            if (typed.map((t) => t.ch).join('') === word) {
              sfx.right(); confetti(); addStar(); fb.className = 'feedback'; fb.textContent = pick(PRAISE);
              say([`${[...word].join(' ')}. That spells ${word}!`, fb.textContent]);
              n += 1; await wait(2000); if (alive(body)) next();
            } else {
              sfx.wrong(); fb.className = 'feedback try'; fb.textContent = 'Not quite. Tap Undo and try again!';
              say(SPELL_TRY);
            }
          }
        });
        $('#undo').onclick = () => { const t = typed.pop(); if (t) { t.b.disabled = false; render(); $('.feedback', body).textContent = ''; } };
      };
      next();
    };
    start();
  }

  // ---------------------------------------------------------------- life cycle
  const STAGES = [['seed', 'seed'], ['sprout', 'sprout'], ['vine', 'vine'], ['pumpkin-flower', 'flower'], ['green-pumpkin', 'green pumpkin'], ['pumpkin', 'orange pumpkin']];
  function runLifeCycle() {
    const start = () => {
      const body = frame('Pumpkin Life Cycle');
      let step = 0;
      const order = shuffle(STAGES.map((_, i) => i));
      body.innerHTML = `
        <div class="prompt"><button class="say" aria-label="Hear it again">🔊</button><span>How does a pumpkin grow? Tap the pictures in order!</span></div>
        <div class="slots6">${STAGES.map((_, i) => `<div class="slot6" data-s="${i}"><span class="n">${i + 1}</span></div>`).join('')}</div>
        <div class="cards6">${order.map((i) => `<button class="choice" data-i="${i}" aria-label="${STAGES[i][1]}">${art(STAGES[i][0])}</button>`).join('')}</div>
        <div class="feedback" aria-live="polite"></div>`;
      const speak = () => say(LIFE_INTRO);
      $('.say', body).onclick = speak; speak();
      body.querySelectorAll('.cards6 .choice').forEach((b) => b.onclick = async () => {
        const i = +b.dataset.i; const fb = $('.feedback', body);
        if (i === step) {
          const slot = body.querySelector(`.slot6[data-s="${i}"]`);
          slot.innerHTML = `<span class="n">${i + 1}</span>${art(STAGES[i][0])}<small>${STAGES[i][1]}</small>`;
          slot.classList.add('filled'); b.style.visibility = 'hidden';
          sfx.right(); addStar(); fb.className = 'feedback'; fb.textContent = STAGES[i][1] + '!';
          say(LIFE_LINES[i]);
          step += 1;
          if (step === STAGES.length) { await wait(2200); if (!alive(body)) return; confetti(40); sfx.win(); fb.textContent = 'You grew a pumpkin!'; say('You grew a pumpkin!'); body.insertAdjacentHTML('beforeend', '<div class="row" style="margin-top:12px"><button class="big-btn" id="again">Play again</button></div>'); $('#again').onclick = start; }
        } else {
          b.classList.remove('wrong'); void b.offsetWidth; b.classList.add('wrong'); sfx.wrong();
          fb.className = 'feedback try'; fb.textContent = 'Not yet! What comes ' + (step === 0 ? 'first?' : 'next?');
        }
      });
    };
    start();
  }

  // ---------------------------------------------------------------- memory
  const MEM_PICS = ['mini', 'maple', 'acorn', 'apple', 'ghost', 'bat', 'owl', 'candy-corn', 'moon', 'cat', 'spider', 'sunflower', 'corn', 'mushroom'];
  function runMemory() {
    let level = store.get('lvl-memory', 0);
    const start = () => {
      const pairs = level ? 8 : 6;
      const body = frame('Fall Memory Match', { levels: ['6 pairs', '8 pairs'], level, onLevel: (l) => { level = l; store.set('lvl-memory', l); start(); } });
      const pics = sample(MEM_PICS, pairs);
      const deck = shuffle([...pics, ...pics]);
      let open = []; let found = 0; let tries = 0; let lock = false;
      body.innerHTML = `
        <div class="prompt"><span>Find the matching pairs!</span> <span id="tries" style="font-size:18px;color:var(--muted)"></span></div>
        <div class="memory ${level ? '' : 'six'}">${deck.map((p, i) => `
          <button class="mcard" data-i="${i}" aria-label="card ${i + 1}"><div class="in"><div class="face front">${art('pumpkin-plain')}</div><div class="face back">${art(p)}</div></div></button>`).join('')}
        </div>`;
      say('Find the matching pairs!');
      body.querySelectorAll('.mcard').forEach((b) => b.onclick = async () => {
        if (lock || b.classList.contains('flip') || b.classList.contains('match')) return;
        b.classList.add('flip'); sfx.flip(); open.push(b);
        if (open.length < 2) return;
        tries += 1; $('#tries').textContent = `Tries: ${tries}`;
        const [x, y] = open; open = [];
        if (deck[+x.dataset.i] === deck[+y.dataset.i]) {
          x.classList.add('match'); y.classList.add('match'); sfx.right(); addStar(); found += 1;
          if (found === pairs) { await wait(700); if (alive(body)) celebrate(body, start); }
        } else {
          lock = true; await wait(950); x.classList.remove('flip'); y.classList.remove('flip'); lock = false;
        }
      });
    };
    start();
  }

  // ---------------------------------------------------------------- feelings
  const FEELINGS = [['happy', 'Happy', 'Share your smile with a friend!'], ['sad', 'Sad', 'It is OK to feel sad. A hug or talking to a grown-up can help.'],
    ['mad', 'Mad', 'Let’s take three slow pumpkin breaths together.'], ['surprised', 'Surprised', 'Wow! Tell a friend what surprised you.'],
    ['sleepy', 'Sleepy', 'Stretch up tall like a pumpkin vine!'], ['silly', 'Silly', 'Silly is fun! Let’s get ready to learn.'],
    ['scared', 'Scared', 'You are safe. Breathe slowly with the pumpkin.'], ['proud', 'Proud', 'Hooray! You worked hard!']];
  function runFeelings() {
    const body = frame('Feelings Check-In');
    body.innerHTML = `
      <div class="prompt"><button class="say" aria-label="Hear it again">🔊</button><span>How do you feel today?</span></div>
      <div class="feel-grid">${FEELINGS.map(([k, t]) => `<button class="choice" data-k="${k}">${art('feel-' + k)}<span>${t}</span></button>`).join('')}</div>
      <div class="row" style="margin-top:18px"><button class="big-btn alt" id="breatheBtn">🎃 Pumpkin breathing</button></div>`;
    const speak = () => say(FEEL_INTRO);
    $('.say', body).onclick = speak; speak();
    body.querySelectorAll('.feel-grid .choice').forEach((b) => b.onclick = () => {
      const [k, t, tip] = FEELINGS.find((f) => f[0] === b.dataset.k);
      sfx.right();
      body.innerHTML = `
        <div class="feel-result">${art('feel-' + k)}<h2>I feel ${t.toLowerCase()}.</h2><p style="font-size:22px">${tip}</p>
        <div class="row"><button class="big-btn alt" id="breatheBtn">🎃 Pumpkin breathing</button><button class="big-btn" id="backFeel">Check in again</button></div></div>`;
      say(`I feel ${t}. ${tip}`);
      $('#backFeel').onclick = runFeelings;
      $('#breatheBtn').onclick = breathing;
    });
    $('#breatheBtn').onclick = breathing;
  }
  function breathing() {
    const body = $('#body');
    body.innerHTML = `
      <div class="prompt"><span>Smell the pumpkin pie... blow out the candle.</span></div>
      <div class="breathe go" id="ball">Breathe in</div>
      <div class="row"><button class="big-btn" id="doneBreathe">I feel calm</button></div>`;
    const ball = $('#ball'); let inhale = true;
    say(BREATHE);
    const t = setInterval(() => { if (!document.body.contains(ball)) return clearInterval(t); inhale = !inhale; ball.textContent = inhale ? 'Breathe in' : 'Breathe out'; }, 4000);
    $('#doneBreathe').onclick = () => { clearInterval(t); runFeelings(); };
  }

  // ---------------------------------------------------------------- roll a jack-o'-lantern
  const ROLL = {
    eyes: ['eye-triangle', 'eye-round', 'eye-star', 'eye-heart', 'eye-angry', 'eye-googly'],
    nose: ['nose-triangle', 'nose-circle', 'nose-heart', 'nose-down', 'nose-square', 'nose-star'],
    mouth: ['mouth-grin', 'mouth-smile', 'mouth-zigzag', 'mouth-vampire', 'mouth-o', 'mouth-tongue'],
  };
  const PIPS = { 1: [4], 2: [0, 8], 3: [0, 4, 8], 4: [0, 2, 6, 8], 5: [0, 2, 4, 6, 8], 6: [0, 2, 3, 5, 6, 8] };
  function runRoll() {
    const body = frame("Roll a Jack-o'-Lantern");
    const steps = ['eyes', 'nose', 'mouth'];
    let step = 0; const face = {};
    body.innerHTML = `
      <div class="roll-wrap">
        <div>
          <div class="stage-wrap"><div class="deco-stage" id="rollStage"></div></div>
        </div>
        <div>
          <div class="prompt"><span id="rollMsg">Roll for the eyes!</span></div>
          <div class="die" id="die">${Array.from({ length: 9 }, () => '<i></i>').join('')}</div>
          <div class="row" style="margin:16px 0"><button class="big-btn" id="rollBtn">🎲 Roll!</button><button class="big-btn alt" id="newBtn">New pumpkin</button></div>
          <table class="chart"><thead><tr><th>Roll</th><th>Eyes</th><th>Nose</th><th>Mouth</th></tr></thead>
          <tbody>${[1, 2, 3, 4, 5, 6].map((r) => `<tr data-r="${r}"><td class="pips">${r}</td><td>${art(ROLL.eyes[r - 1])}</td><td>${art(ROLL.nose[r - 1])}</td><td>${art(ROLL.mouth[r - 1])}</td></tr>`).join('')}</tbody></table>
        </div>
      </div>`;
    const stage = $('#rollStage');
    const draw = () => {
      const parts = [];
      if (face.eyes) { parts.push({ key: face.eyes, x: -15, y: -2, s: 20 }); parts.push({ key: face.eyes, x: 15, y: -2, s: 20, flip: true }); }
      if (face.nose) parts.push({ key: face.nose, x: 0, y: 12, s: 13 });
      if (face.mouth) parts.push({ key: face.mouth, x: 0, y: 27, s: 36 });
      renderStage(stage, 'base-orange', parts.map((p, i) => ({ id: i, flip: false, rot: 0, ...p })));
    };
    const setDie = (n) => $('#die').querySelectorAll('i').forEach((el, i) => el.classList.toggle('on', PIPS[n].includes(i)));
    setDie(1); draw(); say(ROLL_INTRO);
    $('#rollBtn').onclick = async () => {
      if (step >= 3) return;
      const die = $('#die'); die.classList.remove('rolling'); void die.offsetWidth; die.classList.add('rolling'); sfx.roll();
      for (let i = 0; i < 6; i++) { setDie(1 + rand(6)); await wait(90); }
      const r = 1 + rand(6); setDie(r);
      body.querySelectorAll('.chart tr').forEach((tr) => tr.classList.toggle('hl', tr.dataset.r === String(r)));
      const part = steps[step];
      face[part] = ROLL[part][r - 1]; draw(); sfx.right();
      step += 1;
      const msg = rollMsg(r, step);
      $('#rollMsg').textContent = msg; say(msg);
      if (step === 3) { addStar(); confetti(30); }
    };
    $('#newBtn').onclick = runRoll;
  }

  // ---------------------------------------------------------------- decorate
  const STAGE = 140; const BASE_Y = 8;
  function partBox(p) {
    const a = window.ART[p.key]; const k = p.s / 100;
    const x0 = p.flip ? -(a.x0 + a.w) : a.x0;
    return { left: p.x + x0 * k, top: p.y + BASE_Y + a.y0 * k, w: a.w * k, h: a.h * k };
  }
  function pct(v) { return (v / STAGE * 100).toFixed(3) + '%'; }
  function renderStage(stage, baseKey, parts, selId = null) {
    const b = window.ART[baseKey];
    stage.innerHTML = `<div class="base" style="left:${pct(b.x0 + STAGE / 2)};top:${pct(b.y0 + BASE_Y + STAGE / 2)};width:${pct(b.w)};height:${pct(b.h)}">${b.svg}</div>` +
      parts.map((p) => {
        const bx = partBox(p);
        return `<div class="part ${p.id === selId ? 'sel' : ''}" data-id="${p.id}" style="left:${pct(bx.left + STAGE / 2)};top:${pct(bx.top + STAGE / 2)};width:${pct(bx.w)};height:${pct(bx.h)};transform:rotate(${p.rot || 0}deg)"><div style="width:100%;height:100%;transform:scaleX(${p.flip ? -1 : 1})">${window.ART[p.key].svg}</div></div>`;
      }).join('');
  }
  const SWATCHES = [['orange', '#f7902b'], ['green', '#8cc63f'], ['white', '#fff3dd'], ['purple', '#7d4fa6'], ['teal', '#2bb3a3'], ['pink', '#f8a5c2']];
  const CATS = [['eyes', 'Eyes'], ['noses', 'Noses'], ['mouths', 'Mouths'], ['extras', 'Hats & more']];
  function runDecorate() {
    const body = frame('Decorate a Pumpkin');
    const saved = store.get('deco', null);
    let base = (saved && saved.base) || 'base-orange';
    let parts = (saved && saved.parts) || [];
    let nextId = parts.reduce((m, p) => Math.max(m, p.id + 1), 0);
    let sel = null; let cat = 'eyes';
    body.innerHTML = `
      <div class="deco">
        <div class="stage-wrap"><div class="deco-stage" id="stage" aria-label="Your pumpkin. Drag the pieces to move them."></div></div>
        <div class="no-print">
          <div class="swatches" role="group" aria-label="Pumpkin colour"><b>Pumpkin:</b>${SWATCHES.map(([k, c]) => `<button class="swatch" data-b="base-${k}" style="background:${c}" aria-label="${k}" aria-pressed="${'base-' + k === base}"></button>`).join('')}</div>
          <div class="tray-tabs" role="tablist">${CATS.map(([k, t]) => `<button data-c="${k}" aria-pressed="${k === cat}">${t}</button>`).join('')}</div>
          <div class="tray" id="tray"></div>
          <div class="seltools" id="seltools">
            <button data-a="bigger">➕ Bigger</button><button data-a="smaller">➖ Smaller</button>
            <button data-a="flip">⇄ Flip</button><button data-a="turn">↻ Turn</button><button data-a="del">🗑 Remove</button>
          </div>
          <div class="row" style="justify-content:flex-start">
            <button class="big-btn green" id="surprise">✨ Surprise me</button>
            <button class="big-btn alt" id="clearAll">Start over</button>
            <button class="big-btn" id="savePng">💾 Save picture</button>
            <button class="big-btn alt" id="printBtn">🖨 Print</button>
          </div>
        </div>
      </div>`;
    const stage = $('#stage');
    const persist = () => store.set('deco', { base, parts });
    const draw = () => {
      renderStage(stage, base, parts, sel);
      body.querySelectorAll('#seltools button').forEach((b) => b.disabled = sel === null);
      persist();
    };
    const tray = () => {
      $('#tray').innerHTML = window.PARTS.filter((p) => p.cat === cat).map((p) => `<button data-k="${p.key}" aria-label="${p.key.replace(/-/g, ' ')}">${art(p.key)}</button>`).join('');
      body.querySelectorAll('#tray button').forEach((b) => b.onclick = () => {
        const p = window.PARTS.find((x) => x.key === b.dataset.k);
        const jitter = () => (Math.random() - 0.5) * 4;
        if (p.pair) {
          parts.push({ id: nextId++, key: p.key, x: p.x + jitter(), y: p.y, s: p.size, flip: false, rot: 0 });
          parts.push({ id: nextId++, key: p.key, x: -p.x + jitter(), y: p.y, s: p.size, flip: true, rot: 0 });
        } else {
          parts.push({ id: nextId++, key: p.key, x: p.x + jitter(), y: p.y + jitter(), s: p.size, flip: false, rot: 0 });
        }
        sel = parts[parts.length - 1].id; sfx.tap(); draw();
      });
    };
    body.querySelectorAll('.tray-tabs button').forEach((b) => b.onclick = () => {
      cat = b.dataset.c; body.querySelectorAll('.tray-tabs button').forEach((x) => x.setAttribute('aria-pressed', x === b)); tray();
    });
    body.querySelectorAll('.swatch').forEach((b) => b.onclick = () => {
      base = b.dataset.b; body.querySelectorAll('.swatch').forEach((x) => x.setAttribute('aria-pressed', x === b)); sfx.tap(); draw();
    });
    body.querySelectorAll('#seltools button').forEach((b) => b.onclick = () => {
      const p = parts.find((x) => x.id === sel); if (!p) return;
      const a = b.dataset.a;
      if (a === 'bigger') p.s = Math.min(p.s * 1.15, 120);
      if (a === 'smaller') p.s = Math.max(p.s / 1.15, 5);
      if (a === 'flip') p.flip = !p.flip;
      if (a === 'turn') p.rot = ((p.rot || 0) + 15) % 360;
      if (a === 'del') { parts = parts.filter((x) => x !== p); sel = null; }
      sfx.tap(); draw();
    });
    $('#surprise').onclick = () => {
      const by = (c) => window.PARTS.filter((p) => p.cat === c);
      const e = pick(by('eyes')); const n = pick(by('noses')); const m = pick(by('mouths')); const x = pick(by('extras'));
      parts = [{ key: e.key, x: -15, y: -2, s: e.size }, { key: e.key, x: 15, y: -2, s: e.size, flip: true },
        { key: n.key, x: 0, y: 12, s: n.size }, { key: m.key, x: 0, y: 27, s: m.size }];
      if (x.pair) parts.push({ key: x.key, x: x.x, y: x.y, s: x.size }, { key: x.key, x: -x.x, y: x.y, s: x.size, flip: true });
      else parts.push({ key: x.key, x: x.x, y: x.y, s: x.size });
      parts = parts.map((p) => ({ id: nextId++, flip: false, rot: 0, ...p }));
      base = 'base-' + pick(SWATCHES)[0];
      body.querySelectorAll('.swatch').forEach((b) => b.setAttribute('aria-pressed', b.dataset.b === base));
      sel = null; sfx.right(); confetti(12); draw();
    };
    $('#clearAll').onclick = () => { parts = []; sel = null; sfx.tap(); draw(); };
    $('#printBtn').onclick = () => { sel = null; draw(); window.print(); };
    $('#savePng').onclick = () => savePicture(base, parts);

    // dragging
    let drag = null;
    stage.addEventListener('pointerdown', (ev) => {
      const el = ev.target.closest('.part');
      if (!el) { sel = null; draw(); return; }
      const p = parts.find((x) => x.id === +el.dataset.id);
      sel = p.id;
      parts = parts.filter((x) => x !== p).concat(p); // bring to front
      const r = stage.getBoundingClientRect();
      drag = { p, sx: ev.clientX, sy: ev.clientY, ox: p.x, oy: p.y, scale: STAGE / r.width };
      stage.setPointerCapture(ev.pointerId);
      draw();
    });
    stage.addEventListener('pointermove', (ev) => {
      if (!drag) return;
      drag.p.x = Math.max(-68, Math.min(68, drag.ox + (ev.clientX - drag.sx) * drag.scale));
      drag.p.y = Math.max(-70, Math.min(64, drag.oy + (ev.clientY - drag.sy) * drag.scale));
      const el = stage.querySelector(`.part[data-id="${drag.p.id}"]`);
      const bx = partBox(drag.p);
      if (el) { el.style.left = pct(bx.left + STAGE / 2); el.style.top = pct(bx.top + STAGE / 2); }
    });
    const end = () => { if (drag) { drag = null; persist(); } };
    stage.addEventListener('pointerup', end);
    stage.addEventListener('pointercancel', end);

    tray(); draw();
    say(DECO_INTRO);
  }

  function savePicture(base, parts) {
    const inner = (key, x, y, w, h) => window.ART[key].svg.replace('<svg ', `<svg x="${x}" y="${y}" width="${w}" height="${h}" preserveAspectRatio="none" `);
    const b = window.ART[base];
    let body = inner(base, b.x0, b.y0 + BASE_Y, b.w, b.h);
    parts.forEach((p) => {
      const bx = partBox(p); const cx = bx.left + bx.w / 2; const cy = bx.top + bx.h / 2;
      let tf = `rotate(${p.rot || 0} ${cx} ${cy})`;
      if (p.flip) tf += ` translate(${2 * cx} 0) scale(-1 1)`;
      body += `<g transform="${tf}">${inner(p.key, bx.left, bx.top, bx.w, bx.h)}</g>`;
    });
    const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="-70 -70 140 140" width="1200" height="1200"><rect x="-70" y="-70" width="140" height="140" fill="#eaf4ff"/>${body}</svg>`;
    const img = new Image();
    img.onload = () => {
      const cv = document.createElement('canvas'); cv.width = 1200; cv.height = 1200;
      cv.getContext('2d').drawImage(img, 0, 0, 1200, 1200);
      cv.toBlob((blob) => {
        const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = 'my-pumpkin.png';
        document.body.appendChild(a); a.click(); a.remove(); setTimeout(() => URL.revokeObjectURL(a.href), 2000);
      });
    };
    img.src = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(svg);
    sfx.right();
  }

  // ---------------------------------------------------------------- spoken lines
  const tenPrompt = (t) => `Put ${t} pumpkins in the ten frame. Then press check.`;
  const tenYes = (t) => (t === 10 ? 'Yes! 10. You filled the whole ten frame!' : `Yes! ${t}. ${10 - t} more makes 10.`);
  const tenFix = (c, t) => (c < t ? `You have ${c}. Add ${t - c} more!` : `You have ${c}. Take away ${c - t}!`);
  const rollMsg = (r, step) => (step < 3 ? `You rolled ${r}! Next, roll for the ${['eyes', 'nose', 'mouth'][step]}.` : `You rolled ${r}! Your jack-o'-lantern is done!`);
  const SPELL_TRY = "Hmm, not quite. Let's try again!";
  const LIFE_INTRO = 'How does a pumpkin grow? Tap the pictures in order. What comes first?';
  const LIFE_LINES = ['First, a seed.', 'Next, a sprout.', 'Then, a vine grows.', 'A yellow flower blooms.', 'A green pumpkin grows.', 'Last, an orange pumpkin!'];
  const FEEL_INTRO = 'How do you feel today? Tap the pumpkin that shows your feeling.';
  const BREATHE = 'Smell the pumpkin pie. Breathe in. Now blow out the candle. Breathe out.';
  const ROLL_INTRO = "Roll a jack-o'-lantern! Roll for the eyes.";
  const DECO_INTRO = 'Decorate your pumpkin! Tap a piece to add it, then drag it where you want.';

  // Every line the app can say, with the text the voice generator should read (letters are spelled out
  // as capitals so they are read as letter names). Used by tools/voice to pre-record voice.js.
  function speechCatalog() {
    const out = new Map();
    const add = (t, tts) => out.set(t, tts || t);
    const up = (c) => c.toUpperCase();
    add('You did it! Great work!');
    PRAISE.forEach((p) => add(p, { 'Pumpkin-tastic!': 'Pump-kin-tastic!' }[p]));
    ['pumpkins', 'apples', 'acorns', 'ghosts', 'leaves'].forEach((n) => add(`How many ${n}?`));
    for (let n = 1; n <= 20; n++) add(`Yes! ${n}!`);
    for (let a = 1; a <= 9; a++) for (let b = 1; a + b <= 10; b++) { add(`What is ${a} plus ${b}?`); add(`${a} plus ${b} equals ${a + b}!`); }
    add('What comes next?');
    for (const L of 'ABCDEFGHIJKLMNOPQRSTUVWXYZ') {
      add(`Find the lowercase letter that matches capital ${L}.`);
      add(`Yes! Capital ${L} and lowercase ${L.toLowerCase()}!`, `Yes! Capital ${L}, and lowercase ${L}!`);
    }
    SOUND_WORDS.forEach(([, letter, word]) => {
      add(`${word}. What sound does ${word} start with?`, `${word}... What sound does ${word} start with?`);
      add(`Yes! The word ${word} starts with ${letter}!`, `Yes! The word ${word} starts with ${up(letter)}!`);
    });
    RHYME.forEach(([, words]) => words.forEach((a) => {
      add(`What rhymes with ${a[1]}?`, `What rhymes with... ${a[1]}?`);
      const cap = (w) => w[0].toUpperCase() + w.slice(1);
      words.forEach((b) => { if (a !== b) add(`Yes! ${a[1]} and ${b[1]} rhyme!`, `Yes! ${cap(a[1])}... and ${b[1]}... rhyme!`); });
    }));
    for (let t = 1; t <= 10; t++) { add(tenPrompt(t)); add(tenYes(t)); }
    for (let c = 0; c <= 10; c++) for (let t = 1; t <= 10; t++) if (c !== t) add(tenFix(c, t));
    CVC.forEach(([, w]) => {
      add(`Spell ${w}.`);
      add(`Spell ${w}. ${[...w].join(', ')}.`, `Spell ${w}. ${[...w].map(up).join(', ')}.`);
      add(`${[...w].join(' ')}. That spells ${w}!`, `${[...w].map(up).join(', ')}. That spells ${w}!`);
    });
    'abcdefghijklmnopqrstuvwxyz'.split('').forEach((c) => add(c, up(c) + '.'));
    add(SPELL_TRY);
    add(LIFE_INTRO); LIFE_LINES.forEach((l) => add(l)); add('You grew a pumpkin!');
    add('Find the matching pairs!');
    add(FEEL_INTRO); FEELINGS.forEach(([, t, tip]) => add(`I feel ${t}. ${tip}`));
    add(BREATHE); add(ROLL_INTRO);
    for (let r = 1; r <= 6; r++) for (let st = 1; st <= 3; st++) add(rollMsg(r, st));
    add(DECO_INTRO);
    return [...out].map(([text, tts]) => ({ text, tts }));
  }
  window.PPP_SPEECH_CATALOG = speechCatalog;

  // ---------------------------------------------------------------- top bar
  function initBar() {
    $('#starCount').textContent = stars;
    document.querySelectorAll('[data-art]').forEach((el) => el.innerHTML = window.ART[el.dataset.art].svg);
    const sb = $('#soundBtn'); const vb = $('#voiceBtn');
    const sync = () => { sb.setAttribute('aria-pressed', settings.sound); vb.setAttribute('aria-pressed', settings.voice); };
    sb.onclick = () => { settings.sound = !settings.sound; store.set('sound', settings.sound); sync(); sfx.tap(); };
    vb.onclick = () => { settings.voice = !settings.voice; store.set('voice', settings.voice); sync(); if (!settings.voice) stopVoice(); };
    $('#fullBtn').onclick = () => {
      const d = document;
      if (!d.fullscreenElement) (d.documentElement.requestFullscreen || d.documentElement.webkitRequestFullscreen || (() => {})).call(d.documentElement);
      else (d.exitFullscreen || d.webkitExitFullscreen).call(d);
    };
    $('#homeBtn').onclick = () => { history.pushState(null, '', '#'); home(); };
    sync();
  }

  window.addEventListener('popstate', () => go(location.hash.slice(1)));
  initBar();
  if (location.hash.length > 1) go(location.hash.slice(1)); else home();
})();
