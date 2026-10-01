"""Run the actual island visibility bindings through Qt's hide/show lifecycle."""
import os
from pathlib import Path
import re
import subprocess
import tempfile
import unittest

SOURCE = Path(os.environ.get("DICEY_BAR_SOURCE", Path(__file__).resolve().parents[1] / "plugins/dicey.bar/Bar.qml"))

class BarVisibilityTest(unittest.TestCase):
    def test_islands_reappear_after_remap(self):
        source = SOURCE.read_text()
        for region in ("left", "center", "right"):
            with self.subTest(region=region):
                expression = re.search(r"id: " + region + r"Island\s+visible: ([^\n]+)", source).group(1)
                child = region + "Modules"
                qml = """
import QtQuick
import QtTest
Item {
    id: host
    width: 200; height: 40
    property bool mapped: true
    Item {
        visible: host.mapped
        Rectangle {
            id: island
            visible: EXPRESSION
            Item {
                id: CHILD
                property var entries: [1]
                property bool layoutVisible: true
                visible: layoutVisible && entries.length > 0
            }
        }
    }
    TestCase {
        name: "IslandRemapping"
        when: windowShown
        function test_visibility() {
            compare(island.visible, true)
            for (var i = 0; i < 3; i++) {
                host.mapped = false
                compare(island.visible, false)
                host.mapped = true
                compare(island.visible, true)
            }
            CHILD.entries = []
            compare(island.visible, false)
            CHILD.entries = [1]
            compare(island.visible, true)
        }
    }
}
""".replace("EXPRESSION", expression).replace("CHILD", child)
                with tempfile.TemporaryDirectory() as directory:
                    fixture = Path(directory) / "tst_island.qml"
                    fixture.write_text(qml)
                    result = subprocess.run(
                        ["/usr/lib/qt6/bin/qmltestrunner", "-input", str(fixture)],
                        env={**os.environ, "QT_QPA_PLATFORM": "offscreen", "QT_QUICK_BACKEND": "software"},
                        capture_output=True, text=True,
                    )
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

if __name__ == "__main__":
    unittest.main()
