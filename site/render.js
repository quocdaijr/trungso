/*
 * Renders the five stages. A fortune-telling session is an ordered thing, so the
 * page is too: KHAI -> TƯỚNG -> PHÁN -> SỔ NỢ -> SỰ THẬT.
 *
 * Stage 4 is deliberately written in a different voice from stages 0-3. The joke
 * only works if the statistics stay cold while the fortune-teller shouts.
 */
'use strict';

const P = window.TrungsoPersonal;
const T = window.TrungsoTheme;
const THAY = window.TrungsoThay;

/** Self-hosted Twemoji. Explicit beats a runtime DOM walk: no reflow, no library. */
const tw = (cp, alt) =>
  `<img class="tw" src="./img/emoji/${cp}.svg" alt="${alt}" width="20" height="20" loading="lazy">`;

/**
 * What the fortune-teller says about a real hit count. The number drives the line, so
 * the joke can never contradict the data — and line 3 quotes the actual prize maths.
 */
const HIT_LINES = {
  0: 'Mong Tôn Hoa Sen thấy.',
  1: 'Một số. Thầy gọi đó là khởi đầu.',
  2: 'Hai số. Đại đại đi.',
  3: 'Ba số — giải ba! Được 30 nghìn trên 9,24 triệu đã đốt.',
  4: 'Bốn số. Thầy đã nói rồi mà!',
  5: 'Năm số. Thầy cũng sốc.',
  6: 'Sáu số. Con còn ngồi đây đọc cái này làm gì nữa?',
};
const hitLine = (h) => HIT_LINES[Math.min(h, 6)] ?? HIT_LINES[0];

const GENDERS = [['', 'không muốn nói'], ['nam', 'Nam'], ['nữ', 'Nữ']];
const CAN_PHUOC_ROI = -0.8;

const vnd = (n) => (n || 0).toLocaleString('vi-VN') + 'đ';
/** Billions, because 34.897.731.150 is a number nobody reads and "34,90 tỷ" is one they do. */
const billions = (n) => (n / 1e9).toLocaleString('vi-VN', {maximumFractionDigits: 2}) + ' tỷ';

/**
 * The jackpot line.
 *
 * Three things this must never do, in order of how badly they would break the page's
 * one promise:
 *   1. Call the figure the current jackpot. It is the pot as at a completed draw. When
 *      nobody won, the next draw's pot is that plus new ticket sales, so the only true
 *      word is "ít nhất".
 *   2. Show a figure from an older draw as though it described the newest one. If the
 *      prize fetch failed, `matches_latest_draw` is false and the draw id is stated.
 *   3. Put the number anywhere near a suggestion that it is winnable. It sits beside the
 *      cost of chasing it on purpose.
 */
function jackpotLine(game) {
  const p = game.prizes;
  if (!p) return null;

  const pot = billions(p.top_jackpot_vnd);
  const stale = !p.matches_latest_draw;
  let text;
  if (stale) {
    text = `Nồi kỳ #${p.draw_id}: <b>${pot}</b>. Kỳ #${p.latest_draw_id} thầy chưa đọc được.`;
  } else if (p.rolled_over) {
    text = `Nồi đang cộng dồn: <b>ít nhất ${pot}</b> — kỳ #${p.draw_id} không ai lấy.`;
  } else {
    text = `Kỳ #${p.draw_id} đã có người trúng <b>${pot}</b>. Nồi về mức sàn.`;
  }

  const node = el('p', 'note jackpot', text);
  // The ratio is arithmetic, not theatre, so it says itself plainly.
  const odds = Math.round(1 / (game.wheel.combinations / totalCombos(game)));
  node.appendChild(el('span', 'jackpot__odds',
    `bao 12 mua ${game.wheel.combinations} trên ${totalCombos(game).toLocaleString('vi-VN')} `
    + `tổ hợp — 1 phần ${odds.toLocaleString('vi-VN')}`));
  return node;
}

