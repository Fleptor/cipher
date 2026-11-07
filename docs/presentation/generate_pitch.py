#!/usr/bin/env python3
"""Build CIPHER's editable, ten-slide introduction and a plain-text presenter guide.

Requires python-pptx. Run from any directory. Export the PPTX to PDF with
LibreOffice (see README.md). All diagrams are editable PowerPoint shapes.
"""
from pathlib import Path
import json
from PIL import ImageFont

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.oxml.xmlchemy import OxmlElement
from pptx.util import Inches, Pt

ROOT = Path(__file__).resolve().parent
BRAND = ROOT.parents[1] / "website/brand"
THEME = json.loads((BRAND / "theme.json").read_text())
INK, BLUE, MUTED, LINE, PALE = (THEME[k] for k in ("ink", "blue", "muted", "line", "pale"))
ORANGE, DARK = THEME["orange"], THEME["dark"]
DISPLAY, BODY, MONO = THEME["heading_font"], THEME["body_font"], "DejaVu Sans Mono"
SITE = "https://belalhamdan.com/ieee-cs-tech-project/"
GUIDE = []


def text(slide, value, x, y, w, h, size=24, color=INK, bold=False, font=BODY, shape=None):
    shape = shape if shape is not None else slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    shape.left, shape.top, shape.width, shape.height = map(Inches, (x, y, w, h))
    frame = shape.text_frame
    frame.clear()
    frame.word_wrap = True
    frame.margin_left = frame.margin_right = frame.margin_top = frame.margin_bottom = 0
    for i, row in enumerate(value.split("\n")):
        p = frame.paragraphs[0] if i == 0 else frame.add_paragraph()
        p.text = row
        p.alignment = PP_ALIGN.LEFT
        p.font.name, p.font.size, p.font.bold = font, Pt(size), bold
        p.font.color.rgb = RGBColor.from_string(color)
        p.space_after, p.line_spacing = Pt(4), 1.12
        p._p.get_or_add_pPr().append(OxmlElement("a:buNone"))
    return shape


def line(s, x1, y1, x2, y2, color=LINE, width=1):
    sh = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    sh.line.color.rgb, sh.line.width = RGBColor.from_string(color), Pt(width)
    sh._element.spPr.append(OxmlElement("a:effectLst"))


def box(s, x, y, w, h, fill=PALE):
    sh = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    sh.fill.solid()
    sh.fill.fore_color.rgb = RGBColor.from_string(fill)
    sh.line.fill.background()
    sh._element.spPr.append(OxmlElement("a:effectLst"))
    return sh


def base(prs, section, title):
    s = prs.slides.add_slide(prs.slide_layouts[5])
    s.background.fill.solid()
    s.background.fill.fore_color.rgb = RGBColor(255, 255, 255)
    box(s, 0, 0, 13.333333, .97, DARK)
    box(s, 0, .97, 13.333333, .055, ORANGE)
    text(s, "IEEE BAU COMPUTER SOCIETY  /  CIPHER", .68, .17, 9.2, .24, 10, "FFFFFF", True, DISPLAY)
    text(s, section.upper(), .68, .53, 9.1, .28, 12, ORANGE, True, DISPLAY)
    # Place the supplied blue branch mark on white, without recoloring or cropping.
    box(s, 10.05, 0, 3.283333, .97, "FFFFFF")
    logo = s.shapes.add_picture(str(BRAND / THEME["branch_logo"]), Inches(10.93), Inches(.09), width=Inches(1.58))
    logo._element.nvPicPr.cNvPr.set("descr", "IEEE Al-Balqa Applied University, Faculty of Engineering Technology branch logo")
    title_face = ImageFont.truetype(str(BRAND / "fonts/Montserrat-Bold.ttf"), 128)
    title_size = min(32, 32 * (12 * 72 - 8) / (title_face.getlength(title) / 4))
    text(s, title, .68, 1.28, 12.0, 1.0, title_size, bold=True, font=DISPLAY, shape=s.shapes.title)
    line(s, .67, 6.92, 12.65, 6.92, ORANGE, 1.6)
    cs = s.shapes.add_picture(str(BRAND / THEME["society_logo"]), Inches(.68), Inches(7.035), width=Inches(1.1))
    cs._element.nvPicPr.cNvPr.set("descr", "IEEE Computer Society")
    text(s, "CIPHER · The Four Horsemen · @ieee_bau_cs", 2.05, 7.10, 9.2, .22, 10, MUTED)
    text(s, f"{len(prs.slides)} / 10", 11.8, 7.08, .85, .26, 11, MUTED)
    return s


