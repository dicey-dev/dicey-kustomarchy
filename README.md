# dicey-kustomarchy

Personal, version-controlled Omarchy customizations for this machine.

The project keeps the source of user-owned shell plugins and documents every
change made on top of packaged Omarchy. It never edits `/usr/share/omarchy`.

## Current inventory

| Customization | Source | Live location | State |
| --- | --- | --- | --- |
| Dicey floating-island bar | `plugins/dicey.bar` | `~/.config/omarchy/plugins/dicey.bar` | Active |
| Dicey lock-screen experiment | not managed yet | `~/.config/omarchy/plugins/dicey.lock` | Disabled |

The bar retains Quattro's widgets, PAM/session locking, and theme integration.
It adds three floating islands, a five-pixel top margin, gentler corners, and
automatic shell recovery after Omarchy monitor-scale changes.

## Layout

```text
plugins/     User-owned Omarchy plugins, ready to install
scripts/     Explicit install and status helpers
docs/        Design notes and operational guidance
```

## Use

Check the current live state:

```bash
./scripts/status
```

Validate the tracked bar without changing anything:

```bash
omarchy plugin validate plugins/dicey.bar
```

Install or update a tracked plugin intentionally:

```bash
./scripts/install-plugin dicey.bar
omarchy bar use dicey.bar
```

Omarchy rejects symlinked plugin directories, so `install-plugin` copies the
tracked source into the live location and creates a timestamped backup first.
Restart the shell only when a live reload is insufficient:

```bash
omarchy restart shell
```

## Optional automatic synchronization

Omarchy does not accept symlinked plugin folders. If you want project edits to
be copied to the live plugin directory automatically, manage the optional
user-level watcher:

```bash
./scripts/manage-watcher start
./scripts/manage-watcher stop
./scripts/manage-watcher restart
```

Use `enable`, `disable`, or `status` in place of `start` for persistent startup
control or inspection. See [watcher documentation](docs/watcher.md) for its
one-way source-of-truth and backup behavior.

## Adding a customization

1. Add its portable source under `plugins/<id>/`.
2. Document its purpose, dependencies, and activation command in `docs/`.
3. Validate with `omarchy plugin validate plugins/<id>`.
4. Install it with the helper, activate it explicitly, and test its runtime path.
5. Review and commit the project changes.

Do not copy secrets, tokens, caches, screenshots, or generated runtime state
into this repository.
