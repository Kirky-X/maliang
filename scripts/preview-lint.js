/* preview-lint.js —— maliang preview 运行时探针片段(页面内注入,只读取证)
 *
 * 用法(宿主浏览器工具/DevTools 注入;不手动改交付物本身,只注入临时副本):
 *   1. 把 <script src=".../preview-lint.js"></script> 放在 <head> 里、页面脚本之前
 *      (动效探针要早于页面脚本才能捕到首帧;放在 </body> 前会让首屏阶段失明)。
 *   2. 页面稳定后调用 `__maliangLint()` → 返回 [{rule,label,count,examples}]。
 *   3. 动效四相位:`__maliangMotion.setPhase('steps'|'hero'|'scroll')` 切换相位,
 *      各相位末调 `__maliangMotion.summary('load'|'steps'|'hero'|'scroll')`;
 *      结论用 `__maliangMotionIssues(phases, {viewportHeight})` 生成;
 *      简报用 `__maliangMotionBrief(name, phase, {viewportHeight})`。
 *      相位执行顺序(由调用方驱动,与 oil-ui shoot.mjs 一致):
 *        load  = 打开页面等 1.2s 后 summary('load');
 *        steps = setPhase('steps') → 若有动作脚本则执行 → 等 0.9s → summary('steps');
 *        hero  = 滚回顶部 → setPhase('hero') → 每步 h/10 滚到 1.5 屏 → summary('hero');(必做)
 *        scroll= setPhase('scroll') → 从 1.5 屏滚到底 → summary('scroll');(页面可滚动时必做)
 *      summary('scroll') 后由调用方补 `phase.scrollable = 页面可滚动`(供 issues 判定
 *      「没有随滚动出现的变化」)。首屏(hero)只报层数与幅度,不记为问题。
 *
 * 性质与纪律:
 *   * 只读:不修改被检查页面的样式或 DOM(不违反 preview.md「禁止手动改样式代替
 *     预览验证」——它在临时副本里取证,不写回交付物);
 *   * 只报不拦:14 类可量测问题都是默认做法提示,命中的改掉、或写出理由保留;
 *     误报在交付说明写一句;提示清零后仍要自己看截图——"只认得写法,
 *     判断不了好不好看";
 *   * 颜色统一画到 canvas 再读回(oklch / color-mix 也能比较);对比度低于
 *     1.5:1 不报(文字后面多垫了一层查不到的元素,属噪声);
 *   * 动效 weak 阈值逐字符对齐:maxMove<4 && maxSize<0.02 && maxOpacity<0.3;
 *     frames<3 跳过(一次性跳变是状态写入,不是动效);首屏景深只报层数与幅度,
 *     不记为问题;滚动叙事只是提示,不是 hard fail。
 *
 * 来源:oil-ui scripts/shoot.mjs(默认做法提示 lintPage 与动效四相位探针
 * MOTION_PROBE),2026-10 吸收(#2/#4)。
 */

