import uuid
import os
import time
import string
from pydub import AudioSegment

class AudioSplitter():
  """
  Splits audio file into minute long chunks
  """
  def __init__(self, fn: str):
    if fn.index('.wav') > 0:
      self.audio = AudioSegment.from_wav(fn)
      self.fn = fn

  def split(self) -> list:
    split_audios = []
    duration = self.audio.duration_seconds
    while True:
      split_fn = os.path.join(os.path.dirname(os.path.abspath(self.fn)), f'{uuid.uuid4()}.wav')
      if (duration / 60) > 1:
        minute = 60 * 1000 #ms to seconds 
        split = self.audio[:minute] 
        split.export(split_fn, format='wav')
        split_audios.append(split_fn)
      else:
        remainder =  int(self.audio.duration_seconds/60) * 60 * 1000
        split = self.audio[remainder:]
        split.export(split_fn, format='wav')
        split_audios.append(split_fn)
        break
      duration = duration-60
    return split_audios
     
    
      
    
    
