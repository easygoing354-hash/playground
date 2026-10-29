// Builds the printable TPT product:
//   dist/Christmas-Communication-Labels.pdf  (US Letter, print-ready)
//   dist/thumbnail.png                        (square TPT cover thumbnail)
// Usage: node build.js
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');
const { svg } = require('./icons');

const OUT = path.join(__dirname, 'dist');
const TITLE = 'Christmas Communication Labels';

const CATS = {
  starter: { name: 'Sentence Starters', color: '#E8B800', key: 'I / sentence starters',
    items: ['I want', 'I see', 'I like', 'I feel', 'I need'] },
  noun: { name: 'Christmas Things', color: '#F28C28', key: 'Things (nouns)',
    items: ['tree', 'santa', 'present', 'stocking', 'star', 'ornament', 'candy cane', 'snowman', 'reindeer', 'cookie',
      'gingerbread', 'lights', 'wreath', 'bell', 'elf', 'sleigh', 'hot cocoa', 'snow', 'mittens', 'milk'] },
  verb: { name: 'Christmas Actions', color: '#2F9E5A', key: 'Actions (verbs)',
    items: ['open', 'wrap', 'decorate', 'bake', 'sing', 'give', 'eat', 'drink', 'look', 'play'] },
  feeling: { name: 'Feelings & Senses', color: '#3B82C4', key: 'Feelings & senses',
    items: ['happy', 'excited', 'calm', 'sad', 'mad', 'scared', 'surprised', 'tired', 'overwhelmed', 'too loud', 'too bright', 'cold'] },
  social: { name: 'Social Words & Needs', color: '#D9468F', key: 'Social words & needs',
    items: ['yes', 'no', 'help', 'break, please', 'all done', 'more', 'wait', 'my turn', 'headphones', 'quiet',
      'hug', 'no hug, please', 'high five', 'thank you', 'Merry Christmas', 'bathroom', 'go home'] },
};
const NEGATION = '#D93A3A';
const LABEL = { tree: 'Christmas tree', santa: 'Santa' };

const catOf = (id) => Object.keys(CATS).find((k) => CATS[k].items.includes(id));
const colorOf = (id) => (id === 'no' || id === 'no hug, please' ? NEGATION : CATS[catOf(id)].color);
const labelOf = (id) => LABEL[id] || id;
const ALL = Object.values(CATS).flatMap((c) => c.items);

const font = (file) => fs.readFileSync(path.join(__dirname, 'fonts', file)).toString('base64');
const FONTS = `
@font-face{font-family:Andika;font-weight:400;src:url(data:font/ttf;base64,${font('Andika-Regular.ttf')})}
@font-face{font-family:Andika;font-weight:700;src:url(data:font/ttf;base64,${font('Andika-Bold.ttf')})}
@font-face{font-family:Fredoka;font-weight:600;src:url(data:font/ttf;base64,${font('Fredoka-SemiBold.ttf')})}
@font-face{font-family:Fredoka;font-weight:700;src:url(data:font/ttf;base64,${font('Fredoka-Bold.ttf')})}`;

function sizeClass(text) {
  if (text.length > 13) return 'xl';
  if (text.length > 10) return 'l';
  return '';
}

function blank(color, extra = '') {
  return `<div class="card blank ${extra}" style="--c:${color}"><div class="ic"><div class="ph-photo">add a<br>picture</div></div><div class="word">&nbsp;</div></div>`;
}

function card(id, extra = '') {
  const t = labelOf(id);
  return `<div class="card ${extra}" style="--c:${colorOf(id)}"><div class="ic">${svg(id)}</div><div class="word ${sizeClass(t)}">${t}</div></div>`;
}

const chunk = (arr, n) => Array.from({ length: Math.ceil(arr.length / n) }, (_, i) => arr.slice(i * n, i * n + n));

