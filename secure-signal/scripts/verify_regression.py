"""Deliberately remove the ownership check IN MEMORY and prove the test fails.

No vulnerable file is written and no network server is started.
"""
import os
import sys
from pathlib import Path
from unittest.mock import patch
from unittest import TextTestRunner

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django
django.setup()
from django.shortcuts import get_object_or_404
from django.test.runner import DiscoverRunner


def missing_ownership_check(model, **kwargs):
    kwargs.pop("owner", None)
    return get_object_or_404(model, **kwargs)


class EvidenceRunner(TextTestRunner):
    result = None

    def run(self, test):
        result = super().run(test)
        EvidenceRunner.result = result
        return result


runner = DiscoverRunner(verbosity=2)
runner.test_runner = EvidenceRunner
with patch("scans.views.get_object_or_404", missing_ownership_check):
    runner.run_tests([
        "scans.tests.AccessTests.test_other_user_cannot_read",
        "scans.tests.AccessTests.test_other_user_cannot_delete",
    ])
result = EvidenceRunner.result
if result is None or result.errors or len(result.failures) != 2 or result.testsRun != 2:
    raise SystemExit("Regression proof failed: expected both access tests to reject the mutation.")
print("PASS: both access tests detected the deliberately removed ownership checks.")
