# x0r-labs site

Static site — no build step, no framework. Three files plus a font from Google Fonts.

```
index.html     the page
styles.css     all styling (design tokens at the top)
favicon.svg    the XOR mark
```

Preview locally:

```bash
python3 -m http.server 8088
# http://localhost:8088
```

Currently deployed at <https://x0r-labs.github.io/site/> via GitHub Pages. Treat that as a
staging URL — send prospects to `x0rlabs.com` once it's connected.

## Before you publish

1. **Change the prices** in `index.html` if the numbers in `gtm/offer.md` differ.
2. **Replace the booking links.** Both CTAs are `mailto:` with a prefilled body. Swap the
   second one for a Cal.com / Calendly link when you have one:

   ```html
   <a class="btn btn--ghost" href="https://cal.com/x0rlabs/20min">Book a 20-minute call</a>
   ```

3. **Update the GitHub link** once the `core` repo is public.
4. **Set the canonical URL** in the `<link rel="canonical">` tag (add one) and in the
   JSON-LD `url` field if the domain changes.

## Deploying

### Recommended: Cloudflare Pages (free, no interstitial)

1. Push this folder to `github.com/X0R-labs/site`.
2. Cloudflare dashboard → Workers & Pages → Create → Pages → Connect to Git.
3. Framework preset: **None**. Build command: empty. Output directory: `/`.
4. Add the custom domain `x0rlabs.com` and `www`.

You get HTTPS, a global CDN, and no anti-bot challenge page. This matters: the current
`xor.ct.ws` hosting puts a JavaScript challenge in front of every first-time visitor, and
some corporate mail scanners will never pass it.

### InfinityFree (current host)

Upload `index.html`, `styles.css` and `favicon.svg` into `htdocs/` via the file manager or
FTP. Keep the same filenames. Clear the cache in the control panel after uploading.

### Netlify drop

Drag the folder onto <https://app.netlify.com/drop>. Done in ten seconds.

## Editing the design

All colours, radii and the max width are CSS custom properties at the top of `styles.css`:

```css
:root {
  --navy: #0b1220;
  --blue: #2b50f0;
  --sky:  #6f8bff;
  --max:  1140px;
}
```

Typography is Schibsted Grotesk, loaded from Google Fonts. If you want zero third-party
requests, download the woff2 files and self-host them — it will also load faster.

## Accessibility

The page passes Lighthouse at 100 for accessibility, best practices and SEO. Keep it that
way: check contrast when you change colours, keep one `<h1>`, and never remove the
`aria-label`s on icon-only links.
