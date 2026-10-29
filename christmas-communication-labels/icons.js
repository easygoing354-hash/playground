// Original hand-built SVG icons (viewBox 0 0 100 100) for the Christmas
// communication cards. Every icon is drawn from scratch so the artwork is
// fully owned by the seller and safe for commercial resale.

const K = '#2d2a32'; // outline
const C = {
  red: '#E5484D', redDark: '#C2363C', green: '#2F9E5A', greenDark: '#1F7A43',
  gold: '#F5B82E', goldDark: '#D99A1A', face: '#FFD54A', brown: '#9A5B2E',
  tan: '#D9A066', cookie: '#E2A65B', choc: '#5A3420', skin: '#E9B27A',
  white: '#FFFFFF', blue: '#4A90D9', sky: '#BFE3FA', pink: '#F27BA8',
  purple: '#8E6BD8', gray: '#9AA0A6', light: '#E9EDF1', teal: '#1FA6A0',
  cheek: '#F79A8C', orange: '#F28C28',
};

const dot = (x, y, r = 3.2, fill = K) => `<circle cx="${x}" cy="${y}" r="${r}" fill="${fill}" stroke="none"/>`;

function starPts(cx, cy, R, r, n = 5) {
  const pts = [];
  for (let i = 0; i < n * 2; i++) {
    const a = -Math.PI / 2 + (i * Math.PI) / n;
    const rad = i % 2 ? r : R;
    pts.push(`${(cx + rad * Math.cos(a)).toFixed(1)},${(cy + rad * Math.sin(a)).toFixed(1)}`);
  }
  return pts.join(' ');
}
const star = (cx, cy, R, fill = C.gold) =>
  `<polygon points="${starPts(cx, cy, R, R * 0.45)}" fill="${fill}"/>`;

// Four-point sparkle, no outline.
const sparkle = (x, y, s = 6, fill = C.gold) =>
  `<path d="M${x} ${y - s} Q${x + s * 0.2} ${y - s * 0.2} ${x + s} ${y} Q${x + s * 0.2} ${y + s * 0.2} ${x} ${y + s} Q${x - s * 0.2} ${y + s * 0.2} ${x - s} ${y} Q${x - s * 0.2} ${y - s * 0.2} ${x} ${y - s} Z" fill="${fill}" stroke="none"/>`;

// Draws a group of overlapping shapes as one silhouette with a single outline:
// an outline pass (thick stroke) underneath, then the fills on top.
function merged(shapes, fill) {
  return `<g fill="${K}" stroke="${K}" stroke-width="6">${shapes}</g><g fill="${fill}" stroke="none">${shapes}</g>`;
}

// Open palm, fingers up, about 44 x 56 units before scaling.
function hand({ x = 0, y = 0, s = 1, r = 0, flip = false, fill = C.skin } = {}) {
  const shapes =
    `<rect x="8" y="7" width="7" height="30" rx="3.5"/>` +
    `<rect x="16.5" y="2" width="7" height="34" rx="3.5"/>` +
    `<rect x="25" y="3" width="7" height="33" rx="3.5"/>` +
    `<rect x="33.5" y="9" width="6.5" height="28" rx="3.25"/>` +
    `<rect x="8" y="23" width="32" height="30" rx="11"/>` +
    `<rect x="1" y="24" width="8" height="25" rx="4" transform="rotate(-32 7 47)"/>`;
  const fx = flip ? 'scale(-1 1) translate(-44 0)' : '';
  return `<g transform="translate(${x} ${y}) rotate(${r} 22 28) scale(${s}) ${fx}">${merged(shapes, fill)}</g>`;
}

// Round emoji-style face used by the feelings cards.
function face({ cx = 50, cy = 52, r = 36, fill = C.face, cheeks = true } = {}, features = '') {
  return `<circle cx="${cx}" cy="${cy}" r="${r}" fill="${fill}"/>` +
    (cheeks ? `${dot(cx - r * 0.55, cy + r * 0.2, r * 0.13, C.cheek)}${dot(cx + r * 0.55, cy + r * 0.2, r * 0.13, C.cheek)}` : '') +
    features;
}

function tree(tx = 0, ty = 0, s = 1) {
  return `<g transform="translate(${tx} ${ty}) scale(${s})">
    <rect x="43" y="80" width="14" height="12" rx="2" fill="${C.brown}"/>
    <path d="M50 44 L13 84 H87 Z" fill="${C.green}"/>
    <path d="M50 28 L19 64 H81 Z" fill="${C.green}"/>
    <path d="M50 15 L27 44 H73 Z" fill="${C.green}"/>
    ${dot(39, 56, 4.2, C.red)}${dot(62, 53, 4.2, C.gold)}${dot(50, 72, 4.2, C.blue)}
    ${dot(29, 77, 4.2, C.gold)}${dot(71, 77, 4.2, C.red)}${dot(52, 38, 4.2, C.red)}
    ${star(50, 14, 11)}
  </g>`;
}

function present(tx = 0, ty = 0, s = 1, body = C.red, lid = C.redDark, ribbon = C.gold) {
  return `<g transform="translate(${tx} ${ty}) scale(${s})">
    <path d="M50 33 Q33 10 26 23 Q23 34 50 33 Z" fill="${ribbon}"/>
    <path d="M50 33 Q67 10 74 23 Q77 34 50 33 Z" fill="${ribbon}"/>
    <rect x="20" y="45" width="60" height="43" rx="3" fill="${body}"/>
    <rect x="15" y="33" width="70" height="15" rx="3" fill="${lid}"/>
    <rect x="44" y="33" width="12" height="55" fill="${ribbon}"/>
    <circle cx="50" cy="32" r="5.5" fill="${ribbon}"/>
  </g>`;
}