(function () {
  if (window.__maliangLint) return;

  // ---------- 14 类可量测问题的中文标签 ----------
  var LABELS = {
    eyebrow: "标题上方的眉标",
    numbered: "标题上方的编号标签",
    sideStripe: "彩色单侧边线",
    gradientText: "渐变文字",
    nestedCards: "卡片里套卡片",
    emojiIcon: "表情符号当图标",
    englishLabel: "中文界面里的英文大写标签",
    contrastLow: "文字对比度不达标（正文低于 4.5:1，大字低于 3:1）",
    grayOnColor: "有色底上的灰字",
    smallText: "正文小于 13px",
    tightLeading: "多行正文行高过紧",
    longMeasure: "正文行太长",
    stuck: "首屏有内容停在透明状态（出场动画没触发？）",
    headingSpacing: "标题离上文比离下文还近"
  };

  function lint() {
    var found = new Map();
    var describe = function (el) {
      var cls = typeof el.className === "string" && el.className.trim()
        ? "." + el.className.trim().split(/\s+/).slice(0, 2).join(".") : "";
      var text = (el.innerText || el.textContent || "").trim().replace(/\s+/g, " ").slice(0, 24);
      return el.tagName.toLowerCase() + (el.id ? "#" + el.id : "") + cls + (text ? "「" + text + "」" : "");
    };
    var add = function (rule, el, note) {
      var r = found.get(rule);
      if (!r) found.set(rule, r = { rule: rule, label: LABELS[rule], count: 0, examples: [] });
      r.count++;
      if (r.examples.length < 3) r.examples.push(describe(el) + (note ? "（" + note + "）" : ""));
    };
    var css = function (el, pseudo) { return getComputedStyle(el, pseudo); };
    var shown = function (el) {
      var r = el.getBoundingClientRect(), s = css(el);
      return r.width > 0 && r.height > 0 && s.visibility !== "hidden" && s.display !== "none";
    };
    // 颜色统一画到 canvas 再读回，oklch、color-mix 这类写法也能比较。
    var canvas = document.createElement("canvas");
    canvas.width = canvas.height = 1;
    var ctx = canvas.getContext("2d", { willReadFrequently: true });
    var colors = new Map();
    var rgba = function (value) {
      if (!ctx || !value) return { r: 0, g: 0, b: 0, a: 0 };
      if (colors.has(value)) return colors.get(value);
      ctx.clearRect(0, 0, 1, 1);
      ctx.fillStyle = "rgba(0,0,0,0)";
      ctx.fillStyle = value;
      ctx.fillRect(0, 0, 1, 1);
      var d = ctx.getImageData(0, 0, 1, 1).data;
      var c = { r: d[0], g: d[1], b: d[2], a: d[3] / 255 };
      colors.set(value, c);
      return c;
    };
    var luminance = function (c) {
      var f = function (v) { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
      return 0.2126 * f(c.r) + 0.7152 * f(c.g) + 0.0722 * f(c.b);
    };
    var ratio = function (a, b) {
      var x = luminance(a), y = luminance(b);
      return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05);
    };
    var chroma = function (c) { return (Math.max(c.r, c.g, c.b) - Math.min(c.r, c.g, c.b)) / 255; };
    var over = function (top, bottom) {
      return {
        r: top.r * top.a + bottom.r * (1 - top.a),
        g: top.g * top.a + bottom.g * (1 - top.a),
        b: top.b * top.a + bottom.b * (1 - top.a),
        a: 1
      };
    };
    var media = [].slice.call(document.querySelectorAll("img,video,canvas,picture,iframe,svg image"))
      .filter(shown).map(function (m) { return m.getBoundingClientRect(); })
      .filter(function (r) { return r.width * r.height > 2000; });
    var overMedia = function (r) {
      return media.some(function (m) {
        var w = Math.min(r.right, m.right) - Math.max(r.left, m.left);
        var h = Math.min(r.bottom, m.bottom) - Math.max(r.top, m.top);
        return w > 0 && h > 0 && w * h > r.width * r.height * 0.3;
      });
    };
    // 文字背后的底色：沿祖先往上叠，遇到背景图、渐变或媒体就算不知道。
    var backdrop = function (el) {
      var layers = [];
      for (var node = el; node && node.nodeType === 1; node = node.parentElement) {
        var s = css(node);
        if (s.backgroundImage !== "none") return null;
        var c = rgba(s.backgroundColor);
        if (c.a > 0) { layers.push(c); if (c.a >= 0.99) break; }
      }
      return layers.reverse().reduce(function (base, c) { return over(c, base); },
        { r: 255, g: 255, b: 255, a: 1 });
    };
    var ownText = function (el) {
      return [].slice.call(el.childNodes).filter(function (n) { return n.nodeType === 3; })
        .map(function (n) { return n.textContent; }).join("").trim();
    };
    var all = [].slice.call(document.body.querySelectorAll("*")).slice(0, 8000)
      .filter(function (el) {
        return !el.closest("svg,script,style,noscript,template,head,[aria-hidden='true']");
      });
    var texts = all.filter(function (el) { return ownText(el).length >= 2 && shown(el); });
    var cjkCount = (document.body.innerText.match(/[\u4e00-\u9fff]/g) || []).length;
    var latinCount = (document.body.innerText.match(/[A-Za-z]/g) || []).length;
    var chinese = cjkCount > 120 && cjkCount > latinCount / 2;

    // 眉标与编号标签：紧贴在标题正上方、比标题小很多的一行短字
    var flaggedAbove = new Set();
    var headings = [].slice.call(document.querySelectorAll("h1,h2,h3")).filter(shown);
    headings.forEach(function (h) {
      var hs = parseFloat(css(h).fontSize);
      if (hs < 20) return;
      var prev = h.previousElementSibling, node = h;
      while (!prev && node.parentElement && node.parentElement !== document.body) {
        node = node.parentElement; prev = node.previousElementSibling;
      }
      if (!prev || !shown(prev) || prev.closest("nav,[aria-label*='readcrumb' i],[class*='breadcrumb' i]")) return;
      if (prev.querySelector("a,button,input,select,textarea,img,video,canvas")
          || /^(A|BUTTON|INPUT|IMG)$/.test(prev.tagName)) return;
      var text = (prev.innerText || "").trim();
      if (!text || text.length > 48 || text.indexOf("\n") !== -1) return;
      var holder = prev;
      while (!ownText(holder) && holder.children.length === 1) holder = holder.children[0];
      var s = css(holder), size = parseFloat(s.fontSize);
      if (size > 16 || size > hs * 0.6) return;
      var pr = prev.getBoundingClientRect(), hr = h.getBoundingClientRect();
      if (pr.bottom > hr.top + 4 || hr.top - pr.bottom > Math.max(32, hs * 1.2)
          || pr.right < hr.left || pr.left > hr.right) return;
      var caps = s.textTransform === "uppercase"
        || (/[A-Z]{3}/.test(text) && text === text.toUpperCase());
      var tracked = parseFloat(s.letterSpacing) / size >= 0.05;
      var mono = /mono|courier|consolas|menlo/i.test(s.fontFamily);
      var ps = css(prev);
      var pill = parseFloat(ps.borderTopLeftRadius) >= pr.height / 3
        && (rgba(ps.backgroundColor).a > 0.1 || parseFloat(ps.borderTopWidth) >= 1);
      var numbered = /^0\d$/.test(text)
        || /^(?:0?\d{1,2}|[IVX]{1,4})(?:\s*[\/\u00b7\u2014\u2013|]\s*|[.:]\s+)\S/.test(text);
      if (numbered) { add("numbered", prev); flaggedAbove.add(h); }
      else if (caps || tracked || mono || pill) { add("eyebrow", prev); flaggedAbove.add(h); }
    });

    // 标题离下文应比离上文近：标题属于它后面的内容
    headings.forEach(function (h) {
      if (flaggedAbove.has(h)) return;
      var parent = css(h.parentElement);
      if (parent.display.indexOf("grid") !== -1
          || (parent.display.indexOf("flex") !== -1 && parent.flexDirection.indexOf("column") !== 0)) return;
      var prev = h.previousElementSibling, next = h.nextElementSibling;
      while (prev && !shown(prev)) prev = prev.previousElementSibling;
      while (next && !shown(next)) next = next.nextElementSibling;
      if (!prev || !next) return;
      var hr = h.getBoundingClientRect();
      var above = hr.top - prev.getBoundingClientRect().bottom;
      var below = next.getBoundingClientRect().top - hr.bottom;
      if (above >= 0 && below >= 12 && above + 4 < below) {
        add("headingSpacing", h, "上 " + Math.round(above) + "px，下 " + Math.round(below) + "px");
      }
    });

    all.forEach(function (el) {
      var s = css(el);
      if (s.display === "none") return;
      var r = el.getBoundingClientRect();
      if (!r.width || !r.height) return;

      // 单侧彩色边线：边框或贴边的伪元素，中性色的结构分隔线不算
      var sides = {
        left: parseFloat(s.borderLeftWidth), right: parseFloat(s.borderRightWidth),
        top: parseFloat(s.borderTopWidth), bottom: parseFloat(s.borderBottomWidth)
      };
      ["left", "right"].forEach(function (side) {
        var w = sides[side];
        var others = Math.max(sides[side === "left" ? "right" : "left"], sides.top, sides.bottom);
        var c = rgba(s[side === "left" ? "borderLeftColor" : "borderRightColor"]);
        if (w >= 2 && w >= others * 2
            && /solid|double/.test(s[side === "left" ? "borderLeftStyle" : "borderRightStyle"])
            && c.a >= 0.4 && chroma(c) >= 0.15 && r.height >= 16
            && r.width > sides.left + sides.right + 24 && r.height < innerHeight * 0.8) {
          add("sideStripe", el, w + "px");
        }
      });
      ["::before", "::after"].forEach(function (pseudo) {
        var p = css(el, pseudo);
        if (p.content === "none" || p.position !== "absolute") return;
        var pw = parseFloat(p.width), ph = parseFloat(p.height), c = rgba(p.backgroundColor);
        if (pw >= 2 && pw <= 8 && ph >= r.height * 0.6 && r.height >= 24 && r.width > 60
            && c.a >= 0.4 && chroma(c) >= 0.15
            && (parseFloat(p.left) <= 2 || parseFloat(p.right) <= 2)) {
          add("sideStripe", el, pseudo);
        }
      });

      if (/text/.test(s.backgroundClip + " " + s.getPropertyValue("-webkit-background-clip"))
          && /gradient/.test(s.backgroundImage) && (el.textContent || "").trim()) {
        add("gradientText", el);
      }
    });

    // 卡片里套卡片：有边框或阴影的圆角块，放在另一个圆角块里
    var boundary = function (el) {
      if (el.matches('[role="listbox"],[role="menu"],[role="dialog"],[role="tooltip"],[popover]')) return true;
      var position = css(el).position;
      if (position === "fixed") return true;
      if (position !== "absolute" || !el.parentElement) return false;
      var r = el.getBoundingClientRect(), parent = el.parentElement.getBoundingClientRect();
      // A positioned card inside a panel is still a card; a popup crosses its DOM parent's boundary.
      return r.left < parent.left - 1 || r.top < parent.top - 1
        || r.right > parent.right + 1 || r.bottom > parent.bottom + 1;
    };
    var content = function (el) {
      return (el.textContent || "").trim()
        || el.querySelector("img,svg,canvas,video,input,select,textarea,button,a,[contenteditable]");
    };
    var card = function (el, inner) {
      var s = css(el), r = el.getBoundingClientRect();
      if (boundary(el) || !content(el)) return false;
      if (r.width < 120 || r.height < 56
          || /^(BUTTON|A|INPUT|SELECT|TEXTAREA|IMG|VIDEO|CANVAS|LABEL|SUMMARY|PRE|CODE)$/.test(el.tagName)) return false;
      if (parseFloat(s.borderTopLeftRadius) < 6) return false;
      var border = ["Top", "Right", "Bottom", "Left"].every(function (k) {
        return parseFloat(s["border" + k + "Width"]) >= 1 && rgba(s["border" + k + "Color"]).a > 0.05;
      });
      var shadow = s.boxShadow !== "none";
      var fill = rgba(s.backgroundColor).a > 0.05;
      if (inner) return border || (shadow && fill);
      return (border || shadow || fill) && r.width * r.height < innerWidth * innerHeight * 0.6;
    };
    var rCompact = function (el) { return el.getBoundingClientRect().height <= 100; };
    all.forEach(function (el) {
      if (!card(el, true)) return;
      for (var up = el.parentElement, depth = 0; up && up !== document.body && depth < 8;
           up = up.parentElement, depth++) {
        if (boundary(up)) break;
        // A compact attachment with its own removal/retry control is editor content, not another panel.
        var editor = up.matches("form,[role='textbox']")
          || up.querySelector("textarea,[contenteditable='true'],[contenteditable='']");
        if (editor && rCompact(el) && el.querySelector("button,a,[role='button']")
            && !el.querySelector("h1,h2,h3,h4,section,article,textarea,[contenteditable]")) break;
        if (card(up, false)) { add("nestedCards", el, "外层 " + describe(up).split("「")[0]); break; }
      }
    });

    var emoji = /^(?:\p{Emoji_Presentation}|\p{Extended_Pictographic}\uFE0F)(?:\u200D\p{Extended_Pictographic}\uFE0F?)*$/u;
    var reaction = function (el) {
      var button = el.closest("button,[role='button']");
      if (!button) return false;
      var text = (button.textContent || "").trim();
      var symbol = ownText(el);
      // aria-pressed alone also describes toolbar toggles: require an emoji-only value or an adjacent count.
      return (button.hasAttribute("aria-pressed") && text === symbol)
        || (text.indexOf(symbol) === 0 && /^\s*\d+(?:[.,]\d+)?\s*$/.test(text.slice(symbol.length)));
    };
    var emojiHits = texts.filter(function (el) {
      return emoji.test(ownText(el))
        && !el.closest("p,blockquote,li > p,[role='listbox'],[role='menu'],[popover]")
        && !reaction(el);
    });
    if (emojiHits.length >= 2) emojiHits.forEach(function (el) { add("emojiIcon", el); });

    if (chinese) {
      var labels = texts.filter(function (el) {
        var t = (el.innerText || "").trim();
        if (!t || t.length > 40 || /[\u4e00-\u9fff]/.test(t)
            || el.closest("code,pre,kbd,samp")) return false;
        var letters = (t.match(/[A-Za-z]/g) || []).length;
        var upper = css(el).textTransform === "uppercase"
          || (/[A-Z]{2}/.test(t) && t === t.toUpperCase());
        return upper && (letters >= 8 || /[A-Za-z]{2,}\s+[A-Za-z]{2,}/.test(t));
      });
      if (labels.length >= 2) labels.forEach(function (el) { add("englishLabel", el); });
    }

    texts.forEach(function (el) {
      var s = css(el), r = el.getBoundingClientRect();
      if (el.closest("button:disabled,[disabled],[aria-disabled='true'],input,textarea,select,option")) return;
      var size = parseFloat(s.fontSize);
      var alpha = 1;
      for (var node = el; node && node.nodeType === 1; node = node.parentElement) {
        alpha *= parseFloat(css(node).opacity);
      }
      var bg = overMedia(r) ? null : backdrop(el);
      var fg = rgba(s.color);
      if (bg && alpha > 0.05 && fg.a > 0) {
        var color = over({ r: fg.r, g: fg.g, b: fg.b, a: fg.a * alpha }, bg);
        var contrast = ratio(color, bg);
        var large = size >= 24 || (size >= 18.6 && parseInt(s.fontWeight, 10) >= 700);
        // 低于 1.5:1 时文字几乎看不见，多半是文字后面还垫着一层查不到的元素（滑块、绝对定位的底板），不报
        if (contrast < 1.5) return;
        if (contrast < (large ? 3 : 4.5)) add("contrastLow", el, contrast.toFixed(2) + ":1");
        else if (chroma(bg) >= 0.25 && chroma(color) < 0.06
                 && luminance(color) > 0.08 && luminance(color) < 0.6) add("grayOnColor", el);
      }
      // 正文：两行以上的段落
      var text = ownText(el);
      var zh = /[\u4e00-\u9fff]/.test(text);
      if (text.length < (zh ? 30 : 60)
          || el.closest("code,pre,table,nav,button,label,figcaption,kbd")) return;
      var lh = s.lineHeight === "normal" ? size * 1.2 : parseFloat(s.lineHeight);
      if (r.height < lh * 1.8) return;
      if (size < 12.5) add("smallText", el, size + "px");
      if (lh / size < (zh ? 1.4 : 1.3)) add("tightLeading", el, (lh / size).toFixed(2));
      var perLine = zh ? r.width / size : r.width / (size * 0.5);
      if (perLine > (zh ? 46 : 95)) {
        add("longMeasure", el, "每行约 " + Math.round(perLine) + (zh ? " 字" : " 个字符"));
      }
    });

    // 首屏里停在透明的内容：出场动画没触发时截图会缺一块
    all.forEach(function (el) {
      var r = el.getBoundingClientRect();
      if (r.top >= innerHeight || r.bottom <= 0 || r.width < 40 || r.height < 16) return;
      if (!(ownText(el).length >= 4 || (el.tagName === "IMG" && el.complete))) return;
      if (el.closest("[role='dialog'],[role='tooltip'],[role='menu'],[hidden],dialog:not([open]),details:not([open])")) return;
      var alpha = 1, hider = null;
      for (var node = el; node && node.nodeType === 1; node = node.parentElement) {
        var o = parseFloat(css(node).opacity);
        if (o < 0.5 && !hider) hider = node;
        alpha *= o;
      }
      if (alpha >= 0.05 || !hider) return;
      var hs = css(hider);
      if (/absolute|fixed/.test(hs.position) || hs.pointerEvents === "none"
          || css(el).visibility === "hidden") return;
      add("stuck", el);
    });

    return Array.from(found.values());
  }

  window.__maliangLint = lint;

  // ---------- 动效四相位探针 ----------
  // 注入早于页面脚本：记录各相位哪些元素在动、动了多远。
  (function installMotionProbe() {
    if (window.__maliangMotion) return;
    var tracked = new Map();
    var phase = "load";
    var seen = new Set();
    function touch(el, source) {
      if (!(el instanceof Element)) return;
      var t = tracked.get(el);
      if (!t) { if (tracked.size >= 400) return; t = { phases: {} }; tracked.set(el, t); }
      var p = t.phases[phase];
      if (!p) p = t.phases[phase] = { first: null, last: null, frames: 0, move: 0, size: 0, opacity: 0, sources: new Set() };
      p.sources.add(source);
      if (source.indexOf("js:") === 0) t.lastJs = performance.now();
    }
    addEventListener("animationstart", function (e) { touch(e.target, "css:" + e.animationName); }, true);
    addEventListener("transitionrun", function (e) { touch(e.target, "transition:" + e.propertyName); }, true);
    new MutationObserver(function (list) {
      list.forEach(function (m) { touch(m.target, "js:" + m.attributeName); });
    }).observe(document, {
      subtree: true, attributes: true,
      attributeFilter: ["style", "transform", "viewBox", "d", "x", "y", "cx", "cy", "r",
                        "points", "opacity", "stroke-dashoffset"]
    });
    // 首屏阶段按视口坐标量：被固定住的舞台不算在动，舞台里的层次变化才算。
    function read(el) {
      var r = el.getBoundingClientRect();
      var page = phase === "hero" ? 0 : 1;
      return {
        x: r.left + scrollX * page, y: r.top + scrollY * page,
        w: r.width, h: r.height, o: +getComputedStyle(el).opacity
      };
    }
    function sample() {
      if (document.getAnimations) {
        document.getAnimations().forEach(function (a) {
          if (a.playState !== "running" || !a.effect || !a.effect.target) return;
          var tl = a.timeline && a.timeline.constructor && a.timeline.constructor.name;
          var scrollLinked = tl === "ScrollTimeline" || tl === "ViewTimeline";
          if (scrollLinked) touch(a.effect.target, "scroll-timeline:" + (a.animationName || "animation"));
          else if (!seen.has(a)) {
            seen.add(a);
            if (!a.animationName && !a.transitionProperty) touch(a.effect.target, "waapi");
          }
        });
      }
      tracked.forEach(function (t, el) {
        var p = t.phases[phase];
        if (!p || !el.isConnected) return;
        var now = read(el);
        if (!p.first) { p.first = p.last = now; return; }
        var l = p.last;
        if (Math.abs(now.x - l.x) + Math.abs(now.y - l.y) + Math.abs(now.w - l.w) + Math.abs(now.h - l.h) > 0.1
            || Math.abs(now.o - l.o) > 0.005) p.frames++;
        p.last = now;
        p.move = Math.max(p.move, Math.hypot(now.x - p.first.x, now.y - p.first.y));
        p.size = Math.max(p.size,
          Math.abs(now.w - p.first.w) / Math.max(1, p.first.w),
          Math.abs(now.h - p.first.h) / Math.max(1, p.first.h));
        p.opacity = Math.max(p.opacity, Math.abs(now.o - p.first.o));
      });
      requestAnimationFrame(sample);
    }
    requestAnimationFrame(sample);
    window.__maliangMotion = {
      setPhase: function (next) { phase = next; },
      summary: function (name) {
        var items = [];
        tracked.forEach(function (t, el) {
          var p = t.phases[name];
          if (!p) return;
          var label = el.tagName.toLowerCase() + (el.id ? "#" + el.id : "")
            + (typeof el.className === "string" && el.className.trim()
              ? "." + el.className.trim().split(/\s+/).slice(0, 2).join(".") : "");
          var infinite = el.getAnimations
            ? el.getAnimations().some(function (a) {
                return a.effect && a.effect.getTiming && a.effect.getTiming().iterations === Infinity;
              }) : false;
          var loop = infinite || (t.lastJs && performance.now() - t.lastJs < 250);
          if (p.frames < 3) return; // one-off jumps are state writes, not motion
          items.push({
            el: label, move: Math.round(p.move), size: +p.size.toFixed(3),
            opacity: +p.opacity.toFixed(2), loop: !!loop, sources: Array.from(p.sources).slice(0, 3)
          });
        });
        var visible = items.filter(function (i) {
          return ((name !== "scroll" && name !== "hero") || !i.loop)
            && (i.move >= 1 || i.size >= 0.005 || i.opacity >= 0.05
                || i.sources.some(function (s) { return s.indexOf("scroll-timeline:") === 0; }));
        });
        visible.sort(function (a, b) {
          return (b.move + b.size * 400 + b.opacity * 40) - (a.move + a.size * 400 + a.opacity * 40);
        });
        return {
          elements: visible.length,
          loops: visible.filter(function (i) { return i.loop; }).length,
          maxMove: Math.max(0, Math.max.apply(null, visible.map(function (i) { return i.move; }).concat([0]))),
          maxSize: Math.max(0, Math.max.apply(null, visible.map(function (i) { return i.size; }).concat([0]))),
          maxOpacity: Math.max(0, Math.max.apply(null, visible.map(function (i) { return i.opacity; }).concat([0]))),
          top: visible.slice(0, 8)
        };
      }
    };
  })();

  // 三条结论文案 + weak 阈值(逐字符对齐):首屏景深只报层数与幅度,滚动只提示不拦。
  window.__maliangMotionIssues = function (phases, opts) {
    var options = opts || {};
    var names = { load: "首次进入", steps: "--steps 动作", hero: "首屏滚动", scroll: "从头滚到底" };
    var weak = function (p) { return p.maxMove < 4 && p.maxSize < 0.02 && p.maxOpacity < 0.3; };
    var issues = [];
    Object.keys(phases || {}).forEach(function (k) {
      var p = phases[k];
      if (k === "hero") {
        // 首屏景深是可选手法：只报告层数和幅度，供选了它的页面核对，不记为问题。
        var heroH = options.viewportHeight || 0;
        p.layers = p.top.filter(function (i) { return i.size >= 0.05 || i.move >= heroH * 0.05; }).length;
        return;
      }
      if (k === "scroll") {
        if (!p.elements && p.scrollable) {
          issues.push("滚动：没有检测到随滚动出现的变化；落地页、品牌页、发布页和展览页需要一段滚动叙事");
        }
        return;
      }
      if (!p.elements) issues.push(names[k] + "：没有检测到动画");
      else if (p.loops === p.elements) {
        issues.push(names[k] + "：只有持续循环的动画，没有一次性的" + (k === "load" ? "出场" : "反馈"));
      } else if (weak(p)) {
        issues.push(names[k] + "：动画幅度太小，看不出来（最大位移 " + p.maxMove + "px，尺寸变化 "
          + (p.maxSize * 100).toFixed(1) + "%，透明度变化 " + p.maxOpacity + "）");
      }
    });
    return issues;
  };

  window.__maliangMotionBrief = function (name, phase, opts) {
    var options = opts || {};
    var names = { load: "首次进入", steps: "--steps 动作", hero: "首屏滚动", scroll: "从头滚到底" };
    if (name === "scroll" && !phase.scrollable) return "页面不滚动，跳过滚动检查";
    if (name === "hero") {
      var heroH = options.viewportHeight || 0;
      var layers = phase.layers !== undefined ? phase.layers
        : phase.top.filter(function (i) { return i.size >= 0.05 || i.move >= heroH * 0.05; }).length;
      return "首屏滚动 " + layers + " 层在变，最大缩放 " + (phase.maxSize * 100).toFixed(1)
        + "%，最大位移 " + phase.maxMove + "px";
    }
    return names[name] + " " + phase.elements + " 个元素在动，最大位移 " + phase.maxMove
      + "px，透明度变化 " + phase.maxOpacity;
  };
})();
