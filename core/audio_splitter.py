import uuid
import os
import string
from pydub import AudioSegment

AUDIO_SECS_LIMIT = 45 # splits into 45 seconds chunks - can handle 3 convertions per minute with this

class AudioSplitter:
  """
  Splits audio file into fragments
  """
  def __init__(self, filename: str):
    if '.wav' not in filename:
      raise Exception('expects wav audio file as input')

    self.__audio = AudioSegment.from_wav(filename).set_channels(1) # converts to mono as google api supports only mono channel audio
    self.__filename = filename

  def __del__(self):
    os.remove(self.__filename)

  def split(self) -> list:
    audio_fragments = []
    duration = self.__audio.duration_seconds

    while True:
      file_directory = os.path.dirname(self.__filename)
      fragment_filepath = os.path.join(file_directory, f'{uuid.uuid4()}.wav')

      if (duration / AUDIO_SECS_LIMIT) > 1:
        limit_ms = AUDIO_SECS_LIMIT * 1000 # seconds to ms 
        fragment = self.__audio[:limit_ms]
        self.__audio = self.__audio[limit_ms:]
        duration = duration - AUDIO_SECS_LIMIT

        fragment.export(fragment_filepath, format='wav')
        audio_fragments.append(fragment_filepath)
      else:
        fragment = self.__audio

        fragment.export(fragment_filepath, format='wav')
        audio_fragments.append(fragment_filepath)
        break

    return audio_fragments