let pageNo = 0;
function page(body, { cls = '', footer = true } = {}) {
  pageNo++;
  return `<section class="page ${cls}">${body}${footer ? `<div class="foot">${TITLE} &nbsp;•&nbsp; ${pageNo}</div>` : ''}</section>`;
}

function header(title, sub, color = '#C2363C') {
  return `<header class="ph"><h2 style="color:${color}">${title}</h2>${sub ? `<p>${sub}</p>` : ''}</header>`;
}

// ---------- Pages ----------
function coverBody() {
  const picks = ['tree', 'I want', 'present', 'happy', 'break, please', 'cookie', 'too loud', 'help', 'reindeer'];
  return `
  <div class="cv-snow">${svg('snow')}${svg('snow')}${svg('snow')}${svg('snow')}</div>
  <div class="cv-top">
    <div class="cv-kicker">Visual supports for autistic learners &amp; AAC users</div>
    <h1>Christmas<br>Communication Labels</h1>
    <div class="cv-sub">Picture cards • core boards • sentence strips</div>
  </div>
  <div class="cv-grid">${picks.map((p) => card(p)).join('')}</div>
  <div class="cv-badges">
    <div class="badge"><b>64</b><span>picture cards</span></div>
    <div class="badge"><b>2</b><span>card sizes</span></div>
    <div class="badge"><b>2</b><span>talk boards</span></div>
    <div class="badge"><b>6</b><span>color-coded groups</span></div>
  </div>
  <div class="cv-foot">Sentence strips • First / Then board • Calm choices • Printable &amp; low-prep</div>`;
}

function welcomePage() {
  const key = Object.values(CATS).map((c) => `<li><i style="background:${c.color}"></i>${c.key}</li>`).join('') +
    `<li><i style="background:${NEGATION}"></i>No / stop words</li>`;
  return page(`
  ${header('Welcome &amp; How to Use', 'Thank you for downloading! These cards give learners a clear, calm way to talk about the holidays.')}
  <div class="two">
    <div class="box">
      <h3>What's inside</h3>
      <ul class="list">
        <li><b>64 picture cards</b> in 5 groups: sentence starters, Christmas things, actions, feelings &amp; senses, and social words &amp; needs</li>
        <li><b>Large labels</b> (6 per page) for labeling the room, word walls and pocket charts</li>
        <li><b>Small cards</b> (20 per page) for PECS-style exchange, binders and lanyards</li>
        <li><b>2 communication boards</b>: Christmas Talk and Feelings &amp; Needs</li>
        <li><b>Sentence strips</b>: I want, I see, I like, I feel, I need</li>
        <li><b>First / Then board</b> and a <b>Calm Choices</b> board</li>
      </ul>
    </div>
    <div class="box">
      <h3>Color key</h3>
      <p class="small">Card borders follow a Fitzgerald-Key-style color code, so learners and AAC users can find words by color.</p>
      <ul class="key">${key}</ul>
    </div>
  </div>
  <div class="two">
    <div class="box">
      <h3>Prep</h3>
      <ol class="list">
        <li>Print on white cardstock (choose "actual size" / 100%).</li>
        <li>Laminate for durability.</li>
        <li>Cut on the dashed lines.</li>
        <li>Add hook-and-loop dots to cards, boards and strips.</li>
      </ol>
    </div>
    <div class="box">
      <h3>Ways to use</h3>
      <ul class="list">
        <li>Label real items: the tree, presents, the cocoa station.</li>
        <li>Pre-teach words before a party, concert or visit.</li>
        <li>Model on the boards as you talk: point, don't demand.</li>
        <li>Offer 2 to 3 choices for snacks, songs and activities.</li>
        <li>Send a set home for family gatherings.</li>
      </ul>
    </div>
  </div>
  <div class="box tip">
    <h3>Supporting autistic learners over the holidays</h3>
    <p>The holidays bring noise, lights, crowds and schedule changes. The <b>break, please</b>, <b>headphones</b>, <b>too loud</b>, <b>too bright</b> and <b>overwhelmed</b> cards give learners a way to say so. Always honor them when a learner uses them.
    The <b>no hug, please</b> and <b>high five</b> cards let a learner choose how to greet family. Keep cards in the same place every day, and model them often without requiring a response.</p>
  </div>`);
}

