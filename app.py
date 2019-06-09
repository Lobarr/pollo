import os
import time
import asyncio
import socketio
import logging
import aiohttp_cors
from aiohttp import web

#routers
from api import ping_router, transribe_router, sio

is_prod = os.getenv("ENV") is "prod"

if __name__ == "__main__":
  app = web.Application()
  logging.basicConfig(level=logging.INFO)
  logger = logging.getLogger("API")


  app.add_routes(ping_router)
  app.add_routes(transribe_router)
  app.add_routes([web.static('/app', './client/dist')]) if is_prod else None

  cors = aiohttp_cors.setup(app, defaults={
    "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
  })
  for route in list(app.router.routes()):
    cors.add(route)

  sio.attach(app)
   
  web.run_app(app, port=os.getenv("PORT", 3000), access_log=logger)
  