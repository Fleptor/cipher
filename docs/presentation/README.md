# CIPHER presentation

Redesigned for first-year students on 7 November 2026: **10 slides**, with an 8–10 minute narrative and an optional dashboard demonstration. The original filenames are retained so existing links continue to work.

- [Editable PowerPoint](CIPHER_Startup_Alley_Pitch.pptx): editable text and diagrams, with speaker notes on every slide.
- [PDF](CIPHER_Startup_Alley_Pitch.pdf): portable presentation fallback.
- [Presenter notes](CIPHER_Presenter_Notes.txt): accessible plain-text narration, deeper engineering details and repository sources.
- [Project website](https://belalhamdan.com/ieee-cs-tech-project/): the same explanation, demo and downloads in one page.

## Presentation flow

1. CIPHER: notice when a device breaks its routine.
2. One laptop, a familiar routine and a possible scan.
3. Architecture: Linux router → Rust sensor → server → operator.
4. Four signals and the limits of sampled measurements.
5. Fifty-report baseline, deviation score and a worked example.
6. Statistical detection and the AI reviewer's role.
7. Cloud isolation gate and operator control.
8. Demonstration with explicit simulation labels.
9. Implemented behavior and remaining validation.
10. Student entry points, project team and next steps.

Terms are defined as they appear. Notes preserve the scoring formula and floors, generic XDP, FlatBuffers/TLS transport, persistence/retry limits, local edge heuristics, privacy boundaries, comparison plan and pilot scope. They distinguish implemented behavior from hardware validation and measured security outcomes. Monitor mode governs new automatic device isolation; it does not turn off kernel packet filters. The model's score is not a calibrated probability.

## Rebuild

```sh
python3 -m venv .local/slides-venv
.local/slides-venv/bin/pip install -r docs/presentation/requirements.txt
.local/slides-venv/bin/python docs/presentation/generate_pitch.py
libreoffice --headless --convert-to pdf --outdir docs/presentation docs/presentation/CIPHER_Startup_Alley_Pitch.pptx
```

Use Georgia, Verdana and DejaVu Sans Mono for the intended rendering, or choose installed alternatives in the generator and inspect the PDF. The generator checks the slide count and shape bounds; inspect the rendered output for text wrapping after any edits. All essential content is text, with high contrast and no meaning conveyed by color alone. The standalone presenter notes are also available when slide reading order or font substitution is a concern.

Use [the demo guide](../DEMO_GUIDE.md) for presentation commands and [the readiness audit](../BOOTH_READINESS.md) for validation scope. The recorded demo is silent, uses synthetic traffic and a scripted reviewer, and does not establish physical enforcement.
