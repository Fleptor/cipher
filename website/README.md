# CIPHER website

Public URL: https://belalhamdan.com/ieee-cs-tech-project/

A single static page: HTML, CSS, a small SVG favicon and existing project materials. No JavaScript, framework, analytics, external fonts or runtime dependencies. Navigation uses anchors, explanations use native disclosure elements, and the recorded demo uses native video controls with a text walkthrough.

## Preview

```sh
python3 scripts/build_site.py
python3 -m http.server 8080 --directory .local/site
```

Open http://localhost:8080. The package script copies an explicit list of public assets and checks local links and the ten-slide deck. The actual operator dashboard and all runtime files stay outside the publication directory.

## Publish

`.github/workflows/website.yml` packages and deploys the page through GitHub Pages when website or presentation files change on `cipher/booth-readiness` or `main`. The project inherits `belalhamdan.com` from the existing GitHub user site. Do not set the project repository's custom domain to the apex or add a `CNAME`; preserve its `/ieee-cs-tech-project/` path.

The demo branch is named in source links because it contains the integrated dashboard and booth documentation. Update these links and the workflow branch list if that work is merged to a different branch.

Content is grounded in the current source, the booth readiness audit and the demonstration guide. The PDF and PPTX keep their existing filenames for compatibility, although the presentation is now a ten-slide student introduction.

## Verification — 7 November 2026

Browser checks passed at 320, 390, 768 and 1440 CSS pixels, with all disclosures expanded, and at 200% zoom. Checked keyboard skip navigation and disclosure toggles, section anchors, asset responses, the actual PowerPoint download and video metadata. No JavaScript errors occurred. Axe 4.10.3 reported no automated WCAG A/AA violations at desktop and mobile widths. Its manual-review items were the decorative arrow (white on the dark teal button) and the silent video (no audio stream, with an adjacent text alternative); both were inspected. This is not a full accessibility certification.

The PowerPoint and exported PDF each contain ten slides. Each slide has speaker notes; the PDF contains selectable text. The exports were visually inspected for clipping and layout.
