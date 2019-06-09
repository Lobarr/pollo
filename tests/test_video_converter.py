import os
import pytest
import mock
import ffmpeg
from mock import patch
from pollo.video_converter import VideoConverter
from expects import expect, equal, be_true

class TestVideoConverter(object):
  @patch.object(ffmpeg, 'input')
  @patch.object(ffmpeg, 'output')
  @patch.object(ffmpeg, 'run')
  def test_convert(self, *args):
    VideoConverter('test.mp4').convert()
    args[2].assert_called()