function largePages() {
  const out = [];
  for (const c of Object.values(CATS)) {
    const pages = chunk(c.items, 6);
    pages.forEach((items, i) => {
      const fill = Array(6 - items.length).fill(`<div class="cell">${blank(c.color)}</div>`).join('');
      const cells = items.map((id) => `<div class="cell">${card(id)}</div>`).join('') + fill;
      out.push(page(`${header(`Large Labels: ${c.name}`, pages.length > 1 ? `Page ${i + 1} of ${pages.length}` : '', c.color)}
        <div class="grid g-large">${cells}</div>`));
    });
  }
  return out.join('');
}

function smallPages() {
  const pages = chunk(ALL, 20);
  const colors = Object.values(CATS).map((c) => c.color);
  return pages.map((items, i) => {
    const fill = Array.from({ length: 20 - items.length }, (_, j) => `<div class="cell">${blank(colors[j % colors.length], 'sm')}</div>`).join('');
    const sub = items.length < 20 ? 'Blank cards: add a photo of a family member, a favorite toy or a class routine.' : 'For PECS-style exchange, binders &amp; lanyards.';
    return page(`${header('Small Picture Cards', `${sub} Page ${i + 1} of ${pages.length}`)}
    <div class="grid g-small">${items.map((id) => `<div class="cell">${card(id, 'sm')}</div>`).join('')}${fill}</div>`);
  }).join('');
}

function board(title, sub, ids, color, rowH = '1.22in') {
  return page(`${header(title, sub, color)}
    <div class="board" style="grid-auto-rows:${rowH}">${ids.map((id) => card(id, 'bd')).join('')}</div>`);
}

function stripsPage() {
  const strips = CATS.starter.items.map((id) => `
    <div class="strip" style="--c:${colorOf(id)}">
      ${card(id, 'st')}
      <div class="slot"><span></span></div><div class="slot"><span></span></div><div class="slot"><span></span></div>
    </div>`).join('');
  return page(`${header('Sentence Strips', 'Attach a picture card to each square, then read the sentence together.', CATS.starter.color)}${strips}`);
}

function firstThenPage() {
  const calm = ['break, please', 'headphones', 'quiet', 'help'];
  return page(`${header('First / Then &amp; Calm Choices', 'Show what comes next, and give a clear menu of ways to feel calm.', CATS.verb.color)}
    <div class="ft">
      <div class="ftbox"><div class="fthead" style="background:#2F9E5A">first</div><div class="ftslot"><span></span></div></div>
      <div class="ftarrow">➜</div>
      <div class="ftbox"><div class="fthead" style="background:#3B82C4">then</div><div class="ftslot"><span></span></div></div>
    </div>
    <div class="calm">
      <div class="calmhead">When Christmas feels like too much, I can:</div>
      <div class="calmgrid">${calm.map((id) => card(id, 'cm')).join('')}
        <div class="slot cmslot"><span></span></div><div class="slot cmslot"><span></span></div></div>
    </div>`);
}

function termsPage() {
  return page(`${header('Terms of Use &amp; Credits')}
    <div class="box">
      <h3>You may</h3>
      <ul class="list">
        <li>Use this resource with your own students, classroom, therapy caseload or children.</li>
        <li>Print as many copies as you need for the students you serve.</li>
        <li>Share with your students' families for use at home.</li>
      </ul>
    </div>
    <div class="box">
      <h3>Please do not</h3>
      <ul class="list">
        <li>Share, sell or give this file to other teachers or staff. Additional licenses can be purchased at a discount.</li>
        <li>Upload this file to a website, shared drive or school server where others can access it.</li>
        <li>Claim this work as your own or use the artwork to make products for sale.</li>
      </ul>
    </div>
    <div class="box">
      <h3>Credits</h3>
      <p>All illustrations are original artwork made for this resource. Fonts: Andika and Fredoka, used under the SIL Open Font License.</p>
    </div>
    <div class="box tip"><h3>Thank you!</h3>
      <p>If this resource helps your learners, a review on TPT means the world and earns you TPT credits toward future purchases.</p></div>`);
}

