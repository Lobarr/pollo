import os
import time
import asyncio
import socketio
from aiohttp import web

#routers
from api import ping_router, transribe_router, sio

if __name__ == "__main__":
  app = web.Application()
  sio.attach(app)
  app.add_routes(ping_router)
  app.add_routes(transribe_router)
  print(asyncio.get_event_loop().is_running())
  web.run_app(app, port=os.getenv("PORT", 3000))
 