"""Exercise opt-in renderer and startup proof without a real daemon."""
from pathlib import Path
import subprocess
import unittest

RECIPE = Path(__file__).resolve().parent
IMAGE = 'registry.invalid/worker@sha256:' + 'a' * 64


class ValidationRecipeTest(unittest.TestCase):
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
