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

    def test_all(self):
        """Test the all method for the FileStorage class
        """
        # Test if all() returns an empty dictionary
        self.assertEqual(self.test_storage.all(), {})
        # Test if all() return value is of the type dict
        self.assertIsInstance(self.test_storage.all(), dict)

    def test_new(self):
        """Test the new method for the FileStorage class to check
        if it adds new instances of various classes to the dictionary
        """
        # Create new instances for the classes
        amenity = Amenity()
        basemodel = BaseModel()
        city = City()
        place = Place()
        review = Review()
        state = State()
        user = User()
        # Call the new method on each instance
        self.test_storage.new(amenity)
        self.test_storage.new(basemodel)
        self.test_storage.new(city)
        self.test_storage.new(place)
        self.test_storage.new(review)
        self.test_storage.new(state)
        self.test_storage.new(user)
        # Retrieve the new dictionary created
        object_dict = self.test_storage.all()
        # Check if the instances are in the dictionary
        self.assertIn("Amenity." + amenity.id, object_dict)
        self.assertIn("BaseModel." + basemodel.id, object_dict)
        self.assertIn("City." + city.id, object_dict)
        self.assertIn("Place." + place.id, object_dict)
        self.assertIn("Review." + review.id, object_dict)
        self.assertIn("State." + state.id, object_dict)
        self.assertIn("User." + user.id, object_dict)


if __name__ == "__main__":
    unittest.main()
