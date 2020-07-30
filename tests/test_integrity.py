"""
Ensures that the build has been run.
"""

import logging
import os

from manage import do_build


def test_build(caplog):
    caplog.set_level(logging.INFO)  # silence connectionpool.py DEBUG messages

    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'build', 'extensions.json')) as f:
        actual = f.read()

    assert actual == do_build()
