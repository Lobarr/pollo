import ffmpeg
import os
import io
from pydub import AudioSegment

class File:
  @staticmethod
  async def save(field):
    with io.open(File.path(field.filename), 'wb+') as f:
      while True:
        chunk = await field.read_chunk()  # 8192 bytes by default.
        if not chunk:
            break
        f.write(chunk)

  @staticmethod
  def verify_size(fn: str):
    f_size = AudioSegment.from_file(File.path(fn)).duration_seconds
    is_verified = (f_size / 60) <= 5
    return True if is_verified else False

  @staticmethod
  def delete(fn: str):
    os.remove(File.path(fn))

  @staticmethod
  def is_supported(fn: str):
    is_found = fn.find('')
    return True if is_found != -1 else False
  
  @staticmethod
  def path(fn: str):
    return os.path.abspath(f'./tmp/{fn}')
    
