# engineering-log

engineering-log is a Goku-powered site.

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

- This site consumes Goku through `build.zig.zon`.
- This site is pinned to the current `v0.1.0-dev` Goku line for Zig `0.15.0-dev.885+e83776595`.
- The template is wired for the `theme` and `component` hooks used by this site.
