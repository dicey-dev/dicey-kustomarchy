# Dicey Bar

`dicey.bar` is a clone of Omarchy's first-party `omarchy.bar` plugin.
It is deliberately user-owned so Omarchy package updates do not overwrite its
floating-island presentation.

Omarchy rejects symlinked plugin directories. The project copy is the source of
truth; use `./scripts/install-plugin dicey.bar` to copy, validate, and rescan
the live plugin safely.

## What changed

- The top/bottom bar surface is transparent; left, center, and right sections
  paint their own themed rounded islands.
- Islands use `Color.bar.background` and `Style` tokens, so theme and font
  changes continue to apply.
- The bar has a 5px top offset and 6px island corners.
- `ScaleSafeRemap.qml` remaps layer surfaces after monitor geometry changes.
- Widget loaders preserve their instances while monitor changes remap the
  bar surface; monitor changes do not restart the shell.
- Island visibility follows configured entries, not child effective visibility,
  so remapping cannot latch all three islands permanently hidden.

## Activation

```bash
omarchy bar use dicey.bar
omarchy restart shell
```

To return to the packaged bar:

```bash
omarchy bar use omarchy.bar
omarchy restart shell
```
