# engineering-log

engineering-log is a Goku-powered site.

This repo is a consumer of the Goku build-time API rather than a checkout of the Goku source tree.

## Requirements

- Zig 0.15.0-dev.885+e83776595

## Build

From this directory:

```sh
/home/protim/Documents/zig-x86_64-linux-0.15.0-dev.885+e83776595/zig build site
```

The generated site is written to `build/`.

## Preview

```sh
/home/protim/Documents/zig-x86_64-linux-0.15.0-dev.885+e83776595/zig build serve
```

## Notes

- Goku is pinned through `build.zig.zon` to `protimroy/goku` on the `v0.1.0-dev` branch.
- CI is expected to use the same Zig compiler version as local development: `0.15.0-dev.885+e83776595`.
- The site template currently uses the `theme` and `component` hooks.

## Cloudflare Web Analytics

All three sites use the same Cloudflare Web Analytics site token for the hostname `www.protimroy.com`, so traffic can be segmented by path (`/`, `/pro-log/`, `/engineering-log/`). Create a Web Analytics site in the Cloudflare dashboard, select **manual JavaScript installation**, and copy its **public site token** (not an API token). If Cloudflare automatically injects a beacon for this domain, disable automatic injection before using this script to prevent double counting.

After each build and before publishing the generated `build/` directory:

```sh
export CLOUDFLARE_WEB_ANALYTICS_TOKEN="YOUR_32_CHARACTER_PUBLIC_SITE_TOKEN"
python3 scripts/inject_cloudflare_analytics.py --site build
python3 scripts/inject_cloudflare_analytics.py --site build --verify
```

The injector updates all generated HTML pages, including articles, is idempotent, and fails if the token is missing or malformed. It must be rerun **after every build**: `zig build site` regenerates `build/`. Do not run it against source templates. The token is public by design, but do not commit Cloudflare API credentials. The beacon is not included in local previews unless you run the injection step.

### Performance and reliability monitoring

Cloudflare Web Analytics provides traffic and browser-reported Core Web Vitals (LCP, INP, CLS), where supported. Use the dashboard's URL/path filtering to compare the three sites and inspect slow pages. It is not a JavaScript exception or custom-event reporting system. Keep the existing Playwright browser checks for navigation, contrast, console errors, failed requests, broken assets, and responsive overflow; add synthetic uptime checks separately if required. Check the browser Network panel for `beacon.min.js` and Cloudflare's telemetry requests after production deployment. Verify no duplicate beacon and no analytics traffic in local preview.

Privacy: do not add personal identifiers, email addresses, query-string secrets, or custom payloads to analytics. Review the site's privacy disclosure and applicable consent requirements before enabling tracking.
