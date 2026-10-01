# Screens preview ownership

Local patch for `im0001gt.screens` 1.15.2, used with Dicey Bar.

Omarchy scopes the replacement bar's shell API to `dicey.bar`. Screens asks
that API for its own service and receives `null`. Its original panel recovery
code interprets the missing service as an unmapped owner and opens a second
confirmation panel after two retries, even when the owner monitor is present.
That secondary panel can then dismiss and revert the global preview.

The patch uses the persisted owner and connected screen names independently
of the service. Only the owner can show the panel, confirm, revert, or cancel
the shared preview. If that monitor disappears, all widgets elect the same
remaining screen. Widgets temporarily lacking a screen during remapping do
not claim ownership. Owner dismissal explicitly rolls back a pending preview
before clearing shared state, without depending on the window-close callback.

The installed user plugin is patched directly; its upstream files are not
vendored here. Plugin updates can overwrite this local change. The patch is
preserved at `patches/im0001gt.screens-1.15.2-panel-ownership.patch`.

To apply it to an unmodified 1.15.2 installation, from this repository:

```bash
patch --dry-run --forward -p1 -d ~/.config/omarchy/plugins/im0001gt.screens \
  < patches/im0001gt.screens-1.15.2-panel-ownership.patch
patch --forward -p1 -d ~/.config/omarchy/plugins/im0001gt.screens \
  < patches/im0001gt.screens-1.15.2-panel-ownership.patch
node tests/test_screens_ownership.js
omarchy plugin validate ~/.config/omarchy/plugins/im0001gt.screens
omarchy restart shell
```

Restart the shell after applying: a rescan alone retained cached QML during
diagnosis. The regression test extracts and exercises the installed methods;
an alternate `Screens.qml` path can be supplied as its argument.

Validation: the unpatched file fails the secondary-panel test. The patched
file passes owner selection, secondary dismissal/Keep/Revert, missing-owner
election, and temporary screen-loss cases. Live Apply/Keep retained a changed
layout beyond the 20-second deadline with one confirmation panel, two bars,
and an unchanged Quickshell PID. Owner dismissal also restores the preview.
