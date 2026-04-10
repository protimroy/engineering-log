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