/**
 * Six numbers, for the ticket most people actually buy.
 *
 * "Cách chơi: Cơ bản" in the Vietlott app is one row of six at 10,000d. Bao 12 is a real
 * product - Vietlott sells eleven bao sizes - but the page was handing over twelve numbers
 * for a six-number slip and leaving the reader to guess which six, which is not an answer.
 *
 * The split is the honest part. A typical field boosts three of the twelve and leaves the
 * other nine at exactly the same weight, so only the first `basic_reasoned` of these six
 * were chosen for a reason; the rest come out of a tie. Saying so is the point - a page
 * that presented all six as conviction would be inventing a ranking that does not exist.
 */
function basicPick(p) {
  if (!p.basic_pick || !p.basic_pick.length) return null;

  const block = el('div', 'basic');
  block.appendChild(el('p', 'basic__head', 'Chỉ mua một vé Cơ bản? Sáu số này.'));
  block.appendChild(ballRow(p.basic_pick, null));

  const reasoned = p.basic_reasoned || 0;
  const rest = p.basic_pick.length - reasoned;
  const ordered = (p.ranked || []).slice(0, p.basic_pick.length);
  const withReason = ordered.slice(0, reasoned).map(pad).join(' ');

  let text;
  if (reasoned === 0) {
    text = 'Kỳ này không số nào có lý do riêng. Cả sáu thầy bốc — thầy nói thẳng.';
  } else if (rest === 0) {
    text = 'Cả sáu số đều có lý do riêng. Hiếm lắm.';
  } else {
    text = `Có lý do riêng: <b>${withReason}</b>. `
      + `${rest} số còn lại cùng một mức, thầy bốc cho đủ sáu — thầy nói thẳng.`;
  }
  block.appendChild(el('p', 'basic__note', text));
  block.appendChild(el('p', 'note',
    `Vé Cơ bản = 6 số = <b>${vnd(10000)}</b>. Bao 12 ở trên = 924 tổ hợp = `
    + `<b>${vnd(9240000)}</b>. Cùng một bộ số, hai cách mua.`));
  return block;
}

/**
 * "So what do I get if it comes in tonight?"
 *
 * The next draw's estimated pot is not published anywhere a plain request can reach, but
 * this is - every figure here is derived from the real prize values and the real
 * combinatorics of the 924 tickets.
 *
 * Both halves go in the table or neither does. The payouts alone read as an argument FOR
 * playing: four hits already clears the stake. The probabilities alone read as an argument
 * that the prizes are stingy, which they are not. Only together do they say the true
 * thing, which is that the money is real and the odds are what take it back.
 */
function payoutTable(game) {
  const rows = game.payout_if_hit;
  if (!rows || !rows.length) return null;

  const table = el('table', 'stack-sm stack-sm--matrix');
  /* "tiền thưởng", not "thực nhận". Vietnam withholds 10% of whatever a prize exceeds
     10 million dong, so take-home is lower than the announced figure - Mega's four-hit
     row alone grosses 15.12 million. The column used to say "thực nhận" while showing the
     gross, which is the one thing this page must never do. Naming it gross costs nothing;
     computing net would mean guessing whether a bao ticket counts as one vé or 924 for
     tax, and that is not a number to invent. */
  const H = ['1 trên', 'tiền thưởng', 'lãi/lỗ (gộp)'];
  table.innerHTML = '<thead><tr><th>trúng</th>'
    + H.map((h) => `<th class="num">${h}</th>`).join('') + '</tr></thead><tbody>'
    + rows.map((r) => {
        const net = r.net_vnd;
        const sign = net > 0 ? '+' : '';
        const cls = net > 0 ? 'num win' : 'num';
        return `<tr><th>${r.hits} số</th>`
          + `<td class="num" data-label="${H[0]}">${r.one_in ? r.one_in.toLocaleString('vi-VN') : '—'}</td>`
          + `<td class="num" data-label="${H[1]}">${r.payout_vnd ? vnd(r.payout_vnd) : '—'}</td>`
          + `<td class="${cls}" data-label="${H[2]}">${sign}${vnd(net)}</td></tr>`;
      }).join('')
    + '</tbody>';
  return table;
}

