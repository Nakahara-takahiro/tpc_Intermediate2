/*
  circle_wave_demo.js
  circle_wave_demo.html 用のスクリプト。

  WordPress(Lightningテーマ)のカスタムHTMLブロックに貼り付けるときは、
  このファイルの中身をまるごと <script>...</script> タグで囲んでください。

  ページの中に .cw-demo が複数あっても、それぞれ独立して動くようにしています
  (id ではなく class で要素を探しているのはこのためです)。
*/
(function () {
  "use strict";

  var WINDOW_SECONDS = 2.0;              // 波グラフに表示する時間の幅[秒]
  var WAVE_POINTS = 600;                 // 波の線を描く点の数(多いほど、周波数が高くてもなめらかに見える)
  var AMPLITUDE_MAX = 1.5;               // 振幅スライダーの最大値
  var AXIS_LIMIT = AMPLITUDE_MAX * 1.3;  // 円・波グラフの表示範囲(振幅を変えても軸が動かないよう固定)

  // --- キャンバスを、画面に表示されているサイズぴったりの解像度に合わせる ---
  function resizeCanvas(canvas, ctx) {
    var ratio = window.devicePixelRatio || 1;
    var width = canvas.clientWidth;
    var height = canvas.clientHeight;
    canvas.width = Math.round(width * ratio);
    canvas.height = Math.round(height * ratio);
    ctx.setTransform(ratio, 0, 0, ratio, 0, 0); // これ以降はCSSピクセル単位で描画できる
    return { width: width, height: height };
  }

  // データ座標(x, y)を、キャンバス上のピクセル座標に変換する関数を作る
  function makeScaler(size, xMin, xMax, yMin, yMax) {
    return function (x, y) {
      var px = ((x - xMin) / (xMax - xMin)) * size.width;
      var py = size.height - ((y - yMin) / (yMax - yMin)) * size.height;
      return [px, py];
    };
  }

  // 左: 円のグラフの背景(十字線と目盛り)
  function drawCircleBackground(ctx, toPx) {
    ctx.save();
    ctx.strokeStyle = "#ddd";
    ctx.lineWidth = 1;
    ctx.beginPath();
    var left = toPx(-AXIS_LIMIT, 0);
    var right = toPx(AXIS_LIMIT, 0);
    var top = toPx(0, AXIS_LIMIT);
    var bottom = toPx(0, -AXIS_LIMIT);
    ctx.moveTo(left[0], left[1]);
    ctx.lineTo(right[0], right[1]);
    ctx.moveTo(top[0], top[1]);
    ctx.lineTo(bottom[0], bottom[1]);
    ctx.stroke();

    ctx.fillStyle = "#888";
    ctx.font = "11px sans-serif";
    ctx.textAlign = "center";
    ctx.textBaseline = "top";
    [-1, 0, 1].forEach(function (v) {
      var p = toPx(v, 0);
      ctx.fillText(String(v), p[0], p[1] + 4);
    });
    ctx.textAlign = "right";
    ctx.textBaseline = "middle";
    [-1, 1].forEach(function (v) {
      var p = toPx(0, v);
      ctx.fillText(String(v), p[0] - 4, p[1]);
    });
    ctx.restore();
  }

  // 右: 波のグラフの背景(0の基準線と目盛り)
  function drawWaveBackground(ctx, toPx) {
    ctx.save();
    ctx.strokeStyle = "#ddd";
    ctx.lineWidth = 1;
    ctx.beginPath();
    var zeroLeft = toPx(-WINDOW_SECONDS, 0);
    var zeroRight = toPx(0, 0);
    ctx.moveTo(zeroLeft[0], zeroLeft[1]);
    ctx.lineTo(zeroRight[0], zeroRight[1]);
    ctx.stroke();

    ctx.fillStyle = "#888";
    ctx.font = "11px sans-serif";

    ctx.textAlign = "center";
    ctx.textBaseline = "top";
    [-2, -1.5, -1, -0.5, 0].forEach(function (v) {
      var p = toPx(v, -AXIS_LIMIT);
      ctx.fillText(v.toFixed(1), p[0], p[1] + 4);
    });

    ctx.textAlign = "right";
    ctx.textBaseline = "middle";
    [-1, 0, 1].forEach(function (v) {
      var p = toPx(-WINDOW_SECONDS, v);
      ctx.fillText(String(v), p[0] - 4, p[1]);
    });
    ctx.restore();
  }

  function initInstance(root) {
    var circleCanvas = root.querySelector(".cw-demo__canvas--circle");
    var waveCanvas = root.querySelector(".cw-demo__canvas--wave");
    var waveTitle = root.querySelector(".cw-demo__title--wave");
    var freqRange = root.querySelector(".cw-demo__range--freq");
    var freqValueEl = root.querySelector(".cw-demo__control-value--freq");
    var ampRange = root.querySelector(".cw-demo__range--amp");
    var ampValueEl = root.querySelector(".cw-demo__control-value--amp");

    if (!circleCanvas || !waveCanvas) return;

    var circleCtx = circleCanvas.getContext("2d");
    var waveCtx = waveCanvas.getContext("2d");

    var t = 0;              // 経過時間[秒]
    var lastTimestamp = null;
    var isVisible = true;
    var rafId = null;

    function updateValueLabels() {
      freqValueEl.textContent = parseFloat(freqRange.value).toFixed(1) + " Hz";
      ampValueEl.textContent = parseFloat(ampRange.value).toFixed(1);
    }
    freqRange.addEventListener("input", updateValueLabels);
    ampRange.addEventListener("input", updateValueLabels);
    updateValueLabels();

    function draw(frequency, amplitude) {
      var circleSize = resizeCanvas(circleCanvas, circleCtx);
      var waveSize = resizeCanvas(waveCanvas, waveCtx);

      var toCirclePx = makeScaler(circleSize, -AXIS_LIMIT, AXIS_LIMIT, -AXIS_LIMIT, AXIS_LIMIT);
      var toWavePx = makeScaler(waveSize, -WINDOW_SECONDS, 0, -AXIS_LIMIT, AXIS_LIMIT);

      circleCtx.clearRect(0, 0, circleSize.width, circleSize.height);
      waveCtx.clearRect(0, 0, waveSize.width, waveSize.height);

      drawCircleBackground(circleCtx, toCirclePx);
      drawWaveBackground(waveCtx, toWavePx);

      var angle = 2 * Math.PI * frequency * t;   // 時間がたつほど角度が進む = 一定の速さで回る
      var height = amplitude * Math.sin(angle);  // 円の上の点の「高さ」← これが波になる
      var across = amplitude * Math.cos(angle);  // 円のどこにいるか(横方向)

      // 左: 円そのもの(点が通る道)
      circleCtx.beginPath();
      circleCtx.strokeStyle = "#bbb";
      circleCtx.lineWidth = 1;
      for (var i = 0; i <= 100; i++) {
        var a = (i / 100) * Math.PI * 2;
        var cp = toCirclePx(amplitude * Math.cos(a), amplitude * Math.sin(a));
        if (i === 0) circleCtx.moveTo(cp[0], cp[1]);
        else circleCtx.lineTo(cp[0], cp[1]);
      }
      circleCtx.stroke();

      // 左: 中心から点までの半径の線
      var center = toCirclePx(0, 0);
      var pointPx = toCirclePx(across, height);
      circleCtx.beginPath();
      circleCtx.strokeStyle = "#1f6feb";
      circleCtx.lineWidth = 2;
      circleCtx.moveTo(center[0], center[1]);
      circleCtx.lineTo(pointPx[0], pointPx[1]);
      circleCtx.stroke();

      // 左: 高さのガイド線(点線。右の波グラフの高さと同じであることを示す)
      var guideRight = toCirclePx(AXIS_LIMIT, height);
      circleCtx.beginPath();
      circleCtx.setLineDash([4, 4]);
      circleCtx.strokeStyle = "#e5484d";
      circleCtx.moveTo(pointPx[0], pointPx[1]);
      circleCtx.lineTo(guideRight[0], guideRight[1]);
      circleCtx.stroke();
      circleCtx.setLineDash([]);

      // 左: 回転する点
      circleCtx.beginPath();
      circleCtx.fillStyle = "#e5484d";
      circleCtx.arc(pointPx[0], pointPx[1], 5, 0, Math.PI * 2);
      circleCtx.fill();

      // 右: 波の線(今から window 秒前までを、毎回まとめて計算し直す)
      // 1点ずつ記録を積み上げる方式だと、周波数が高いときに点の間隔が粗くなって
      // 波がガタガタに見えてしまうため、常に WAVE_POINTS 個の点で描き直している。
      waveCtx.beginPath();
      waveCtx.strokeStyle = "#1f6feb";
      waveCtx.lineWidth = 2;
      for (var j = 0; j < WAVE_POINTS; j++) {
        var x = -WINDOW_SECONDS + (WINDOW_SECONDS * j) / (WAVE_POINTS - 1);
        var y = amplitude * Math.sin(2 * Math.PI * frequency * (t + x));
        var wp = toWavePx(x, y);
        if (j === 0) waveCtx.moveTo(wp[0], wp[1]);
        else waveCtx.lineTo(wp[0], wp[1]);
      }
      waveCtx.stroke();

      // 右: 高さのガイド線(点線)
      var guideLeft = toWavePx(-WINDOW_SECONDS, height);
      var headPx = toWavePx(0, height);
      waveCtx.beginPath();
      waveCtx.setLineDash([4, 4]);
      waveCtx.strokeStyle = "#e5484d";
      waveCtx.moveTo(guideLeft[0], guideLeft[1]);
      waveCtx.lineTo(headPx[0], headPx[1]);
      waveCtx.stroke();
      waveCtx.setLineDash([]);

      // 右: いまの点(左の円の点と同じ高さ)
      waveCtx.beginPath();
      waveCtx.fillStyle = "#e5484d";
      waveCtx.arc(headPx[0], headPx[1], 5, 0, Math.PI * 2);
      waveCtx.fill();

      waveTitle.textContent =
        "振幅(しんぷく) = " + amplitude.toFixed(1) +
        "　周波数(しゅうはすう) = " + frequency.toFixed(1) + " Hz";
    }

    function frame(timestamp) {
      rafId = null;
      if (!isVisible) return;

      if (lastTimestamp === null) lastTimestamp = timestamp;
      var dt = (timestamp - lastTimestamp) / 1000;
      lastTimestamp = timestamp;
      if (dt > 0.1) dt = 0.1; // タブを切り替えた直後などに時間が飛びすぎないようにする
      t += dt;

      draw(parseFloat(freqRange.value), parseFloat(ampRange.value));

      rafId = window.requestAnimationFrame(frame);
    }

    function requestFrame() {
      if (rafId === null && isVisible) {
        rafId = window.requestAnimationFrame(frame);
      }
    }

    // 画面外にスクロールしているときはアニメーションを止めて、パソコンの負荷を減らす
    if (window.IntersectionObserver) {
      var observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          isVisible = entry.isIntersecting;
          if (isVisible) {
            lastTimestamp = null; // 再開時に時間が飛ばないようにリセットする
            requestFrame();
          }
        });
      }, { threshold: 0.01 });
      observer.observe(root);
    }

    requestFrame();
  }

  function initAll() {
    var roots = document.querySelectorAll(".cw-demo");
    roots.forEach(function (root) {
      initInstance(root);
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initAll);
  } else {
    initAll();
  }
})();
