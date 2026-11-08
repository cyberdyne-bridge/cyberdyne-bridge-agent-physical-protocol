# -*- coding: utf-8 -*-
"""按 zh.html 的模板生成 research 系列页面（复用现有 CSS 类，不引入新样式）。"""
from pathlib import Path
import re

SITE = Path("/tmp/cpnc-repo/site")
TPL = (SITE / "zh.html").read_text(encoding="utf-8")

# 取出 <main> 前后的骨架
head_end = TPL.index('<main id="main">')
main_end = TPL.index("</main>") + len("</main>")
PREFIX, SUFFIX = TPL[:head_end], TPL[main_end:]

def head(title, desc, slug):
    h = PREFIX
    h = h.replace("<title>临界协议：中枢核 · CPNC</title>", f"<title>{title}</title>")
    h = re.sub(r'<meta name="description" content="[^"]*">',
               f'<meta name="description" content="{desc}">', h, count=1)
    h = re.sub(r'<meta property="og:title" content="[^"]*">',
               f'<meta property="og:title" content="{title}">', h, count=1)
    h = re.sub(r'<link rel="canonical" href="[^"]*">',
               f'<link rel="canonical" href="https://www.cyberdyne-bridge.com/{slug}">', h, count=1)
    return h

def nav(h, active):
    """把页内锚点指向 zh.html，并标出当前页。"""
    h = h.replace('<a class="brand" href="#top"', '<a class="brand" href="./zh.html"')
    for sec in ("what", "architecture", "principles", "security", "mcp-status",
                "protocol-map", "os", "agents"):
        h = h.replace(f'<a href="#{sec}">', f'<a href="./zh.html#{sec}">')
    link = '<a href="./research.html">其他研究</a>'
    h = h.replace('<a href="./zh.html#agents">Agent 子仓</a>',
                  '<a href="./zh.html#agents">Agent 子仓</a>\n      ' + link, 1)
    if active != "research.html":
        # 详情页：把「其他研究」指向索引，自身不重复
        pass
    return h

def stats(items):
    cells = "".join(f'<div><strong>{v}</strong><span>{k}</span></div>' for v, k in items)
    return f'<div class="carriage-stats">{cells}</div>'

def cards(items, accent_first=False):
    out = []
    for i, (num, title, body, href) in enumerate(items):
        cls = "card card-small"
        if accent_first and i == 0:
            cls += " card-accent"
        inner = f'<span class="card-num">{num}</span><h3>{title}</h3><p>{body}</p>'
        if href:
            out.append(f'<a class="{cls}" href="{href}" style="text-decoration:none">'
                       f'{inner}</a>')
        else:
            out.append(f'<article class="{cls}">{inner}</article>')
    return '<div class="cards cards-six">' + "".join(out) + "</div>"

def section(kicker, h2, lede, body, foot=None, anchor=None):
    idattr = f' id="{anchor}"' if anchor else ""
    f = ""
    if foot:
        f = f'<div class="section-foot"><a class="text-link" href="{foot[1]}" target="_blank" rel="noopener">{foot[0]} <span aria-hidden="true">↗</span></a></div>'
    return f'''    <section class="section"{idattr}>
      <div class="section-head">
        <p class="kicker">{kicker}</p>
        <div>
          <h2>{h2}</h2>
          <p class="section-lede">{lede}</p>
        </div>
      </div>
      {body}
      {f}
    </section>'''

BANNER = re.compile(r'\s*<div class="audit-banner" role="status">.*?</div>', re.S)

def page(slug, title, desc, main_html, active=None):
    html = head(title, desc, slug) + '<main id="main">\n' + main_html + '\n  </main>' + SUFFIX
    html = nav(html, active or slug)
    html = BANNER.sub("", html)
    (SITE / slug).write_text(html, encoding="utf-8")
    return slug