const CSS = `${FONTS}
*{box-sizing:border-box;margin:0;padding:0}
@page{size:8.5in 11in;margin:0}
html,body{background:#fff}
body{font-family:Andika,sans-serif;color:#2d2a32}
.page{width:8.5in;height:11in;position:relative;overflow:hidden;page-break-after:always;padding:.5in}
.foot{position:absolute;bottom:.22in;left:0;right:0;text-align:center;font-size:8pt;color:#9a9aa2}
.ph{text-align:center;margin-bottom:.16in}
.ph h2{font-family:Fredoka;font-weight:700;font-size:24pt;line-height:1.1}
.ph p{font-size:10.5pt;color:#5b5862;margin-top:.03in}

.card{--c:#999;background:#fff;border:.08in solid var(--c);border-radius:.22in;display:flex;flex-direction:column;align-items:center;justify-content:center;width:100%;height:100%;padding:.1in}
.card .ic{flex:1;min-height:0;width:100%;display:flex;align-items:center;justify-content:center}
.card .ic svg{height:100%;max-width:100%}
.card .word{font-weight:700;font-size:28pt;line-height:1.05;text-align:center;padding-top:.06in}
.card .word.l{font-size:23pt}.card .word.xl{font-size:20pt}

.grid{display:grid;border-top:1px dashed #b9b9c0;border-left:1px dashed #b9b9c0;margin:0 auto}
.cell{border-right:1px dashed #b9b9c0;border-bottom:1px dashed #b9b9c0;padding:.14in}
.g-large{grid-template-columns:repeat(2,3.75in);grid-template-rows:repeat(3,3.08in);width:7.5in}
.g-small{grid-template-columns:repeat(4,1.8in);grid-template-rows:repeat(5,1.8in);width:7.2in}
.g-small .cell{padding:.09in}
.card.sm{border-width:.05in;border-radius:.13in;padding:.06in}
.card.sm .word{font-size:12.5pt;padding-top:.02in}.card.sm .word.l{font-size:10.5pt}.card.sm .word.xl{font-size:9pt}

.board{display:grid;grid-template-columns:repeat(6,1fr);grid-auto-rows:1.22in;gap:.05in;width:7.5in;margin:0 auto;border:3px solid #2d2a32;border-radius:.15in;padding:.08in}
.card.bd{border-width:.045in;border-radius:.1in;padding:.04in}
.card.bd .word{font-size:11pt;padding-top:.01in}.card.bd .word.l{font-size:9.5pt}.card.bd .word.xl{font-size:8.2pt}

.strip{display:flex;gap:.12in;align-items:stretch;height:1.62in;margin:0 auto .14in;width:7.5in;border:2px dashed #b9b9c0;border-radius:.18in;padding:.1in;background:#fffdf5}
.card.st{width:1.42in;flex:none;border-width:.05in;border-radius:.13in;padding:.06in}
.card.st .word{font-size:13pt}
.slot{flex:1;border:.035in dashed #c8c8cf;border-radius:.13in;display:flex;align-items:center;justify-content:center;background:#fff}
.slot span{width:.42in;height:.42in;border-radius:50%;background:#eef0f3;border:1px solid #d9dce1}

.ft{display:flex;align-items:center;justify-content:center;gap:.15in;margin-top:.1in}
.ftbox{width:3.35in;border:3px solid #2d2a32;border-radius:.2in;overflow:hidden;background:#fff}
.fthead{color:#fff;font-family:Fredoka;font-weight:700;font-size:30pt;text-align:center;padding:.06in 0}
.ftslot{height:3in;display:flex;align-items:center;justify-content:center;border-top:3px solid #2d2a32}
.ftslot span{width:.5in;height:.5in;border-radius:50%;background:#eef0f3;border:1px solid #d9dce1}
.ftarrow{font-size:30pt;color:#2d2a32}
.calm{margin:.35in auto 0;width:7.5in;border:3px solid #2d2a32;border-radius:.2in;overflow:hidden}
.calmhead{background:#3B82C4;color:#fff;font-family:Fredoka;font-weight:600;font-size:17pt;text-align:center;padding:.08in}
.calmgrid{display:grid;grid-template-columns:repeat(3,1fr);grid-auto-rows:1.75in;gap:.12in;padding:.15in}
.card.cm{border-width:.05in;border-radius:.13in;padding:.06in}.card.cm .word{font-size:14pt}.card.cm .word.l{font-size:12pt}

.two{display:grid;grid-template-columns:1fr 1fr;gap:.18in;margin-bottom:.18in}
.box{border:2px solid #e3e0da;border-radius:.16in;padding:.16in .2in;margin-bottom:.18in;background:#fffdf8}
.two .box{margin-bottom:0}
.box h3{font-family:Fredoka;font-weight:600;font-size:15pt;color:#2F9E5A;margin-bottom:.06in}
.box p,.list{font-size:11.5pt;line-height:1.45}
.list{padding-left:.2in}.list li{margin-bottom:.03in}
.small{font-size:9.5pt!important;color:#5b5862;margin-bottom:.08in}
.key{list-style:none;font-size:10.5pt}
.key li{display:flex;align-items:center;gap:.1in;margin-bottom:.05in}
.key i{width:.32in;height:.22in;border-radius:.05in;display:inline-block}
.ph-photo{width:62%;height:86%;border:.03in dashed #c8c8cf;border-radius:.1in;display:flex;align-items:center;justify-content:center;text-align:center;color:#a5a5ad;font-size:12pt;line-height:1.15}
.card.sm .ph-photo{font-size:7.5pt}
.card.blank .word{width:75%;border-bottom:.02in solid #c8c8cf;margin-bottom:.06in}
.tip{background:#F1F7FD;border-color:#cfe2f5}.tip h3{color:#3B82C4}

/* cover */
.cover{background:#FFF8EE;padding:.45in .55in}
.cv-snow svg{position:absolute;width:1.1in;opacity:.35}
.cv-snow svg:nth-child(1){top:.25in;left:.3in}.cv-snow svg:nth-child(2){top:.5in;right:.35in;width:.8in}
.cv-snow svg:nth-child(3){top:2.4in;left:.15in;width:.6in}.cv-snow svg:nth-child(4){top:2.2in;right:.2in;width:.7in}
.cv-top{text-align:center;position:relative}
.cv-kicker{display:inline-block;background:#2F9E5A;color:#fff;font-weight:700;font-size:12pt;padding:.06in .22in;border-radius:1in}
.cover h1{font-family:Fredoka;font-weight:700;color:#C2363C;font-size:44pt;line-height:1.02;margin:.14in 0 .08in}
.cv-sub{font-size:15pt;font-weight:700;color:#2d2a32}
.cv-grid{display:grid;grid-template-columns:repeat(3,2.1in);grid-template-rows:repeat(3,2.1in);gap:.14in;justify-content:center;margin:.25in 0 .22in}
.cv-grid .card{box-shadow:0 .04in .1in rgba(0,0,0,.12)}
.cv-grid .card .word{font-size:17pt}.cv-grid .card .word.l{font-size:14pt}.cv-grid .card .word.xl{font-size:12pt}
.cv-badges{display:flex;justify-content:center;gap:.14in}
.badge{background:#fff;border:3px solid #C2363C;border-radius:.16in;width:1.62in;padding:.06in;text-align:center}
.badge b{display:block;font-family:Fredoka;font-size:24pt;color:#C2363C;line-height:1}
.badge span{font-size:10pt;font-weight:700}
.cv-foot{text-align:center;font-size:12pt;font-weight:700;color:#2F9E5A;margin-top:.16in}

/* square thumbnail */
.thumb{width:1500px;height:1500px;background:#FFF8EE;position:relative;overflow:hidden;padding:60px}
.thumb .cv-snow svg{width:150px}
.thumb .cover-inner{transform-origin:top left}
`;

