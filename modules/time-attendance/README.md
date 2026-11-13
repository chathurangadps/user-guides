# Time & Attendance user guide

**Share with users:** [Time & Attendance](https://chathurangadps.github.io/user-guides/modules/time-attendance/)

- [All versions](https://chathurangadps.github.io/user-guides/modules/time-attendance/versions/)
- [Fixed edition 1.1.2](https://chathurangadps.github.io/user-guides/modules/time-attendance/versions/v1.1.2/index.html)
- [All modules](https://chathurangadps.github.io/user-guides/)

## Compatibility

Guide **1.1.2**, dated **13 November 2026**, documents plugin **13.0.0.202611130100**, dictionary Pack In **SLERPTECHAttendanceCapability 1.66.0**, and company masters **SLERPTECHITOperationsMasters 1.0.0**.

The 37 chapters cover company setup, rosters, policies, calendars, CSV upload and preview, exceptions, corrections, supervisor review, overtime, payable decisions, communications, period close/reopen, payroll handoff, reconciliation and troubleshooting. Four cropped application screenshots illustrate selected steps. Captions identify historical demo captures and layout differences; publication does not replace browser acceptance of the installed release.

Versions **1.1**, **1.1.1** and **1.1.2** retain their own HTML, metadata and assets in `docs/modules/time-attendance/versions/` from the repository root. Moving them into this module did not change their instructions or screenshots.

## Edit and build

1. Edit chapters in this folder's `content/guide.json`. Keep chapter IDs stable so users' chapter links continue working.
2. For changed instructions, increase `metadata.guide_version`, update the date, compatible plugin/Pack In versions and change notes. Never reuse a published version number for changed content.
3. Edit screenshot captions in `content/screenshots.json` and put reviewed, cropped application screenshots in `assets/screens/`. Exclude browser tabs, address bars, credentials and private employee evidence.
4. Edit `content/template.html` and `assets/` for layout changes. Each edition receives its own copy of the working assets.
5. From the repository root run:

   ```sh
   python3 tools/build.py
   python3 tools/check.py
   ```

6. Review the new edition, search, chapter links, screenshots and version selector against the relevant application release. Keep all previously published version folders intact.
7. Commit source and generated files. Tag the release using `time-attendance-guide-v<version>`, then push to `main`. GitHub Pages publishes the committed `/docs` folder.

The module's stable link opens its latest edition. Use a fixed edition and chapter anchor for deployment-specific help:

`https://chathurangadps.github.io/user-guides/modules/time-attendance/versions/v1.1.2/index.html#upload-and-preview-attendance`

The former `/user-guides/versions/v1.1.2/index.html` link redirects here and preserves its chapter anchor. The main website root now lists modules.

## Offline use

Open this folder's `OPEN-GUIDE.html`. No server, package installation or CDN is required. JavaScript provides chapter navigation and search; the instructions remain readable without it.