/** C(pool, pick), computed rather than shipped, so it cannot disagree with the game spec. */
function totalCombos(game) {
  let n = 1;
  for (let i = 0; i < game.pick; i++) n = n * (game.pool - i) / (i + 1);
  return Math.round(n);
}
const pct = (n) => (n * 100).toFixed(2) + '%';
const pad = (n) => String(n).padStart(2, '0');

function el(tag, cls, html) {
  const node = document.createElement(tag);
  if (cls) node.className = cls;
  if (html != null) node.innerHTML = html;
  return node;
}

function stage(mark, title, lede) {
  const section = el('section', 'stage reveal');
  section.id = 'stage-' + mark;
  section.appendChild(el('div', 'stage__mark', mark));
  section.appendChild(el('h2', 'stage__title', title));
  if (lede) section.appendChild(el('p', 'stage__lede', lede));
  return section;
}

function ballRow(numbers, bonus) {
  const box = el('div', 'balls');
  (numbers || []).forEach((n, i) => {
    const ball = el('div', 'ball ball--pick ball--in', pad(n));
    ball.style.animationDelay = i * 40 + 'ms';
    box.appendChild(ball);
  });
  if (bonus != null) box.appendChild(el('div', 'ball ball--bonus', pad(bonus)));
  return box;
}

function sermonList(numbers, sermon) {
  const list = el('ul', 'sermon');
  numbers.forEach((n) => {
    const line = sermon[n] ?? sermon[String(n)];
    if (line) list.appendChild(el('li', null, `<b>${pad(n)}</b> — ${line}`));
  });
  return list;
}

/* ============================ 00 · KHAI ============================ */

function stageKhai(data, onSubmit) {
  const section = stage('00', `${tw('1fa84','🪄')} Khai báo`, 'Thầy cần ngày sinh. Chỉ ngày sinh thôi.');
  const block = el('div', 'block');
  const profile = P.loadProfile();

  block.appendChild(el('div', 'privacy', `<b>🔒 Riêng tư:</b> ${data.privacy}`));

  const form = el('form', 'khai');
  form.innerHTML = `
    <label>Ngày sinh (bắt buộc)
      <input type="date" name="birthDate" required min="1930-01-01" max="2035-12-31"
             value="${profile?.birthDate ?? ''}"></label>
    <label>Họ tên (tuỳ chọn — để tính số tên)
      <input type="text" name="name" placeholder="bỏ trống cũng được"
             value="${profile?.name ? profile.name.replace(/"/g, '&quot;') : ''}"></label>
    <label>Giới tính (tuỳ chọn — để tính sao chiếu mệnh)
      <select name="gender">${GENDERS.map(([v, t]) =>
        `<option value="${v}"${(profile?.gender ?? '') === v ? ' selected' : ''}>${t}</option>`
      ).join('')}</select></label>
    <button class="btn" type="submit">Thầy xem cho</button>
    <button class="btn btn--ghost" type="button" data-forget>Xoá sạch</button>`;
  block.appendChild(form);

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    const fd = new FormData(form);
    const birthDate = fd.get('birthDate');
    if (!birthDate) return;
    P.saveProfile({
      birthDate,
      name: (fd.get('name') || '').trim(),
      gender: fd.get('gender') || null,
    });
    onSubmit();
  });
  form.querySelector('[data-forget]').addEventListener('click', () => {
    P.clearAll();
    onSubmit();
  });

  if (!profile?.birthDate) {
    block.appendChild(el('p', 'hand',
      'Con điền ngày sinh vào đây. Thầy không hỏi số điện thoại — hỏi làm gì, thầy có bán số đâu.'));
  }
  section.appendChild(block);
  return section;
}

/* ============================ 01 · TƯỚNG ============================ */

