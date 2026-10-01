const assert = require("node:assert/strict");
const fs = require("node:fs");
const vm = require("node:vm");
const path = require("node:path");

const source = fs.readFileSync(process.argv[2] || path.join(
  process.env.HOME, ".config/omarchy/plugins/im0001gt.screens/Screens.qml"
), "utf8");

// Exercise the installed QML methods, with only their window/IO boundaries stubbed.
function method(name) {
  const start = source.indexOf(`  function ${name}(`);
  assert.ok(start >= 0, `Missing ${name}`);
  let end = source.indexOf("{", start) + 1;
  let depth = 1;
  while (depth && end < source.length) {
    if (source[end] === "{") depth++;
    if (source[end] === "}") depth--;
    end++;
  }
  return source.slice(start, end);
}

function widget(screen, screens = ["eDP-1", "HDMI-A-1"]) {
  const calls = { show: 0, hide: 0, write: 0, revert: 0, keep: 0 };
  const root = {
    barScreenName: screen, panelOwnerScreen: "HDMI-A-1", careService: null,
    stickyPanel: true, opened: false, pendingConfirm: true, resumeTries: 3,
    controller: { show() { calls.show++; }, hide() { calls.hide++; } },
    barWindow: () => ({ screen: { name: screen } }),
    shouldHoldPanel: () => false,
    restoreLiveTextSize() {}, armDismissGuard() {},
    writePanelState() { calls.write++; root.pendingConfirm = false; },
  };
  const context = vm.createContext({
    root, Quickshell: { screens: screens.map(name => ({ name })) },
    revertTick: { stop() {} },
    keepProc: { set command(value) { calls.keep++; } },
    revertProc: { running: false, set command(value) { calls.revert++; } },
  });
  for (const name of ["isPanelOwner", "forceShowPanel", "close", "keepLayout", "revertLayout"]) {
    root[name] = vm.runInContext(`(${method(name)})`, context);
  }
  return { root, calls };
}

const secondary = widget("eDP-1");
assert.equal(secondary.root.isPanelOwner(), false);
secondary.root.forceShowPanel();
assert.equal(secondary.calls.show, 0, "A missing shared service must not open a second panel");
secondary.root.opened = true;
secondary.root.close();
assert.equal(secondary.calls.hide, 1);
assert.equal(secondary.calls.write, 0, "Secondary dismissal must not cancel the global preview");
secondary.root.keepLayout();
secondary.root.revertLayout();
assert.equal(secondary.calls.keep, 0);
assert.equal(secondary.calls.revert, 0);

const owner = widget("HDMI-A-1");
owner.root.forceShowPanel();
assert.equal(owner.calls.show, 1);
owner.root.close();
assert.equal(owner.calls.write, 1, "Owner dismissal still updates the global panel state");
assert.equal(owner.calls.hide, 1);
assert.equal(owner.calls.revert, 1, "Owner dismissal explicitly restores the pending layout");

const survivors = ["DP-2", "eDP-1"];
const elected = survivors.filter(name => widget(name, survivors).root.isPanelOwner());
assert.deepEqual(elected, ["DP-2"], "Unplugging the owner must elect exactly one surviving panel");
assert.equal(widget("", survivors).root.isPanelOwner(), false, "A remapping widget has no ownership");
assert.equal(widget("eDP-1", []).root.isPanelOwner(), false);
console.log("PASS: owner selection, secondary dismissal, unplug fallback, and remapping");
