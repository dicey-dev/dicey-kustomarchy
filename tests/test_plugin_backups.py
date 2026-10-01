import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


class PluginBackupTests(unittest.TestCase):
    def test_install_and_sync_keep_backups_outside_plugin_scan(self):
        source = Path(__file__).resolve().parents[1]
        for script in ("install-plugin", "sync-plugins"):
            with self.subTest(script=script), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                project = root / "project"
                shutil.copytree(source / "scripts", project / "scripts")
                plugin = project / "plugins/dicey.bar"
                plugin.mkdir(parents=True)
                manifest = json.dumps({"id": "dicey.bar"})
                (plugin / "manifest.json").write_text(manifest)
                home = root / "home"
                live = home / ".config/omarchy/plugins/dicey.bar"
                live.mkdir(parents=True)
                (live / "manifest.json").write_text(manifest)
                (live / "version").write_text("original")

                # Stub desktop commands; use the real install/sync scripts.
                bin_dir = root / "bin"
                bin_dir.mkdir()
                commands = {
                    "omarchy": "exit 0\n",
                    "omarchy-shell": "exit 0\n",
                    "getent": 'printf "test:x:1000:1000::%s:/bin/bash\\n" "$DICEY_TEST_HOME"\n',
                }
                for name, body in commands.items():
                    path = bin_dir / name
                    path.write_text("#!/bin/bash\n" + body)
                    path.chmod(0o755)
                env = dict(os.environ, HOME=str(home), DICEY_TEST_HOME=str(home))
                env["PATH"] = str(bin_dir) + os.pathsep + env["PATH"]
                args = ["bash", str(project / "scripts" / script)]
                if script == "install-plugin":
                    args.append("dicey.bar")
                for version in ("first", "second"):
                    (plugin / "version").write_text(version)
                    subprocess.run(args, env=env, check=True, capture_output=True)
                    self.assertEqual((live / "version").read_text(), version)
                    self.assertEqual(
                        list(live.parent.glob("*/manifest.json")),
                        [live / "manifest.json"],
                    )
                backups = home / ".local/state/dicey-kustomarchy/plugin-backups"
                self.assertEqual(
                    sorted(p.read_text() for p in backups.glob("*/version")),
                    ["first", "original"],
                )


if __name__ == "__main__":
    unittest.main()
