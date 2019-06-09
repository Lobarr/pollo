import os
import pytest
import mock
import uuid
from mock import patch
from pollo.audio_splitter import AudioSplitter, LIMIT
from pollo.video_converter import VideoConverter
from pydub import AudioSegment
from expects import expect, equal, be_true, be

filepath = os.path.abspath('./tests/videos/test.mp4') # due to relative path change 

class TestAudioSplitter(object):
  @patch.object(AudioSegment, 'set_channels')
  @patch.object(os.path, 'dirname')
  @patch.object(os.path, 'join')
  @patch.object(os, 'remove')
  @patch.object(uuid, 'uuid4')
  @patch.object(AudioSegment, 'from_wav')
  def test_split(self, *args):
    mock_file = 'test.wav'
    splitter = AudioSplitter(mock_file)
    args[0].assert_called_once_with(mock_file)