# ---------------------------------------------------------------- 索引
idx = section(
    "08 / OTHER RESEARCH",
    "协议之外，<br>还有几条研究线。",
    "这些都不属于 CBAP，也不计入 129 条 conformance：一个是长程连续性的实验装置，"
    "一个是「框架 vs 模型」的证据集，另外还有部署底座、第二身体和独立小工具。"
    "分开放，免得混进协议。",
    stats([("5", "项目"), ("2", "研究线"), ("1", "部署底座"), ("0", "计入 conformance")]) +
    cards([
        ("研究装置", "岸 · boundary-agent",
         "跑在本机 1.5B–4B 上的关系型 Agent。把记忆、情绪、边界做成可查的账本，"
         "研究的是「200 轮之后还像不像同一个它」。不是产品，也不是意识。", "./research-an.html"),
        ("证据集", "框架实验 · boundary-lab",
         "P1–P4 主线 + P-Mini 外传：65 个脚手架、75 篇报告、66 组原始结果。"
         "负结果占了大半，这才是重点。", "./research-lab.html"),
        ("部署", "CBAP OS",
         "Debian 13 + CBAP 运行时层：多版本槽、开机选择、登录后热切换、失败回滚。", "./research-os.html"),
        ("第二身体", "桌宠 · cbap-pet-body",
         "四个 agent 都指向 Minecraft；这个补上「表现面身体」：本地事件流 + 回环动作，"
         "estop 的安全态是隐藏。", "./research-pet.html"),
        ("工具", "tools",
         "与协议无关的独立小工具。首个是 webm 插帧（保留 alpha）+ 音频快修。", "./research-tools.html"),
        ("协议本体", "回到 CPNC",
         "上面这些都不改变协议：Kernel、租约、审计、conformance 仍在主仓。", "./zh.html"),
    ], accent_first=True),
    foot=("看组织全部仓库", "https://github.com/cyberdyne-bridge"),
    anchor="research")
page("research.html", "其他研究 · CPNC", "CPNC 协议之外的研究线：岸（长程连续性）、框架实验（模型之外的脚手架）、CBAP OS、桌宠身体与独立工具。", idx)

# ---------------------------------------------------------------- 岸
an = section(
    "OTHER RESEARCH / 01",
    "一个研究「连续性」的装置。",
    "岸 跑在本机 1.5B–4B 上，把记忆、情绪、边界和没说出口的话做成可见账本。"
    "它不追任务成功率，它追的是「200 轮之后还像不像同一个它」。",
    stats([("200", "轮长对话"), ("68", "commits"), ("12,940", "行 Python"), ("5", "层")]) +
    cards([
        ("01", "五个层", "身体（GPU 温度/负载）、情绪（V/A/S 三轴）、记忆（facts + FTS5 + 冲突）、"
                        "边界（allow/refuse/silence/door）、叙事（inner/shadow/房间）。", "https://github.com/cyberdyne-bridge/boundary-agent/blob/main/README.md"),
        ("02", "拒绝发生在生成之前", "闸门在 LLM 之前：拒绝路径根本拿不到答案。先生成再「改成拒绝」，"
                                  "模型会先道歉然后把答案给出来。", "https://github.com/cyberdyne-bridge/boundary-agent/blob/main/README.md"),
        ("03", "账本", "memory.sqlite3 / facts.sqlite3 / rejections.jsonl / shadow_cache.jsonl，"
                      "物理分离，清空对话也不丢拒绝记录。", "https://github.com/cyberdyne-bridge/boundary-agent/blob/main/README.md"),
        ("04", "不是意识", "inner/shadow 是叙事层，不是意识证据。情绪是惩罚项，不是感受。", "https://github.com/cyberdyne-bridge/boundary-agent/blob/main/DISCLAIMER.md"),
        ("05", "情感依赖风险", "会被读成「在意」。免责声明里写了自检清单：什么时候该停。", "https://github.com/cyberdyne-bridge/boundary-agent/blob/main/DISCLAIMER.md"),
        ("06", "历史", "2026-10-19 首个版本 → 10-23 时间感知检索；研究纪事按阶段记录了取舍与踩坑。", "https://github.com/cyberdyne-bridge/boundary-agent/blob/main/CHRONICLE.md"),
    ], accent_first=True),
    foot=("boundary-agent 仓库", "https://github.com/cyberdyne-bridge/boundary-agent"),
    anchor="an")
