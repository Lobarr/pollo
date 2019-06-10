import sys
import os

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

import mock
from mock import patch
from google.cloud import speech
from pollo.transcriber import Transcriber, ACCENTS, Const
from pollo.video_converter import VideoConverter
from pollo.audio_splitter import AudioSplitter, AudioSegment
from expects import expect, equal, be_true, be

filepath = os.path.abspath('./tests/videos/test.mp4') # due to relative path change 

class TestTranscriber(object):
  @patch.object(Transcriber, '__del__')
  @patch.object(Transcriber, '_sample_rate')
  @patch.object(VideoConverter, '__init__')
  @patch.object(VideoConverter, 'convert')
  @patch.object(AudioSplitter, '__init__')
  @patch.object(AudioSplitter, 'split', lambda x: [])
  @patch.object(Transcriber, '_load_audio')
  @patch.object(Transcriber, '_transcribe')
  @patch.object(speech, 'SpeechClient')
  def test_transribe_run(self, *args):
    transribed = Transcriber(filepath, Const.EN_GB.value).run()
    args[0].assert_called_with()
    args[1].assert_called_with()
  
    

