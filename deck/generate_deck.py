#!/usr/bin/env python3
"""Generate SuperSeed 5-min AI Agent OS deck (1920x1080) and snapshot PNGs."""

from __future__ import annotations

import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent
SLIDES = ROOT / "slides"
SHOTS = ROOT / "snapshots"
ASSETS = ROOT / "assets/logos"

SLIDES.mkdir(exist_ok=True)
SHOTS.mkdir(exist_ok=True)


def logo(name: str, size: int = 36) -> str:
    path = ASSETS / name
    if not path.exists():
        return ""
    return (
        f'<img class="logo" src="../assets/logos/{name}" '
        f'width="{size}" height="{size}" alt="">'
    )


CSS = r"""
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
:root {
  --bg: #0c1018;
  --panel: #151b27;
  --line: #2a3344;
  --gold: #d4a017;
  --gold2: #f3d27a;
  --ink: #f4f1ea;
  --mute: #9aa3b5;
  --red: #ef4444;
  --ok: #34d399;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { background: #000; }
.slide {
  width: 1920px; height: 1080px; overflow: hidden;
  background: radial-gradient(1200px 700px at 90% -10%, #1d2433 0%, var(--bg) 55%);
  color: var(--ink); font-family: Inter, system-ui, sans-serif;
  padding: 72px 88px 64px; position: relative;
}
.slide:before {
  content:""; position:absolute; left:0; top:0; bottom:0; width:8px; background: var(--gold);
}
.kicker { color: var(--gold); letter-spacing: .18em; text-transform: uppercase; font-size: 18px; font-weight: 700; margin-bottom: 18px; }
h1 { font-size: 64px; line-height: 1.08; font-weight: 800; max-width: 1600px; }
.sub { margin-top: 18px; color: var(--mute); font-size: 28px; }
.footer { position:absolute; left:88px; right:88px; bottom:36px; display:flex; justify-content:space-between; color:#6b7384; font-size:16px; }
.grid { display:grid; gap: 24px; margin-top: 48px; }
.cards-4 { grid-template-columns: repeat(4, 1fr); }
.cards-3 { grid-template-columns: repeat(3, 1fr); }
.cards-2 { grid-template-columns: 1fr 1fr; }
.card {
  background: var(--panel); border: 1px solid var(--line); border-radius: 20px; padding: 28px;
}
.card h3 { font-size: 26px; margin-bottom: 10px; }
.card p, .card li { color: var(--mute); font-size: 20px; line-height: 1.35; }
.stat { text-align:center; padding: 36px 20px; }
.stat .n { font-size: 92px; font-weight: 800; color: var(--gold2); line-height: 1; }
.stat .l { margin-top: 12px; color: var(--mute); font-size: 24px; }
.logo { vertical-align: middle; background: #fff; border-radius: 8px; padding: 4px; object-fit: contain; }
.chip {
  display:inline-flex; align-items:center; gap:10px;
  background:#fff; color:#111; border-radius: 999px; padding: 10px 18px 10px 10px;
  font-weight: 700; font-size: 22px;
}
.flow { display:flex; align-items:center; gap:14px; margin-top: 56px; flex-wrap:wrap; }
.flow .step {
  background: var(--panel); border:1px solid var(--line); border-radius: 16px;
  padding: 22px 26px; font-size: 24px; font-weight: 700;
}
.arrow { color: var(--gold); font-size: 36px; }
.ui {
  background: #0f141c; border: 1px solid #2c3648; border-radius: 16px; overflow: hidden;
  box-shadow: 0 20px 60px rgba(0,0,0,.35);
}
.ui-bar { background:#1b2230; padding: 12px 16px; display:flex; gap:8px; align-items:center; color:#8b93a7; font-size:14px; }
.dot { width:10px; height:10px; border-radius:50%; }
.blur {
  display:inline-block; height: 18px; width: 140px; border-radius: 6px;
  background: linear-gradient(90deg, #3a4254, #6b7388, #3a4254);
  filter: blur(3px); vertical-align: middle;
}
.blur.sm { width: 90px; height: 14px; }
.blur.xs { width: 70px; height: 12px; }
.blur.phone { width: 110px; }
.row { display:flex; gap: 18px; align-items:stretch; margin-top: 36px; }
.heat { display:inline-block; padding: 4px 10px; border-radius: 999px; font-size: 16px; font-weight: 800; }
.p1 { background:#3b1010; color:#fca5a5; }
.p2 { background:#3b2a10; color:#fcd34d; }
.p3 { background:#10261a; color:#6ee7b7; }
.mono { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; }
small.note { color:#6b7384; font-size: 16px; display:block; margin-top: 10px; }
"""

