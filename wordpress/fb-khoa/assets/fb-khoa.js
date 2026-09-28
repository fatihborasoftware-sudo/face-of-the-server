/* FB Khoa — connects the page buttons to the Khoa frames (postMessage), pauses frames that are off screen,
   loads the stage only when asked, and fades the hero title while Khoa has the stage. No dependencies. */
(function () {
  'use strict';
  var send = function (frame, msg) {
    if (!frame || !frame.contentWindow) return;
    msg.khoa = 1;
    try { frame.contentWindow.postMessage(msg, '*'); } catch (e) {}
  };
  var frameOf = function (sel) {
    var box = sel ? document.querySelector(sel) : null;
    return box ? box.querySelector('iframe.khoa-frame') : null;
  };
  var loadStage = function (stage, then) {
    var f = stage.querySelector('iframe.khoa-frame');
    if (!f) return;
    var want = f.getAttribute('data-src');
    if (f.getAttribute('src') !== want) {
      f.setAttribute('src', want);
      stage.classList.add('is-loaded');
      if (then) f.addEventListener('load', function () { setTimeout(then, 1400); }, { once: true });
    } else if (then) then();
  };
  // PANELS: Face of the Server / Command Map (the same switch as on the server)
  var setPanel = function (stage, name) {
    if (stage.getAttribute('data-panel') === name) return false;
    var tab = stage.querySelector('[data-khoa-panel="' + name + '"]');
    if (!tab) return false;
    stage.setAttribute('data-panel', name);
    stage.querySelectorAll('[data-khoa-panel]').forEach(function (t) { var on = t === tab; t.classList.toggle('is-on', on); t.setAttribute('aria-selected', on ? 'true' : 'false'); });
    stage.querySelectorAll('[data-khoa-group]').forEach(function (g) { g.hidden = g.getAttribute('data-khoa-group') !== name; });
    var f = stage.querySelector('iframe.khoa-frame');
    f.setAttribute('data-src', tab.getAttribute('data-src'));
    return true;
  };

  document.addEventListener('click', function (e) {
    var b = e.target.closest ? e.target.closest('[data-khoa-cmd],[data-khoa-sit],[data-khoa-start],[data-khoa-panel],[data-khoa-talk]') : null;
    if (!b) return;
    if (b.hasAttribute('data-khoa-start')) { loadStage(b.closest('.khoa-stage')); return; }
    if (b.hasAttribute('data-khoa-panel')) { var st = b.closest('.khoa-stage'); setPanel(st, b.getAttribute('data-khoa-panel')); if (st.classList.contains('is-loaded')) loadStage(st); return; }
    if (b.hasAttribute('data-khoa-talk')) {
      var ts = document.querySelector(b.getAttribute('data-khoa-target')); if (!ts) return;
      var who = b.getAttribute('data-khoa-talk');
      ts.querySelectorAll('[data-khoa-talk]').forEach(function (x) { x.classList.toggle('is-on', x === b); });
      setPanel(ts, 'map');
      loadStage(ts, function () { send(ts.querySelector('iframe.khoa-frame'), { cmd: 'talk', name: who }); setTimeout(function () { send(ts.querySelector('iframe.khoa-frame'), { cmd: 'talk', name: '' }); }, 7000); });
      return;
    }
    var target = b.getAttribute('data-khoa-target');
    if (b.hasAttribute('data-khoa-cmd')) {
      send(frameOf(target), { cmd: b.getAttribute('data-khoa-cmd') });
      return;
    }
    var stage = document.querySelector(target);
    if (!stage) return;
    var name = b.getAttribute('data-khoa-sit');
    stage.querySelectorAll('[data-khoa-sit]').forEach(function (x) { x.classList.toggle('is-on', x === b); });
    setPanel(stage, 'face');
    loadStage(stage, function () { send(frameOf(target), { cmd: 'sit', name: name }); });
  });

  // messages from Khoa: "stage" true/false -> fade the hero title
  window.addEventListener('message', function (e) {
    var d = e.data;
    if (!d || typeof d !== 'object' || !d.khoa) return;
    document.querySelectorAll('iframe.khoa-frame').forEach(function (f) {
      if (f.contentWindow !== e.source) return;
      var hero = f.closest('.khoa-hero');
      if (hero && 'stage' in d) hero.classList.toggle('is-onstage', !!d.stage);
    });
  });

  // pause Khoa when he is scrolled out of view (saves the visitor's battery and GPU)
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { send(en.target, { cmd: 'pause', on: !en.isIntersecting }); });
    }, { threshold: 0.05 });
    var watch = function () { document.querySelectorAll('iframe.khoa-frame').forEach(function (f) { io.observe(f); }); };
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', watch); else watch();
  }
})();
