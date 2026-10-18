# kikomono-hugo project instructions

Purpose: publish useful AI guides and monitor public official-source VPS offers and prices. Runtime: Hugo 0.167.0 static site; Python stdlib for scraping and prebuild.

## Architecture

- `content/` — Markdown source. Article bodies are raw HTML blocks (converted once from the old Python build; do not hand-edit bodies unless the source article changes).
- `tools/prebuild.py` — runs before every `hugo` build. Generates: `hugo.yaml`, `data/active_offers.json`, `data/ai_tools.json`, `data/schemas.json`, `data/sitemap.json`, `content/providers/*.md`, `content/deals/*.md`, `static/data/offers.json`, `static/_headers`, `static/robots.txt`. Stdlib only. Reuses `active_offers`/`offer_schema` from `build.py`.
- `tools/convert_content.py` — one-shot converter (old build → Markdown). Not part of the deploy pipeline; keep for reference.
- `layouts/` — Hugo templates. `_default/baseof.html` is a monolithic shell (no `{{ block }}`); page bodies come from `.Content` or type partials (`p-hosting`, `p-offers`, `p-compare`, `p-provider`, `p-deal`, `p-guides`).
- `build.py` / `scraper.py` — kept for business logic (`active_offers`, `offer_schema`) and source checks. `build.py`'s HTML output is no longer deployed.
- Single source of truth: `site-config/site.conf`; both `scraper.py` and `tools/prebuild.py` read it.

## Byte-parity contract

The Hugo output must stay byte-identical to the old Python build (verified against `site_old/`). Quirks preserved deliberately:
- `esc` partial replicates Python `html.escape` exactly (`& < > " '` → `&amp; &lt; &gt; &quot; &#x27;`).
- JSON-LD is pre-rendered by prebuild with Python `json.dumps` separators and the `\u003c` escape; templates output it via `safeJS`.
- Byline injection: for `/ai-tools/free-ai-tools-*` pages, baseof replaces the first `</h1>` with `<p class="byline">By Lika</p>` (replicates build.py).
- `lead`/`trail` front matter: exact leading/trailing newline counts inside `<main>` (Goldmark normalizes them; baseof re-applies).
- `strings.TrimRight "\n" $main` — note Hugo's argument order is CUTSET first, STRING second.
- `disableHugoGeneratorInject: true` in generated hugo.yaml; no `--minify`.
- Providers section list page suppressed via `build: {render: false}` on generated `_index.md` (`_build` was removed in Hugo 0.167; use `build`).
- Use `hugo.Data`, not the deprecated `.Site.Data`.

## Allowed / Never

- Allowed: fix parsers, edit templates/partials, add public official sources, test, deploy.
- Sources: read only public official price pages, feeds or sitemaps; check robots first; never bypass a failure.
- One record = provider + real plan name + currency, deduplicated; must have a current price source and purchase conditions.
- Config change => re-run scrape, prebuild and build; test that removing a provider removes its pages and navigation.
- Domain switch => write back base_url and domain with the real Pages domain or activated custom domain; verify canonical/sitemap/robots externally after building.
- Affiliation: only use approved, legitimate affiliate links; with no approval keep bare official links and state clearly there is no commission.
- Never: invent offers, prices, commissions or expiry dates; fake traffic; buy followers; bypass anti-bot; brand-keyword bidding; cookie injection; self-referral.
- Never: commit credentials or tokens; publish unverified offers; claim domain age guarantees rankings.
- Verify with: `python -m unittest discover -s tests`; `python scraper.py`; `python tools/prebuild.py`; `hugo -d site`; `python validate.py`; then check live content, schema and sitemap.

## Deploy

Cloudflare Pages builds from this repo: build command `python tools/prebuild.py && hugo -d site`, `HUGO_VERSION=0.167.0`. The 6-hour `update.yml` workflow scrapes sources and commits fresh `data/offers.json`.
