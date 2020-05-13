import unittest
import FormatAudioFile

class TestFormatAudioFile(unittest.TestCase):

  def test_reconstructDataOutOfFilename(self):
    artistName, trackName = FormatAudioFile.reconstructDataOutOfFilename(
        '01-Ciara Feat. Justin Timberlake-Love Sex Magic.mp3')
    self.assertEqual(artistName, 'Ciara Ft. Justin Timberlake')
    self.assertEqual(trackName, 'Love Sex Magic')
