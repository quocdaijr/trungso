/*
 * First-visit warning gate.
 *
 * The site hands strangers lottery numbers. Before anyone sees one, they read the
 * sentence that matters: this cannot predict anything. The acknowledgement is stored
 * locally - there is no server to record it on, and recording it is not the point.
 *
 * The point is that nobody reaches the numbers without passing the sentence.
 */
'use strict';

const ACK_KEY = 'trungso.ack.v1';

function hasAcknowledged() {
  try {
    return localStorage.getItem(ACK_KEY) === '1';
  } catch {
    // Private browsing refuses reads. Show the warning again rather than assume consent.
    return false;
  }
}

function remember() {
  try {
    localStorage.setItem(ACK_KEY, '1');
  } catch {
    // Storage blocked. The modal still closes - see closeGate. Failing to remember a
    // dismissal must never leave the visitor locked out of the page.
  }
}

function buildGate() {
  const gate = document.createElement('div');
  gate.className = 'gate';
  gate.setAttribute('role', 'dialog');
  gate.setAttribute('aria-modal', 'true');
  gate.setAttribute('aria-labelledby', 'gate-title');
  gate.innerHTML = `
    <div class="gate__panel">
      <p class="gate__eyebrow">⚠ Đọc trước khi xem số</p>
      <h2 class="gate__title" id="gate-title">Trang này không dự đoán được xổ số.<br>Không phần mềm nào làm được.</h2>
      <p class="gate__lede">
        Đây là một thí nghiệm đốt token AI. Mọi con số ở đây là ngẫu nhiên, và trang tự
        công khai chứng minh điều đó bằng chi-square trên 12.578 kỳ quay.
      </p>
      <ul class="gate__list">
        <li>Không bán gì — không thu tiền, không tài khoản, không quảng cáo</li>
        <li>Không liên quan Vietlott — không liên kết, không tài trợ, không uỷ quyền</li>
        <li>Dữ liệu từ mirror bên thứ ba, có thể sai — cần chính xác thì tra vietlott.vn</li>
        <li>18+ · tự chịu rủi ro</li>
      </ul>
      <div class="gate__actions">
        <button class="btn" type="button" id="gate-ok">TÔI HIỂU</button>
        <a class="gate__more" href="https://github.com/quocdaijr/trungso/blob/main/DISCLAIMER.md"
           target="_blank" rel="noopener">Đọc bản đầy đủ →</a>
      </div>
    </div>`;
  return gate;
}

function closeGate(gate) {
  gate.remove();
  document.documentElement.classList.remove('is-gated');
  remember();
  const firstStamp = document.querySelector('.stamp');
  if (firstStamp) firstStamp.focus();
}

/** Keep Tab inside the dialog while it is open. */
function trapFocus(gate, event) {
  if (event.key !== 'Tab') return;
  const focusable = gate.querySelectorAll('button, a[href]');
  if (!focusable.length) return;
  const first = focusable[0];
  const last = focusable[focusable.length - 1];
  if (event.shiftKey && document.activeElement === first) {
    event.preventDefault();
    last.focus();
  } else if (!event.shiftKey && document.activeElement === last) {
    event.preventDefault();
    first.focus();
  }
}

function openGate() {
  const gate = buildGate();
  document.documentElement.classList.add('is-gated');
  document.body.appendChild(gate);

  const ok = gate.querySelector('#gate-ok');
  ok.addEventListener('click', () => closeGate(gate));
  gate.addEventListener('keydown', (event) => {
    // Escape deliberately does nothing: the button must be pressed.
    if (event.key === 'Escape') event.preventDefault();
    trapFocus(gate, event);
  });
  ok.focus();
  return gate;
}

function initWarningGate() {
  if (hasAcknowledged()) return null;
  return openGate();
}

window.TrungsoWarning = { ACK_KEY, hasAcknowledged, initWarningGate, openGate, closeGate };

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initWarningGate);
} else {
  initWarningGate();
}
