import os
import io
import logging

from pydub import AudioSegment 
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

ACCENTS = ['en-US', 'en-GB']

class Transcriber:
  """
  Transcribes .wav file to text using Google speech-to-text API
  """
  def __init__(self, fn: str):
    if fn.index('.wav') > 0:
      self.client = speech.SpeechClient()
      self.fn: str = fn
      self.audio: bytes = None
      self.transcript: str = None
      self._load_audio()
  """
  loads audio file into memory
  """
  def _load_audio(self):
    with io.open(self.fn, 'rb') as f:
      content = f.read()
      self.audio = types.RecognitionAudio(content=content)
  """
  returns sample rate of audio file
  """
  def _sample_rate(self):
    file = AudioSegment.from_wav(self.fn)
    return file.frame_rate
  """
  returns transcript of audio file
  """ 
  def transcribe(self, accent: str):
    if accent not in ACCENTS:
      raise Exception('Invalid accent type')
    config = types.RecognitionConfig(
    encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=self._sample_rate(),
    language_code=accent)

    response = self.client.recognize(config, self.audio)

    for result in response.results:
        print(f'Transcript: {result.alternatives[0].transcript}')
    print("Transcript ", response.results)