function stageTuong(fortune, error) {
  const section = stage('01', `${tw('262f','☯')} Xem tướng`, 'Lá số dựng từ ngày sinh, tính ngay trong máy con.');
  const block = el('div', 'block');

  if (error) {
    block.appendChild(el('p', 'err', error));
    section.appendChild(block);
    return section;
  }
  if (!fortune) {
    block.appendChild(el('p', 'hand', 'Thầy không phải thần. Thầy cần ngày sinh — con quay lên trên đi.'));
    section.appendChild(block);
    return section;
  }

  const facts = [
    ['Năm âm lịch', `${fortune.canChi} (${fortune.lunarYear})`],
    ['Con giáp', fortune.animal],
    ['Mệnh', `${fortune.napAm} — ${fortune.element}`],
    ['Cung hoàng đạo', fortune.westernSign],
    ['Số chủ đạo', fortune.lifePath],
  ];
  if (fortune.nameNumber) facts.push(['Số tên', fortune.nameNumber]);
  if (fortune.guardianStar) facts.push(['Sao chiếu mệnh', fortune.guardianStar]);
  if (fortune.tamHop.length) facts.push(['Tam hợp', fortune.tamHop.join(', ')]);
  if (fortune.tuHanhXung.length) facts.push(['Tứ hành xung', fortune.tuHanhXung.join(', ')]);

  const grid = el('div', 'facts');
  facts.forEach(([k, v]) => grid.appendChild(
    el('div', 'fact', `<div class="fact__k">${k}</div><div class="fact__v">${v}</div>`)));
  block.appendChild(grid);
  block.appendChild(el('p', 'note',
    'Can chi, nạp âm và ngày Tết lấy từ bảng tra do Python sinh sẵn — trình duyệt không tự '
    + 'tính lại thuật toán âm lịch, nên hai bên không thể lệch nhau.'));
  section.appendChild(block);
  return section;
}

/* ============================ 02 · PHÁN ============================ */

function stagePhan(data, profile, fortune) {
  const section = stage('02', `${tw('1f52e','🔮')} Thầy phán`,
    'Mười hai số mỗi kỳ. Ghi trước giờ quay, không sửa được.');

  const intro = el('div', 'thay-row');
  intro.innerHTML = THAY.flip('idle', 'blink')
    + '<p class="thay__say">Cảm ơn vũ trụ đã cho con công việc. Nhưng thầy thấy con thích '
    + 'trúng số hơn.<br>Vũ trụ ơi, cho con trúng số đi. Thầy xin hộ nó một câu.</p>';
  section.appendChild(intro);

  data.games.forEach((game) => {
    const row = el('div', 'row');

    /* --- the house oracle --- */
    const house = el('div', 'block block--torn');
    house.appendChild(el('h3', 'block__head', `${game.display} · oracle nhà cái`));
    if (game.pending_prophecy) {
      const p = game.pending_prophecy;
      house.appendChild(el('div', 'note',
        `Kỳ #${p.draw_id} · quay ${p.draw_date} lúc 18h00 · oracle v${p.oracle_version}`));
      house.appendChild(ballRow(p.numbers, null));
      house.appendChild(el('p', 'note',
        `bao 12 = ${game.wheel.combinations} tổ hợp = <b>${vnd(game.wheel.cost_vnd)}</b>`));
      const basic = basicPick(p);
      if (basic) house.appendChild(basic);
      const jackpot = jackpotLine(game);
      if (jackpot) house.appendChild(jackpot);
      const payout = payoutTable(game);
      if (payout) {
        house.appendChild(el('p', 'note', 'Hôm nay trúng thì thực nhận bao nhiêu:'));
        house.appendChild(payout);
        house.appendChild(el('p', 'note',
          'Số gộp, chưa trừ thuế. Trúng thưởng bị 10% trên phần vượt 10 triệu, '
          + 'nên trên 10 triệu là về tay ít hơn con số ghi ở đây.'));
        const six = game.payout_if_hit[game.payout_if_hit.length - 1];
        if (!six.uses_live_jackpot) {
          house.appendChild(el('p', 'note',
            'Hàng cuối tính theo mức sàn — kỳ này thầy chưa đọc được nồi.'));
        }
        if (game.has_bonus) {
          house.appendChild(el('p', 'note',
            'Bảng này không tính số phụ. Trúng 5 số mà có cả số phụ thì ăn Jackpot 2.'));
        }
      }
      house.appendChild(sermonList(p.numbers, p.sermon));
    } else {
      house.appendChild(el('p', 'hand', 'Kỳ này thầy chưa phán. Con chờ.'));
    }
    row.appendChild(house);

    /* --- the personal oracle --- */
    const mine = el('div', 'block block--torn');
    mine.appendChild(el('h3', 'block__head', `${game.display} · số riêng của con`));
    if (!fortune) {
      mine.appendChild(el('p', 'hand', 'Chưa khai ngày sinh thì thầy lấy gì mà xem.'));
    } else if (!game.pending_prophecy) {
      mine.appendChild(el('p', 'hand', 'Chưa tới kỳ.'));
    } else {
      try {
        const pending = game.pending_prophecy;
        const pick = P.personalProphecy(profile, fortune, game, pending.draw_id, pending.draw_date);
        P.savePick(pick);
        mine.appendChild(el('div', 'note', `Kỳ #${pending.draw_id} · quay ${pending.draw_date}`));
        mine.appendChild(ballRow(pick.numbers, null));
        mine.appendChild(sermonList(pick.numbers, pick.sermon));
      } catch (e) {
        mine.appendChild(el('p', 'err', e.message));
      }
    }
    row.appendChild(mine);
    section.appendChild(row);
  });

  return section;
}