function doc(body) {
  return `<!doctype html><html><head><meta charset="utf-8"><title>${TITLE}</title><style>${CSS}</style></head><body>${body}</body></html>`;
}

function buildPdfHtml() {
  pageNo = 0;
  const b1 = ['I want', 'I see', 'I like', 'yes', 'no', 'more', ...CATS.noun.items, ...CATS.verb.items];
  const social2 = CATS.social.items.filter((id) => !['yes', 'no', 'help', 'thank you', 'Merry Christmas'].includes(id));
  const b2 = ['I feel', 'I need', 'I want', 'yes', 'no', 'help', ...CATS.feeling.items, ...social2];
  return doc([
    page(coverBody(), { cls: 'cover', footer: false }),
    welcomePage(),
    largePages(),
    smallPages(),
    board('Christmas Talk Board', 'Point to the words as you talk. Learners can point, tap or hand you a card.', b1, '#C2363C'),
    board('Feelings &amp; Needs Board', 'Keep this board nearby at parties, concerts and family visits.', b2, CATS.feeling.color, '1.5in'),
    stripsPage(),
    firstThenPage(),
    termsPage(),
  ].join(''));
}

function buildThumbHtml() {
  // The 8.5x11 cover scaled into a square canvas with room for the badges.
  return doc(`<div class="thumb"><div class="cv-snow">${svg('snow')}${svg('snow')}${svg('snow')}${svg('snow')}</div>
    <div style="position:absolute;left:50%;top:40px;width:8.5in;transform:translateX(-50%) scale(1.75);transform-origin:top center">
      <div class="cv-top"><div class="cv-kicker">For autistic learners &amp; AAC users</div>
        <h1 class="h1" style="font-family:Fredoka;font-weight:700;color:#C2363C;font-size:40pt;line-height:1.02;margin:.12in 0 .06in">Christmas<br>Communication Labels</h1></div>
      <div class="cv-grid" style="grid-template-columns:repeat(4,1.6in);grid-template-rows:repeat(3,1.6in);gap:.12in;margin:.18in 0 .18in">
        ${['tree', 'I want', 'present', 'happy', 'break, please', 'too loud', 'cookie', 'help', 'santa', 'headphones', 'overwhelmed', 'reindeer'].map((p) => card(p)).join('')}</div>
      <div class="cv-badges">
        <div class="badge"><b>64</b><span>picture cards</span></div>
        <div class="badge"><b>2</b><span>card sizes</span></div>
        <div class="badge"><b>2</b><span>talk boards</span></div>
        <div class="badge"><b>+</b><span>strips &amp; first/then</span></div>
      </div>
    </div></div>`);
}

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch();
  const pg = await browser.newPage();

  await pg.setContent(buildPdfHtml(), { waitUntil: 'load' });
  await pg.evaluate(() => document.fonts.ready);
  await pg.pdf({ path: path.join(OUT, 'Christmas-Communication-Labels.pdf'), preferCSSPageSize: true, printBackground: true });

  const th = await browser.newPage({ viewport: { width: 1500, height: 1500 } });
  await th.setContent(buildThumbHtml(), { waitUntil: 'load' });
  await th.evaluate(() => document.fonts.ready);
  await th.screenshot({ path: path.join(OUT, 'thumbnail.png') });

  await browser.close();
  console.log(`Built ${pageNo} pages -> dist/`);
})();
