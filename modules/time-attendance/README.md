# Time & Attendance user guide

**Share with users:** [Time & Attendance](https://chathurangadps.github.io/user-guides/modules/time-attendance/)

- [All versions](https://chathurangadps.github.io/user-guides/modules/time-attendance/versions/)
- [Fixed edition 1.2.1](https://chathurangadps.github.io/user-guides/modules/time-attendance/versions/v1.2.1/index.html)
- [All modules](https://chathurangadps.github.io/user-guides/)

## Compatibility

Guide **1.2.1**, dated **13 November 2026**, documents plugin **13.0.0.202611130100**, dictionary Pack In **SLERPTECHAttendanceCapability 1.66.0**, and company masters **SLERPTECHITOperationsMasters 1.0.0**.

The 37 chapters cover company setup, rosters, policies, calendars, CSV upload and preview, exceptions, corrections, supervisor review, overtime, payable decisions, communications, period close/reopen, payroll handoff, reconciliation and troubleshooting. Twelve cropped application screenshots and twelve offline SVG process diagrams explain the main flows. Eight screenshots were captured from the current application on 13 November 2026; four historical examples are retained. Version 1.2.1 reframes all 12 images to the window content only, excluding Favorites / Recent Items, account headers and the application tab strip. Field walkthroughs explain what to check and the expected outcome. The visual index links directly to each flow; images open in an accessible viewer with actual-size inspection. Captions identify draft setup, empty scopes, historical demo captures and layout differences. Publication does not replace browser acceptance of the installed release.

Versions **1.1**, **1.1.1**, **1.1.2** and **1.2.0** retain their own HTML, metadata and assets in `docs/modules/time-attendance/versions/` from the repository root. Moving them into this module did not change their instructions or screenshots.

## Edit and build

1. Edit chapters in this folder's `content/guide.json`. Keep chapter IDs stable so users' chapter links continue working.
2. For changed instructions, increase `metadata.guide_version`, update the date, compatible plugin/Pack In versions and change notes. Never reuse a published version number for changed content.
3. Edit process maps in `content/diagrams.json`. The local SVG renderer in `tools/diagrams.py` generates standalone assets with titles, descriptions and matching text explanations. Keep branches and role boundaries consistent with the implementation.
4. Edit screenshot captions in `content/screenshots.json` and put reviewed, cropped application screenshots in `assets/screens/`. Exclude browser tabs, address bars, credentials and private employee evidence.
5. Edit `content/template.html` and `assets/` for layout changes. Each edition receives its own copy of the working assets.
6. From the repository root run:

   ```sh
   python3 tools/build.py
   python3 tools/check.py
   ```

7. Review the new edition, search, chapter links, screenshots and version selector against the relevant application release. Keep all previously published version folders intact.
8. Commit source and generated files. Tag the release using `time-attendance-guide-v<version>`, then push to `main`. GitHub Pages publishes the committed `/docs` folder.

The module's stable link opens its latest edition. Use a fixed edition and chapter anchor for deployment-specific help:

`https://chathurangadps.github.io/user-guides/modules/time-attendance/versions/v1.2.1/index.html#upload-and-preview-attendance`

The former `/user-guides/versions/v1.1.2/index.html` link redirects here and preserves its chapter anchor. The main website root now lists modules.

## Screenshot capture standard

Use this checklist for every new or replacement application screenshot:

1. Open only the window being documented. Close all other iDempiere window/process/form tabs before capture. Do not discard unsaved work to achieve this; use a clean session if necessary.
2. Hide or collapse the left navigation pane, including Favorites and Recent Items. Expand the target window into the available workspace.
3. Use the relevant company/demo scope and wait for the form, values, results and controls to finish rendering. Keep the captured workflow state authentic; do not stage a success state merely for a picture.
4. Move the pointer away from important controls and dismiss transient menus and tooltips. Keep unrelated browser/extension overlays out of the capture.
5. Export only the target window body and its relevant child tabs. Exclude browser tabs, URL/bookmarks, account header, navigation sidebar and the entire top application tab strip. Keep field labels, values, useful actions and the result being explained readable and intact.
6. Inspect the original-resolution image and the guide's enlarged view. If a long screen needs several views, capture separate labelled sections; identify any content that continues below the image.
7. Record the capture context and crop coordinates/checksum in `content/screenshots.json` and `content/screenshot-crops.json`. Reframe historical evidence from its immutable archived image; do not invent data or rerun a business transaction solely to reproduce a historical screenshot.

The 1.2.1 images are reframed copies of the 1.2.0 captures, not new ERP transactions. Earlier editions retain their original assets for reproducibility.

## Offline use

Open this folder's `OPEN-GUIDE.html`. No server, package installation or CDN is required. JavaScript provides chapter navigation and search; the instructions remain readable without it.
