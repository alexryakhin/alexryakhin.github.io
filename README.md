# alexriakhin.com

Personal website of Aleksandr Riakhin, served by GitHub Pages from `main` at https://alexriakhin.com. Pushing to `main` deploys it.

## Languages

The homepage is in English plus Arabic, German, Spanish, French, Croatian, Japanese, Korean, Brazilian Portuguese, Russian and Ukrainian (the My Dictionary set plus Portuguese), switched with the language menu in the header. **The homepages are generated — don't edit `index.html` or `<lang>/index.html` by hand:**

- markup: `i18n/template.html` (`{{key}}` placeholders, root-absolute asset paths)
- strings: `i18n/<lang>.json` (English `i18n/en.json` is the source; every language has the same keys)
- then run `python3 scripts/build_pages.py`, which also writes `sitemap.xml` and the hreflang tags

`resume.html` is English only and edited by hand.
