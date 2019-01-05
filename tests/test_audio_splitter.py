import sys
import os

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

import pytest
from pollo.audio_splitter import AudioSplitter, LIMIT
from pollo.video_converter import VideoConverter
from pydub import AudioSegment
from expects import expect, equal, be_true, be

filepath = os.path.abspath('./tests/videos/test.mp4') # due to relative path change 

class TestAudioSplitter(object):
  def test_split_files(self):
    video_converter = VideoConverter(filepath)
    video_converter.convert()
    filename, _ = os.path.splitext(filepath)
    splitter = AudioSplitter(f'{filename}.wav')
    files = splitter.split()
    [expect(os.path.exists(file)).to(be_true) for file in files]
    os.remove(f'{filename}.wav')
    [os.remove(file) for file in files]
  def test_split_length(self):
    video_converter = VideoConverter(filepath)
    video_converter.convert()
    filename, _ = os.path.splitext(filepath)
    audio = AudioSegment.from_wav(f'{filename}.wav')
    splitter = AudioSplitter(f'{filename}.wav')
    files = splitter.split()
    for index in range(len(files)):
      if index != len(files)-1:
        split = AudioSegment.from_wav(files[index])
        expect(int(split.duration_seconds)).to(be(LIMIT))
      else:
        _, secs = divmod(audio.duration_seconds, LIMIT)
        split = AudioSegment.from_wav(files[index])
        expect(int(split.duration_seconds)).to(be(int(secs)))
    os.remove(f'{filename}.wav')
    [os.remove(file) for file in files]