/* ============================ 03 · SỔ NỢ ============================ */

function stageSoNo(data, fortune) {
  const section = stage('03', `${tw('1f4c9','📉')} Sổ nợ`,
    'Thầy phán xong thì phải chịu chấm điểm. Tiền ở đây là tiền giấy.');

  data.games.forEach((game) => {
    const score = game.score;
    const block = el('div', 'block');
    block.appendChild(el('h3', 'block__head', game.display));

    if (!score.draws_scored) {
      block.appendChild(el('p', 'hand',
        'Chưa kỳ nào chấm được. Thầy tạm thời vô tội.'));
    } else {
      const delta = score.hits_per_draw_actual - score.hits_per_draw_expected;
      block.appendChild(el('div', 'kpi ' + (score.roi > 0 ? 'kpi--good' : 'kpi--bad'), pct(score.roi)));
      block.appendChild(el('div', 'note', 'ROI cộng dồn'));

      const table = el('table', 'stack-sm');
      table.innerHTML = `<tbody>
        <tr><th>kỳ đã chấm</th><td class="num">${score.draws_scored}</td></tr>
        <tr><th>trúng / kỳ</th><td class="num">${score.hits_per_draw_actual}</td></tr>
        <tr><th>ngẫu nhiên / kỳ</th><td class="num">${score.hits_per_draw_expected}</td></tr>
        <tr><th>chênh lệch</th><td class="num">${delta >= 0 ? '+' : ''}${delta.toFixed(3)}</td></tr>
        <tr><th>đã đốt (giấy)</th><td class="num">${vnd(score.paper_burned_vnd)}</td></tr>
        <tr><th>thắng (giấy)</th><td class="num">${vnd(score.paper_won_vnd)}</td></tr>
        <tr><th>ROI bỏ jackpot</th><td class="num">${pct(score.roi_excluding_jackpot)}</td></tr>
      </tbody>`;
      block.appendChild(table);

      /* The drawing is chosen by the real hit count, so it can never flatter the data. */
      if (score.best_draw) {
        const hits = score.best_draw.hits;
        const row = el('div', 'thay-row');
        row.innerHTML = THAY.still(THAY.poseForHits(hits))
          + `<div><p class="thay__say">Kỳ đỉnh nhất #${score.best_draw.draw_id}: `
          + `trúng ${hits}/12 số.<br>${hitLine(hits)}</p>`
          + (hits >= 5
            ? '<figure class="print"><img src="./img/dong-ho-dai-cat.webp" alt="Tranh Đông Hồ Đại Cát" '
              + 'width="240" height="329" loading="lazy">'
              + '<figcaption>“Đại Cát” — vận may lớn. Tranh Đông Hồ, public domain.</figcaption></figure>'
            : '')
          + '</div>';
        block.appendChild(row);
      }

      if (score.roi_excluding_jackpot < CAN_PHUOC_ROI) {
        block.appendChild(el('div', 'verdict-stamp', 'CẠN PHƯỚC'));
        block.appendChild(el('p', 'hand',
          `ROI bỏ jackpot ${pct(score.roi_excluding_jackpot)}. Thầy nói thật đấy, lần này không đùa.`));
      }
      if (score.jackpot_hits && score.roi > 0) {
        block.appendChild(el('div', 'disclaim',
          `ROI dương chỉ nhờ ${score.jackpot_hits} kỳ trúng jackpot. Bỏ jackpot ra còn `
          + `${pct(score.roi_excluding_jackpot)}, và tỉ lệ trúng ${score.hits_per_draw_actual} `
          + `vẫn đúng bằng mức ngẫu nhiên ${score.hits_per_draw_expected}. `
          + `Một cú may che hết phần còn lại — đó là cách mọi "hệ thống" tự lừa mình.`));
      }
    }

    /* head-to-head, only meaningful once the visitor has picks of their own */
    if (fortune) {
      const mine = P.scorePicks(P.loadPicks(),
        { key: game.key, pool: game.pool, pick: game.pick }, game.recent);
      /* Two measures across three contenders, so this one is a real matrix. It cannot
         just stack like the label/value tables: drop the header row on a narrow screen
         and each row becomes two bare numbers with nothing saying what they measure.
         Every cell carries its own column name instead, which the mobile rule reveals. */
      const versus = el('table', 'stack-sm stack-sm--matrix');
      const KY = 'kỳ đã chấm', TR = 'trúng / kỳ';
      versus.innerHTML = `<thead><tr><th></th><th class="num">${KY}</th>
        <th class="num">${TR}</th></tr></thead><tbody>
        <tr><th>Số tử vi của con</th>
            <td class="num" data-label="${KY}">${mine.scored}</td>
            <td class="num" data-label="${TR}">${mine.scored ? mine.hitsPerDraw.toFixed(3) : '—'}</td></tr>
        <tr><th>Oracle nhà cái</th>
            <td class="num" data-label="${KY}">${score.draws_scored}</td>
            <td class="num" data-label="${TR}">${score.draws_scored ? score.hits_per_draw_actual : '—'}</td></tr>
        <tr><th>Ngẫu nhiên thuần</th>
            <td class="num" data-label="${KY}">∞</td>
            <td class="num" data-label="${TR}">${mine.expected.toFixed(3)}</td></tr>
      </tbody>`;
      block.appendChild(el('p', 'note', 'So kè'));
      block.appendChild(versus);
    }

    block.appendChild(el('p', 'note',
      `ROI kỳ vọng lý thuyết: ${pct(game.wheel.expected_roi)} · `
      + `bỏ jackpot: ${pct(game.wheel.expected_roi_excluding_jackpot)}`));
    section.appendChild(block);
  });

  return section;
}

