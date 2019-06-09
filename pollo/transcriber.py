import os
import io

from threading import Thread
from enum import Enum
from queue import Queue
from pydub import AudioSegment 
from google.cloud import speech
from google.cloud.speech import enums, types
from pollo.audio_splitter import AudioSplitter
from pollo.video_converter import VideoConverter

class Const(Enum):
  EN_US = 'en-US'
  EN_GB = 'en-GB'
  CONCURRENCY = 6

ACCENTS = ['en-US', 'en-GB']

class Transcriber(VideoConverter, AudioSplitter):
  """
  Transcribes .wav file to text using Google speech-to-text API
  """
  def __init__(self, fn: str, accent: str):
    if accent not in ACCENTS:
      raise Exception('Invalid accent type')
    VideoConverter.__init__(self, fn)
    self.convert()
    split_fn, _ = os.path.splitext(fn)
    AudioSplitter.__init__(self, f'{split_fn}.wav')
    self.__client: speech.SpeechClient = speech.SpeechClient()
    self.__transcripts: dict = {}
    self.__jobs: Queue = Queue()
    self.__files: list = self.split()
    self.__accent: str = accent
    for index, file in enumerate(self.__files): 
      self.__jobs.put({'index': index, 'fn': file})
  """
  deletes files created from splitting
  """
  def __del__(self):
    for file in self.__files:
      os.remove(file)
  """
  loads audio file into memory
  """
  def _load_audio(self, fn: str) -> None:
    with io.open(fn, 'rb') as f:
      content = f.read()
      return types.RecognitionAudio(content=content)
  """
  returns sample rate of audio file
  """
  def _sample_rate(self, fn: str) -> int:
    file = AudioSegment.from_wav(fn)
    return file.frame_rate
  """
  returns transcript of audio file
  """ 
  def _transcribe(self) -> None:
    while not self.__jobs.empty():
      try:
        job = self.__jobs.get()
        audio = self._load_audio(job['fn'])
        config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=self._sample_rate(job['fn']),
        language_code=self.__accent)
        response = self.__client.recognize(config, audio)
        self.__transcripts[str(job['index'])] = ' '.join([result.alternatives[0].transcript for result in response.results])
      except Exception as e:
        self.__transcripts[str(job['index'])] = {'exception': e}
      finally:
        self.__jobs.task_done()
  """
  runs the transriber engine with specified concurrency
  """
  def run(self) -> dict:
    for _ in range(Const.CONCURRENCY.value):
      worker = Thread(target=self._transcribe)
      worker.start()
    self.__jobs.join()
    return ' '.join([self._transcripts[str(index)] for index in range(len(self.__transcripts)) if isinstance(self.__transcripts[str(index)], str)])
