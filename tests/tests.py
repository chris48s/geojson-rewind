import json
import os
import unittest
from geojson_rewind import rewind


class RewindTests(unittest.TestCase):

    maxDiff = None

    def get_fixture_path(self, filename):
        basedir = os.path.dirname(os.path.abspath(__file__))
        return os.path.abspath(os.path.join(basedir, 'fixtures/', filename))

    def test_collection(self):
        infile = self.get_fixture_path('collection.input.geojson')
        outfile = self.get_fixture_path('collection.output.geojson')
        self.assertDictEqual(
            rewind(json.load(open(infile))),
            json.load(open(outfile))
        )

    def test_both_reversed(self):
        # both rings are reversed in input file
        # outer = clockwise
        # inner = anti-clockwise
        infile = self.get_fixture_path('both_reversed.input.geojson')
        outfile = self.get_fixture_path('both_reversed.output.geojson')
        self.assertDictEqual(
            rewind(json.load(open(infile))),
            json.load(open(outfile))
        )

    def test_passthrough(self):
        # input file is already valid
        infile = self.get_fixture_path('passthrough.input.geojson')
        outfile = self.get_fixture_path('passthrough.output.geojson')
        self.assertDictEqual(
            rewind(json.load(open(infile))),
            json.load(open(outfile))
        )
        self.assertDictEqual(
            rewind(json.load(open(infile))),
            json.load(open(infile))
        )

    def test_multipolygon(self):
        infile = self.get_fixture_path('multipolygon.input.geojson')
        outfile = self.get_fixture_path('multipolygon.output.geojson')
        self.assertDictEqual(
            rewind(json.load(open(infile))),
            json.load(open(outfile))
        )

    def test_inner_reversed(self):
        # inner ring is reversed in input file
        # outer = anti-clockwise
        # inner = anti-clockwise
        infile = self.get_fixture_path('inner_reversed.input.geojson')
        outfile = self.get_fixture_path('inner_reversed.output.geojson')
        self.assertDictEqual(
            rewind(json.load(open(infile))),
            json.load(open(outfile))
        )

    def test_str(self):
        # should convert str -> str
        infile = self.get_fixture_path('passthrough.input.geojson')
        output = rewind(open(infile).read())
        self.assertIsInstance(output, str)
        self.assertEqual(
            output,
            json.dumps(json.load(open(infile)))
        )

    def test_no_mutate(self):
        # should not transform in-place
        infile = self.get_fixture_path('inner_reversed.input.geojson')
        _input = json.load(open(infile))
        output = rewind(_input)
        self.assertNotEqual(_input, output)
