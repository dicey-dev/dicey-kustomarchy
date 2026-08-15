import QtQuick

// Hyprland needs layer surfaces to be unmapped and remapped when a monitor
// changes scale as well as when it moves. The stock guard watches x/y only;
// this user-bar variant also watches the screen's logical dimensions and DPI.
Item {
  id: root

  required property var window
  readonly property var screen: window ? window.screen : null
  property bool remapping: false

  visible: false

  Timer {
    id: settleTimer
    interval: 250
    onTriggered: root.remapping = true
  }

  Timer {
    interval: 75
    running: root.remapping
    onTriggered: root.remapping = false
  }

  Connections {
    target: root.screen

    function queueRemap() { settleTimer.restart() }
    function onXChanged() { queueRemap() }
    function onYChanged() { queueRemap() }
    function onWidthChanged() { queueRemap() }
    function onHeightChanged() { queueRemap() }
    function onDevicePixelRatioChanged() { queueRemap() }
  }
}
