import os
import pipes
import logging 
import ffmpeg
from pydub import AudioSegment

class VideoConverter:
  """
  Converts videos to wav
  """
  def __init__(self, fn: str):
    self.fn = fn
  
  def convert(self):
    fn, f_ext = os.path.splitext(self.fn)
    (
      ffmpeg
      .input(f'{fn}{f_ext}')
      .output(f'{fn}.wav')
      .run()
    )