def note(s, say, detail, sources):
    title = s.shapes.title.text
    value = f"SAY\n{say}\n\nTECHNICAL DETAIL / QUESTIONS\n{detail}\n\nREPOSITORY SOURCES\n" + "\n".join(sources)
    s.notes_slide.notes_text_frame.text = value
    GUIDE.append(f"SLIDE {len(GUIDE)+1}: {title}\n{'=' * 64}\n{value}\n")


def row(s, y, heading, body, heading_w=3.0, size=22):
    line(s, .7, y-.16, 12.6, y-.16)
    text(s, heading, .72, y, heading_w, .75, size, INK, True)
    text(s, body, heading_w+1.0, y, 11.55-heading_w, .82, size)


def build_deck():
    GUIDE.clear()
    p = Presentation()
    p.slide_width, p.slide_height = Inches(13.333333), Inches(7.5)
    p.core_properties.title = "CIPHER — A first look at network security"
    p.core_properties.author = "The Four Horsemen / IEEE Computer Society"
    p.core_properties.subject = "Ten-slide student introduction with technical speaker notes"
    p.core_properties.keywords = "CIPHER, eBPF, XDP, Rust, network security, first year"

    s = base(p, "A first look at network security", "CIPHER")
    text(s, "CIPHER", .68, 1.5, 11.8, 1.15, 65, INK, bold=True, font=DISPLAY, shape=s.shapes.title)
    text(s, "Notice when a device\nbreaks its routine.", .72, 3.0, 10.8, 1.6, 39, font=DISPLAY)
    text(s, "Learn normal activity. Explain unusual behavior.\nLet the operator decide how to respond.", .76, 5.05, 11.6, 1.0, 24)
    note(s, "Imagine a small office with laptops, cameras and a router, but no security team. CIPHER learns a routine for each device and highlights changes worth investigating. Today we will follow one laptop from normal activity to an alert.",
         "This is an experimental network detection and response system for small networks, designed to complement an established firewall. It is not a proven replacement for a mature firewall or intrusion prevention system. No measured accuracy, latency, throughput or production-readiness claims are made. Target users are small offices, shops and similar organizations; customer demand and willingness to pay remain hypotheses.",
         ["README.md", "docs/BOOTH_READINESS.md"])

    s = base(p, "The problem", "An allowed connection can still look unusual.")
    text(s, "The laptop’s routine", .75, 2.5, 5.65, .5, 26, INK, True)
    text(s, "A few familiar services.\nA familiar amount of traffic.", .75, 3.3, 5.55, 1.6, 26)
    line(s, 6.6, 2.5, 6.6, 5.5)
    text(s, "A sudden change", 7.05, 2.5, 5.5, .5, 26, INK, True)
    text(s, "Many different service ports.\nMore rejected traffic.", 7.05, 3.3, 5.5, 1.6, 26)
    text(s, "A port is a service’s “door”. Trying many doors can be a scan.", .75, 5.65, 11.9, .5, 21)
    text(s, "Unusual does not automatically mean malicious.", .75, 6.3, 11.9, .45, 22, INK, True)
    note(s, "A port is a numbered endpoint used by a network service. A scan tries many of them, like trying door handles. That change can deserve attention, even when traffic is permitted by the existing firewall. An administrator doing a legitimate scan can look unusual too.",
         "This is an illustrative scenario, not proof of attack detection. Firewalls can already include sophisticated security features. CIPHER adds a per-device behavioral experiment; port or IP filtering alone is not novel. Encrypted legitimate and malicious transfers may share similar metadata. CIPHER does not decrypt HTTPS or establish an attacker's intent.",
         ["Server/src/ai.rs", "Router/ebpf/src/kernel_space.c"])

    s = base(p, "Architecture", "Small summaries travel. Packets stay at the router.")
    entries = [("Linux router", "eBPF / XDP\nTraffic hook"), ("Rust sensor", "Summarize\nmetadata"), ("Rust server", "Statistics\n+ AI review"), ("Dashboard", "Review\n+ respond")]
    for i, (head, body) in enumerate(entries):
        x = .75+i*3.05
        box(s, x, 2.65, 2.65, 2.55)
        text(s, head, x+.16, 2.92, 2.33, .7, 23, INK, True)
        text(s, body, x+.16, 3.95, 2.33, 1.1, 20)
        if i<3:
            text(s, "→", x+2.71, 3.65, .34, .5, 23)
    text(s, "Sensor → server: FlatBuffers reports over a TLS WebSocket", .8, 5.65, 11.9, .5, 22)
    text(s, "Response returns to the sensor; the dashboard waits for acknowledgment.", .8, 6.3, 11.8, .45, 20)
    note(s, "The kernel is the core of Linux. eBPF lets it run small verified programs; XDP is the network receive hook we use. A Rust background program summarizes observations and sends them securely to a Rust server. The dashboard is the operator's view. The AI is not consulted for every packet.",
         "The current loader uses generic/SKB XDP. The sensor aggregates ring-buffer events, including diagnostic flags; HyperLogLog estimates distinct addresses. FlatBuffers is the binary report format; TLS WebSockets provide encrypted transport. The Axum server stores state in SQLite. Baselines, trust, local blocks and a bounded outbox persist across restarts. Reports and commands have acknowledgments and retries. The outbox holds at most 10,000 reports; old entries can be dropped. Deduplication is not exactly-once delivery: a crash between ingestion and receipt storage can duplicate a report. Reports older than 60 seconds are stored without driving current cloud isolation. A map-update acknowledgment does not prove packet-level blocking on hardware.",
         ["Router/daemon/src/main.rs", "Router/daemon/src/network.rs", "Server/src/router_socket.rs", "router.fbs"])

    s = base(p, "Traffic measurements", "Four signals describe a device’s routine.")
    row(s, 2.45, "Incoming bytes", "How much incoming payload was observed.")
    row(s, 3.4, "Outgoing bytes", "How much outgoing payload was observed.")
    row(s, 4.35, "Dropped events", "How many reported packet events were blocked.")
    row(s, 5.3, "Port entropy", "How spread out the observed port use is.")
    text(s, "These are sampled observations, not complete traffic totals.", .75, 6.4, 11.8, .38, 20, INK)
    note(s, "A camera and a laptop need different baselines. We measure traffic size, blocked observations and how varied the ports are. Entropy here means how spread out port use is; it is not simply the number of ports. These four signals feed the server's statistical detector.",
         "Feature order in Server/src/ai.rs: observed_bytes_in, observed_bytes_out, observed_drops, port_entropy. The default single-interface ingress mapping does not yet provide complete bidirectional gateway attribution. Sampled packet events and payload-byte counters must not be presented as connection counts or exact throughput. Reports contain metadata, not message bodies; the kernel nevertheless parses headers and selected DNS fields for filtering. The AI receives structured evidence and recent report context, which can include device identifiers. Avoid saying the system reads no packet fields or that metadata is anonymous.",
         ["Server/src/ai.rs", "Server/src/router_socket.rs", "Router/daemon/src/main.rs", "Router/ebpf/src/kernel_space.c"])

    s = base(p, "Statistical detection", "Learn “normal”, then measure the difference.")
    text(s, "50 reports", .75, 2.45, 4.1, .8, 40, INK, font=DISPLAY)
    text(s, "Build a baseline:\nthe usual level and variation\nfor each signal.", .8, 3.5, 4.5, 1.8, 25)
    line(s, 5.7, 2.45, 5.7, 5.95)
    text(s, "Deviation score", 6.2, 2.55, 6.0, .5, 25, INK, True)
    text(s, "distance from the baseline\n÷ expected variation", 6.2, 3.4, 6.0, 1.3, 29, font=DISPLAY)
    text(s, "Above 3 on any signal → an alert", 6.2, 5.2, 6.0, .9, 23)
    text(s, "Example: a 24 KiB change ÷ 4 KiB scale = 6.  Illustrative values.", .8, 6.35, 11.8, .4, 20, MUTED)
    note(s, "The first fifty reports teach CIPHER a baseline. Afterwards it asks how far a new value is from that routine. It compares the distance to normal variation, so a naturally busy device is not judged like a quiet one. Above three on any signal creates an anomaly, subject to the alert cooldown.",
         "Exact implementation: score_i = abs(value_i - mean_i) / max(std_dev_i, floor_i, abs(mean_i)*0.1). Floors are [4096 bytes, 4096 bytes, 5 dropped events, 0.25 entropy units]. The baseline uses population standard deviation across 50 reports. This is a stabilized deviation score, not an unmodified textbook z-score or a guaranteed probability. Means and deviations are persisted and remain fixed until reset; the first 50 reports should be representative. Example: 10 KiB mean, 34 KiB observation, standard deviation below 4 KiB: effective scale 4 KiB, score 6. Any score strictly greater than 3 is a signal; two signals are needed for cloud automatic isolation. Default per-device alert/review cooldown is 120 seconds. Training data and thresholds require real-world evaluation.",
         ["Server/src/ai.rs: NetworkBaseline::observe", "Server/src/router_socket.rs"])

    s = base(p, "The AI reviewer", "Statistics raise the flag. AI adds an explanation.")
    row(s, 2.55, "Evidence in", "Baseline, unusual measurements and recent reports.", 2.9)
    row(s, 3.65, "Review out", "An explanation, a block recommendation and a score.", 2.9)
    row(s, 4.75, "Operator sees", "Why it was flagged, what happened and what to review.", 2.9)
    text(s, "Model confidence is self-reported, not measured accuracy.", .75, 6.15, 11.8, .65, 23, INK, True)
    note(s, "A language model is a reviewer of the evidence. It can explain possible causes, but it does not prove that an attack happened. Its answer is checked before the response policy can use it. If the reviewer fails, statistical alerts remain available.",
         "Adapters support Anthropic and OpenAI-compatible chat endpoints, including an appropriately configured local server. Expected verdict fields are threat_name, confidence, human_explanation and should_block. JSON is validated; invalid or unavailable reviews cannot authorize cloud isolation. The model's 0–100 score is self-reported and uncalibrated. The default offline demonstration uses a labeled deterministic fixture, not a language model; real provider availability must be verified separately. The value of model review versus statistics alone remains unmeasured. No payload bodies are sent in the review evidence, but metadata may still be sensitive.",
         ["Server/src/ai.rs: Supervisor", "scripts/demo_supervisor.py", "docs/LLM_SETUP.md"])

    s = base(p, "Response policy", "Automatic quarantine needs every gate to pass.")
    text(s, "Cloud-reviewed isolation", .75, 2.3, 11.8, .5, 24, INK, True)
    gates = [("Permission", "Automatic mode is on; the device is not trusted."), ("Evidence", "At least two statistical signals are abnormal."), ("Review", "Valid AI review says block, with a score ≥ 85/100."), ("Fresh decision", "Incident stays open; policy revision has not changed.")]
    for i, (h, b) in enumerate(gates):
        row(s, 3.05+i*.77, h, b, 2.6, 20)
    text(s, "Default: monitor. A person can isolate, restore or trust a device.", .75, 6.26, 11.8, .42, 21, INK, True)
    note(s, "Quarantine means blocking one device at the router. The cloud path needs all four conditions shown here, not just the AI's vote. The sensor checks the policy again when applying an automatic command. The dashboard distinguishes a request from an acknowledged response. A person can restore the device.",
         "This gate describes CLOUD-reviewed automatic isolation only. The edge also has local heuristics (for example, flagged-event volume and TCP reset/SYN ratios), gated by enforcement mode and trust but without an LLM requirement. Existing protocol, IP and DNS packet filters are separate: monitor mode does not disable them or remove existing blocks. Trusted devices still generate alerts and are exempt from automatic cloud/edge isolation; explicitly requested manual isolation remains possible. Granting trust queues restoration of an existing MAC block. Review failure prevents this cloud decision from automatically isolating, but does not disable independent edge protections. Sensor acknowledgment proves its map update, not actual packet blocking in a validated gateway.",
         ["Server/src/router_socket.rs: apply_review", "Server/src/policy.rs", "Router/daemon/src/main.rs", "Router/daemon/src/network.rs"])

    s = base(p, "The demonstration", "Follow one laptop from alert to response.")
    row(s, 2.4, "Monitor", "Simulate a scan. Read the alert and its evidence.", 2.2)
    row(s, 3.4, "Allow response", "Enable automatic mode; repeat and check the acknowledgment.", 2.2)
    row(s, 4.4, "Trust + recover", "Trust the device; test reviewer failure; reset the demo.", 2.2)
    box(s, .75, 5.65, 11.85, .95)
    text(s, "Real backend. Simulated sensor. Scripted offline reviewer.\nThe booth demonstration does not block real packets.", .95, 5.83, 11.45, .7, 20, INK)
    note(s, "Show the actual dashboard, not these slides, for this part. Start with an alert in monitor mode, open its evidence, then demonstrate the response acknowledgment. Trust the device and show that alerts remain. Finally show a failed review and restore the next-visitor state.",
         "From the repository root: bash setup.sh --demo; python3 scripts/booth.py doctor; python3 scripts/booth.py start. In a second terminal run python3 scripts/booth.py tour. Open https://localhost:3100 and use the disposable operator credentials printed by the runner. The deterministic supervisor is explicitly labeled DEMO. Use docs/demo/CIPHER_demo.mp4 if live presentation fails. Manual hooks and rehearsal assertions are documented in docs/DEMO_GUIDE.md. The software rehearsal exercises alerts, trust, response modes, command failures, provider errors and recovery; it does not establish hardware enforcement or detection accuracy.",
         ["docs/DEMO_GUIDE.md", "docs/demo/README.md", "scripts/booth.py"])

    s = base(p, "What is proven so far?", "A working software demo. Hardware proof comes next.")
    text(s, "Implemented + rehearsed", .75, 2.5, 5.65, .55, 25, INK, True)
    text(s, "Statistical alerts + saved baselines\nTrust + incident review\nCommand acknowledgments\nReconnect + retry handling", .75, 3.4, 5.65, 2.65, 23)
    line(s, 6.6, 2.45, 6.6, 6.2)
    text(s, "Still to measure", 7.02, 2.5, 5.55, .55, 25, INK, True)
    text(s, "Actual gateway packet blocking\nCorrect traffic attribution\nMissed attacks + false alarms\nSpeed, resource use + AI value", 7.02, 3.4, 5.55, 2.65, 23)
    note(s, "We can demonstrate the software behavior. The next step is to verify the real gateway: are we seeing the right traffic, and do the response commands really block it? After that, we can measure whether this approach helps more than it disrupts.",
         "The repository's readiness audit reports builds, integration checks, fixture-based provider tests, eBPF compilation and real daemon transport reconnect tests. These are earlier engineering checks, not new hardware tests performed for this presentation. Physical XDP attachment/enforcement, full bidirectional attribution, live provider/account availability, attack accuracy and performance need separate validation. Compare the same hardware with firewall alone, firewall plus statistics, and firewall plus model review. Measure missed threats, false blocks per device-day, CPU/RAM, throughput, tail latency, failure recovery, model cost and operator effort. Telemetry retention is 24 hours; dashboard history is capped at 5,000 reports and exports at 10,000. Shared sensor secrets and MAC-based identity need hardening before broader deployment.",
         ["docs/BOOTH_READINESS.md", "README.md", "tests/integration.py", "tests/supervisor.py"])

    s = base(p, "The Four Horsemen / IEEE Computer Society", "You can understand the system one layer at a time.")
    row(s, 2.5, "Networks + Linux", "Follow a packet through the router and its filters.", 3.3)
    row(s, 3.52, "Rust + data", "Trace one report from the sensor to an incident.", 3.3)
    row(s, 4.54, "Testing + interface", "Reproduce a scenario and make its evidence clearer.", 3.3)
    text(s, "Next: gateway testing, security review and small-office pilot feedback.", .75, 5.85, 11.9, .5, 21)
    link = text(s, SITE, .75, 6.4, 11.9, .35, 16, BLUE)
    link.text_frame.paragraphs[0].runs[0].hyperlink.address = SITE
    note(s, "You do not need to know every technology to start. Choose one layer and follow one report. The website has the slides, a recorded demo, the source and setup instructions. We welcome technical feedback on the gateway and on how to explain the evidence clearly.",
         "The Four Horsemen is the project team. Networks, eBPF, Rust, statistical analysis and interface work describe technical domains, not invented specialist credentials. The practical ask is for infrastructure/security review, hardware testing feedback and small-office design partners after validation. No partnership, hiring offer, customer commitment or immediate live deployment is promised. Suggested first-year exercise: explain why a port scan is only a hypothesis, then identify which isolation gates would prevent a false block. A useful discussion question: what benign activity could also produce an alert?",
         ["README.md", "docs/CIPHER_EXPLAINED.md", "docs/DEMO_GUIDE.md"])

    assert len(p.slides) == 10
    for n, s in enumerate(p.slides, 1):
        for sh in s.shapes:
            # The stock theme supplies shadows even for lines; keep the deck flat.
            for effect in sh._element.findall(".//{http://schemas.openxmlformats.org/drawingml/2006/main}effectRef"):
                effect.set("idx", "0")
            if sh.left < 0 or sh.top < 0 or sh.left+sh.width > p.slide_width or sh.top+sh.height > p.slide_height:
                raise ValueError(f"Slide {n}: out-of-bounds shape {sh.name}")
    return p


if __name__ == "__main__":
    deck = build_deck()
    output = ROOT / "CIPHER_Slide_Deck_Pitch.pptx"
    deck.save(output)
    (ROOT / "CIPHER_Presenter_Notes.txt").write_text("CIPHER — 10-slide student introduction\nSuggested pace: 8–10 minutes, plus optional demo.\n\n" + "\n".join(GUIDE), encoding="utf-8")
    print(f"Created {output} ({len(deck.slides)} slides) and presenter notes")
