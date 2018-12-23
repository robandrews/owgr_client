#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from owgr_client.skeleton import fib

__author__ = "Rob Andrews"
__copyright__ = "Rob Andrews"
__license__ = "mit"


def test_fib():
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(7) == 13
    with pytest.raises(AssertionError):
        fib(-10)