SHELL = """<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head>
<body>{body}</body></html>"""


def foot(n: int) -> str:
    return f'<div class="footer"><span>SuperSeed · Multi-agent OS</span><span>{n:02d} / 18</span></div>'


def slide(n: int, inner: str) -> str:
    return SHELL.format(css=CSS, body=f'<div class="slide">{inner}{foot(n)}</div>')


def gmail_snapshot() -> str:
    return f"""
    <div class="ui" style="width:100%;height:100%;">
      <div class="ui-bar"><span class="dot" style="background:#ff5f56"></span><span class="dot" style="background:#ffbd2e"></span><span class="dot" style="background:#27c93f"></span>
      {logo('gmail.svg', 18)} Gmail · Daily Growth Checklist</div>
      <div style="padding:18px 20px;background:#fff;color:#111;font-size:15px;">
        <div style="color:#667085;letter-spacing:.12em;text-transform:uppercase;font-size:11px;">Superseed Media</div>
        <div style="font-size:22px;font-weight:800;margin:4px 0 8px;">Daily Growth Checklist — 20 Aug 2026</div>
        <div style="display:flex;gap:8px;margin-bottom:12px;">
          <span style="border:2px solid #344054;padding:2px 8px;font-weight:800;font-size:12px;">26 actions</span>
          <span style="border:2px solid #b42318;color:#b42318;padding:2px 8px;font-weight:800;font-size:12px;">8 broken loops</span>
          <span style="border:2px solid #344054;padding:2px 8px;font-weight:800;font-size:12px;">2 waits</span>
        </div>
        <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-bottom:12px;">
          <div style="background:#f2f4f7;padding:10px;text-align:center;border:1px solid #d0d5dd;"><div style="font-size:11px;color:#344054;">ZEN</div><div style="font-size:28px;font-weight:800;">9</div></div>
          <div style="background:#f2f4f7;padding:10px;text-align:center;border:1px solid #d0d5dd;"><div style="font-size:11px;color:#344054;">TAMMY</div><div style="font-size:28px;font-weight:800;">6</div></div>
          <div style="background:#f2f4f7;padding:10px;text-align:center;border:1px solid #d0d5dd;"><div style="font-size:11px;color:#344054;">ELICIA</div><div style="font-size:28px;font-weight:800;">11</div></div>
        </div>
        <div style="font-weight:800;margin-bottom:6px;">Priority follow-ups (PII blurred)</div>
        <div>1. <span class="heat p1">P1 🌶️🌶️🌶️🌶️🌶️</span> <span class="blur"></span> · 1st Meeting Arranged · OVERDUE</div>
        <div>2. <span class="heat p1">P1 🌶️🌶️🌶️🌶️</span> <span class="blur"></span> · Proposal / sign-off</div>
        <div>3. <span class="heat p2">P2 🌶️🌶️🌶️</span> <span class="blur"></span> · Topic hold · confirm date</div>
        <div>4. <span class="heat p2">P2 🌶️🌶️</span> <span class="blur"></span> · New opportunity · qualify intent</div>
        <div style="margin-top:10px;color:#667085;font-size:12px;">Generated by prospect-follow-up-engine · routed by owner</div>
      </div>
    </div>"""


def sheets_snapshot() -> str:
    cells = "".join(
        f"""<tr>
          <td><span class="blur sm"></span></td>
          <td><span class="blur phone"></span></td>
          <td><span class="blur"></span></td>
          <td style="color:#344054;">FA firm</td>
          <td>{status}</td>
          <td><span class="blur xs"></span></td>
          <td>{src}</td>
        </tr>"""
        for status, src in [
            ("Considering", "IG DM"),
            ("Not now", "IG DM"),
            ("Won", "Ads"),
            ("1st mtg arranged", "Referral"),
        ]
    )
    return f"""
    <div class="ui" style="width:100%;">
      <div class="ui-bar">{logo('googlesheets.svg', 18)} Google Sheets · Financial Advisors Leads · Active Advisor Pipeline</div>
      <div style="background:#fff;color:#111;padding:0;font-size:14px;">
        <div style="background:#188038;color:#fff;padding:8px 12px;font-weight:700;">Active Advisor Pipeline</div>
        <table style="width:100%;border-collapse:collapse;">
          <tr style="background:#e8f0fe;font-weight:700;">
            <td style="padding:8px;border:1px solid #dadce0;">Name</td>
            <td style="padding:8px;border:1px solid #dadce0;">Phone</td>
            <td style="padding:8px;border:1px solid #dadce0;">Email</td>
            <td style="padding:8px;border:1px solid #dadce0;">Company</td>
            <td style="padding:8px;border:1px solid #dadce0;">Last outcome</td>
            <td style="padding:8px;border:1px solid #dadce0;">Meeting</td>
            <td style="padding:8px;border:1px solid #dadce0;">Source</td>
          </tr>
          {cells}
        </table>
      </div>
    </div>"""


