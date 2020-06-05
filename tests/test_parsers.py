import pytest
import utils.protocol
import subprocess
import parsers

def test_parser_parse_pose():
    snapshot = utils.protocol.Snapshot(1234)
    snapshot.translation = (1.0, 2.0, 3.0)
    snapshot.rotation = (0.5, -0.5, 0.25, 0.75)
    parsed_data = parsers.parse('pose', (200639318).to_bytes(8, 'little') + \
        (1234).to_bytes(8, 'little') + snapshot.serialize())
    assert parsed_data == {'translation': (1.0, 2.0, 3.0), "rotation": (0.5, -0.5, 0.25, 0.75)}

def test_parser_parse_feelings():
    snapshot = utils.protocol.Snapshot(1234)
    snapshot.hunger = 1.0
    snapshot.thirst = -1.0
    snapshot.exhaustion = 0.0
    snapshot.happiness = -0.5
    parsed_data = parsers.parse('feelings', (200639318).to_bytes(8, 'little') + \
        (1234).to_bytes(8, 'little') + snapshot.serialize())
    assert parsed_data == {'hunger': 1.0, 'thirst': -1.0, 'exhaustion': 0.0, 'happiness': -0.5}

def test_parser_parse_color_image():
    snapshot = utils.protocol.Snapshot(1234)
    parsed_data = parsers.parse('color_image', (200639318).to_bytes(8, 'little') + \
        (1234).to_bytes(8, 'little') + snapshot.serialize())
    assert parsed_data == '../../static/200639318_1234_color.png'

def test_parser_parse_depth_image():
    snapshot = utils.protocol.Snapshot(1234)
    parsed_data = parsers.parse('depth_image', (200639318).to_bytes(8, 'little') + \
        (1234).to_bytes(8, 'little') + snapshot.serialize())
    assert parsed_data == '../../static/200639318_1234_depth.png'
