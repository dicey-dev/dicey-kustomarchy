# Automatic Plugin Synchronization

Omarchy rejects symlinked plugin directories. This project instead offers an
optional one-way watcher: project source to the current user's live Omarchy
plugin directory.

## Lifecycle

Run these from any directory; the manager finds its own checkout location.

```bash
~/dicey-kustomarchy/scripts/manage-watcher start
~/dicey-kustomarchy/scripts/manage-watcher stop
~/dicey-kustomarchy/scripts/manage-watcher restart
```

`start` lasts for the current login. To have it start automatically at later
logins, use `enable`; to remove that startup behavior, use `disable`.

```bash
./scripts/manage-watcher enable
./scripts/manage-watcher disable
./scripts/manage-watcher status
```

## Safety and behavior

- The watcher calculates the current username and home directory with `id` and
  `getent`; it does not contain `divy` or another fixed account name.
- It calculates the checkout root relative to the script, so relocating or
  recloning the project is supported. Run `restart` after relocating it to
  regenerate its user-unit files with the new path.
- It only copies project → live configuration. Make changes under `plugins/`;
  direct live edits will be replaced the next time that plugin is synchronized.
- Before a changed plugin replaces its live copy, a staged copy is validated.
  Existing live copies are timestamped backups.
- The watcher asks Omarchy to rescan only after a successful change. It does
  not restart the shell unless your plugin itself requires that separately.
