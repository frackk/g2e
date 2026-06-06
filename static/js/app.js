// Symbol palette
    const SYMBOL_TABS = [
      {
        id: "texto", name: "Texto", symbols: [
          [" ","espacio"],["0","0"],["1","1"],["2","2"],["3","3"],["4","4"],["5","5"],["6","6"],["7","7"],["8","8"],["9","9"],
          ["A","A"],["B","B"],["C","C"],["D","D"],["E","E"],["F","F"],["G","G"],["H","H"],["I","I"],["J","J"],["K","K"],["L","L"],["M","M"],["N","N"],["O","O"],["P","P"],["Q","Q"],["R","R"],["S","S"],["T","T"],["U","U"],["V","V"],["W","W"],["X","X"],["Y","Y"],["Z","Z"],
          ["a","a"],["b","b"],["c","c"],["d","d"],["e","e"],["f","f"],["g","g"],["h","h"],["i","i"],["j","j"],["k","k"],["l","l"],["m","m"],["n","n"],["o","o"],["p","p"],["q","q"],["r","r"],["s","s"],["t","t"],["u","u"],["v","v"],["w","w"],["x","x"],["y","y"],["z","z"],
          [".","."],[",",","],[";",";"],[":",":"],["'","'"],["\"","\""],["`","`"],["_","_"],["~","~"],["#","#"],["$","$"],["%","%"],["&","&"],["?","?"],["!","!"],["@","@"],["(","("],[")",")"],["[","["],["]","]"],["{","{"],["}","}"],["|","|"]
        ]
      },
      {
        id: "acentos", name: "Acentos/Cyr", symbols: [
          ["À","À"],["Á","Á"],["Â","Â"],["Ã","Ã"],["Ä","Ä"],["Å","Å"],["Ç","Ç"],["È","È"],["É","É"],["Ê","Ê"],["Ë","Ë"],["Ì","Ì"],["Í","Í"],["Î","Î"],["Ï","Ï"],["Ñ","Ñ"],["Ò","Ò"],["Ó","Ó"],["Ô","Ô"],["Õ","Õ"],["Ö","Ö"],["Ø","Ø"],["Ù","Ù"],["Ú","Ú"],["Û","Û"],["Ü","Ü"],["Ý","Ý"],["Ÿ","Ÿ"],
          ["à","à"],["á","á"],["â","â"],["ã","ã"],["ä","ä"],["å","å"],["ç","ç"],["è","è"],["é","é"],["ê","ê"],["ë","ë"],["ì","ì"],["í","í"],["î","î"],["ï","ï"],["ñ","ñ"],["ò","ò"],["ó","ó"],["ô","ô"],["õ","õ"],["ö","ö"],["ø","ø"],["ù","ù"],["ú","ú"],["û","û"],["ü","ü"],["ý","ý"],["ÿ","ÿ"],
          ["¡","¡"],["¿","¿"],["€","€"],["ƒ","ƒ"],["…","…"],["‘","‘"],["’","’"],["“","“"],["”","”"],["¢","¢"],["£","£"],["¤","¤"],["¥","¥"],["§","§"],["¬","¬"],["«","«"],["»","»"],["▫","▫"],["·","·"],
          ["А","А"],["Б","Б"],["В","В"],["Г","Г"],["Д","Д"],["Е","Е"],["Ё","Ё"],["Ж","Ж"],["З","З"],["И","И"],["Й","Й"],["К","К"],["Л","Л"],["М","М"],["Н","Н"],["О","О"],["П","П"],["Р","Р"],["С","С"],["Т","Т"],["У","У"],["Ф","Ф"],["Х","Х"],["Ц","Ц"],["Ч","Ч"],["Ш","Ш"],["Щ","Щ"],["Ъ","Ъ"],["Ы","Ы"],["Ь","Ь"],["Э","Э"],["Ю","Ю"],["Я","Я"],
          ["а","а"],["б","б"],["в","в"],["г","г"],["д","д"],["е","е"],["ё","ё"],["ж","ж"],["з","з"],["и","и"],["й","й"],["к","к"],["л","л"],["м","м"],["н","н"],["о","о"],["п","п"],["р","р"],["с","с"],["т","т"],["у","у"],["ф","ф"],["х","х"],["ц","ц"],["ч","ч"],["ш","ш"],["щ","щ"],["ъ","ъ"],["ы","ы"],["ь","ь"],["э","э"],["ю","ю"],["я","я"]
        ]
      },
      {
        id: "griegas", name: "Griegas", symbols: [
          ["Α","Α"],["Β","Β"],["Γ","Γ"],["Δ","Δ"],["Ε","Ε"],["Ζ","Ζ"],["Η","Η"],["Θ","Θ"],["Ι","Ι"],["Κ","Κ"],["Λ","Λ"],["Μ","Μ"],["Ν","Ν"],["Ξ","Ξ"],["Ο","Ο"],["Π","Π"],["Ρ","Ρ"],["Σ","Σ"],["Τ","Τ"],["Υ","Υ"],["Φ","Φ"],["Χ","Χ"],["Ψ","Ψ"],["Ω","Ω"],
          ["α","α"],["β","β"],["γ","γ"],["δ","δ"],["ε","ε"],["ζ","ζ"],["η","η"],["θ","θ"],["ι","ι"],["κ","κ"],["λ","λ"],["μ","μ"],["ν","ν"],["ξ","ξ"],["ο","ο"],["π","π"],["ρ","ρ"],["σ","σ"],["ς","ς"],["τ","τ"],["υ","υ"],["φ","φ"],["χ","χ"],["ψ","ψ"],["ω","ω"]
        ]
      },
      {
        id: "supsub", name: "Sup/Sub", symbols: [
          ["⁰","⁰"],["¹","¹"],["²","²"],["³","³"],["⁴","⁴"],["⁵","⁵"],["⁶","⁶"],["⁷","⁷"],["⁸","⁸"],["⁹","⁹"],["⁺","⁺"],["⁻","⁻"],
          ["₀","₀"],["₁","₁"],["₂","₂"],["₃","₃"],["₄","₄"],["₅","₅"],["₆","₆"],["₇","₇"],["₈","₈"],["₉","₉"],["₊","₊"],["₋","₋"],["ₙ","ₙ"],
          ["x^{n}","potencia"],["\\frac{num}{den}","fracción"],["\\sqrt{x}","raíz"],["\\sqrt[n]{x}","raíz n"],["\\abs{x}","valor abs"],["\\int ","integral"]
        ]
      },
      {
        id: "math", name: "Math", symbols: [
          ["+","+"],["-","-"],["*","*"],["/","/"],["=","="],["<","<"],[">",">"],["≤","≤"],["≥","≥"],["≠","≠"],["⇒","⇒"],
          ["×","×"],["÷","÷"],["°","°"],["√","√"],["∛","∛"],["∫","∫"],["∬","∬"],["∮","∮"],["∂","∂"],["∡","∡"],
          ["≒","≒"],["≈","≈"],["≡","≡"],["≢","≢"],["≅","≅"],["∽","∽"],["∝","∝"],["′","′"],["″","″"]
        ]
      },
      {
        id: "sets", name: "Sets/Forms", symbols: [
          ["∈","∈"],["∋","∋"],["⊆","⊆"],["⊇","⊇"],["⊂","⊂"],["⊃","⊃"],["⋃","⋃"],["⋂","⋂"],["∪","alias ⋃"],["∩","alias ⋂"],["∉","∉"],["∌","∌"],["⊈","⊈"],["⊉","⊉"],["⊄","⊄"],["⊅","⊅"],["∅","∅"],["∃","∃"],["∀","∀"],["∨","∨"],["∧","∧"],
          ["⊕","⊕"],["⊖","⊖"],["⊗","⊗"],["⊘","⊘"],["⟂","⟂"],["≬","≬"],["∥","∥"],["∦","∦"],["⫽","⫽"],["∴","∴"],["∵","∵"],["∟","∟"],
          ["←","←"],["→","→"],["↑","↑"],["↓","↓"],["↔","↔"],["↕","↕"],["↖","↖"],["↗","↗"],["↘","↘"],["↙","↙"],
          ["◀","◀"],["▶","▶"],["▲","▲"],["▼","▼"],["▸","▸"],["▹","▹"],["⋇","⋇"],["【","【"],["】","】"],["○","○"],["●","●"],["□","□"],["■","■"],["♢","♢"],["♦","♦"],["⊠","⊠"],["∙","∙"],["▽","▽"]
        ]
      }
    ];

    const textarea  = document.getElementById("content");
    const stripList = document.getElementById("stripList");

    function escHtml(s) {
      return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
    }

    function focusEditorWithoutScroll(x, y) {
      try {
        textarea.focus({ preventScroll: true });
      } catch (_) {
        textarea.focus();
      }
      window.scrollTo(x, y);
      requestAnimationFrame(() => window.scrollTo(x, y));
    }

    function insertAtCursor(text, selectStart = null, selectEnd = null) {
      const keepX = window.scrollX;
      const keepY = window.scrollY;
      const s = textarea.selectionStart;
      const e = textarea.selectionEnd;
      textarea.value = textarea.value.slice(0, s) + text + textarea.value.slice(e);
      if (selectStart !== null && selectEnd !== null) {
        textarea.selectionStart = s + selectStart;
        textarea.selectionEnd   = s + selectEnd;
      } else {
        textarea.selectionStart = textarea.selectionEnd = s + text.length;
      }
      refresh();
      focusEditorWithoutScroll(keepX, keepY);
    }

    function buildSymbolPalette() {
      const tabs = document.getElementById("symTabs");
      tabs.innerHTML = "";
      document.querySelectorAll(".sym-panel").forEach(p => p.remove());

      SYMBOL_TABS.forEach((tab, idx) => {
        const tabBtn = document.createElement("button");
        tabBtn.type = "button";
        tabBtn.className = "sym-tab" + (idx === 0 ? " active" : "");
        tabBtn.dataset.tab = tab.id;
        tabBtn.textContent = tab.name;
        tabs.appendChild(tabBtn);

        const panel = document.createElement("div");
        panel.className = "sym-panel" + (idx === 0 ? " active" : "");
        panel.id = "tab-" + tab.id;
        tab.symbols.forEach(([glyph, label]) => {
          const btn = document.createElement("span");
          btn.className = "sym";
          btn.title = label;
          btn.innerHTML = `<span class="glyph">${escHtml(glyph === " " ? "␠" : glyph)}</span><span class="sym-label">${escHtml(label)}</span>`;
          btn.addEventListener("mousedown", event => event.preventDefault());
          btn.addEventListener("click", event => {
            event.preventDefault();
            insertAtCursor(glyph);
          });
          panel.appendChild(btn);
        });
        tabs.parentNode.appendChild(panel);
      });
    }

    const symTabsEl = document.getElementById("symTabs");
    symTabsEl.addEventListener("mousedown", event => event.preventDefault());
    symTabsEl.addEventListener("click", e => {
      const tab = e.target.closest(".sym-tab");
      if (!tab) return;
      document.querySelectorAll(".sym-tab").forEach(t => t.classList.remove("active"));
      document.querySelectorAll(".sym-panel").forEach(p => p.classList.remove("active"));
      tab.classList.add("active");
      document.getElementById("tab-" + tab.dataset.tab).classList.add("active");
    });

    // Math markup parser
    function extractBraced(text, start) {
      let depth = 1, i = start;
      while (i < text.length && depth > 0) {
        if (text[i] === "{") depth++;
        else if (text[i] === "}") depth--;
        i++;
      }
      return { inner: text.slice(start, Math.max(start, i - 1)), end: i };
    }

    function flushText(tokens, state) {
      if (state.buf) {
        tokens.push({ t: "text", s: state.buf });
        state.buf = "";
      }
    }

    function tokenFromLastBase(tokens, state) {
      if (state.buf.length > 0) {
        const base = state.buf.slice(-1);
        state.buf = state.buf.slice(0, -1);
        flushText(tokens, state);
        return [{ t: "text", s: base }];
      }
      if (tokens.length > 0) return [tokens.pop()];
      return [];
    }

    function parseMathTokens(text) {
      const tokens = [];
      const state = { buf: "" };
      let i = 0;
      while (i < text.length) {
        const rest = text.slice(i);
        if (rest.startsWith("\\frac{")) {
          flushText(tokens, state);
          const r1 = extractBraced(text, i + 6);
          const r2 = r1.end < text.length && text[r1.end] === "{" ? extractBraced(text, r1.end + 1) : { inner: "", end: r1.end };
          tokens.push({ t: "frac", num: parseMathTokens(r1.inner), den: parseMathTokens(r2.inner), numRaw: r1.inner, denRaw: r2.inner });
          i = r2.end;
        } else if (rest.startsWith("\\sqrt[")) {
          flushText(tokens, state);
          const cb = text.indexOf("]", i + 6);
          if (cb === -1) {
            tokens.push({ t: "sqrt", arg: [], argRaw: "" });
            i += 5;
          } else {
            const idxRaw = text.slice(i + 6, cb);
            const after = cb + 1;
            if (after < text.length && text[after] === "{") {
              const r = extractBraced(text, after + 1);
              tokens.push({ t: "nroot", idx: parseMathTokens(idxRaw), arg: parseMathTokens(r.inner), idxRaw, argRaw: r.inner });
              i = r.end;
            } else {
              tokens.push({ t: "nroot", idx: parseMathTokens(idxRaw), arg: [], idxRaw, argRaw: "" });
              i = after;
            }
          }
        } else if (rest.startsWith("\\sqrt{")) {
          flushText(tokens, state);
          const r = extractBraced(text, i + 6);
          tokens.push({ t: "sqrt", arg: parseMathTokens(r.inner), argRaw: r.inner });
          i = r.end;
        } else if (rest.startsWith("\\sqrt")) {
          flushText(tokens, state);
          tokens.push({ t: "sqrt", arg: [], argRaw: "" });
          i += 5;
        } else if (rest.startsWith("\\abs{")) {
          flushText(tokens, state);
          const r = extractBraced(text, i + 5);
          tokens.push({ t: "abs", arg: parseMathTokens(r.inner), argRaw: r.inner });
          i = r.end;
        } else if (rest.startsWith("\\int")) {
          flushText(tokens, state);
          tokens.push({ t: "text", s: "∫" });
          i += 4;
        } else if (text[i] === "^" && text[i + 1] === "{") {
          const base = tokenFromLastBase(tokens, state);
          const r = extractBraced(text, i + 2);
          tokens.push({ t: "super", base, exp: parseMathTokens(r.inner), expRaw: r.inner });
          i = r.end;
        } else {
          state.buf += text[i];
          i++;
        }
      }
      flushText(tokens, state);
      return tokens;
    }

    function tokensContainMath(tokens) {
      return tokens.some(tok => tok.t !== "text" || (tok.t === "text" && tok.s.includes("∫")));
    }

    function tokensNeedTwoRows(tokens) {
      for (const tok of tokens) {
        if (tok.t === "frac") return true;
        if (tok.num && tokensNeedTwoRows(tok.num)) return true;
        if (tok.den && tokensNeedTwoRows(tok.den)) return true;
        if (tok.arg && tokensNeedTwoRows(tok.arg)) return true;
        if (tok.base && tokensNeedTwoRows(tok.base)) return true;
        if (tok.exp && tokensNeedTwoRows(tok.exp)) return true;
      }
      return false;
    }

    function lineHasMathMarkup(text) {
      return text.includes("\\frac{") || text.includes("\\sqrt") || text.includes("\\abs{") || text.includes("\\int") || text.includes("^{");
    }

    // Strip parser and strip list
    function parseStrips(text) {
      const strips = [];
      let curTitle = null, curLines = [];
      for (const raw of text.split("\n")) {
        const m = raw.trim().match(/^[=\-]{3,}\s*(.*?)\s*[=\-]{3,}$/);
        if (m) {
          if (curLines.length || curTitle !== null) strips.push([curTitle || "", curLines]);
          curTitle = m[1];
          curLines = [];
        } else {
          curLines.push(raw);
        }
      }
      if (curLines.length || curTitle !== null) strips.push([curTitle || "", curLines]);
      return strips.length ? strips : [["", []]];
    }

    function updateStripPreview(strips) {
      stripList.innerHTML = "";
      strips.forEach(([title, lines]) => {
        const li = document.createElement("li");
        const lineCount = lines.filter(l => l.trim() !== "").length;
        li.innerHTML =
          `<span class="strip-title">${title ? escHtml(title) : "(sin título)"}</span>` +
          `<span class="strip-lines">— ${lineCount} línea${lineCount !== 1 ? "s" : ""}</span>`;
        stripList.appendChild(li);
      });
    }

    // Screen simulation
    const COLS   = 21;
    const ROWS   = 8;
    const SCALE  = 3;
    const CELL_W = 6;
    const CELL_H = 8;
    const PX_W   = CELL_W * SCALE;
    const PX_H   = CELL_H * SCALE;

    const LCD_BG   = "#9cba90";
    const LCD_FG   = "#182613";
    const INV_BG   = "#182613";
    const INV_FG   = "#9cba90";

    const CANVAS_FONT = "'GraphicSeries', 'Casio Graph', 'Casio', 'ClassWiz Display', 'Courier New', Consolas, monospace";

    const canvas = document.getElementById("screen");
    canvas.width  = COLS * PX_W;
    canvas.height = ROWS * PX_H;
    const ctx = canvas.getContext("2d");
    ctx.imageSmoothingEnabled = false;

    let currentPage = 0;
    let totalPages  = 1;

    function calcSafeTitle(title) {
      const raw = title || document.getElementById("filename")?.value || "EACT";
      return raw.replace(/\.g2e$/i, "").replace(/[^A-Za-z0-9_~\-]/g, "_").slice(0, 8) || "EACT";
    }

    function makeHeading(title) {
      const safe = calcSafeTitle(title);
      const left = "======";
      const rightLen = Math.max(1, 21 - left.length - safe.length);
      return (left + safe + "=".repeat(rightLen)).slice(0, 21);
    }

    function measureTextPx(text, scale = 1) {
      return [...String(text || "")].length * PX_W * scale;
    }

    function measureTokensPx(tokens, scale = 1) {
      let w = 0;
      for (const tok of tokens || []) {
        if (tok.t === "text") w += measureTextPx(tok.s, scale);
        else if (tok.t === "frac") w += Math.max(measureTokensPx(tok.num, scale * 0.78), measureTokensPx(tok.den, scale * 0.78), PX_W * scale) + PX_W * 0.45;
        else if (tok.t === "super") w += measureTokensPx(tok.base, scale) + Math.max(PX_W * 0.55, measureTokensPx(tok.exp, scale * 0.58));
        else if (tok.t === "sqrt") w += PX_W * scale + measureTokensPx(tok.arg, scale * 0.88);
        else if (tok.t === "nroot") w += PX_W * scale + measureTokensPx(tok.arg, scale * 0.88);
        else if (tok.t === "abs") w += PX_W * scale * 2 + measureTokensPx(tok.arg, scale);
      }
      return w;
    }

    function setFont(scale = 1) {
      const px = Math.max(8, Math.round(PX_H * scale));
      ctx.font = `bold ${px}px ${CANVAS_FONT}`;
      ctx.textBaseline = "alphabetic";
    }

    function drawText(text, x, baseline, fg, scale = 1, maxX = canvas.width) {
      ctx.fillStyle = fg;
      setFont(scale);
      for (const ch of [...String(text || "")]) {
        if (x >= maxX) break;
        ctx.fillText(ch, x, baseline);
        x += PX_W * scale;
      }
      return x;
    }

    function drawTokens(tokens, x, y0, rows, fg, bg, scale = 1, maxX = canvas.width) {
      const baseLine = rows >= 2 ? y0 + PX_H + Math.round(PX_H * 0.78) : y0 + Math.round(PX_H * 0.82);
      for (const tok of tokens || []) {
        if (x >= maxX) break;
        if (tok.t === "text") {
          x = drawText(tok.s, x, baseLine, fg, scale, maxX);
        } else if (tok.t === "super") {
          x = drawTokens(tok.base, x, y0, rows, fg, bg, scale, maxX);
          const expBase = baseLine - Math.round(PX_H * 0.45 * scale);
          x = drawTokensAtBaseline(tok.exp, x, expBase, fg, scale * 0.58, maxX);
        } else if (tok.t === "frac") {
          const numW = measureTokensPx(tok.num, scale * 0.78);
          const denW = measureTokensPx(tok.den, scale * 0.78);
          const w = Math.max(numW, denW, PX_W * scale) + PX_W * 0.45;
          const xEnd = Math.min(maxX, x + w);
          ctx.fillStyle = bg;
          ctx.fillRect(x, y0, xEnd - x, Math.min(2 * PX_H, canvas.height - y0));
          const center = x + w / 2;
          const numX = center - numW / 2;
          const denX = center - denW / 2;
          drawTokensAtBaseline(tok.num, numX, y0 + Math.round(PX_H * 0.74), fg, scale * 0.78, xEnd);
          ctx.fillStyle = fg;
          ctx.fillRect(x + PX_W * 0.15, y0 + PX_H - SCALE, Math.max(SCALE, w - PX_W * 0.3), SCALE);
          drawTokensAtBaseline(tok.den, denX, y0 + PX_H + Math.round(PX_H * 0.74), fg, scale * 0.78, xEnd);
          x += w;
        } else if (tok.t === "sqrt" || tok.t === "nroot") {
          if (tok.t === "nroot" && tok.idx && tok.idx.length) {
            drawTokensAtBaseline(tok.idx, x, baseLine - Math.round(PX_H * 0.45), fg, scale * 0.48, maxX);
          }
          x = drawText("√", x, baseLine, fg, scale, maxX);
          const argW = measureTokensPx(tok.arg, scale * 0.88);
          if (argW > 0) {
            ctx.fillStyle = fg;
            ctx.fillRect(x, baseLine - Math.round(PX_H * 0.74 * scale), Math.min(argW, maxX - x), SCALE);
            x = drawTokensAtBaseline(tok.arg, x, baseLine, fg, scale * 0.88, maxX);
          }
        } else if (tok.t === "abs") {
          x = drawText("|", x, baseLine, fg, scale, maxX);
          x = drawTokensAtBaseline(tok.arg, x, baseLine, fg, scale, maxX);
          x = drawText("|", x, baseLine, fg, scale, maxX);
        }
      }
      return x;
    }

    function drawTokensAtBaseline(tokens, x, baseline, fg, scale = 1, maxX = canvas.width) {
      for (const tok of tokens || []) {
        if (x >= maxX) break;
        if (tok.t === "text") x = drawText(tok.s, x, baseline, fg, scale, maxX);
        else if (tok.t === "super") {
          x = drawTokensAtBaseline(tok.base, x, baseline, fg, scale, maxX);
          x = drawTokensAtBaseline(tok.exp, x, baseline - Math.round(PX_H * 0.45 * scale), fg, scale * 0.58, maxX);
        } else if (tok.t === "sqrt" || tok.t === "nroot") {
          if (tok.t === "nroot" && tok.idx && tok.idx.length) {
            drawTokensAtBaseline(tok.idx, x, baseline - Math.round(PX_H * 0.45), fg, scale * 0.48, maxX);
          }
          x = drawText("√", x, baseline, fg, scale, maxX);
          const argW = measureTokensPx(tok.arg, scale * 0.88);
          if (argW > 0) {
            ctx.fillStyle = fg;
            ctx.fillRect(x, baseline - Math.round(PX_H * 0.74 * scale), Math.min(argW, maxX - x), SCALE);
            x = drawTokensAtBaseline(tok.arg, x, baseline, fg, scale * 0.88, maxX);
          }
        } else if (tok.t === "abs") {
          x = drawText("|", x, baseline, fg, scale, maxX);
          x = drawTokensAtBaseline(tok.arg, x, baseline, fg, scale, maxX);
          x = drawText("|", x, baseline, fg, scale, maxX);
        } else if (tok.t === "frac") {
          // Compact fraction inside another expression.
          const localY = baseline - PX_H;
          const numW = measureTokensPx(tok.num, scale * 0.66);
          const denW = measureTokensPx(tok.den, scale * 0.66);
          const w = Math.max(numW, denW, PX_W * scale) + PX_W * 0.35;
          const center = x + w / 2;
          drawTokensAtBaseline(tok.num, center - numW / 2, localY + Math.round(PX_H * 0.55), fg, scale * 0.66, x + w);
          ctx.fillStyle = fg;
          ctx.fillRect(x + PX_W * 0.1, baseline - Math.round(PX_H * 0.22), Math.max(SCALE, w - PX_W * 0.2), SCALE);
          drawTokensAtBaseline(tok.den, center - denW / 2, baseline + Math.round(PX_H * 0.48), fg, scale * 0.66, x + w);
          x += w;
        }
      }
      return x;
    }

    function renderTextAt(text, x0, y0, fg, bg, isTitle = false) {
      ctx.fillStyle = bg;
      ctx.fillRect(0, y0, canvas.width, PX_H);
      drawText(String(text || "").slice(0, COLS), x0, y0 + Math.round(PX_H * 0.82), fg, 1, canvas.width);
    }

    function buildScreenLines(strips) {
      const lines = [];
      for (const [title, rawLines] of strips) {
        lines.push({ isTitle: true, text: makeHeading(title), tokens: null, rows: 1 });
        for (const raw of rawLines) {
          if (!raw) {
            lines.push({ isTitle: false, text: "", tokens: [], rows: 1 });
          } else if (lineHasMathMarkup(raw)) {
            const tokens = parseMathTokens(raw);
            const rows = tokensNeedTwoRows(tokens) ? 2 : 1;
            lines.push({ isTitle: false, text: raw, tokens, rows });
          } else {
            let remaining = raw;
            while (remaining.length > 0) {
              lines.push({ isTitle: false, text: remaining.slice(0, COLS), tokens: null, rows: 1 });
              remaining = remaining.slice(COLS);
            }
          }
        }
      }
      return lines.length ? lines : [{ isTitle: false, text: "", tokens: [], rows: 1 }];
    }

    function renderScreen(lines, page) {
      let skip = page * ROWS;
      let budget = ROWS;
      const drawList = [];
      let r = 0;
      for (const el of lines) {
        if (skip >= el.rows) { skip -= el.rows; continue; }
        if (budget <= 0) break;
        const visibleRows = Math.min(el.rows - skip, budget);
        drawList.push({ el, canvasRow: r, skipRows: skip, visibleRows });
        r += visibleRows;
        budget -= visibleRows;
        skip = 0;
      }

      ctx.fillStyle = LCD_BG;
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      for (const { el, canvasRow } of drawList) {
        const bg = el.isTitle ? INV_BG : LCD_BG;
        const fg = el.isTitle ? INV_FG : LCD_FG;
        const y0 = canvasRow * PX_H;
        const blockH = el.rows * PX_H;

        ctx.fillStyle = bg;
        ctx.fillRect(0, y0, canvas.width, Math.min(blockH, canvas.height - y0));

        if (el.tokens && el.tokens.length > 0) {
          drawTokens(el.tokens, 0, y0, el.rows, fg, bg, 1, canvas.width);
        } else {
          renderTextAt(el.text || "", 0, y0, fg, bg, el.isTitle);
        }
      }

      ctx.strokeStyle = "rgba(0,0,0,0.08)";
      ctx.lineWidth = 1;
      for (let rr = 1; rr < ROWS; rr++) {
        ctx.beginPath();
        ctx.moveTo(0, rr * PX_H);
        ctx.lineTo(canvas.width, rr * PX_H);
        ctx.stroke();
      }
    }

    function updateScreen(strips) {
      const lines = buildScreenLines(strips);
      const totalLogicalRows = lines.reduce((s, l) => s + l.rows, 0);
      totalPages = Math.max(1, Math.ceil(totalLogicalRows / ROWS));
      currentPage = Math.min(currentPage, totalPages - 1);

      renderScreen(lines, currentPage);

      document.getElementById("pageInfo").textContent = `Página ${currentPage + 1} / ${totalPages}`;
      document.getElementById("prevPage").disabled = currentPage <= 0;
      document.getElementById("nextPage").disabled = currentPage >= totalPages - 1;

      const titleRows = strips.length;
      document.getElementById("screenStats").innerHTML =
        `<strong>${totalLogicalRows}</strong> filas totales<br>` +
        `<strong>${titleRows}</strong> strip${titleRows !== 1 ? "s" : ""}<br>` +
        `<strong>${COLS}</strong> col / <strong>${ROWS}</strong> filas`;
    }

    document.getElementById("prevPage").addEventListener("click", () => {
      if (currentPage > 0) {
        currentPage--;
        updateScreen(parseStrips(textarea.value));
      }
    });

    document.getElementById("nextPage").addEventListener("click", () => {
      if (currentPage < totalPages - 1) {
        currentPage++;
        updateScreen(parseStrips(textarea.value));
      }
    });

    function refresh() {
      const strips = parseStrips(textarea.value);
      updateStripPreview(strips);
      updateScreen(strips);
    }

    // Math template buttons
    document.getElementById("btnFrac").addEventListener("click", () => insertAtCursor("\\frac{num}{den}", 6, 9));
    document.getElementById("btnPow").addEventListener("click", () => insertAtCursor("x^{n}", 3, 4));
    document.getElementById("btnSqrt").addEventListener("click", () => insertAtCursor("\\sqrt{x}", 6, 7));
    document.getElementById("btnNroot").addEventListener("click", () => insertAtCursor("\\sqrt[n]{x}", 6, 7));
    document.getElementById("btnInt").addEventListener("click", () => insertAtCursor("\\int ", 0, 5));
    document.getElementById("btnAbs").addEventListener("click", () => insertAtCursor("\\abs{x}", 5, 6));

    textarea.addEventListener("input", refresh);
    document.getElementById("filename")?.addEventListener("input", refresh);

    buildSymbolPalette();
    refresh();
