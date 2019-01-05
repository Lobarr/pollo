import uuid
import os
import string
from pydub import AudioSegment

LIMIT = 45 # splits into 45 seconds chunks - can handle 3 convertions per minute with this
class AudioSplitter:
  """
  Splits audio file into minute long chunks
  """
  def __init__(self, fn: str):
    if fn.index('.wav') > 0:
      self.__audio = AudioSegment.from_wav(fn).set_channels(1) # converts to mono as google api supports just mono
      self.__fn = fn

  def split(self) -> list:
    split_audios = []
    duration = self.__audio.duration_seconds
    while True:
      split_fn = os.path.join(os.path.dirname(os.path.abspath(self.__fn)), f'{uuid.uuid4()}.wav')
      if (duration / LIMIT) > 1:
        limit_ms = LIMIT * 1000 # seconds to ms 
        split = self.__audio[:limit_ms] 
        split.export(split_fn, format='wav')
        split_audios.append(split_fn)
      else:
        remainder =  int(self.__audio.duration_seconds/LIMIT) * 60 * 1000
        split = self.__audio[remainder:]
        split.export(split_fn, format='wav')
        split_audios.append(split_fn)
        break
      duration = duration-LIMIT
    return split_audios