def fireflies_snapshot() -> str:
    return f"""
    <div class="ui" style="width:100%;">
      <div class="ui-bar">{logo('fireflies.png', 18)} Fireflies · 100% recorded prospect meeting</div>
      <div style="padding:16px;background:#111827;color:#e5e7eb;font-size:15px;">
        <div style="font-size:20px;font-weight:800;">Prospect intro · 22 min</div>
        <div style="color:#9ca3af;margin:4px 0 12px;">Speakers: <span class="blur sm"></span> · SuperSeed</div>
        <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;">
          <div style="background:#1f2937;border-radius:10px;padding:12px;"><div style="color:#fbbf24;font-weight:800;">PAIN</div><div>Need high-intent appointments without cold prospecting.</div></div>
          <div style="background:#1f2937;border-radius:10px;padding:12px;"><div style="color:#f87171;font-weight:800;">CHALLENGE</div><div>Compliance + speaker quality before marketing.</div></div>
          <div style="background:#1f2937;border-radius:10px;padding:12px;"><div style="color:#34d399;font-weight:800;">SOLUTION</div><div>Co-marketing event IP · attendance-based model.</div></div>
        </div>
        <div style="margin-top:12px;color:#9ca3af;">→ Agent writes summary onto follow-up dashboard. Names/emails blurred.</div>
      </div>
    </div>"""


def lark_snapshot() -> str:
    tasks = [
        "Kickoff + client group",
        "Topic recommendations",
        "Speaker + venue hold",
        "Landing page + ads",
        "WhatsApp follow-up pack",
        "Event-day run of show",
    ]
    items = "".join(
        f'<div style="display:flex;gap:10px;padding:8px 0;border-bottom:1px solid #2a3344;"><input type="checkbox"> {t} · <span class="blur xs"></span></div>'
        for t in tasks
    )
    return f"""
    <div class="ui" style="width:100%;">
      <div class="ui-bar">{logo('lark.png', 18)} Lark · New opportunity → template tasks (auto)</div>
      <div style="padding:16px;background:#0b1220;color:#e5e7eb;">
        <div style="font-weight:800;font-size:20px;margin-bottom:8px;">Event pack · Opportunity <span class="blur sm"></span></div>
        {items}
        <div style="margin-top:10px;color:#9aa3b5;font-size:14px;">Nobody on the team creates these tasks by hand.</div>
      </div>
    </div>"""


def github_snapshot() -> str:
    return f"""
    <div class="ui" style="width:100%;">
      <div class="ui-bar">{logo('github.svg', 18)} github.com/SuperseedMedia</div>
      <div style="padding:8px 0;background:#0d1117;color:#c9d1d9;font-family:ui-monospace,monospace;font-size:18px;">
        <div style="padding:10px 16px;border-bottom:1px solid #21262d;">sales-follow-up</div>
        <div style="padding:10px 16px;border-bottom:1px solid #21262d;">events-registration</div>
        <div style="padding:10px 16px;border-bottom:1px solid #21262d;">marketing-assets</div>
        <div style="padding:10px 16px;">ops-lark</div>
      </div>
    </div>"""


def mcp_snapshot() -> str:
    rows = [
        ("gmail.svg", "Gmail", "Inbox + Daily Growth Checklist"),
        ("fireflies.png", "Fireflies", "Every meeting transcript"),
        ("lark.png", "Lark", "Full PM dashboard"),
        ("googlesheets.svg", "Google Sheets", "Pipeline data"),
        ("canva.svg", "Canva", "Design + brand assets"),
    ]
    body = "".join(
        f'<div style="display:flex;align-items:center;gap:12px;padding:10px 16px;border-bottom:1px solid #2a3344;">{logo(f, 28)} <b>{n}</b><span style="color:#9aa3b5"> — {d}</span> <span style="margin-left:auto;color:#34d399;">connected</span></div>'
        for f, n, d in rows
    )
    return f"""
    <div class="ui" style="width:100%;">
      <div class="ui-bar">{logo('cursor.png', 18)} Cursor · MCP servers</div>
      {body}
    </div>"""


