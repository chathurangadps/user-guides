# SLERPTECH user guides

Versioned HTML operating guides for the SLERPTECH iDempiere 13 HR and Payroll plugin.

**Share with users:** [Open the Time & Attendance guide](https://chathurangadps.github.io/user-guides/)

- [All editions](https://chathurangadps.github.io/user-guides/versions/)
- [Fixed link to edition 1.1.2](https://chathurangadps.github.io/user-guides/versions/v1.1.2/index.html)
- [Plugin source and deployment packages](https://github.com/chathurangadps/com.slerptech.hrpayroll)

## Current edition

Guide **1.1.2**, dated **13 November 2026**, documents plugin **13.0.0.202611130100**, dictionary Pack In **SLERPTECHAttendanceCapability 1.66.0**, and company masters **SLERPTECHITOperationsMasters 1.0.0**.

The 37 chapters cover company setup, rosters, policies, calendars, CSV upload and preview, exceptions, corrections, supervisor review, overtime, payable decisions, communications, period close/reopen, payroll handoff, reconciliation and troubleshooting. Four cropped application screenshots illustrate selected steps; their captions identify historical demo captures and layout differences. Publication does not certify company policy or replace browser acceptance of the installed release.

Versions **1.1** and **1.1.1** are retained with their own HTML and assets. Edition 1.1.2 updates the Pack In reference after the column-registration fix and adds the hosted guide and edition index.

## Open locally

Open `OPEN-GUIDE.html` or `docs/index.html`. Do not open `content/template.html`: it is the unbuilt template and contains placeholders.

No web server, package installation or CDN is required. JavaScript provides chapter navigation and search; the guide content remains readable without it.

## Update the guide

1. Edit the chapters in `content/guide.json`. Keep chapter IDs stable so shared chapter links continue to work.
2. For a new edition, increase `metadata.guide_version`, set the release date, compatible plugin/Pack In versions and change notes. Never reuse an already published edition number for changed instructions.
3. Update screenshot captions in `content/screenshots.json` and place reviewed, cropped iDempiere screenshots in `docs/assets/screens/`. Keep browser tabs, address bars, credentials and private employee evidence out of the repository.
4. Edit `content/template.html` and `docs/assets/` when layout changes are required.
5. Build and validate:

   ```sh
   python3 tools/build.py
   python3 tools/check.py
   ```

6. Review the built page, search, edition selector, chapter links and screenshots. Check changed operating instructions against the corresponding application release.
7. Commit both source and generated `docs/` files. Preserve all prior `docs/versions/v*/` folders, including their assets. Tag the new release, for example `guide-v1.1.2`.
8. Push to `main`. GitHub Pages publishes the committed `/docs` directory. Verify the Pages deployment and live guide before announcing the update.

The stable root link always opens the newest edition. Use a fixed edition URL for support or deployment documentation, and append a chapter anchor for direct help, for example:

`https://chathurangadps.github.io/user-guides/versions/v1.1.2/index.html#upload-and-preview-attendance`

The builder generates `docs/versions.json` and the edition index from each version's `metadata.json`. It writes the current edition only; old editions remain unchanged when a new version number is used.

## Hosting

GitHub Pages source: branch **main**, folder **/docs**. The `.nojekyll` file serves the generated HTML directly. This repository and its guide are public; readers do not need a GitHub account.

Only static documentation is hosted. Publishing the guide does not deploy the plugin, import a Pack In, change ERP access, or configure an in-system help link.
