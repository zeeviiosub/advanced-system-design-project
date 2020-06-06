import json
from datetime import datetime
import pytest
import utils.protocol
import subprocess
import parsers
import os

def test_parser_parse_user():
    hello = utils.protocol.Hello(200639318, 'Zeevi Iosub', datetime(1988, 4, 27).timestamp(), 'm')
    parsed_data = parsers.parse('user', hello.serialize())
    assert parsed_data == {'user_id': 200639318, 'username': 'Zeevi Iosub',
                           'birth_date': datetime(1988, 4, 27).timestamp(), 'gender': 'm'}

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

def test_parser_parse_user_cli():
    hello = utils.protocol.Hello(200639318, 'Zeevi Iosub', datetime(1988, 4, 27).timestamp(), 'm')
    try:
        with open('.__test_parsers_temporary_file__', 'wb') as f:
            f.write(hello.serialize())
        process = subprocess.run(['python', '-m', 'parsers', 'parse-file', 'user', '.__test_parsers_temporary_file__'],
                                  capture_output=True)
        parsed_data = json.loads(process.stdout)
        assert parsed_data == {'user_id': 200639318, 'username': 'Zeevi Iosub',
                               'birth_date': datetime(1988, 4, 27).timestamp(), 'gender': 'm'}
    finally:
        os.remove('.__test_parsers_temporary_file__')

def test_parser_parse_pose_cli():
    snapshot = utils.protocol.Snapshot(1234)
    snapshot.translation = (1.0, 2.0, 3.0)
    snapshot.rotation = (0.5, -0.5, 0.25, 0.75)
    try:
        with open('.__test_parsers_temporary_file__', 'wb') as f:
            f.write((200639318).to_bytes(8, 'little'))
            f.write((1234).to_bytes(8, 'little'))
            f.write(snapshot.serialize())
        process = subprocess.run(['python', '-m', 'parsers', 'parse-file', 'pose', '.__test_parsers_temporary_file__'],
                                  capture_output=True)
        parsed_data = json.loads(process.stdout)
        assert parsed_data == {'translation': [1.0, 2.0, 3.0], "rotation": [0.5, -0.5, 0.25, 0.75]}
        parsed_data = json.loads(process.stdout)
    finally:
        os.remove('.__test_parsers_temporary_file__')

def test_parser_parse_feelings_cli():
    snapshot = utils.protocol.Snapshot(1234)
    snapshot.hunger = 1.0
    snapshot.thirst = -1.0
    snapshot.exhaustion = 0.0
    snapshot.happiness = -0.5
    try:
        with open('.__test_parsers_temporary_file__', 'wb') as f:
            f.write((200639318).to_bytes(8, 'little'))
            f.write((1234).to_bytes(8, 'little'))
            f.write(snapshot.serialize())
        process = subprocess.run(['python', '-m', 'parsers', 'parse-file', 'feelings', '.__test_parsers_temporary_file__'],
                                  capture_output=True)
        parsed_data = json.loads(process.stdout)
        assert parsed_data == {'hunger': 1.0, 'thirst': -1.0, 'exhaustion': 0.0, 'happiness': -0.5}
        parsed_data = json.loads(process.stdout)
    finally:
        os.remove('.__test_parsers_temporary_file__')

def test_parser_parse_color_image_cli():
    snapshot = utils.protocol.Snapshot(1234)
    try:
        with open('.__test_parsers_temporary_file__', 'wb') as f:
            f.write((200639318).to_bytes(8, 'little'))
            f.write((1234).to_bytes(8, 'little'))
            f.write(snapshot.serialize())
        process = subprocess.run(['python', '-m', 'parsers', 'parse-file', 'color_image', '.__test_parsers_temporary_file__'],
                                  capture_output=True)
        parsed_data = json.loads(process.stdout)
        assert parsed_data == '../../static/200639318_1234_color.png'
        parsed_data = json.loads(process.stdout)
    finally:
        os.remove('.__test_parsers_temporary_file__')

def test_parser_parse_depth_image_cli():
    snapshot = utils.protocol.Snapshot(1234)
    try:
        with open('.__test_parsers_temporary_file__', 'wb') as f:
            f.write((200639318).to_bytes(8, 'little'))
            f.write((1234).to_bytes(8, 'little'))
            f.write(snapshot.serialize())
        process = subprocess.run(['python', '-m', 'parsers', 'parse-file', 'depth_image', '.__test_parsers_temporary_file__'],
                                  capture_output=True)
        parsed_data = json.loads(process.stdout)
        assert parsed_data == '../../static/200639318_1234_depth.png'
        parsed_data = json.loads(process.stdout)
    finally:
        os.remove('.__test_parsers_temporary_file__')
