import pytest
import sys
import os

from trusty.conf import init_conf
from trusty.checksums import Checksum


def test_checksum_md5():
    init_conf()
    filename = 'data/checksum/checksum.md5'
    checker = Checksum(filename)
    invalids = checker.check()
    assert invalids == []
