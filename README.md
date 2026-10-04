# Metachlorian website

A static, responsive marketing site for [Metachlorian](https://github.com/JeremySNR/Metachlorian), with an illustrated cinematic hero, local sample-library interactions, actual product screenshots, and two technical guides.

## Run locally

```sh
python3 -m http.server 4173 --bind 127.0.0.1 --directory dist
```

Open `http://127.0.0.1:4173`. There is no framework install or build step. `dist/` is the deployable source. All content and SEO metadata are served as HTML; JavaScript progressively enhances navigation, the demo, dialogs and installation tabs.

## Checks

```sh
python3 scripts/check-site.py
node --check dist/app.js
python3 design-system/build.py --output dist/foundations.css --check
python3 design-system/verify.py
```

The static checker verifies internal links and anchors, assets, heading counts, IDs, metadata, JSON-LD and the XML sitemap. Browser checks cover mobile/desktop layouts, search and rights filters, empty-state recovery, shot dialogs, keyboard-operated installation tabs, copy feedback, FAQ disclosure and guide navigation.

## Content and editing

- `dist/index.html`: landing page and structured data.
- `dist/styles.css`: shared responsive styles.
- `dist/app.js`: deterministic sample-library demo and small interface interactions.
- `scripts/generate-guides.py`: guide content and generation; updates the two guide pages and crawl files. Run after updating shared navigation or guide content.
- `dist/guides/`: crawlable self-hosting and MCP guides.
- `.openai/hosting.json`: Sites identity and static hosting configuration.
- `vercel.json`: Vercel configuration; serves `dist/` with no build step and applies the same headers as `dist/_headers`.

The demo uses six illustrative records and generated still imagery. It does not connect to a running Metachlorian backend, analyse uploads, or imply real permissions. The product screenshot is from the actual repository. Product facts and commands were checked against commit `2d07f6f9743848c526d66b106fb4d9cba8ea8bcb` on 4 October 2026.

## SEO and performance

Three static HTML routes, unique titles/descriptions/canonicals, SoftwareApplication/WebSite/TechArticle/BreadcrumbList structured data, semantic headings, descriptive link text, sitemap and robots.txt. No invented reviews or ratings. Rich results and rankings are not guaranteed.

The initial artwork has responsive WebP variants (~85 KB mobile, ~257 KB desktop). Fonts are self-hosted; images below the fold are lazy loaded. The site's JavaScript compresses to roughly 3.5 KB gzip. Reduced motion is respected. Real-world Core Web Vitals still need measurement on the public deployment with actual traffic.

The Sites deployment starts private. Search-engine indexing requires a public launch. When adding the production domain, update canonical/Open Graph URLs, the origin in `scripts/generate-guides.py`, sitemap and robots.txt. Then submit the sitemap in Search Console. Cache headers use a short asset lifetime because filenames are not content-hashed.

## Art and attribution

The built-in image-generation tool produced these original assets:

- `dist/assets/coast-1600.webp` and `coast-800.webp`: cinematic aerial photograph of a rugged Atlantic coastline at golden hour, dark teal ocean, warm sunlit cliffs, photographic texture and subtle film grain; no people, text, UI, logos or watermark.

The hero reel is now drawn in `dist/reel.js`: a projected film loop with five original code-drawn landscapes, perspective-correct mesh strips, a fixed focus aperture, and subtle pointer response. It needs no external images or runtime dependencies. A visible pause/play control, reduced-motion default, offscreen/hidden-tab suspension, and a static `reel-poster.webp` fallback cover accessibility and resource use. The illustrative coastal stills elsewhere in the demo remain generated imagery.

`dist/assets/search-interface.webp` is optimised from `review/m4/screens/01-search-results--desktop-light.jpg` in the Apache-2.0-licensed product repository. See [the product licence](https://github.com/JeremySNR/Metachlorian/blob/HEAD/LICENSE).

Bricolage Grotesque and DM Sans are bundled under the SIL Open Font License; full licences are in `licences/`.

## Design research

- [Lusion](https://lusion.co/): sculptural 3D imagery and interactive visual storytelling informed the revised art direction.
- [Siena Film Foundation](https://siena.film/): expressive film-led identity and immersive composition.
- [Frame.io](https://frame.io/): visual product storytelling and concrete workflow explanation.
- [Linear](https://linear.app/): clarity of hierarchy and product presentation.
- [Google Search developer guidance](https://developers.google.com/search/docs/fundamentals/get-started-developers): crawlable content, descriptive metadata and structured information.

These are design references, not measured claims about those sites' conversion rates, search rankings or performance. The layout, copy and generated art are original to this website.


## Family identity and design system

The approved logo is installed in the header/footer of all three pages. Its SVG embeds the original PNG unchanged; the compact mark and favicon use the same artwork with different viewports. See [the family design system](design-system/README.md) for exact-source verification, semantic tokens, marketing/library/editor profiles, accessibility contracts, component guidance and adoption in Metachlorian and Cutawan.

`dist/foundations.css` is generated from `design-system/tokens.json`. `dist/tokens.css` adapts those foundations for this site; `dist/family.css` applies shared identity and component rules. Keep these styles on generated guide pages by editing `scripts/generate-guides.py` as well.

### Animated hero verification

`python scripts/check-reel-browser.py` exercises the animation and hero search at desktop/mobile sizes, pause/resume, offscreen suspension, reduced motion, keyboard control and the no-JavaScript poster. It requires Playwright 1.55.0 and Chromium. CI saves screenshots as `reel-browser-review` for visual review. The poster is rendered from the same `createRenderer` exported by `dist/reel.js`, at 1800 × 1300.
