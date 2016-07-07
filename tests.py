import unittest
from unittest.mock import MagicMock
from billboard_utils import *


class tests(unittest.TestCase):

    def test_format_feat(self):
        test_str = 'drake featuring drake'
        self.assertEquals(format_feat(test_str), 'drake feat. drake')
        test_str = 'drake Featuring drake'
        self.assertEquals(format_feat(test_str), 'drake feat. drake')
        test_str = 'drake Feat. drake'
        self.assertEquals(format_feat(test_str), 'drake feat. drake')
        test_str = 'drake Feat drake'
        self.assertEquals(format_feat(test_str), 'drake feat. drake')

    def test_format_ampersand(self):
        artist = 'drake featuring drake, drake, & drake'
        artist = format_feat(artist)
        # split on featured
        featured_artists = artist.split(' feat. ')
        featured = format_ampersand(featured_artists[1]).split(', ')
        self.assertEquals(featured, ['drake', 'drake', 'drake'])


if __name__ == '__main__':
    unittest.main()
