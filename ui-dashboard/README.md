# CIPHER operator dashboard

Project team: **The Four Horsemen** — Zakaria Alqarra, Belal Hamdan, Raneem Abdullah and Ayham Idais. **Contributor:** Omar Eid.

The Rust server serves this directory as its authenticated operator interface.
`index.html`, `styles.css`, and `app.js` are the active frontend. The older
stylesheets in `css/` are not loaded by this interface.

## Computer Society identity

The console uses the promotional site's charcoal navigation, orange emphasis,
warm white panels, Montserrat headings, Open Sans body text, and CIPHER monogram.
The original Computer Society and BAU branch logos appear on a white field with
clear space. Their provenance and font licenses are documented in
`docs/brand/BRAND_AND_SOURCES.txt` and the bundled `assets/brand/fonts/` licenses.

Operational colors have separate meanings: green for allowed/healthy states,
amber for pending/review states, and red for blocked/failed states. Labels remain
visible, and the two traffic series differ in line style as well as color.
Isolation and enforcement confirmations use the danger button treatment.

The source of the shared palette, fonts, and logos remains `website/brand/`.
Refresh the dashboard's checked-in copy after changing those assets:

```sh
python3 scripts/build_brand.py --dashboard
```

This copies the public brand assets and favicon into `ui-dashboard/assets/`.
Keeping these files in the dashboard allows the existing server and offline demo
to serve the UI without external font requests or changes to backend routing.
Do not edit the generated copies directly. Normal public-site packaging does not
include the authenticated dashboard.

## Local review

```sh
python3 scripts/booth.py start --llm fixture
python3 scripts/booth.py hook scan
```

Use the disposable operator credentials printed by the runner. The fixture uses
the real backend with a simulated sensor and a scripted reviewer; it does not
control physical devices. See `docs/DEMO_GUIDE.md` for the complete workflow.

Checked in Chromium on 7 November 2026: all five views at desktop and mobile
sizes, authenticated and signed-out states, action and sign-in dialogs, device
search/filtering, CSV export, trust/revoke, isolate/restore acknowledgments,
policy changes, incident review/reopening, and evidence retained across refresh.
The mobile menu removes closed navigation from keyboard focus and restores focus
on Escape. Automated WCAG A/AA scans passed for all views at 320, 390, and 1440
pixels and for the dialogs; this is not a full accessibility certification.
