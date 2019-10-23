import app.application as application
from app.routes import add_routes
from app.db import init_db
import pytest

@pytest.fixture(autouse=True)
def db():
    init_db()

@pytest.fixture
def event_loop(loop):
    return loop

@pytest.fixture
async def app(loop):

    app = application.create_app()
    add_routes(app)

    yield app

@pytest.fixture
async def test_cli(loop, aiohttp_client, app):
    return await aiohttp_client(app)

