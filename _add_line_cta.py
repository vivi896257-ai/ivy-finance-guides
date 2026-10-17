# 2026-10-01 Ivy：「幫我把諮詢懶人包系列都加上 LINE 諮詢的資訊，也希望有一個官方 LINE 的小圖」
# 範圍：懶人包網站 8 頁（跟同日早上加 IG 圖示的是同一組）
# 每頁：①頁尾上方加「官方 LINE 諮詢卡」②頁尾 IG 旁加 LINE 小圖示連結
# 每頁先備份 index.html.bak_<時間>（.gitignore 已排除）；紀錄邊做邊寫
import os, shutil, datetime, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
PAGES = ["after-mortgage", "bond-yield", "dividend-source", "dividend-tax",
         "home-budget", "loan-term", "reserved-portion", "retirement-gap"]
LINE_URL = "https://line.me/R/ti/p/@062buxpy"
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
LOG = os.path.join(ROOT, f"_add_line_cta_紀錄_{TS}.txt")

ICON = ('<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="1" y="1" width="22" height="22" rx="6" fill="#06C755"/>'
        '<path fill="#fff" d="M12 5.4c-4.5 0-8.1 2.9-8.1 6.4 0 3.2 2.9 5.8 6.7 6.3.3.1.6.2.7.4.1.2.1.5 0 .8l-.1.7c0 .2-.2.8.7.4.9-.4 4.9-2.9 6.6-4.9 1.2-1.3 1.6-2.6 1.6-3.7 0-3.5-3.6-6.4-8.1-6.4z"/></svg>')

CSS = """  /* 官方 LINE 諮詢卡＋頁尾 LINE 圖示（2026-10-01） */
  .line-cta { margin-top:2rem; padding:1.1rem 1.2rem; border:1px solid var(--line); border-radius:14px;
              display:flex; gap:.9rem; align-items:center; flex-wrap:wrap; }
  .line-cta > svg { width:2.6rem; height:2.6rem; flex:0 0 auto; }
  .line-cta .txt { flex:1 1 13rem; min-width:0; }
  .line-cta .txt b { display:block; font-size:1.02rem; margin-bottom:.2rem; }
  .line-cta .txt p { margin:0; font-size:.9rem; color:var(--ink-soft); }
  .line-cta a.btn { background:#06C755; color:#fff; font-weight:700; padding:.6rem 1.1rem; border-radius:999px;
                    text-decoration:none; white-space:nowrap; }
  .line-cta a.btn:hover { opacity:.88; }
  a.handle.line { display:inline-flex; align-items:center; gap:.3em; text-decoration:none; }
  a.handle.line svg { width:1.1em; height:1.1em; flex:0 0 auto; }
  a.handle.line:hover { opacity:.8; }
"""

CARD = f"""  <aside class="line-cta" aria-label="官方 LINE 諮詢">
    {ICON}
    <div class="txt">
      <b>想把自己的狀況算清楚？</b>
      <p>加入官方 LINE，輸入「諮詢」，我會先問你幾個小問題。</p>
    </div>
    <a class="btn" href="{LINE_URL}" target="_blank" rel="noopener">加入官方 LINE →</a>
  </aside>

"""

FOOT_LINK = f'　<a class="handle line" href="{LINE_URL}" target="_blank" rel="noopener" aria-label="官方 LINE">{ICON}官方 LINE</a>'


def log(msg):
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(msg + "\n")
        f.flush()
    print(msg)


log(f"開始 {TS}｜範圍 {len(PAGES)} 頁")
for slug in PAGES:
    p = os.path.join(ROOT, slug, "index.html")
    src = open(p, encoding="utf-8").read()
    if "line-cta" in src:
        log(f"⏭ {slug}：已經有 LINE 卡片，跳過")
        continue
    # 前置檢查：結構必須跟預期一樣，否則整頁不動
    if src.count("</style>") != 1 or src.count("<footer") != 1 or src.count('class="handle ig"') != 1:
        log(f"⛔ {slug}：結構不符，未修改")
        continue
    bak = p + ".bak_" + TS
    shutil.copy2(p, bak)
    out = src.replace("</style>", CSS + "</style>", 1)
    i = out.index("<footer")
    line_start = out.rfind("\n", 0, i) + 1
    out = out[:line_start] + CARD + out[line_start:]
    j = out.index('class="handle ig"')
    k = out.index("</a>", j) + len("</a>")
    out = out[:k] + FOOT_LINK + out[k:]
    open(p, "w", encoding="utf-8", newline="").write(out)
    chk = open(p, encoding="utf-8").read()
    ok = chk.count("line-cta") >= 2 and chk.count(LINE_URL) == 2 and chk.count("<footer") == 1
    log(f"{'✅' if ok else '⛔'} {slug}：卡片＋頁尾 LINE｜備份 {os.path.basename(bak)}｜LINE 連結數 {chk.count(LINE_URL)}")
log("結束")