/* ============================ 04 · SỰ THẬT ============================
 * From here down the fortune-teller is not allowed to speak. */

function chiSquareTable(chi, label) {
  const block = el('div', 'block');
  block.appendChild(el('h3', 'block__head', label));
  const table = el('table', 'stack-sm');
  table.innerHTML = `<tbody>
    <tr><th>lượt số quan sát</th><td class="num">${chi.observations.toLocaleString('vi-VN')}</td></tr>
    <tr><th>chi-square</th><td class="num">${chi.statistic}</td></tr>
    <tr><th>bậc tự do</th><td class="num">${chi.degrees_of_freedom}</td></tr>
    <tr><th>p-value</th><td class="num">${chi.p_value}</td></tr>
  </tbody>`;
  block.appendChild(table);
  block.appendChild(el('p', 'note', chi.verdict));
  return block;
}

/**
 * Tappable heatmap. `title` tooltips do not exist on touch, so every cell is a button
 * that writes into a live readout — otherwise the frequency data is desktop-only.
 */
function heatmap(freq, pool, offset = 1) {
  const box = el('div');
  const matrix = pool === 100; // 00..99 is a natural 10x10 grid, easier to read than auto-fill
  const wrap = el('div', 'heat ' + (matrix ? 'heat--matrix' : 'heat--pool'));
  wrap.setAttribute('role', 'group');
  wrap.setAttribute('aria-label', 'Tần suất từng số, bấm để xem');

  const values = Object.values(freq).map(Number);
  const lo = Math.min(...values);
  const hi = Math.max(...values);
  const readout = el('p', 'heat__readout', 'Bấm một số để xem tần suất.');
  readout.setAttribute('role', 'status');
  readout.setAttribute('aria-live', 'polite');

  for (let i = 0; i < pool; i++) {
    const n = i + offset;
    const count = Number(freq[String(n)] ?? freq[pad(n)] ?? 0);
    // Deliberately gentle: a strong gradient would imply the spread means something.
    const t = hi === lo ? 0.5 : (count - lo) / (hi - lo);
    const cell = el('button', 'cell', pad(n));
    cell.type = 'button';
    /* The heat used to be the cell's own opacity, which faded the LABEL along with it -
       the coldest number measured 2.78:1 on veso, well under AA, and no contrast check
       caught it because opacity never touches the computed `color`. The tint moved to the
       background; the label now always reads at full ink. Custom property rather than an
       inline background so the pressed-state rule can still win. */
    // Unitless 0..1. How far that goes is --heat-max, which is per skin because the
    // safe ceiling is: 60% on veso, 37% on thantai. CSS does the multiply, so switching
    // theme re-tints every cell with no JS involved.
    cell.style.setProperty('--heat', t.toFixed(3));
    cell.setAttribute('aria-label', `Số ${pad(n)}, ra ${count} lần`);
    cell.setAttribute('aria-pressed', 'false');
    cell.addEventListener('click', () => {
      wrap.querySelectorAll('[aria-pressed="true"]')
        .forEach((b) => b.setAttribute('aria-pressed', 'false'));
      cell.setAttribute('aria-pressed', 'true');
      readout.textContent = `Số ${pad(n)} đã ra ${count} lần.`;
    });
    wrap.appendChild(cell);
  }
  box.appendChild(wrap);
  box.appendChild(readout);
  return box;
}

