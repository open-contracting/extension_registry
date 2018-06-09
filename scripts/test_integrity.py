"""
Ensures that `compile.py` has been run.
"""

import logging
import os

from .compile import compile_extensions_js, compile_extension_versions_wide_csv

directory = os.path.dirname(os.path.realpath(__file__))


def compare(caplog, basename, expected):
    caplog.set_level(logging.INFO)  # silence connectionpool.py DEBUG messages

    with open(os.path.join(directory, '..', 'build', basename)) as f:
        actual = f.read()

    assert actual == expected

def test_extensions_js_is_in_sync(caplog):
    compare(caplog, 'extensions.js', compile_extensions_js())


def test_extension_versions_wide_csv_is_in_sync(caplog):
    compare(caplog, 'extension_versions_wide.csv', compile_extension_versions_wide_csv())
