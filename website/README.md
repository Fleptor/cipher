# CIPHER website

Public URL: https://belalhamdan.com/ieee-cs-tech-project/

A static project presentation built with HTML, CSS and a small progressive-enhancement script. The hero contains an original SVG network illustration with two selectable scenarios; the rest of the page walks through architecture, detection, response, the recorded demo and project resources. No framework, analytics, externally hosted fonts or runtime dependencies. Navigation, technical disclosures and video controls remain usable without JavaScript; motion respects the reader’s reduced-motion preference.

Computer Society branding is shared with the deck and technical sheet through `brand/theme.json`: Montserrat headings, Open Sans body copy, charcoal headers and orange accents. `brand/logos` contains the original BAU branch artwork and the full Computer Society mark. Both fonts are served locally. The branch Instagram informed the restrained grid and dark hero treatment; see `docs/brand/BRAND_AND_SOURCES.txt` for sources.

## Preview

```sh
python3 scripts/build_site.py
python3 -m http.server 8080 --directory .local/site
```

Open http://localhost:8080. The package script generates `brand/brand.css` from the shared tokens, copies the public assets (including both technical-sheet formats), and checks local links and the ten-slide deck. The actual operator dashboard and all runtime files stay outside the publication directory.

## Publish

`.github/workflows/website.yml` packages and deploys the page through GitHub Pages when website or presentation files change on `cipher/booth-readiness` or `main`. The project inherits `belalhamdan.com` from the existing GitHub user site. Do not set the project repository's custom domain to the apex or add a `CNAME`; preserve its `/ieee-cs-tech-project/` path.

The demo branch is named in source links because it contains the integrated dashboard and booth documentation. Update these links and the workflow branch list if that work is merged to a different branch.

The resource thumbnails in `website/assets/` are WebP renders of the actual PDF covers. Refresh them when those covers change (render page one with `pdftoppm`, then convert to WebP). The video poster is packaged directly from `docs/demo/incident-evidence.png`. The network map and signal charts are explicitly labeled illustrations, not live or measured project data.

Content is grounded in the current source, the booth readiness audit and the demonstration guide. The PDF and PPTX are a ten-slide student introduction. The build also keeps the earlier public download filenames as aliases for existing links.

## Verification — 7 November 2026

The redesigned website renders without horizontal overflow at 320, 390, 768, 1024 and 1440 pixels. Local fonts, logos and document thumbnails load; the video, four document downloads and presenter notes return HTTP 200. Video metadata confirms a 78.24-second, 1440 × 900 recording. The scenario controls, mobile navigation, Escape/focus behavior and all four technical disclosures were exercised in Chromium without page errors. Navigation and disclosures also work with JavaScript disabled.

Axe 4.10.3 reported no automated WCAG A/AA violations at desktop and mobile widths, including expanded technical content. Reduced-motion mode disables animation. Desktop and mobile layouts were visually inspected, and the silent video retains an adjacent text alternative. These checks are not a full accessibility certification.

The earlier interactive showcase verification covered its trusted-device and reviewer-outage interactions, responsive layout, keyboard-focusable table and automated accessibility checks.

The PowerPoint and exported PDF each contain ten slides; every slide has presenter notes and the original branch logo. Both the PDF technical sheet and Word export fit one A4 page, and their QR codes decode correctly. Fonts are embedded in PDF exports; rendered layouts were inspected for clipping and text wrapping.
