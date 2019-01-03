import os
import io
import logging

from pollo import VideoConverter
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
    self.client = speech.SpeechClient()
    self.fn = fn
    self.audio: bytes = None
    self.transcript: str = None
    vc = VideoConverter(self.fn)
    vc.convert()
    self._load_audio()
  """
  loads audio file into memory
  """
  def _load_audio(self):
    logging.info("Loading audio file")
    fn, _ = os.path.splitext(self.fn)
    with io.open('{}.wav'.format(fn), 'rb') as f:
      content = f.read()
      self.audio = types.RecognitionAudio(content=content)
  """
  returns sample rate of audio file
  """
  def _sample_rate(self):
    fn, _ = os.path.splitext(self.fn)
    file = AudioSegment.from_wav('{}.wav'.format(fn))
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
        print('Transcript: {}'.format(result.alternatives[0].transcript))
    print("Transcript ", response.results)
