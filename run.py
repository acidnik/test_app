#!/usr/bin/env python3

from app.application import create_app
from aiohttp import web

from app.routes import add_routes

application = create_app()

add_routes(application.router)

web.run_app(application, port=8000)
