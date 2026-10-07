"""Exercise opt-in renderer and startup proof without a real daemon."""
from pathlib import Path
import os
import subprocess
import tempfile
import unittest

RECIPE = Path(__file__).resolve().parent
IMAGE = 'registry.invalid/worker@sha256:' + 'a' * 64


class ValidationRecipeTest(unittest.TestCase):
    def test_companion_readiness_uses_its_actual_socket(self):
        # Exercise the startup readiness stage with the CLI's real default-host
        # behavior; the main container's environment is not inherited here.
        stage = (RECIPE/'daemon-validation-preflight.sh').read_text().split('parent_limit=', 1)[0]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            stage = stage.replace('/run/docker/validation-accounting.json', str(root/'receipt'))
            commands = {
                'docker': 'test "${DOCKER_HOST:-unix:///var/run/docker.sock}" = unix:///run/docker/docker.sock || exit 1; case "$*" in "info") exit 0;; "info --format "*) echo "2 cgroupfs";; *) exit 2;; esac',
                'date': 'n=0; test ! -f "$CLOCK" || n=$(cat "$CLOCK"); n=$((n+10)); echo "$n" > "$CLOCK"; echo "$n"',
                'sleep': 'exit 0',
            }
            for name, body in commands.items():
                command = root/name
                command.write_text('#!/bin/sh\n' + body + '\n')
                command.chmod(0o755)
            for inherited in ('', 'unix:///wrong.sock'):
                with self.subTest(inherited=inherited):
                    (root/'clock').unlink(missing_ok=True)
                    result = subprocess.run(['sh', '-ceu', '/bin/sleep 30 & daemon_pid=$!\n' + stage],
                        capture_output=True, text=True, timeout=5,
                        env={**os.environ, 'PATH': f"{root}:{os.environ['PATH']}",
                             'CLOCK': str(root/'clock'), 'DOCKER_HOST': inherited})
                    self.assertEqual(result.returncode, 0, result.stderr)

    def test_default_renderer_does_not_enable_validation(self):
        result = subprocess.run(['bash', str(RECIPE/'render-template.sh'), IMAGE],
                                capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn('FULL_WORKER_CHECK_MODE', result.stdout)

    def test_isolated_renderer_embeds_accounting_before_readiness(self):
        result = subprocess.run(['bash', str(RECIPE/'render-template.sh'), '--isolated', IMAGE],
                                capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)
        for token in ('FULL_WORKER_CHECK_MODE', 'validation-accounting.json', 'parent_delta',
                      '/proc/', 'memory.max', '--cgroup-parent=docker', 'kill', IMAGE):
            self.assertIn(token, result.stdout)
        self.assertNotIn('VALIDATION_HELPER_REQUIRED', result.stdout)

    def test_preparation_checks_accounting_before_repository_setup(self):
        source = (RECIPE/'prepare.sh').read_text()
        self.assertIn('check.py --preflight', source)
        self.assertLess(source.index('check.py --preflight'), source.index('workspace={{workspace.path}}'))

    def test_baked_runner_has_no_runtime_dependency(self):
        source = (RECIPE/'Dockerfile').read_text()
        self.assertIn('COPY check.py /opt/full-worker/check.py', source)


if __name__ == '__main__':
    unittest.main()