function mug(tx = 0, ty = 0, s = 1, r = 0) {
  return `<g transform="translate(${tx} ${ty}) rotate(${r} 50 60) scale(${s})">
    <path d="M74 48 Q90 48 89 62 Q88 76 72 74" fill="none" stroke="${K}" stroke-width="13"/>
    <path d="M74 48 Q90 48 89 62 Q88 76 72 74" fill="none" stroke="${C.red}" stroke-width="7"/>
    <path d="M24 38 L28 84 Q29 90 36 90 L64 90 Q71 90 72 84 L76 38 Z" fill="${C.red}"/>
    <ellipse cx="50" cy="38" rx="26" ry="6" fill="#6B3E26"/>
    <rect x="34" y="30" width="11" height="9" rx="2.5" fill="${C.white}" transform="rotate(-12 39 34)"/>
    <rect x="50" y="29" width="11" height="9" rx="2.5" fill="${C.white}" transform="rotate(10 55 33)"/>
    <path d="M42 60 l3 -4 l3 4 l-3 4 Z M54 66 l3 -4 l3 4 l-3 4 Z" fill="${C.white}" stroke="none"/>
  </g>`;
}

function kid({ tx = 0, ty = 0, s = 1, shirt = C.blue } = {}) {
  return `<g transform="translate(${tx} ${ty}) scale(${s})">
    <path d="M24 92 Q24 56 50 56 Q76 56 76 92 Z" fill="${shirt}"/>
    <circle cx="50" cy="34" r="17" fill="${C.skin}"/>
    <path d="M33 32 Q33 15 50 15 Q67 15 67 32 Q60 24 50 25 Q40 24 33 32 Z" fill="#6B3E26"/>
    ${dot(44, 36, 2.6)}${dot(56, 36, 2.6)}
    <path d="M44 43 Q50 48 56 43" fill="none"/>
  </g>`;
}

function bigEye(cx, cy) {
  return `<ellipse cx="${cx}" cy="${cy}" rx="16" ry="20" fill="${C.white}"/>
    <circle cx="${cx + 2}" cy="${cy + 3}" r="9" fill="${C.blue}"/>
    ${dot(cx + 2, cy + 3, 4.5)}${dot(cx + 5, cy - 1, 2.2, C.white)}`;
}

function snowflakeArms(cx, cy, len, color, w) {
  let d = '';
  for (let i = 0; i < 6; i++) {
    const a = (i * Math.PI) / 3 - Math.PI / 2;
    const ex = cx + len * Math.cos(a), ey = cy + len * Math.sin(a);
    const bx = cx + len * 0.6 * Math.cos(a), by = cy + len * 0.6 * Math.sin(a);
    const b = len * 0.28;
    const l1x = bx + b * Math.cos(a - 0.8), l1y = by + b * Math.sin(a - 0.8);
    const l2x = bx + b * Math.cos(a + 0.8), l2y = by + b * Math.sin(a + 0.8);
    d += `M${cx} ${cy} L${ex.toFixed(1)} ${ey.toFixed(1)} M${bx.toFixed(1)} ${by.toFixed(1)} L${l1x.toFixed(1)} ${l1y.toFixed(1)} M${bx.toFixed(1)} ${by.toFixed(1)} L${l2x.toFixed(1)} ${l2y.toFixed(1)} `;
  }
  return `<path d="${d}" fill="none" stroke="${color}" stroke-width="${w}"/>`;
}

function hugPair() {
  return `
    <path d="M10 94 Q10 58 36 58 Q58 58 58 94 Z" fill="${C.red}"/>
    <path d="M42 94 Q42 58 64 58 Q90 58 90 94 Z" fill="${C.blue}"/>
    <circle cx="35" cy="38" r="15" fill="${C.skin}"/>
    <circle cx="65" cy="38" r="15" fill="${C.skin}"/>
    <path d="M21 36 Q21 21 35 21 Q49 21 49 36 Q43 29 35 30 Q27 29 21 36 Z" fill="#6B3E26"/>
    <path d="M51 36 Q51 21 65 21 Q79 21 79 36 Q73 29 65 30 Q57 29 51 36 Z" fill="#2d2a32"/>
    ${dot(31, 40, 2.3)}${dot(40, 40, 2.3)}${dot(60, 40, 2.3)}${dot(69, 40, 2.3)}
    <path d="M31 46 Q35.5 50 40 46 M60 46 Q64.5 50 69 46" fill="none"/>
    <path d="M30 70 Q50 82 76 68" fill="none" stroke="${K}" stroke-width="12"/>
    <path d="M30 70 Q50 82 76 68" fill="none" stroke="${C.red}" stroke-width="6"/>
    <circle cx="77" cy="68" r="6" fill="${C.skin}"/>`;
}

