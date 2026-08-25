# brandandpr

## Cursor Cloud specific instructions

### What this repo is

This repo currently holds a **static presentation deck generator** for the
"SuperSeed multi-agent OS" pitch. The `main` branch is a stub (only this file
and `README.md`); the actual deck lives under `deck/` on the feature branch
`cursor/ai-agent-os-deck-a42f`. Check out that branch (or work from a merged
state) to see/build the deck.

There is no web service, backend, database, or test/lint/build tooling — the
only "app" is the deck generator script.

### Building / running the deck (the core workflow)

From the `deck/` directory:

```bash
cd deck
python3 generate_deck.py
```

This regenerates, in place:
- `slides/NN.html` + `slides/NN.png` (18 slides, 1920×1080)
- `snapshots/*.html` + `snapshots/*.png` (5 UI mock snapshots)
- `slides/index.html` (contact sheet)
- `superseed-agent-os.pdf` (18-page PDF stitched from the slide PNGs)

There are no CLI args; running the script rebuilds everything. Expect ~12s.

### Non-obvious gotchas

- **PNG rendering uses headless Chrome, not a Python image lib.** The script
  shells out to `google-chrome-stable --headless=new --screenshot=...`. Chrome
  is preinstalled in the Cloud environment; if it is missing or renamed the
  screenshots silently fail (the subprocess stdout/stderr are sent to
  `DEVNULL`), leaving stale/blank PNGs. Verify Chrome with
  `google-chrome-stable --version` if slides look wrong.
- **PDF stitching needs Pillow** (`PIL`), the repo's only pip dependency. It is
  installed by the environment update script. Pillow can open the individual
  PNGs but cannot re-open the generated PDF — that is expected, not a failure.
- Fonts are pulled from Google Fonts at render time (`@import` of Inter). The
  environment has unrestricted egress, so this works; offline rendering would
  fall back to a system sans-serif.
