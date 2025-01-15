from __future__ import annotations


def pytest_collection_modifyitems(items):
    """Modify test items in place to ensure test_views.py runs first"""

    def get_order_key(item):
        if "test_views.py" in str(item.fspath):
            return -1  # Will run first
        return 0  # All other tests run after

    items.sort(key=get_order_key)