function stageSuThat(data) {
  const section = stage('04', `${tw('1f4ca','📊')} Sự thật`,
    'Phần này thầy không được nói. Đây là số liệu, và số liệu không nể ai.');

  data.games.forEach((game) => {
    const row = el('div', 'row');
    if (game.chi_square) {
      row.appendChild(chiSquareTable(game.chi_square, `${game.display} · ${game.draw_count} kỳ`));
    }
    const heat = el('div', 'block');
    heat.appendChild(el('h3', 'block__head', `Tần suất · ${game.display}`));
    heat.appendChild(heatmap(game.frequency, game.pool));
    heat.appendChild(el('p', 'note',
      'Đậm hơn = ra nhiều hơn. Trông như có quy luật, nhưng chi-square bên cạnh nói đó là nhiễu thuần.'));
    row.appendChild(heat);
    section.appendChild(row);

    const recent = el('div', 'block');
    recent.appendChild(el('h3', 'block__head', `Các kỳ gần đây · ${game.display}`));
    const scroll = el('div', 'scroll');
    const table = el('table');
    table.innerHTML = '<thead><tr><th>kỳ</th><th>ngày</th><th>số</th>'
      + (game.has_bonus ? '<th>phụ</th>' : '') + '<th>nguồn</th></tr></thead>';
    const body = el('tbody');
    [...game.recent].reverse().forEach((d) => {
      body.innerHTML += `<tr><td>#${d.draw_id}</td><td>${d.date}</td>`
        + `<td>${d.main.map(pad).join(' ')}</td>`
        + (game.has_bonus ? `<td>${d.bonus != null ? pad(d.bonus) : '—'}</td>` : '')
        + `<td>${d.source}</td></tr>`;
    });
    table.appendChild(body);
    scroll.appendChild(table);
    recent.appendChild(scroll);
    section.appendChild(recent);
  });

  if (data.xsmb) {
    const x = data.xsmb;
    const row = el('div', 'row');
    row.appendChild(chiSquareTable(x.chi_square,
      `XSMB Miền Bắc · ${x.draw_count.toLocaleString('vi-VN')} kỳ · ${x.first_date} → ${x.last_date}`));
    const heat = el('div', 'block');
    heat.appendChild(el('h3', 'block__head', 'Tần suất 00–99'));
    heat.appendChild(heatmap(x.frequency, 100, 0));
    heat.appendChild(el('p', 'note',
      `21 năm, ${x.chi_square.observations.toLocaleString('vi-VN')} lượt số. Vẫn đều tăm tắp.`));
    row.appendChild(heat);
    section.appendChild(row);
  }

  section.appendChild(el('div', 'disclaim', data.disclaimer));
  return section;
}

