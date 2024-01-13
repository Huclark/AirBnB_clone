#!/usr/bin/python3
"""Unit tests for the FileStorage class
"""


import json
import os
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
    def setUp(self):
        """Set up resources and  configurations needed for the
        test cases
        """
        # Create an instance of the FileStorage class
        self.test_storage = FileStorage()
        # Reset the __objects attribute before each test
        FileStorage._FileStorage__objects = {}
        # Set the FileStorage __file_path attribute to avoid
        # modifying the actual JSON file used for the program
        self.test_storage._FileStorage__file_path = "test_file.json"

    def tearDown(self):
        """Clean up any resources or configurations to prepare for
        new tests.
        """
        # Delete the JSON file used for the tests if it exists
        if os.path.exists("test_file.json"):
            os.remove("test_file.json")



if __name__ == "__main__":
    unittest.main()