page("research-an.html", "岸 · 研究装置 · CPNC",
     "岸：跑在本机小模型上的关系型 Agent，研究长程对话中的连续性。含免责声明、五层结构与账本设计。", an)

# ---------------------------------------------------------------- 框架实验
lab = section(
    "OTHER RESEARCH / 02",
    "模型之外的那层框架。",
    "P 系列主线是 P1–P4，P-Mini 是外传。核心不是「模型变强」，"
    "而是一层层把世界模型、自我模型、语言层、验证器拆开测。",
    stats([("65", "脚手架"), ("75", "报告"), ("66", "组原始结果"), ("P1–P4", "主线")]) +
    cards([
        ("P1", "反转宇宙 3/3 死", "AIF 能看见预测误差，但「看见」不等于「改动作」。"
                                 "固定环境会活，规则一反转就学不动。", "https://github.com/cyberdyne-bridge/boundary-lab/blob/main/docs/P-SERIES.md"),
        ("P2.0", "cue 2/3 vs blind 0/3", "给可见 cue 就能查表；P2.0d 把 6 个格子强制填满后 3/3、0 延迟 100%。"
                                        "但这是「会查表」，不是「知道自己有地图」。", "https://github.com/cyberdyne-bridge/boundary-lab/blob/main/docs/P-SERIES.md"),
        ("P2.1", "四组分离", "accurate fitness 87/79/84，reckless 3 tick 全死。"
                            "但风险函数、归因标签、C 惩罚都是人手写的。", "https://github.com/cyberdyne-bridge/boundary-lab/blob/main/docs/P-SERIES.md"),
        ("P3", "0/3 自发审计", "4B 会翻译、会服从、会合理化，但不会自己把 8 和 10 放进同一个因果链。", "https://github.com/cyberdyne-bridge/boundary-lab/blob/main/docs/P-SERIES.md"),
        ("P4", "Verifier 3/3", "外部 Verifier 能拒；4B 对误报的审计 0/3，会替校验器圆。"
                             "模板 3/3 精确，但算术是底层给的。", "https://github.com/cyberdyne-bridge/boundary-lab/blob/main/docs/P-SERIES.md"),
        ("P-Mini", "外传", "特征记忆能让行为变好；第一人称痛觉/内感受 0。", "https://github.com/cyberdyne-bridge/boundary-lab/blob/main/docs/P-SERIES.md"),
    ], accent_first=True),
    foot=("完整口径：docs/P-SERIES.md", "https://github.com/cyberdyne-bridge/boundary-lab/blob/main/docs/P-SERIES.md"),
    anchor="lab")
page("research-lab.html", "框架实验 · boundary-lab · CPNC",
     "P1–P4 与 P-Mini 实验全貌：世界模型、自我模型、语言层、验证器逐层拆开测，负结果占大半。", lab)

# ---------------------------------------------------------------- CBAP OS
os_page = section(
    "OTHER RESEARCH / 03",
    "把协议装进<br>一个可启动的系统。",
    "Debian 13 + 一层 CBAP 运行时：多个版本槽并存，开机选一个，登录后还能换，换挂了能回滚。"
    "旧槽永远不被修改。",
    stats([("11", "单元测试"), ("3", "systemd 单元"), ("1", "条挂载链"), ("0", "复制协议代码")]) +
    '''<figure class="arch-note" style="margin:0 0 1.2rem">
        <img src="./assets/cbap-os-desktop.png" alt="CBAP OS 桌面" style="width:100%;border:1px solid var(--line)">
        <figcaption>CBAP OS 0.1：XFCE 底座 + 版本槽选择，GRUB 每个槽一项。</figcaption>
      </figure>''' +
    cards([
        ("01", "版本槽", "/opt/cbap-os/versions/cbap/&lt;version&gt;，不可变；current 是 bind mount，不是副本。", None),
        ("02", "开机选择", "GRUB 每槽一项，或内核参数 cbap.cbap=… cbap.python=…；无头机直接给参数。", None),
        ("03", "热切换与回滚", "停服务 → 切挂载 → 起服务；失败恢复旧槽。", None),
        ("04", "没 hand 也能起", "cbap.service 用 ExecCondition 等 socket，没有 hand 就跳过，不卡在 failed。", None),
        ("05", "诚实的未验证项", "tty1 菜单代码在，但没在 QEMU 镜像里验证成功；10-24 之后没重跑过完整镜像。", None),
        ("06", "三种「控制」不混", "cbap-control 管槽位（Tk）；Console 管 Kernel 状态（web，在主仓）；cbap-os 是 CLI。", None),
    ], accent_first=True),
    foot=("cbap-os 仓库", "https://github.com/cyberdyne-bridge/cbap-os"),
    anchor="os")
