import os
import io
import logging

from threading import Thread
from queue import Queue
from pydub import AudioSegment 
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from pollo.audio_splitter import AudioSplitter
from pollo.video_converter import VideoConverter

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
    self.__client = speech.SpeechClient()
    self.__transcripts = {}
    self.__files_queue = Queue()
    self.__files = self.split()
    self.__file = split_fn
    self.__accent = accent
    for index, file in enumerate(self.__files): 
      self.__files_queue.put({'index': index, 'fn': file})
  """
  deletes files created from splitting
  """
  def __del__(self):
    os.remove(f'{self.__file}.wav')
    for file in self.__files:
      os.remove(file)
  """
  loads audio file into memory
  """
  def _load_audio(self, fn):
    with io.open(fn, 'rb') as f:
      content = f.read()
      return types.RecognitionAudio(content=content)
  """
  returns sample rate of audio file
  """
  def _sample_rate(self, fn):
    file = AudioSegment.from_wav(fn)
    return file.frame_rate
  """
  returns transcript of audio file
  """ 
  def __transcribe(self):
    while not self.__files_queue.empty():
      work = self.__files_queue.get()
      audio = self._load_audio(work['fn'])
      config = types.RecognitionConfig(
      encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
      sample_rate_hertz=self._sample_rate(work['fn']),
      language_code=self.__accent)
      response = self.__client.recognize(config, audio)
      self.__transcripts[str(work['index'])] = response.results
      self.__files_queue.task_done()
  def run(self):
    num_threads = 4
    for _ in range(num_threads):
      worker = Thread(target=self.__transcribe)
      worker.start()
    self.__files_queue.join()
    return self.__transcripts