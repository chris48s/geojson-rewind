import argparse
import copy
import json
import logging
import math
import sys


RADIUS = 6378137

def rewind(geojson, rfc7946=True):
    gj = copy.deepcopy(geojson)
    _check_crs(geojson)
    if isinstance(gj, str):
        return json.dumps(_rewind(json.loads(gj), rfc7946))
    else:
        return _rewind(gj, rfc7946)

def _check_crs(geojson):
    if (
        'crs' in geojson
        and 'properties' in geojson['crs']
        and 'name' in geojson['crs']['properties']
        and geojson['crs']['properties']['name'] != 'urn:ogc:def:crs:OGC:1.3:CRS84'
    ):
        logging.warning(
            'Co-ordinates in the input data are assumed to be WGS84 with '
            '(lon, lat) ordering, as per RFC 7946. Input with co-ordinates '
            'using any other CRS may lead to unexpected results.'
        )

def _rewind(gj, rfc7946):
    if gj['type'] == 'FeatureCollection':
        gj['features'] = list(
            map(lambda obj: _rewind(obj, rfc7946), gj['features'])
        )
        return gj
    if gj['type'] == 'GeometryCollection':
        gj['geometries'] = list(
            map(lambda obj: _rewind(obj, rfc7946), gj['geometries'])
        )
        return gj
    if gj['type'] == 'Feature':
        gj['geometry'] = _rewind(gj['geometry'], rfc7946)
    if gj['type'] in ['Polygon', 'MultiPolygon']:
        return correct(gj, rfc7946)
    return gj

def correct(feature, rfc7946):
    if feature['type'] == 'Polygon':
        feature['coordinates'] = correctRings(feature['coordinates'], rfc7946)
    if feature['type'] == 'MultiPolygon':
        feature['coordinates'] = list(
            map(lambda obj: correctRings(obj, rfc7946), feature['coordinates'])
        )
    return feature

def correctRings(rings, rfc7946):
    # change from rfc7946: True/False to clockwise: True/False here
    # RFC 7946 ordering determines how we deal with an entire polygon
    # but at this point we are switching to deal with individual rings
    # (which in isolation are just clockwise or anti-clockwise)
    clockwise = not(bool(rfc7946))
    rings[0] = wind(rings[0], clockwise)
    for i in range(1, len(rings)):
        rings[i] = wind(rings[i], not(clockwise))
    return rings

def wind(ring, clockwise):
    if is_clockwise(ring) == clockwise:
        return ring
    return ring[::-1]

def is_clockwise(ring):
    return ringArea(ring) >= 0

def ringArea(coords):
    area = 0
    coordsLength = len(coords)

    if coordsLength > 2:
        for i in range(0, coordsLength):
            if i == coordsLength - 2:
                lowerIndex = coordsLength - 2
                middleIndex = coordsLength - 1
                upperIndex = 0
            elif i == coordsLength - 1:
                lowerIndex = coordsLength - 1
                middleIndex = 0
                upperIndex = 1
            else:
                lowerIndex = i
                middleIndex = i + 1
                upperIndex = i + 2
            p1 = coords[lowerIndex]
            p2 = coords[middleIndex]
            p3 = coords[upperIndex]
            area = area + ( rad(p3[0]) - rad(p1[0]) ) * math.sin(rad(p2[1]))

        area = area * RADIUS * RADIUS / 2

    return area

def rad(coord):
    return coord * math.pi / 180


def main():
    parser = argparse.ArgumentParser(
        description='Enforce RFC 7946 ring winding order on a GeoJSON file'
    )
    parser.add_argument(
        'file',
        nargs='?',
        help='Input file, if empty stdin is used',
        type=argparse.FileType('r'),
        default=sys.stdin,
    )
    args = parser.parse_args()

    if args.file.isatty():
        parser.print_help()
        return 0

    sys.stdout.write(rewind(args.file.read()))
    return 0


if __name__ == '__main__':
    sys.exit(main())