SLIDE_BODIES = {}


def build_bodies() -> dict[int, str]:
    g = gmail_snapshot()
    sh = sheets_snapshot()
    ff = fireflies_snapshot()
    lk = lark_snapshot()
    gh = github_snapshot()
    mcp = mcp_snapshot()

    bodies = {
        1: f"""
        <div class="kicker">SuperSeed Media</div>
        <h1>How I built a multi-agent OS<br>for this company</h1>
        <p class="sub">Cursor agents · GitHub repos · Automations · live tools</p>
        <div class="row" style="margin-top:48px;">
          <div style="flex:1.2">{g}</div>
          <div style="flex:.8">{gh}</div>
        </div>
        """,
        2: f"""
        <h1>This company is impossible<br>without agents</h1>
        <div class="grid cards-3">
          <div class="card stat"><div class="n">8</div><div class="l">full-time staff</div></div>
          <div class="card stat"><div class="n">1</div><div class="l">freelancer</div></div>
          <div class="card stat"><div class="n">~25</div><div class="l">webinars / seminars a month</div></div>
        </div>
        """,
        3: f"""
        <h1>Our ecosystem</h1>
        <div class="grid cards-3">
          <div class="card" style="text-align:center;"><h3>Financial advisor teams</h3><p>Clients who sponsor the event</p></div>
          <div class="card" style="text-align:center;border-color:var(--gold);"><h3>SuperSeed events</h3><p>Webinars + seminars in the middle</p></div>
          <div class="card" style="text-align:center;"><h3>Expert speakers</h3><p>Content partners who teach</p></div>
        </div>
        <div style="display:flex;gap:18px;margin-top:40px;align-items:center;flex-wrap:wrap;">
          <span class="chip">{logo('sgpaincare.png', 28)} Singapore Paincare</span>
          <span class="chip">{logo('cpf.png', 28)} CPF Board</span>
          <span class="chip" style="padding-left:18px;">Fund houses</span>
        </div>
        """,
        4: f"""
        <h1>We sell content IP that books appointments</h1>
        <p class="sub">High-quality, high-intent financial planning appointments</p>
        <div class="flow">
          <div class="step">Ads</div><div class="arrow">→</div>
          <div class="step">Landing page</div><div class="arrow">→</div>
          <div class="step">Webinar / seminar</div><div class="arrow">→</div>
          <div class="step">WhatsApp follow-up</div><div class="arrow">→</div>
          <div class="step" style="border-color:var(--gold);color:var(--gold2);">Appointments</div>
        </div>
        """,
        5: f"""
        <h1>Four apps. That’s the company OS.</h1>
        <div class="grid cards-4">
          <div class="card stat">{logo('cursor.png', 64)}<div class="l" style="margin-top:18px;color:#fff;font-weight:700;">Cursor</div><p>Agents + automations</p></div>
          <div class="card stat">{logo('github.svg', 64)}<div class="l" style="margin-top:18px;color:#fff;font-weight:700;">GitHub</div><p>Repos by function</p></div>
          <div class="card stat">{logo('googlesheets.svg', 64)}<div class="l" style="margin-top:18px;color:#fff;font-weight:700;">Google Sheets</div><p>Pipeline data</p></div>
          <div class="card stat">{logo('lark.png', 64)}<div class="l" style="margin-top:18px;color:#fff;font-weight:700;">Lark</div><p>Project management</p></div>
        </div>
        """,
        6: f"""
        <h1>Four systems. Not four extra headcount.</h1>
        <div class="grid cards-4" style="margin-top:80px;">
          <div class="card"><h3>Sales follow-up</h3><p>{logo('gmail.svg', 28)} {logo('googlesheets.svg', 28)}</p><p>Daily checklist · heat ranking</p></div>
          <div class="card"><h3>Project management</h3><p>{logo('lark.png', 28)}</p><p>Template tasks, auto-created</p></div>
          <div class="card"><h3>Event registration</h3><p class="mono">&lt;/&gt; code</p><p>Custom app on GitHub</p></div>
          <div class="card"><h3>Asset generation</h3><p>{logo('openai.svg', 28)} {logo('netlify.svg', 28)}</p><p>LLMs + Netlify</p></div>
        </div>
        """,
        7: f"""
        <h1>GitHub is the central brain</h1>
        <div class="row">
          <div style="flex:1">{gh}</div>
          <div class="card" style="flex:1;"><h3>Why repos</h3><p>Different departments ship different code. Agents work on the repo that owns the function.</p></div>
        </div>
        """,
        8: f"""
        <h1>One repo per department / function</h1>
        <div class="grid" style="grid-template-columns: 1.2fr 1fr 1.4fr; align-items:center; margin-top:40px;">
          <div class="card"><h3>Department</h3>
            <p style="margin:16px 0;font-size:26px;color:#fff;">Sales · follow-up</p>
            <p style="margin:16px 0;font-size:26px;color:#fff;">Events · registration</p>
            <p style="margin:16px 0;font-size:26px;color:#fff;">Marketing · assets</p>
            <p style="margin:16px 0;font-size:26px;color:#fff;">Ops</p>
          </div>
          <div style="text-align:center;font-size:48px;color:var(--gold);">→</div>
          <div class="card"><h3>Tools the agents use</h3>
            <p style="margin:14px 0;display:flex;gap:10px;align-items:center;">{logo('gmail.svg', 32)} {logo('googlesheets.svg', 32)} Gmail + Sheets only</p>
            <p style="margin:14px 0;font-size:24px;color:#fff;">&lt;/&gt;  100% code</p>
            <p style="margin:14px 0;display:flex;gap:10px;align-items:center;">{logo('openai.svg', 32)} {logo('netlify.svg', 32)} LLMs + Netlify</p>
            <p style="margin:14px 0;display:flex;gap:10px;align-items:center;">{logo('lark.png', 32)} Lark app</p>
          </div>
        </div>
        """,
        9: f"""
        <h1>Agents don’t just chat.<br>They refine automations.</h1>
        <p class="sub">Humans write the playbook. Cursor agents keep the engine sharp.</p>
        <div class="row"><div style="flex:1">{g}</div></div>
        """,
        10: f"""
        <h1>Daily growth checklist, ranked by heat</h1>
        <div class="row">
          <div style="flex:1.4">{g}</div>
          <div class="card" style="flex:.7;">
            <h3>What the agent does</h3>
            <p>1. Summarise the day’s activity</p>
            <p>2. Rate prospects (spiciness 🌶️)</p>
            <p>3. Route P1/P2 to Zen / Tammy / Elicia</p>
            <p>4. Send one company-wide checklist</p>
          </div>
        </div>
        """,
        11: f"""
        <h1>100% recorded. Then the dashboard writes itself.</h1>
        <div class="flow">
          <div class="step">Meeting</div><div class="arrow">→</div>
          <div class="step">Fireflies</div><div class="arrow">→</div>
          <div class="step">Agent extract</div><div class="arrow">→</div>
          <div class="step">Follow-up dashboard</div>
        </div>
        <div class="row"><div style="flex:1">{ff}</div></div>
        """,
        12: f"""
        <h1>We don’t create tasks anymore</h1>
        <p class="sub">Productized work. New opportunity → Lark template pack.</p>
        <div class="row"><div style="flex:1">{lk}</div></div>
        """,
        13: f"""
        <h1>Agents only work if they can touch the business</h1>
        <div class="row"><div style="flex:1">{mcp}</div></div>
        """,
        14: f"""
        <h1>Next: marketing OS, with Hypergrowth IP</h1>
        <p class="sub">Paid Hypergrowth Summit attendee · Dennis Yu marketing suite</p>
        <div class="grid cards-3">
          <div class="card stat"><h3>SEO</h3><p>Agent-led</p></div>
          <div class="card stat"><h3>Paid audit</h3><p>Agent-led</p></div>
          <div class="card stat"><h3>Reputation → sales gap</h3><p>In process now</p></div>
        </div>
        """,
        15: f"""
        <h1>The SuperSeed agent OS</h1>
        <div class="card" style="margin-top:40px;padding:40px;">
          <div class="flow" style="margin-top:0;">
            <div class="step">{logo('github.svg', 28)} GitHub repos</div>
            <div class="arrow">→</div>
            <div class="step">{logo('cursor.png', 28)} Cursor agents / automations</div>
          </div>
          <div class="flow">
            <div class="step">{logo('gmail.svg', 22)} Gmail</div>
            <div class="step">{logo('fireflies.png', 22)} Fireflies</div>
            <div class="step">{logo('lark.png', 22)} Lark</div>
            <div class="step">{logo('googlesheets.svg', 22)} Sheets</div>
            <div class="step">{logo('canva.svg', 22)} Canva</div>
          </div>
          <div class="flow">
            <div class="step">Sales follow-up</div>
            <div class="step">PM templates</div>
            <div class="step">Events app</div>
            <div class="step">Assets</div>
          </div>
        </div>
        """,
        16: f"""
        <h1>Same team. Different operating system.</h1>
        <div class="grid cards-2">
          <div class="card"><h3>Before</h3>
            <p>Manual tasks</p><p>Notes after meetings</p><p>Follow-up in people’s heads</p><p>Assets from scratch</p>
          </div>
          <div class="card" style="border-color:var(--gold);"><h3>After</h3>
            <p>Template tasks auto-created</p><p>Transcript → dashboard</p><p>🌶️ ranked daily checklist</p><p>Asset generation system</p>
          </div>
        </div>
        """,
        17: f"""
        <h1>How to copy this</h1>
        <div class="grid cards-4">
          <div class="card"><h3>1</h3><p>Put work in GitHub by function</p></div>
          <div class="card"><h3>2</h3><p>Connect MCP to real tools</p></div>
          <div class="card"><h3>3</h3><p>Productize tasks</p></div>
          <div class="card"><h3>4</h3><p>Automate daily ops + record every meeting</p></div>
        </div>
        """,
        18: f"""
        <h1>8 people. 25 events.<br>Agents as staff.</h1>
        <p class="sub">This is how SuperSeed actually runs.</p>
        <div class="row">
          <div style="flex:1">{g}</div>
          <div style="flex:1">{mcp}</div>
        </div>
        """,
    }
    return bodies