page("research-os.html", "CBAP OS · 可版本化运行底座 · CPNC",
     "CBAP OS：Debian 13 + CBAP 运行时层，多版本槽、开机选择、热切换、失败回滚。", os_page)

# ---------------------------------------------------------------- 桌宠
pet = section(
    "OTHER RESEARCH / 04",
    "同一个内核，<br>第二个身体。",
    "四个 agent 全部指向 Minecraft，host_desktop 是控制面（文件/显示/输入）而不是表现面。"
    "桌宠补的是「表现面身体」这一格：本地事件流进，回环动作出。",
    stats([("6", "状态词汇"), ("23", "单元测试"), ("1", "cbap-device-v1"), ("hidden", "estop 安全态")]) +
    cards([
        ("01", "入：事件流", "&lt;config&gt;/agent-events/&lt;agent&gt;.jsonl，字节偏移增量读：不回放、半行缓冲、单次 64KB 有界。", None),
        ("02", "六态", "thinking / working / attention / error / idle / sleeping；显式 state 优先于 event。", None),
        ("03", "出：回环", "POST http://127.0.0.1:&lt;port&gt;/api/respond；非回环地址直接拒绝。", None),
        ("04", "设备契约", "cbap-device-v1：class=presence，capabilities 含 estop，resources 限 5Hz。", None),
        ("05", "estop = 隐藏", "发 hide 并锁存 paused，之后 send() 一律 False——「急停必须有 safe-state 证据」。", None),
        ("06", "现状", "draft：单元测试过，未接真桌宠、未跑 kernel 端到端。", None),
    ], accent_first=True),
    foot=("cbap-pet-body 仓库", "https://github.com/cyberdyne-bridge/cbap-pet-body"),
    anchor="pet")
page("research-pet.html", "桌宠身体 · cbap-pet-body · CPNC",
     "把桌宠当作 CBAP 的第二个身体：本地 JSONL 事件 + 回环 HTTP 动作，estop 安全态为隐藏。", pet)

# ---------------------------------------------------------------- 工具
tools = section(
    "OTHER RESEARCH / 05",
    "独立小工具，<br>不进协议。",
    "与 CBAP 没有关系，也不依赖主仓任何代码——放在同一个组织下只是因为作者是同一个。",
    stats([("24→120", "fps"), ("alpha", "保留"), ("3", "端启动脚本"), ("0", "联网")]) +
    cards([
        ("01", "插帧", "VP9 透明通道原样保留；带音轨的 webm 音轨不重编码直接搬。24 插到 48/72/90/120。", None),
        ("02", "音频快修", "去闷 / 响度 / 裁静音 / 降噪，外挂模型缺失时自动降级成 DSP，不影响插帧主流程。", None),
        ("03", "先自检", "一键自检会列出 ffmpeg / ffprobe / rife 的实际情况，报 bug 前先跑它。", None),
        ("04", "不联网", "只处理本地文件；输出默认落在工具目录的 output/。", None),
        ("05", "许可更正", "原仓 LICENSE 误抄了上游 Merzlin 的版权行，已更正为本项目作者；上游在 NOTICE 署名。", None),
        ("06", "边界", "它是周边生产线，不改主仓、不是官方补丁。", None),
    ], accent_first=True),
    foot=("tools 仓库", "https://github.com/cyberdyne-bridge/tools"),
    anchor="tools")
page("research-tools.html", "tools · 独立小工具 · CPNC",
     "与协议无关的独立工具：webm 插帧（保留透明通道）与音频快修。", tools)

print("生成:", ", ".join(sorted(p.name for p in SITE.glob("research*.html"))))