/* ============================ boot ============================ */

function render(data) {
  const app = document.getElementById('app');
  app.innerHTML = '';

  const profile = P.loadProfile();
  let fortune = null;
  let fortuneError = null;
  if (profile?.birthDate) {
    try {
      fortune = P.readFortune(profile, data.astrology, new Date().toISOString().slice(0, 10));
    } catch (e) {
      fortuneError = e.message;
    }
  }

  app.appendChild(stageKhai(data, () => render(data)));
  app.appendChild(stageTuong(fortune, fortuneError));
  app.appendChild(stagePhan(data, profile, fortune));
  app.appendChild(stageSoNo(data, fortune));
  app.appendChild(stageSuThat(data));

  observeReveals();
  observeFlips();
}

function observeReveals() {
  const targets = document.querySelectorAll('.reveal');
  if (!('IntersectionObserver' in window)) {
    targets.forEach((t) => t.classList.add('is-in'));
    return;
  }
  const io = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-in');
        io.unobserve(entry.target);
      }
    });
  }, { rootMargin: '0px 0px -8% 0px' });
  targets.forEach((t) => io.observe(t));
}

/**
 * Pause the looping figure whenever it scrolls out of view.
 *
 * This is the condition attached to having a looping animation at all: one that only
 * runs while somebody is looking costs almost nothing, one that never stops costs
 * battery on the phones this page was just tuned for.
 */
function observeFlips() {
  const flips = document.querySelectorAll('.thay--flip');
  if (!('IntersectionObserver' in window)) return;
  const io = new IntersectionObserver((entries) => {
    entries.forEach((e) => e.target.classList.toggle('is-paused', !e.isIntersecting));
  }, { threshold: 0 });
  flips.forEach((f) => { f.classList.add('is-paused'); io.observe(f); });
}

T.initThemeControls();

fetch('./data.json', { cache: 'no-store' })
  .then((r) => { if (!r.ok) throw new Error('HTTP ' + r.status); return r.json(); })
  .then(render)
  .catch((e) => {
    document.getElementById('app').innerHTML =
      `<div class="block"><p class="err">Không tải được <code>data.json</code> (${e.message}). `
      + 'Chạy <code>uv run trungso site</code> rồi serve thư mục này.</p></div>';
  });
