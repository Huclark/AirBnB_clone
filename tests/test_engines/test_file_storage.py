#!/usr/bin/python3
"""Unit tests for the FileStorage class
"""


import json
import unittest
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.engine.file_storage import FileStorage
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class TestFileStorage(unittest.TestCase):
    """FileStorage class test cases

    Args:
        unittest (module): Module for unit tests
    """
    def test_all(self):
        self.assertEqual(FileStorage().all(), {})
        self.assertIsInstance(FileStorage().all(), dict)



if __name__ == "__main__":
    unittest.main()
