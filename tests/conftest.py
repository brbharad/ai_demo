from __future__ import annotations

import pytest

from app import create_app


@pytest.fixture()
def app():
    """Create a fresh Flask application for each test."""
    application = create_app()
    application.config.update({"TESTING": True})
    yield application


@pytest.fixture()
def client(app):
    """Flask test client bound to a fresh app instance."""
    return app.test_client()