const ICONS = {
  // ---------- Nouns ----------
  tree: () => tree(),

  santa: () => `
    <path d="M27 44 Q29 15 53 11 Q74 9 80 33 L71 40 L72 44 Z" fill="${C.red}"/>
    <circle cx="80" cy="34" r="7.5" fill="${C.white}"/>
    <circle cx="50" cy="57" r="19" fill="#F6C9A0"/>
    <path d="M28 55 Q26 87 50 91 Q74 87 72 55 Q66 67 50 67 Q34 67 28 55 Z" fill="${C.white}"/>
    <path d="M50 65 Q40 60 33 66 Q42 73 50 68 Q58 73 67 66 Q60 60 50 65 Z" fill="${C.white}"/>
    <circle cx="50" cy="61" r="4.5" fill="${C.cheek}"/>
    <rect x="24" y="37" width="52" height="13" rx="6.5" fill="${C.white}"/>
    ${dot(43, 55, 2.8)}${dot(57, 55, 2.8)}`,

  present: () => present(),

  stocking: () => `
    <path d="M66 14 Q78 6 76 18" fill="none" stroke-width="3.5"/>
    <path d="M38 26 L38 56 Q21 60 19 72 Q19 89 38 89 Q53 89 63 79 Q69 72 69 62 L69 26 Z" fill="${C.red}"/>
    <path d="M38 89 Q24 89 21 76 Q30 74 34 84 Z" fill="${C.white}" stroke="none"/>
    ${star(54, 56, 8, C.gold)}
    <rect x="32" y="12" width="42" height="17" rx="5" fill="${C.white}"/>`,

  star: () => `${star(50, 54, 40)}${sparkle(14, 18, 6)}${sparkle(86, 20, 5)}${sparkle(84, 86, 5)}`,

  ornament: () => `
    <path d="M50 24 Q49 9 59 11 Q66 13 61 20" fill="none"/>
    <circle cx="50" cy="60" r="30" fill="${C.red}"/>
    <path d="M21 57 L29 51 L37 57 L45 51 L53 57 L61 51 L69 57 L79 51" fill="none" stroke="${C.gold}" stroke-width="4.5"/>
    <path d="M23 68 H77" fill="none" stroke="${C.white}" stroke-width="3.5"/>
    <path d="M33 45 Q36 38 43 36" fill="none" stroke="${C.white}" stroke-width="4"/>
    <rect x="41" y="21" width="18" height="12" rx="2.5" fill="${C.gold}"/>`,

  'candy cane': () => {
    const p = 'M62 90 L62 36 Q62 15 46 15 Q30 15 30 34';
    return `<path d="${p}" fill="none" stroke="${K}" stroke-width="21"/>
      <path d="${p}" fill="none" stroke="${C.white}" stroke-width="14"/>
      <path d="${p}" fill="none" stroke="${C.red}" stroke-width="14" stroke-dasharray="9 9" stroke-linecap="butt"/>`;
  },

  snowman: () => `
    <path d="M32 62 L14 50 M20 54 L14 46 M68 62 L86 50 M80 54 L86 46" fill="none" stroke="${C.brown}" stroke-width="4"/>
    <circle cx="50" cy="71" r="22" fill="${C.white}"/>
    <circle cx="50" cy="38" r="16" fill="${C.white}"/>
    <rect x="34" y="50" width="32" height="9" rx="4.5" fill="${C.red}"/>
    <rect x="55" y="53" width="9" height="18" rx="3.5" fill="${C.red}"/>
    ${dot(50, 69, 2.8)}${dot(50, 80, 2.8)}
    ${dot(44, 35, 2.8)}${dot(56, 35, 2.8)}
    <path d="M50 40 L66 43 L50 45 Z" fill="${C.orange}"/>
    <rect x="31" y="20" width="38" height="6" rx="2.5" fill="${K}"/>
    <rect x="38" y="4" width="24" height="18" rx="2" fill="${K}"/>
    <rect x="38" y="16" width="24" height="4" fill="${C.red}" stroke="none"/>`,

  reindeer: () => {
    const a = 'M40 34 C34 24 30 17 25 8 M31 20 Q24 19 17 22 M35 27 Q29 31 21 32 M60 34 C66 24 70 17 75 8 M69 20 Q76 19 83 22 M65 27 Q71 31 79 32';
    return `<path d="${a}" fill="none" stroke="${K}" stroke-width="9"/>
      <path d="${a}" fill="none" stroke="#B9814A" stroke-width="4"/>
      <ellipse cx="29" cy="45" rx="11" ry="5.5" fill="${C.brown}" transform="rotate(-25 29 45)"/>
      <ellipse cx="71" cy="45" rx="11" ry="5.5" fill="${C.brown}" transform="rotate(25 71 45)"/>
      <path d="M50 30 Q70 30 70 52 Q70 70 62 80 Q56 88 50 88 Q44 88 38 80 Q30 70 30 52 Q30 30 50 30 Z" fill="${C.brown}"/>
      <ellipse cx="50" cy="76" rx="13" ry="10" fill="${C.tan}"/>
      <circle cx="50" cy="69" r="7.5" fill="${C.red}"/>
      ${dot(42, 52, 4)}${dot(58, 52, 4)}${dot(43.5, 50.5, 1.4, C.white)}${dot(59.5, 50.5, 1.4, C.white)}
      <path d="M45 82 Q50 86 55 82" fill="none"/>`;
  },

  cookie: () => `
    <circle cx="50" cy="52" r="35" fill="${C.cookie}"/>
    <ellipse cx="38" cy="38" rx="4.5" ry="3.5" fill="${C.choc}" stroke="none"/>
    <ellipse cx="62" cy="40" rx="4" ry="3.5" fill="${C.choc}" stroke="none"/>
    <ellipse cx="50" cy="56" rx="4.5" ry="3.5" fill="${C.choc}" stroke="none"/>
    <ellipse cx="32" cy="62" rx="4" ry="3.5" fill="${C.choc}" stroke="none"/>
    <ellipse cx="66" cy="66" rx="4.5" ry="3.5" fill="${C.choc}" stroke="none"/>
    <ellipse cx="48" cy="76" rx="4" ry="3" fill="${C.choc}" stroke="none"/>
    <path d="M48 28 l5 2 M72 54 l3 4 M26 48 l2 5 M58 72 l5 -1" fill="none" stroke="${C.red}" stroke-width="3"/>
    <path d="M40 46 l4 -3 M60 54 l2 4 M38 72 l4 2" fill="none" stroke="${C.green}" stroke-width="3"/>`,

  gingerbread: () => `
    <path d="M50 13 A13 13 0 0 1 59 35 L76 40 Q85 44 81 52 Q77 57 68 53 L64 51 L64 64 L74 82 Q76 90 68 90 Q63 90 60 84 L50 70 L40 84 Q37 90 32 90 Q24 90 26 82 L36 64 L36 51 L32 53 Q23 57 19 52 Q15 44 24 40 L41 35 A13 13 0 0 1 50 13 Z" fill="#C97B3D"/>
    ${dot(45, 24, 2.6)}${dot(55, 24, 2.6)}
    <path d="M44 29 Q50 34 56 29" fill="none" stroke-width="2.5"/>
    <path d="M74 43 Q77.5 46.5 74 50 M26 43 Q22.5 46.5 26 50 M64 82 Q68 86 72 83 M36 82 Q32 86 28 83" fill="none" stroke="${C.white}" stroke-width="2.8"/>
    ${dot(50, 45, 3.6, C.red)}${dot(50, 56, 3.6, C.green)}`,

  lights: () => `<g transform="translate(0 12)">
    <path d="M4 26 Q28 52 50 30 Q72 8 96 34" fill="none" stroke-width="3.5"/>
    ${[[17, 37, C.red], [39, 38, C.green], [61, 22, C.gold], [83, 23, C.blue]].map(([x, y, c]) => `
      <ellipse cx="${x}" cy="${y + 19}" rx="8.5" ry="12" fill="${c}"/>
      <rect x="${x - 5}" y="${y}" width="10" height="8" rx="1.5" fill="${C.gray}"/>
      <path d="M${x - 3.5} ${y + 13} Q${x - 4.5} ${y + 18} ${x - 3} ${y + 22}" fill="none" stroke="${C.white}" stroke-width="2.5"/>`).join('')}
  </g>`,

  wreath: () => {
    const berries = [200, 250, 320, 20, 70, 130].map((deg) => {
      const a = (deg * Math.PI) / 180;
      return dot(50 + 28 * Math.cos(a), 48 + 28 * Math.sin(a), 4.2, C.red);
    }).join('');
    return `<circle cx="50" cy="48" r="28" fill="none" stroke="${K}" stroke-width="25"/>
      <circle cx="50" cy="48" r="28" fill="none" stroke="${C.green}" stroke-width="19"/>
      <circle cx="50" cy="48" r="28" fill="none" stroke="${C.greenDark}" stroke-width="3" stroke-dasharray="4 9"/>
      ${berries}
      <path d="M46 80 L39 95 L46 93 L48 82 Z M54 80 L61 95 L54 93 L52 82 Z" fill="${C.red}"/>
      <path d="M50 78 Q33 65 31 78 Q33 91 50 78 Z M50 78 Q67 65 69 78 Q67 91 50 78 Z" fill="${C.red}"/>
      <circle cx="50" cy="78" r="5.5" fill="${C.redDark}"/>`;
  },

  bell: () => `
    <path d="M13 40 Q8 50 13 60 M87 40 Q92 50 87 60" fill="none" stroke-width="3.5"/>
    <circle cx="50" cy="81" r="7.5" fill="${C.goldDark}"/>
    <path d="M50 18 Q30 18 28 45 L26 64 Q18 70 16 77 L84 77 Q82 70 74 64 L72 45 Q70 18 50 18 Z" fill="${C.gold}"/>
    <path d="M38 32 Q34 42 34 58" fill="none" stroke="${C.white}" stroke-width="4"/>
    <path d="M50 18 Q36 6 32 14 Q32 22 50 18 Z M50 18 Q64 6 68 14 Q68 22 50 18 Z" fill="${C.red}"/>
    <circle cx="50" cy="17" r="4.5" fill="${C.redDark}"/>`,

  elf: () => `
    <path d="M31 74 L37 86 L43 78 L50 88 L57 78 L63 86 L69 74 Z" fill="${C.green}"/>
    <path d="M34 58 L17 47 L32 70 Z M66 58 L83 47 L68 70 Z" fill="#F6C9A0"/>
    <circle cx="50" cy="60" r="19" fill="#F6C9A0"/>
    <path d="M30 48 Q34 18 70 8 Q60 24 70 48 Z" fill="${C.green}"/>
    <circle cx="70" cy="9" r="5.5" fill="${C.gold}"/>
    <rect x="27" y="42" width="46" height="11" rx="5.5" fill="${C.red}"/>
    ${dot(43, 60, 2.8)}${dot(57, 60, 2.8)}
    ${dot(38, 67, 3.2, C.cheek)}${dot(62, 67, 3.2, C.cheek)}
    <path d="M44 68 Q50 74 56 68" fill="none"/>`,

  sleigh: () => `
    <rect x="44" y="30" width="18" height="16" rx="2" fill="${C.green}"/>
    <rect x="51" y="30" width="4" height="16" fill="${C.gold}" stroke="none"/>
    <rect x="62" y="34" width="16" height="12" rx="2" fill="${C.blue}"/>
    <path d="M30 68 L26 82 M74 68 L74 82" fill="none" stroke-width="4.5"/>
    <path d="M8 82 L80 82 Q94 82 94 70" fill="none" stroke-width="5"/>
    <path d="M18 27 Q11 27 13 36 L22 62 Q24 69 32 69 L80 69 Q88 69 88 61 L88 49 Q88 44 83 44 L42 44 L37 31 Q35 25 28 25 Z" fill="${C.red}"/>
    <path d="M30 58 Q40 49 50 57 Q60 65 70 56" fill="none" stroke="${C.gold}" stroke-width="3.5"/>`,

  'hot cocoa': () => `
    <path d="M40 26 Q34 19 40 12 M52 24 Q46 17 52 9 M62 26 Q58 20 62 14" fill="none" stroke="${C.gray}" stroke-width="3.5"/>
    ${mug(0, 2)}`,

  snow: () => `${snowflakeArms(50, 50, 38, K, 10)}${snowflakeArms(50, 50, 38, C.sky, 5)}
    <circle cx="50" cy="50" r="7" fill="${C.sky}"/>`,

  mittens: () => {
    const m = `<rect x="34" y="16" width="30" height="50" rx="15"/><rect x="31" y="46" width="33" height="20"/>` +
      `<ellipse cx="29" cy="45" rx="7" ry="12" transform="rotate(-28 29 45)"/>`;
    const one = (t, fill) => `<g transform="${t}">${merged(m, fill)}
      <rect x="29" y="62" width="39" height="15" rx="4" fill="${C.white}"/>
      ${star(49, 38, 7, C.white).replace('<polygon', '<polygon stroke="none"')}</g>`;
    return `${one('translate(-12 8) rotate(-12 50 50) scale(0.9)', C.green)}${one('translate(20 4) rotate(10 50 50) scale(0.9)', C.red)}`;
  },

  milk: () => `
    <path d="M32 20 L36 86 Q36 90 40 90 L60 90 Q64 90 64 86 L68 20 Z" fill="${C.sky}" stroke="none"/>
    <path d="M32.9 34 L36 86 Q36 90 40 90 L60 90 Q64 90 64 86 L67.1 34 Z" fill="${C.white}" stroke="none"/>
    <path d="M32.9 34 H67.1" fill="none" stroke-width="2.5"/>
    <path d="M32 20 L36 86 Q36 90 40 90 L60 90 Q64 90 64 86 L68 20 Z" fill="none"/>
    <path d="M42 44 L44 78" fill="none" stroke="${C.light}" stroke-width="4"/>
    <circle cx="80" cy="80" r="13" fill="${C.cookie}"/>
    ${dot(76, 76, 2.4, C.choc)}${dot(84, 82, 2.4, C.choc)}${dot(78, 86, 2, C.choc)}`,

  // ---------- Verbs ----------
  open: () => `
    <path d="M50 44 L50 18 M38 46 L28 26 M62 46 L74 28 M30 50 L16 42 M70 50 L86 44" fill="none" stroke="${C.gold}" stroke-width="4"/>
    ${sparkle(50, 13, 6)}${sparkle(25, 22, 5)}${sparkle(77, 24, 5)}
    <rect x="22" y="52" width="56" height="36" rx="3" fill="${C.red}"/>
    <rect x="22" y="52" width="56" height="8" fill="#7A1F25"/>
    <rect x="44" y="52" width="12" height="36" fill="${C.gold}"/>
    <rect x="6" y="34" width="44" height="13" rx="3" fill="${C.redDark}" transform="rotate(-28 50 47)"/>`,

  wrap: () => `
    <path d="M8 74 L44 58 L94 70 L58 90 Z" fill="${C.red}"/>
    ${[[30, 72], [48, 66], [66, 72], [52, 80], [74, 80], [36, 80]].map(([x, y]) => dot(x, y, 2.6, C.white)).join('')}
    <path d="M36 62 L36 34 L58 34 L58 66" fill="#D7A86E"/>
    <path d="M36 34 L46 24 L68 24 L58 34 Z" fill="#E9C38F"/>
    <path d="M58 34 L68 24 L68 56 L58 66 Z" fill="#B98A52"/>
    <path d="M30 66 L36 62 L36 40 L30 46 Z" fill="${C.red}"/>
    <rect x="42" y="40" width="10" height="5" fill="${C.sky}" opacity="0.9" transform="rotate(-8 47 42)"/>`,

  decorate: () => `
    ${tree(30, 8, 0.72)}
    <path d="M20 30 Q30 10 52 22" fill="none" stroke-width="3.5" stroke-dasharray="1 6"/>
    <path d="M48 16 L55 23 L46 26" fill="none" stroke-width="3.5"/>
    <path d="M20 34 L20 44" fill="none" stroke-width="2.5"/>
    <circle cx="20" cy="54" r="11" fill="${C.blue}"/>
    <rect x="16" y="40" width="8" height="6" rx="1.5" fill="${C.gold}"/>
    <path d="M15 51 Q16 47 20 46" fill="none" stroke="${C.white}" stroke-width="2.5"/>`,

  bake: () => `
    <path d="M36 18 Q32 12 36 6 M50 18 Q46 12 50 6 M64 18 Q60 12 64 6" fill="none" stroke="${C.gray}" stroke-width="3"/>
    <rect x="12" y="24" width="76" height="68" rx="6" fill="${C.light}"/>
    <rect x="12" y="24" width="76" height="15" rx="6" fill="${C.gray}"/>
    ${dot(24, 31.5, 4, C.white)}${dot(36, 31.5, 4, C.white)}
    <rect x="58" y="28" width="22" height="7" rx="2" fill="${K}"/>
    <rect x="30" y="44" width="40" height="4" rx="2" fill="${C.gray}"/>
    <rect x="22" y="52" width="56" height="32" rx="4" fill="#FFB35C"/>
    <path d="M26 76 H74" fill="none" stroke-width="2.5"/>
    ${[34, 50, 66].map((x) => `<ellipse cx="${x}" cy="71" rx="6" ry="4" fill="${C.cookie}" stroke-width="2"/>`).join('')}`,

  sing: () => `${face({ cx: 40, cy: 56, r: 32 },
    `<path d="M26 50 Q31 45 36 50 M44 50 Q49 45 54 50" fill="none" stroke-width="3.5"/>
     <ellipse cx="40" cy="69" rx="8" ry="10" fill="#7A2E2E"/>`)}
    <path d="M74 38 V14 L90 10 V32" fill="none" stroke-width="4"/>
    <ellipse cx="70" cy="38" rx="6" ry="4.5" fill="${K}"/>
    <ellipse cx="86" cy="32" rx="6" ry="4.5" fill="${K}"/>
    <path d="M86 70 V52 L94 56" fill="none" stroke-width="3.5"/>
    <ellipse cx="82" cy="70" rx="5" ry="4" fill="${K}"/>`,

  give: () => `
    <path d="M18 18 Q50 0 82 18" fill="none" stroke-width="4"/>
    <path d="M74 10 L83 18 L72 22" fill="none" stroke-width="4"/>
    ${present(20, 20, 0.6)}
    <rect x="24" y="80" width="18" height="20" rx="3" fill="${C.green}"/>
    <rect x="58" y="80" width="18" height="20" rx="3" fill="${C.green}"/>
    <ellipse cx="38" cy="75" rx="13" ry="7" fill="${C.skin}"/>
    <ellipse cx="62" cy="75" rx="13" ry="7" fill="${C.skin}"/>`,

  eat: () => `${face({ cx: 40, cy: 52, r: 32 },
    `${dot(30, 44, 3.4)}${dot(50, 44, 3.4)}
     <path d="M30 62 Q40 76 52 62 Z" fill="#7A2E2E"/>`)}
    <circle cx="76" cy="66" r="16" fill="${C.cookie}"/>
    ${dot(71, 61, 2.4, C.choc)}${dot(81, 66, 2.4, C.choc)}${dot(74, 73, 2.2, C.choc)}
    ${dot(58, 82, 1.8, C.cookie)}${dot(62, 88, 1.6, C.cookie)}`,

  drink: () => `${face({ cx: 38, cy: 52, r: 32 },
    `${dot(28, 44, 3.4)}${dot(48, 44, 3.4)}
     <ellipse cx="54" cy="64" rx="4" ry="5" fill="#7A2E2E"/>`)}
    ${mug(30, 22, 0.62, -28)}`,

  look: () => `
    <path d="M14 22 Q30 10 46 20 M54 20 Q70 10 86 22" fill="none" stroke-width="4"/>
    ${bigEye(30, 52)}${bigEye(70, 52)}
    <path d="M10 84 Q50 98 90 84" fill="none" stroke="${C.gray}" stroke-width="3" stroke-dasharray="2 7"/>`,

  play: () => `
    <rect x="12" y="56" width="34" height="34" rx="4" fill="${C.red}"/>
    ${star(29, 74, 10, C.white)}
    <rect x="54" y="56" width="34" height="34" rx="4" fill="${C.blue}"/>
    <circle cx="71" cy="73" r="9" fill="${C.white}"/>
    <rect x="33" y="16" width="34" height="34" rx="4" fill="${C.green}" transform="rotate(8 50 33)"/>
    <path d="M50 22 L60 40 H40 Z" fill="${C.white}" transform="rotate(8 50 33)"/>`,

  // ---------- Feelings ----------
  happy: () => face({}, `${dot(38, 44, 4)}${dot(62, 44, 4)}
    <path d="M33 60 Q50 77 67 60" fill="none" stroke-width="4"/>`),

  excited: () => `${face({}, `
    <path d="M30 34 Q37 28 44 33 M56 33 Q63 28 70 34" fill="none" stroke-width="3.5"/>
    ${dot(38, 44, 4.6)}${dot(62, 44, 4.6)}${dot(39.5, 42.5, 1.5, C.white)}${dot(63.5, 42.5, 1.5, C.white)}
    <path d="M31 57 Q50 86 69 57 Z" fill="#7A2E2E"/>
    <path d="M40 72 Q50 66 60 72 Q50 80 40 72 Z" fill="${C.pink}" stroke="none"/>`)}
    ${sparkle(10, 14, 7)}${sparkle(90, 14, 7)}${sparkle(92, 86, 6)}${sparkle(8, 86, 6)}`,

  sad: () => face({ cheeks: false }, `
    <path d="M29 37 L42 31 M58 31 L71 37" fill="none" stroke-width="3.5"/>
    ${dot(38, 45, 4)}${dot(62, 45, 4)}
    <path d="M36 70 Q50 58 64 70" fill="none" stroke-width="4"/>
    <path d="M64 52 Q58 62 64 64 Q70 62 64 52 Z" fill="${C.sky}"/>`),

  mad: () => face({ cheeks: false }, `
    <path d="M28 33 L44 40 M56 40 L72 33" fill="none" stroke-width="4.5"/>
    ${dot(38, 46, 4)}${dot(62, 46, 4)}
    <path d="M36 70 Q50 60 64 70" fill="none" stroke-width="4.5"/>
    <path d="M12 24 L20 30 M8 36 L17 38 M88 24 L80 30 M92 36 L83 38" fill="none" stroke="${C.red}" stroke-width="3.5"/>`),

  scared: () => `${face({ cheeks: false }, `
    <path d="M30 30 Q37 25 44 30 M56 30 Q63 25 70 30" fill="none" stroke-width="3.5"/>
    <circle cx="38" cy="44" r="7.5" fill="${C.white}"/><circle cx="62" cy="44" r="7.5" fill="${C.white}"/>
    ${dot(38, 45, 2.6)}${dot(62, 45, 2.6)}
    <path d="M34 68 Q38 63 42 68 Q46 73 50 68 Q54 63 58 68 Q62 73 66 68" fill="none" stroke-width="3.5"/>
    <path d="M77 30 Q72 38 77 41 Q82 38 77 30 Z" fill="${C.sky}"/>`)}
    <path d="M6 44 Q2 52 6 60 M94 44 Q98 52 94 60" fill="none" stroke-width="3"/>`,

  surprised: () => face({}, `
    <path d="M29 30 Q37 22 45 29 M55 29 Q63 22 71 30" fill="none" stroke-width="3.5"/>
    <circle cx="38" cy="44" r="5" fill="${K}"/><circle cx="62" cy="44" r="5" fill="${K}"/>
    ${dot(39.5, 42.5, 1.5, C.white)}${dot(63.5, 42.5, 1.5, C.white)}
    <ellipse cx="50" cy="67" rx="7" ry="9" fill="#7A2E2E"/>`),

  tired: () => `${face({ cheeks: false }, `
    <path d="M30 46 H46 M54 46 H70" fill="none" stroke-width="4"/>
    <path d="M32 46 Q38 52 44 46 M56 46 Q62 52 68 46" fill="${K}" stroke-width="2"/>
    <ellipse cx="50" cy="68" rx="6" ry="5" fill="#7A2E2E"/>`)}
    <text x="72" y="26" font-family="Fredoka" font-weight="700" font-size="20" fill="${C.blue}" stroke="none">z</text>
    <text x="82" y="14" font-family="Fredoka" font-weight="700" font-size="14" fill="${C.blue}" stroke="none">z</text>`,

  calm: () => `${face({}, `
    <path d="M31 45 Q38 51 45 45 M55 45 Q62 51 69 45" fill="none" stroke-width="3.5"/>
    <path d="M39 63 Q50 71 61 63" fill="none" stroke-width="3.5"/>`)}
    <path d="M4 40 Q8 36 12 40 Q16 44 20 40 M80 40 Q84 36 88 40 Q92 44 96 40 M4 54 Q8 50 12 54 Q16 58 20 54 M80 54 Q84 50 88 54 Q92 58 96 54" fill="none" stroke="${C.teal}" stroke-width="3"/>`,

  overwhelmed: () => `
    <path d="M20 14 Q26 4 34 12 Q40 2 48 10 Q56 2 62 12 Q70 4 76 14 Q86 14 80 22" fill="none" stroke="${C.purple}" stroke-width="3.5"/>
    ${face({ cy: 56, r: 34, cheeks: false }, `
    <path d="M33 48 m-6 0 a6 6 0 1 1 6 6 a3.5 3.5 0 1 1 -3.5 -3.5" fill="none" stroke-width="3"/>
    <path d="M67 48 m-6 0 a6 6 0 1 1 6 6 a3.5 3.5 0 1 1 -3.5 -3.5" fill="none" stroke-width="3"/>
    <path d="M36 72 Q40 67 44 72 Q48 77 52 72 Q56 67 60 72 Q62 75 64 72" fill="none" stroke-width="3.5"/>`)}`,

  'too loud': () => `
    <path d="M10 20 Q2 30 6 42 M18 12 Q6 26 12 42 M90 20 Q98 30 94 42 M82 12 Q94 26 88 42" fill="none" stroke="${C.red}" stroke-width="3.5"/>
    ${face({ cy: 56, r: 30, cheeks: false }, `
    <path d="M36 46 L44 50 L36 54 M64 46 L56 50 L64 54" fill="none" stroke-width="3.5"/>
    <path d="M40 68 Q45 64 50 68 Q55 72 60 68" fill="none" stroke-width="3.5"/>`)}
    <ellipse cx="20" cy="56" rx="9" ry="14" fill="${C.face}"/>
    <ellipse cx="80" cy="56" rx="9" ry="14" fill="${C.face}"/>`,

  'too bright': () => {
    let rays = '';
    for (let i = 0; i < 12; i++) {
      const a = (i * Math.PI) / 6;
      rays += `M${(50 + 30 * Math.cos(a)).toFixed(1)} ${(46 + 30 * Math.sin(a)).toFixed(1)} L${(50 + 44 * Math.cos(a)).toFixed(1)} ${(46 + 44 * Math.sin(a)).toFixed(1)} `;
    }
    return `<path d="${rays}" fill="none" stroke="${C.gold}" stroke-width="5"/>
      <rect x="40" y="66" width="20" height="16" rx="3" fill="${C.gray}"/>
      <path d="M40 72 H60 M40 77 H60" fill="none" stroke-width="2"/>
      <path d="M50 22 Q70 22 70 42 Q70 54 60 62 L60 68 H40 L40 62 Q30 54 30 42 Q30 22 50 22 Z" fill="#FFF3A8"/>
      <path d="M40 38 L46 42 L40 46 M60 38 L54 42 L60 46" fill="none" stroke-width="3"/>
      <path d="M44 54 Q50 50 56 54" fill="none" stroke-width="3"/>`;
  },

  cold: () => `${face({ cy: 56, r: 33, cheeks: false }, `
    ${dot(38, 52, 4)}${dot(62, 52, 4)}
    <rect x="36" y="64" width="28" height="11" rx="3" fill="${C.white}"/>
    <path d="M43 64 V75 M50 64 V75 M57 64 V75 M36 69.5 H64" fill="none" stroke-width="2"/>`)}
    <path d="M17 40 Q17 12 50 12 Q83 12 83 40 Z" fill="${C.blue}"/>
    <rect x="14" y="34" width="72" height="11" rx="5" fill="${C.sky}"/>
    <circle cx="50" cy="10" r="7" fill="${C.white}"/>
    <path d="M6 54 L10 58 L6 62 L10 66 M94 54 L90 58 L94 62 L90 66" fill="none" stroke-width="3"/>`,

  // ---------- Social & needs ----------
  yes: () => `<circle cx="50" cy="50" r="38" fill="${C.green}"/>
    <path d="M30 51 L44 65 L71 36" fill="none" stroke="${C.white}" stroke-width="10"/>`,

  no: () => `<circle cx="50" cy="50" r="38" fill="${C.red}"/>
    <path d="M34 34 L66 66 M66 34 L34 66" fill="none" stroke="${C.white}" stroke-width="10"/>`,

  help: () => `
    <path d="M14 30 Q8 40 14 50 M86 30 Q92 40 86 50" fill="none" stroke-width="3.5"/>
    <rect x="35" y="74" width="30" height="22" rx="3" fill="${C.blue}"/>
    ${hand({ x: 22, y: 6, s: 1.3 })}`,

  'break, please': () => `<circle cx="50" cy="50" r="38" fill="${C.blue}"/>
    <rect x="35" y="30" width="10" height="40" rx="3" fill="${C.white}"/>
    <rect x="55" y="30" width="10" height="40" rx="3" fill="${C.white}"/>`,

  'all done': () => `
    <path d="M12 22 Q22 8 34 14 M88 22 Q78 8 66 14" fill="none" stroke-width="3.5"/>
    <path d="M30 14 L35 15 L33 20 M70 14 L65 15 L67 20" fill="none" stroke-width="3.5"/>
    ${hand({ x: 9, y: 30, s: 0.85, r: -18 })}
    ${hand({ x: 53, y: 30, s: 0.85, r: 18, flip: true })}`,

  more: () => `<circle cx="50" cy="50" r="38" fill="${C.teal}"/>
    <path d="M50 28 V72 M28 50 H72" fill="none" stroke="${C.white}" stroke-width="11"/>`,

  wait: () => `
    <path d="M30 20 H70 Q70 40 54 50 Q70 60 70 80 H30 Q30 60 46 50 Q30 40 30 20 Z" fill="#EAF6FD" stroke="none"/>
    <path d="M37 33 H63 Q59 42 52 47 H48 Q41 42 37 33 Z" fill="${C.gold}" stroke="none"/>
    <path d="M33 79 Q39 64 50 62 Q61 64 67 79 Z" fill="${C.gold}" stroke="none"/>
    <path d="M50 48 V63" fill="none" stroke="${C.gold}" stroke-width="2.5"/>
    <path d="M30 20 H70 Q70 40 54 50 Q70 60 70 80 H30 Q30 60 46 50 Q30 40 30 20 Z" fill="none"/>
    <rect x="22" y="12" width="56" height="9" rx="3" fill="${C.brown}"/>
    <rect x="22" y="79" width="56" height="9" rx="3" fill="${C.brown}"/>`,

  'my turn': () => `${kid({ tx: -12, s: 1 })}
    <path d="M96 70 H74 M80 62 L72 70 L80 78" fill="none" stroke="${K}" stroke-width="11"/>
    <path d="M96 70 H74 M80 62 L72 70 L80 78" fill="none" stroke="${C.gold}" stroke-width="5"/>`,

  headphones: () => `
    <path d="M22 62 Q22 16 50 16 Q78 16 78 62" fill="none" stroke="${K}" stroke-width="13"/>
    <path d="M22 62 Q22 16 50 16 Q78 16 78 62" fill="none" stroke="${C.purple}" stroke-width="7"/>
    <rect x="10" y="52" width="22" height="34" rx="9" fill="${C.purple}"/>
    <rect x="68" y="52" width="22" height="34" rx="9" fill="${C.purple}"/>
    <rect x="26" y="57" width="8" height="24" rx="4" fill="${C.gray}"/>
    <rect x="66" y="57" width="8" height="24" rx="4" fill="${C.gray}"/>`,

  quiet: () => `${face({ cy: 52 }, `
    ${dot(38, 42, 4)}${dot(62, 42, 4)}
    <ellipse cx="50" cy="66" rx="7" ry="4" fill="#7A2E2E"/>`)}
    <rect x="45" y="52" width="10" height="34" rx="5" fill="#F2C12E"/>
    <text x="70" y="18" font-family="Fredoka" font-weight="700" font-size="15" fill="${C.purple}" stroke="none">shh</text>`,

  hug: () => `${hugPair()}
    <path d="M50 18 Q44 10 40 15 Q37 20 50 28 Q63 20 60 15 Q56 10 50 18 Z" fill="${C.pink}"/>`,

  'no hug, please': () => `<g transform="translate(10 10) scale(0.8)">${hugPair()}</g>
    <circle cx="50" cy="50" r="41" fill="none" stroke="${K}" stroke-width="13"/>
    <circle cx="50" cy="50" r="41" fill="none" stroke="${C.red}" stroke-width="7"/>
    <path d="M21 21 L79 79" fill="none" stroke="${K}" stroke-width="13"/>
    <path d="M21 21 L79 79" fill="none" stroke="${C.red}" stroke-width="7"/>`,

  'high five': () => `
    ${hand({ x: 14, y: 36, s: 0.88, r: 24 })}
    ${hand({ x: 47, y: 36, s: 0.88, r: -24, flip: true })}
    <path d="M50 26 V10 M38 28 L30 16 M62 28 L70 16" fill="none" stroke="${C.gold}" stroke-width="4"/>`,

  'thank you': () => `
    <path d="M50 86 Q16 62 14 40 Q12 18 32 16 Q44 15 50 28 Q56 15 68 16 Q88 18 86 40 Q84 62 50 86 Z" fill="${C.pink}"/>
    <path d="M28 30 Q24 36 26 44" fill="none" stroke="${C.white}" stroke-width="4"/>
    ${sparkle(88, 12, 7)}${sparkle(12, 84, 6)}${sparkle(90, 78, 5)}`,

  'Merry Christmas': () => `
    <path d="M16 12 H84 Q93 12 93 21 V68 Q93 77 84 77 H46 L28 93 L31 77 H16 Q7 77 7 68 V21 Q7 12 16 12 Z" fill="${C.white}"/>
    ${tree(25, 11, 0.5)}
    ${sparkle(20, 26, 5, C.red)}${sparkle(80, 26, 5, C.red)}`,

  bathroom: () => `
    <rect x="24" y="10" width="52" height="26" rx="4" fill="${C.white}"/>
    <rect x="58" y="16" width="12" height="5" rx="2" fill="${C.gray}"/>
    <path d="M20 48 Q22 72 38 77 L36 90 H64 L62 77 Q78 72 80 48 Z" fill="${C.white}"/>
    <ellipse cx="50" cy="48" rx="31" ry="10" fill="${C.white}"/>
    <ellipse cx="50" cy="48" rx="20" ry="5" fill="${C.sky}"/>
    <rect x="44" y="36" width="12" height="6" fill="${C.white}"/>`,

  'go home': () => `
    <rect x="64" y="16" width="11" height="22" fill="${C.redDark}"/>
    <rect x="20" y="48" width="60" height="42" fill="#F6E3C8"/>
    <path d="M10 52 L50 16 L90 52 Z" fill="${C.red}"/>
    <path d="M22 41 L50 16 L78 41 Q70 46 64 40 Q58 46 50 40 Q42 46 36 40 Q30 46 22 41 Z" fill="${C.white}"/>
    <rect x="42" y="62" width="17" height="28" rx="2" fill="${C.brown}"/>
    <circle cx="50.5" cy="70" r="5" fill="none" stroke="${C.green}" stroke-width="3"/>
    <rect x="25" y="58" width="12" height="12" fill="${C.sky}"/>
    <rect x="64" y="58" width="12" height="12" fill="${C.sky}"/>`,

  // ---------- Sentence starters ----------
  'I want': () => `${present(40, 2, 0.6)}
    ${hand({ x: 14, y: 38, s: 0.92, r: 60 })}`,

  'I see': () => `${bigEye(50, 50).replace('rx="16" ry="20"', 'rx="30" ry="22"')}
    <path d="M14 26 Q50 2 86 26" fill="none" stroke-width="4"/>`,

  'I feel': () => `${face({ cx: 34, cy: 46, r: 26, cheeks: false }, `${dot(26, 40, 3)}${dot(42, 40, 3)}
      <path d="M24 54 Q34 64 44 54" fill="none" stroke-width="3.5"/>`)}
    ${face({ cx: 66, cy: 60, r: 26, cheeks: false }, `${dot(58, 56, 3)}${dot(74, 56, 3)}
      <path d="M57 72 Q66 64 75 72" fill="none" stroke-width="3.5"/>`)}`,

  'I like': () => `
    <rect x="12" y="46" width="22" height="40" rx="3" fill="${C.blue}"/>
    ${merged(`<rect x="32" y="44" width="40" height="42" rx="10"/><rect x="34" y="12" width="16" height="44" rx="8"/>`, C.skin)}
    <path d="M52 56 H72 M52 66 H72 M52 76 H70" fill="none" stroke-width="3"/>
    ${sparkle(84, 20, 7)}`,

  'I need': () => `${kid({ tx: -14, ty: 4, s: 0.95 })}
    <path d="M66 8 H92 Q96 8 96 12 V40 Q96 44 92 44 H76 L68 52 L70 44 H66 Q62 44 62 40 V12 Q62 8 66 8 Z" fill="${C.white}"/>
    <path d="M79 16 V30" fill="none" stroke="${C.red}" stroke-width="5"/>
    ${dot(79, 37, 3, C.red)}`,
};

function svg(name, cls = '') {
  const fn = ICONS[name];
  if (!fn) throw new Error(`No icon: ${name}`);
  return `<svg class="${cls}" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg"><g stroke="${K}" stroke-width="3" stroke-linejoin="round" stroke-linecap="round">${fn()}</g></svg>`;
}

module.exports = { ICONS, svg };
