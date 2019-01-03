from vibora import Vibora
from vibora.responses import JsonResponse
from pollo import VideoConverter, Transcriber
import os

app = Vibora()

@app.route('/ping')
async def ping():
  return JsonResponse({'ping': 'pong'})

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=3000)
  # transcriber = Transcriber(os.path.abspath('./pollo/videos/test2.m4a'))
  # transcriber.transcribe(accent='en-US')
  # vc = VideoConverter(os.path.abspath('./pollo/videos/test2.m4a'))
  # vc.convert()
  # fn, ext = os.path.splitext(os.path.abspath('./pollo/videos/test2.m4a'))
  # print('.'.join([fn, 'wav']))

  