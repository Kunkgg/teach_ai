/**
 * copy-code.js — One-click "复制" button for every <pre><code> block.
 *
 * Self-contained (injects its own styles), so a lesson only needs ONE line,
 * placed just before </body>:
 *
 *     <script src="../assets/copy-code.js" defer></script>
 *
 * Behavior:
 *   - Auto-enhances every <pre> on the page, except ASCII diagrams
 *     (<pre> inside .diagram) — those are pictures, not code to copy.
 *   - Prefers navigator.clipboard; falls back to a hidden <textarea> +
 *     document.execCommand('copy'), because the Clipboard API is NOT
 *     available on file:// pages (where these lessons are opened locally).
 *   - Extracts the raw code text (handles both `<pre><code>x` and the
 *     newline-after-<code> formatting style), trims a leading newline
 *     and trailing whitespace.
 */
(function () {
  'use strict';

  var STYLE = [
    '.cc-pre { position: relative; }',
    '.cc-btn {',
    '  position: absolute; top: 0.4rem; right: 0.4rem;',
    '  display: inline-flex; align-items: center; gap: 0.3rem;',
    '  padding: 0.26rem 0.6rem;',
    '  font-family: var(--f-mono, monospace); font-size: 0.72rem; font-weight: 500;',
    '  line-height: 1.2; color: var(--c-text-muted, #6b6b6b);',
    '  background: var(--c-bg, #fff); border: 1px solid var(--c-border, #ddd8d0);',
    '  border-radius: 5px; cursor: pointer; opacity: 0.6;',
    '  transition: opacity .15s ease, color .15s ease, border-color .15s ease;',
    '  user-select: none; z-index: 2;',
    '}',
    '.cc-btn:hover, .cc-btn:focus-visible {',
    '  opacity: 1; color: var(--c-accent, #c05621);',
    '  border-color: var(--c-accent, #c05621); outline: none;',
    '}',
    '.cc-btn--ok  { opacity: 1; color: var(--c-success, #16a34a); border-color: var(--c-success, #16a34a); }',
    '.cc-btn--err { opacity: 1; color: var(--c-error, #dc2626); border-color: var(--c-error, #dc2626); }',
    '@media print { .cc-btn { display: none; } }',
  ].join('\n');

  function injectStyles() {
    if (document.getElementById('cc-style')) return;
    var s = document.createElement('style');
    s.id = 'cc-style';
    s.textContent = STYLE;
    document.head.appendChild(s);
  }

  // Fallback for non-secure contexts (file://) where navigator.clipboard is unavailable.
  function fallbackCopy(text) {
    var ta = document.createElement('textarea');
    ta.value = text;
    ta.setAttribute('readonly', '');
    ta.style.position = 'fixed';
    ta.style.top = '-1000px';
    ta.style.left = '0';
    ta.style.opacity = '0';
    document.body.appendChild(ta);
    ta.focus();
    ta.select();
    var ok = false;
    try { ok = document.execCommand('copy'); } catch (e) { ok = false; }
    document.body.removeChild(ta);
    return ok;
  }

  function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) {
      return navigator.clipboard.writeText(text)
        .then(function () { return true; })
        .catch(function () { return fallbackCopy(text); });
    }
    return Promise.resolve(fallbackCopy(text));
  }

  function extractCode(pre) {
    var code = pre.querySelector('code');
    var el = code || pre;
    return el.textContent.replace(/^\n/, '').replace(/\s+$/, '');
  }

  function setLabel(btn, text, cls) {
    btn.textContent = text;
    btn.classList.remove('cc-btn--ok', 'cc-btn--err');
    if (cls) btn.classList.add(cls);
  }

  function enhance(pre) {
    if (pre.dataset.cc === '1') return;          // already enhanced
    if (pre.closest('.diagram')) return;          // skip ASCII diagrams
    pre.dataset.cc = '1';
    pre.classList.add('cc-pre');

    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'cc-btn';
    btn.setAttribute('aria-label', '复制代码到剪贴板');
    btn.textContent = '复制';

    var timer = null;
    btn.addEventListener('click', function () {
      copyText(extractCode(pre)).then(function (ok) {
        setLabel(btn, ok ? '已复制 ✓' : '复制失败', ok ? 'cc-btn--ok' : 'cc-btn--err');
        if (timer) clearTimeout(timer);
        timer = setTimeout(function () { setLabel(btn, '复制'); }, 1800);
      });
    });

    pre.appendChild(btn);
  }

  function init() {
    injectStyles();
    Array.prototype.forEach.call(document.querySelectorAll('pre'), enhance);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
