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
    self.__fn = fn
  
  def convert(self):
    if self.__fn.find('.wav') == -1:
      fn, f_ext = os.path.splitext(self.__fn)
      (
        ffmpeg
        .input(f'{fn}{f_ext}')
        .output(f'{fn}.wav')
        .run()
      )
