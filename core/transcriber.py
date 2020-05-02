import os
import io
import ffmpeg

import logging
from threading import Thread
from enum import Enum
from queue import Queue
from pydub import AudioSegment 
from google.cloud import speech
from google.cloud.speech import enums, types
from core.audio_splitter import AudioSplitter

class Const(Enum):
  EN_US = 'en-US'
  EN_GB = 'en-GB'
  CONCURRENCY = 6

class Transcriber:
  """
  Transcribes .wav file to text using Google speech-to-text API
  """
 

  def __init__(self, filename: str, accent: str):
    if accent not in [Const.EN_GB.value, Const.EN_US.value]:
      raise Exception('Invalid accent provided')

    self._convert_to_wav(filename)

    root, _ = os.path.splitext(filename)
    self.__audio_splitter: AudioSplitter = AudioSplitter(f'{root}.wav')
    self.__client: speech.SpeechClient = speech.SpeechClient()
    self.__transcripts: dict = {}
    self.__jobs: Queue = Queue()
    self.__files: list = self.__audio_splitter.split()
    self.__accent: str = accent

    for index, file in enumerate(self.__files): 
      self.__jobs.put({
        'index': index, 
        'filename': file
      })

  def __del__(self):
    """
    deletes files created from splitting
    """
    if self.__files:
      for file in self.__files:
        os.remove(file)

  def _load_audio(self, filename: str) -> None:
    """
    loads audio file into memory
    """
    with io.open(filename, 'rb') as file:
      content = file.read()
      return types.RecognitionAudio(content=content)

  def _sample_rate(self, filename: str) -> int:
    """
    returns sample rate of audio file
    """
    file = AudioSegment.from_wav(filename)
    return file.frame_rate

  def _transcribe(self) -> None:
    """
    returns transcript of audio file
    """ 
    while not self.__jobs.empty():
      try:
        job = self.__jobs.get()
        audio = self._load_audio(job['filename'])
        config = types.RecognitionConfig(
          encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
          sample_rate_hertz=self._sample_rate(job['filename']),
          language_code=self.__accent
        )
        response = self.__client.recognize(config, audio)
        
        self.__transcripts[str(job['index'])] = ' '.join([result.alternatives[0].transcript for result in response.results])
      
      except Exception as e:
        self.__transcripts[str(job['index'])] = {'exception': str(e)}

      finally:
        self.__jobs.task_done()

  def run(self) -> str:
    """
    runs the transriber engine with specified concurrency
    """
    for _ in range(Const.CONCURRENCY.value):
      worker = Thread(target=self._transcribe)
      worker.start()

    self.__jobs.join()

    return ' '.join([self.__transcripts[str(index)] for index in range(len(self.__transcripts)) if isinstance(self.__transcripts[str(index)], str)])

  def _convert_to_wav(self, filename: str):
    if '.wav' not in filename:
      root, ext = os.path.splitext(filename)
      (
        ffmpeg
        .input(f'{root}{ext}')
        .output(f'{root}.wav')
        .run()
      )
