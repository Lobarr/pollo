import os
from vibora import Vibora
from vibora.responses import JsonResponse
from pollo import VideoConverter, Transcriber, AudioSplitter

#routers
from api import ping_router

app = Vibora()

if __name__ == "__main__":
  app.add_blueprint(ping_router, prefixes={'v1': '/v1'})
  app.run(host="0.0.0.0", port=3000) 
  