"""
Ensures that `compile.py` has been run.
"""

import logging
import os

from .compile import compile_extensions_json


def test_extensions_js_is_in_sync(caplog):
    caplog.set_level(logging.INFO)  # silence connectionpool.py DEBUG messages

    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'build', 'extensions.json')) as f:
        actual = f.read()

    assert actual == compile_extensions_json()
