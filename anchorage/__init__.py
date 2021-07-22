"""
Anchorage is a Python package which provides methods to
archive your bookmark collection in bulk simply and
effectively.

Anchorage can be used programmatically or using its CLI.

.. include:: ./documentation.md
.. include:: ../docs/anchorage_flow.svg
"""

from anchorage.anchor_infrs.infrastructure import init
from anchorage.bookmarks import bookmarks, path, load
from anchorage.anchor import anchor_locally, anchor_online
from anchorage.anchor_tools.local import add as add_local, server
from anchorage.anchor_tools.online import add as add_online
