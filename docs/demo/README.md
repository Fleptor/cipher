# Demonstration evidence and fallback

Project team: **The Four Horsemen** — Zakaria Alqarra, Belal Hamdan, Raneem Abdullah and Ayham Idais. **Contributor:** Omar Eid.

- [CIPHER_demo.mp4](CIPHER_demo.mp4): approximately 86 seconds, silent, with captions and team credits. Shows the actual dashboard, statistical alert, explicit enforcement, simulated isolation acknowledgment, permanent trust, provider outage and reset.
- [incident-evidence.png](incident-evidence.png): expanded detection evidence in monitoring mode.
- [trusted-alert.png](trusted-alert.png): a new alert remains visible after permanent trust.
- [rehearsal-results.json](rehearsal-results.json): 17 checks against the real backend and offline fixture.

Recorded on 17 October 2026 using the isolated `BOOTH_DEMO` network. Traffic, sensor acknowledgments and supervisor responses are simulated. The backend, detector, persistence and dashboard controls are real. No real packet was blocked, no paid model was called, and no customer data or credentials are included. Presentation captions were added to the recorded browser view; they are not part of the application UI.

- [../showcase/plain-english-incidents.png](../showcase/plain-english-incidents.png): incident history with the "In plain English" summaries (18 October 2026, fixture session).

These artifacts support the software walkthrough, not attack-detection accuracy or physical enforcement claims. Re-run `python3 scripts/booth.py rehearse` against a running fixture before presenting on another machine. For narration and setup see [the demo guide](../DEMO_GUIDE.md).

## Team credit card

An eight-second Computer Society credit card was appended on 7 November 2026.
The original 78.24 seconds retain every frame and timestamp. Names come from
`docs/project-credits.json`; the MP4 metadata also lists the team and contributor.

To rebuild, use the original recording without credits, the brochure Python
dependencies, FFmpeg and Poppler (`pdftoppm`):

```sh
mkdir -p .local
git show f7720bf:docs/demo/CIPHER_demo.mp4 > .local/demo-recording.mp4
.local/brochure-venv/bin/python docs/demo/add_credits.py --input .local/demo-recording.mp4 --output docs/demo/CIPHER_demo.mp4
```

Do not use the already credited output as the input, or credits will be appended
again. The public video is 86.24 seconds at 1440 × 900 and 25 frames per second.
