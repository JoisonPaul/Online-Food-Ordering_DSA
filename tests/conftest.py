import sys
import os
import importlib
import pytest

# Ensure project root directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import menu
import hash_table
import circular_queue
import order
import search
import app


@pytest.fixture(autouse=True)
def client():
    """
    Reload all application modules before each test to guarantee independent state,
    then return a fresh Flask test client.
    """
    importlib.reload(menu)
    importlib.reload(hash_table)
    importlib.reload(circular_queue)
    importlib.reload(order)
    importlib.reload(search)
    importlib.reload(app)
    return app.app.test_client()
