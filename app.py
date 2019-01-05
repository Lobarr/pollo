import os
from vibora import Vibora
from vibora.responses import JsonResponse
from pollo import Transcriber, AudioSplitter, VideoConverter


#routers
from api import ping_router

app = Vibora()

@app.route('/pwd')
async def pwd():
  return JsonResponse({'pwd': os.getcwd()})

if __name__ == "__main__":
  transcriber = Transcriber(os.path.abspath('./tests/videos/test.mp4'), 'en-US')
  print(transcriber.run())
  # app.add_blueprint(ping_router, prefixes={'v1': '/v1'})
  # app.run(host="0.0.0.0", port=3000) 