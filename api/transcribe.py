import os
import socketio
import asyncio
from threading import Thread
from typing import Dict
from pollo import File, Transcriber
from aiohttp import web

sio = socketio.AsyncServer(async_mode='aiohttp')
router = web.RouteTableDef()

async def emit(event: str, data: object, sid: str = None):
  if sid != None:
    await sio.emit(event=event, data=data, sid=sid)
  else:
    await sio.emit(event=event, data=data)

def transribe_job(fn, accent, sid):
  try:
    transcribed = Transcriber(File.path(fn), accent).run()
    asyncio.run(emit('transcribe', {
      'msg': transcribed,
      'status': 'success'
    }, sid))
  except Exception as error:
    asyncio.run(emit('status', {
      'msg': str(error),
      'status': 'error'
    }, sid))
  finally:
    File.delete(fn)
    _fn = fn.split('.')[0]
    File.delete(f'{_fn}.wav')


@router.post('/upload')
async def upload(request):
  reader = await request.multipart()
  field = await reader.next()
  await File.save(field)
  await emit('status', {
    'msg': 'Uploaded',
    'status': 'info'
  })
  return web.json_response({'status': 'success', 'msg': 'uploaded'})

@sio.on('transcribe')
async def transcribe(sid, data: Dict[str, str]):
  try:
    fn = data.get('fn')
    accent = data.get('accent')
    is_verified = File.verify_size(fn)
    if is_verified:
      await emit('status', {
        'msg': 'Transcribing',
        'status': 'info'
      })
      worker = Thread(target=transribe_job, args=(fn, accent, sid))
      worker.start()
    else:
      await emit('status', {
        'msg': 'File uploaded exceeds 5 mins limit',
        'status': 'error'
      })
  except Exception as error:
    await emit('status', {
      'msg': str(error),
      'status': 'error'
    })

