import ffmpeg
import os
import io
from pydub import AudioSegment

class File:
  @staticmethod
  async def save(file_ctx):
    with io.open(File.path(file_ctx.filename), 'wb+') as f:
      while True:
        chunk = await file_ctx.read_chunk()  # 8192 bytes by default.

        if not chunk:
            break
          
        f.write(chunk)

  @staticmethod
  def verify_size(filename: str):
    filepath = File.path(filename)
    duration = AudioSegment.from_file(filepath).duration_seconds
    is_verified = (duration / 60) <= 5 # ensures audio files are at most 5 mins in length

    return True if is_verified else False

  @staticmethod
  def delete(filename: str):
    filepath = File.path(filename)
    os.remove(filepath)
  
  @staticmethod
  def path(fn: str):
    return os.path.abspath(f'./tmp/{fn}')
    
