import os
import socketio
import asyncio
from threading import Thread
from typing import Dict
from core import File, Transcriber
from aiohttp import web, multipart
from enum import Enum

socket = socketio.AsyncServer(async_mode='aiohttp')
router = web.RouteTableDef()


class Status(Enum):
  SUCCESS = 'success'
  ERROR = 'error'
  INFO = 'info'

class SocketMessage(Enum):
  STATUS = 'status'
  TRANSCRIBE = 'transcribe'



def transribe_job(filename: str, accent: str, socket_id: str):
  try:
    file_path = File.path(filename)
    transcriber = Transcriber(file_path, accent)
    message = transcriber.run()
    ctx = {
      'message': message,
      'status': Status.SUCCESS.value
    }

    asyncio.run(socket.emit(event=SocketMessage.TRANSCRIBE.value, data=ctx, sid=socket_id))

  except Exception as error:
    ctx = {
      'message': str(error),
      'status': Status.ERROR.value
    }
    
    asyncio.run(socket.emit(event=SocketMessage.STATUS.value, data=ctx, sid=socket_id))

  finally:
    File.delete(filename)
    root = filename.split('.')[0]
    File.delete(f'{root}.wav')


@router.post('/upload')
async def upload(request: web.Request):
  reader: multipart.MultipartReader = await request.multipart()
  file_ctx = await reader.next()

  await File.save(file_ctx)

  return web.json_response({
    'message': 'File Uploaded',
    'status': Status.SUCCESS.value
  })

@socket.on(SocketMessage.TRANSCRIBE.value)
async def transcribe(socket_id: str, data: Dict[str, str]):
  try:
    filename = data.get('filename')
    accent = data.get('accent')
    is_verified = File.verify_size(filename)

    if is_verified:
      ctx = {
        'message': 'Transcribing',
        'status': Status.INFO.value
      }

      await socket.emit(event=SocketMessage.STATUS.value, data=ctx, sid=socket_id)

      worker = Thread(target=transribe_job, args=(filename, accent, socket_id))
      worker.start()

    else:
      ctx = {
        'message': 'File uploaded exceeds 5 mins limit',
        'status': Status.ERROR.value
      }
      await socket.emit(event=SocketMessage.STATUS.value, data=ctx, sid=socket_id)

  except Exception as error:
    ctx = {
      'message': str(error),
      'status': Status.ERROR.value
    }
    
    await socket.emit(event=SocketMessage.STATUS.value, data=ctx, sid=socket_id)

