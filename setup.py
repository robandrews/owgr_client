#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from setuptools import setup

try:
    from packaging.version import Version
    import importlib.metadata as metadata
    v = metadata.version('setuptools')
    if Version(v) < Version('38.3'):
        print("Error: version of setuptools is too old (<38.3)!")
        sys.exit(1)
except Exception:
    pass

if __name__ == "__main__":
    setup(use_pyscaffold=True)
