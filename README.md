# SLERPTECH user guides

User documentation organized by **module**, then **guide version**.

**Share the module directory:** [SLERPTECH User Guides](https://chathurangadps.github.io/user-guides/)

| Module | Latest guide | Version history |
| --- | --- | --- |
| Time & Attendance | [Open guide](https://chathurangadps.github.io/user-guides/modules/time-attendance/) | [All editions](https://chathurangadps.github.io/user-guides/modules/time-attendance/versions/) |

## Repository structure

```text
modules/
  time-attendance/
    README.md           # Module compatibility and maintenance instructions
    OPEN-GUIDE.html      # Local shortcut to this module
    content/            # Editable chapter text, template, diagram definitions and screenshot captions
    assets/             # Working styles, scripts, process diagrams and cropped screenshots
    tools/              # Module-specific build and validation

docs/                   # GitHub Pages publishing directory
  index.html            # Module directory
  modules/
    time-attendance/
      index.html        # Opens this module's latest edition
      versions.json
      assets/
      versions/
        index.html      # This module's version history
        v1.1/
        v1.1.1/
        v1.1.2/
        v1.2.0/
        v1.2.1/

tools/                  # Builds and checks all registered modules
modules.json            # Registered documentation modules
```

The complete guides and version assets live under their module, not at the site root. The small files left under `docs/versions/` redirect previously shared URLs to their new module paths, preserving chapter bookmarks.

## Update and publish

Read the [Time & Attendance maintenance instructions](modules/time-attendance/README.md) before editing that module. Increase its guide version for changed instructions and keep all previous version folders intact.

```sh
python3 tools/build.py
python3 tools/check.py
```

Commit the source and generated `docs/` files, then push to `main`. GitHub Pages publishes **main /docs** automatically. Verify the deployment before sharing an update.

Each module has its own versions and module-prefixed release tags, for example `time-attendance-guide-v1.2.1`. The earlier `guide-v1.1.2` tag is retained at its original commit.

To add another module, create its source/assets/build tools under `modules/<module-id>/`, register it in `modules.json`, and have its builder publish into `docs/modules/<module-id>/versions/v<version>/`. The shared builder discovers each registered module's version manifest and updates the module directory.

## Open locally

Open `OPEN-GUIDE.html` for the module directory, or `modules/time-attendance/OPEN-GUIDE.html` for Time & Attendance. Do not open a `content/template.html` file: templates require building first.

This is public static documentation. Publishing does not deploy the plugin or change ERP settings. [Plugin source and deployment packages](https://github.com/chathurangadps/com.slerptech.hrpayroll) are maintained separately.
