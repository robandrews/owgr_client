# -*- coding: utf-8 -*-
from owgr_client.client import OwgrClient  # noqa: F401
from owgr_client.models.owgr_tour import OwgrTour  # noqa: F401

try:
    from importlib.metadata import version, PackageNotFoundError
    __version__ = version(__name__)
except (PackageNotFoundError, Exception):
    __version__ = 'unknown'
