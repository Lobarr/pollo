import sys
import os

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

import pytest
from pollo.video_converter import VideoConverter
from expects import expect, equal, be_true

class TestVideoConverter(object):
  def test_convert(self):
    filepath = os.path.abspath('./tests/videos/test.mp4') # due to relative path change 
    video_converter = VideoConverter(filepath)
    video_converter.convert()
    filename, _ = os.path.splitext(filepath)
    expect(os.path.exists(f'{filename}.wav')).to(be_true)
    os.remove(f'{filename}.wav')