def screenshot(html_path: pathlib.Path, png_path: pathlib.Path) -> None:
    subprocess.run(
        [
            "google-chrome-stable",
            "--headless=new",
            "--no-sandbox",
            "--disable-gpu",
            "--hide-scrollbars",
            "--allow-file-access-from-files",
            "--force-device-scale-factor=1",
            "--window-size=1920,1080",
            f"--screenshot={png_path}",
            html_path.as_uri(),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def main() -> None:
    bodies = build_bodies()
    index_cards = []
    for n, inner in bodies.items():
        html = slide(n, inner)
        path = SLIDES / f"{n:02d}.html"
        path.write_text(html, encoding="utf-8")
        png = SLIDES / f"{n:02d}.png"
        screenshot(path, png)
        index_cards.append(f'<a href="{n:02d}.html"><img src="{n:02d}.png" width="480"></a>')
        print("slide", n)

    # standalone snapshots
    for name, html in {
        "gmail-checklist.html": SHELL.format(css=CSS, body=f'<div style="padding:24px;background:#0c1018;">{gmail_snapshot()}</div>'),
        "sheets-pipeline.html": SHELL.format(css=CSS, body=f'<div style="padding:24px;background:#0c1018;">{sheets_snapshot()}</div>'),
        "fireflies-extract.html": SHELL.format(css=CSS, body=f'<div style="padding:24px;background:#0c1018;">{fireflies_snapshot()}</div>'),
        "lark-templates.html": SHELL.format(css=CSS, body=f'<div style="padding:24px;background:#0c1018;">{lark_snapshot()}</div>'),
        "mcp-servers.html": SHELL.format(css=CSS, body=f'<div style="padding:24px;background:#0c1018;">{mcp_snapshot()}</div>'),
    }.items():
        p = SHOTS / name
        p.write_text(html, encoding="utf-8")
        screenshot(p, p.with_suffix(".png"))

    (SLIDES / "index.html").write_text(
        "<!doctype html><meta charset=utf-8><title>SuperSeed Agent OS deck</title>"
        "<body style='background:#111;color:#eee;font-family:Inter,sans-serif;padding:24px'>"
        "<h1>SuperSeed multi-agent OS — 18 slides</h1>"
        "<p>Open any slide. Present from 01.html in a 1920×1080 window.</p>"
        + "".join(index_cards)
        + "</body>",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
