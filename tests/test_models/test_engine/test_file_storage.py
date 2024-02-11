#!/usr/bin/python3
"""Unit tests for the FileStorage class
"""


import json
import os
import unittest
from datetime import datetime
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
        """Test the all() method for the FileStorage class
        """
        # Test if all() returns an empty dictionary
        self.assertEqual(self.test_storage.all(), {})
        # Test if all() return value is of the type dict
        self.assertIsInstance(self.test_storage.all(), dict)

    def test_new(self):
        """Test the new() method for the FileStorage class to check
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

    def test_save(self):
        """Test the save() method
        """
        # Create new instances for the classes
        amenity = Amenity()
        basemodel = BaseModel()
        city = City()
        place = Place()
        review = Review()
        state = State()
        user = User()
        # Call the new() method on each instance
        self.test_storage.new(amenity)
        self.test_storage.new(basemodel)
        self.test_storage.new(city)
        self.test_storage.new(place)
        self.test_storage.new(review)
        self.test_storage.new(state)
        self.test_storage.new(user)
        # Dump the new instances created to the JSON file
        self.test_storage.save()
        # Create an empty string to store the contents of the JSON file
        all_objects = ""
        # Open the JSON file
        with open("test_file.json", "r", encoding="utf-8") as file:
            # Save the contents of the JSON file
            all_objects = file.read()
            # Check if IDs of all instances are present in all_objects
            self.assertIn("Amenity." + amenity.id, all_objects)
            self.assertIn("BaseModel." + basemodel.id, all_objects)
            self.assertIn("City." + city.id, all_objects)
            self.assertIn("Place." + place.id, all_objects)
            self.assertIn("Review." + review.id, all_objects)
            self.assertIn("State." + state.id, all_objects)
            self.assertIn("User." + user.id, all_objects)

    def test_reload(self):
        """Test the save() method
        """
        # Create new instances for the classes
        amenity = Amenity()
        basemodel = BaseModel()
        city = City()
        place = Place()
        review = Review()
        state = State()
        user = User()
        # Call the new() method on each instance
        self.test_storage.new(amenity)
        self.test_storage.new(basemodel)
        self.test_storage.new(city)
        self.test_storage.new(place)
        self.test_storage.new(review)
        self.test_storage.new(state)
        self.test_storage.new(user)
        # Dump the new instances created to the JSON file
        self.test_storage.save()
        # Load the saved data from the JSON file
        self.test_storage.reload()
        # Retrieve the __object dictionary from FileStorage class
        object_dict = self.test_storage.all()
        # Check if IDs of all instances are present in object_dict
        self.assertIn("Amenity." + amenity.id, object_dict)
        self.assertIn("BaseModel." + basemodel.id, object_dict)
        self.assertIn("City." + city.id, object_dict)
        self.assertIn("Place." + place.id, object_dict)
        self.assertIn("Review." + review.id, object_dict)
        self.assertIn("State." + state.id, object_dict)
        self.assertIn("User." + user.id, object_dict)

    def test_reload_nonexistent_file(self):
        """Test if reload() does nothing if the file does not exist
        """
        # Call save to create the JSON file
        self.test_storage.save()
        try:
            with open(
                    self.test_storage._FileStorage__file_path,
                    "r",
                    encoding="utf-8"
                    ) as file:
                file_content = file.read()
        except (FileNotFoundError, PermissionError):
            pass
        self.assertEqual(file_content, "{}")
        # Delete the JSON file
        os.remove("test_file.json")
        with self.assertRaises(FileNotFoundError):
            open(
                self.test_storage._FileStorage__file_path,
                "r",
                encoding="utf-8"
                )
        # Try to load the saved data from the JSON file
        self.test_storage.reload()
        # Check if __objects is empty
        self.assertEqual(self.test_storage.all(), {})

    def test_reload_corrupted_file(self):
        """Test if reload() does nothing if the JSON file is has an
        invalid format
        """
        # Open a JSON file
        with open("test_file.json", "w", encoding="utf-8") as file:
            # Create an invalid JSON format in the JSON file
            file.write("Trying to create an invalid JSON file")
        try:
            # Reload the content from the JSON file
            self.test_storage.reload()
        except json.JSONDecodeError:
            pass
        # Check if __objects is still empty
        self.assertEqual(self.test_storage.all(), {})

    def test_no_instances(self):
        """Test save() and reload() when there are no instances
        """
        # Save and reload from JSON file with no instances
        self.test_storage.all()
        self.test_storage.reload()
        # Check if __objects is still empty
        self.assertEqual(self.test_storage.all(), {})

    def test_duplicate_instances(self):
        """Tests new() method for duplicate instances
        """
        # Create a Place instance
        place = Place()
        # Call new() twice on the same instance
        self.test_storage.new(place)
        self.test_storage.new(place)
        # Check if there is only one instance of the same id in the
        # __objects dictionary
        self.assertEqual(len(self.test_storage.all()), 1)

    def wrong_file_path(self):
        """Test reload with wrong file path
        """
        # create a JSON file with save()
        self.test_storage.save()
        # Modify file path
        self.test_storage._FileStorage__file_path = "new.json"
        # Reload from a different file path
        self.test_storage.reload()
        # Check if __object is still empty
        # since the file path was changed
        self.assertEqual(self.test_storage.all(), {})

    def test_special_characters(self):
        """Test if save() can handle instances with attributes
        containing special characters
        """
        # Create an instance with attributes containing special characters
        timestamp = datetime.isoformat(datetime.now())
        user = User(id="Dmi#%*2", created_at=timestamp,
                    updated_at=timestamp, name="John&Doe")
        # Call new() on user
        self.test_storage.new(user)
        # Save user onto the JSON file
        self.test_storage.save()
        # Reload and check if the instance is present
        self.test_storage.reload()
        self.assertIn("User.Dmi#%*2", self.test_storage.all())

    def test_empty_instances(self):
        """Test save() and reload() on empty instances to ensure it
        does not raise any errors
        """
        # Create a User instance
        user = User()
        # Call new() on user
        self.test_storage.new(user)
        # Save user onto the JSON file
        self.test_storage.save()
        # Reload and check if the instance is present
        self.test_storage.reload()
        self.assertIn("User." + user.id, self.test_storage.all())

    def test_new_args(self):
        """Test new() method with more arguments than it takes
        """
        # Raise a TypeError
        with self.assertRaises(TypeError):
            self.test_storage.new(User(), 1)

    def test_reload_args(self):
        """Test new() method with invalid argument type
        """
        # Raise TypeError
        with self.assertRaises(TypeError):
            self.test_storage.reload(None)

    def test_updated_attributes(self):
        """Test save() and reload() method by modifying the attributes
        of instances
        """
        # Create an instance
        timestamp = datetime.isoformat(datetime.now())
        user = User(id="1234", created_at=timestamp,
                    updated_at=timestamp, first_name="John")
        # Call new()
        self.test_storage.new(user)
        # Save the user instance
        self.test_storage.save()
        # Update the user attribute
        user.first_name = "James"
        # Save the change
        self.test_storage.save()
        # Load data from JSON file
        self.test_storage.reload()
        # Get the User instance from __objects
        user_obj = self.test_storage.all()["User." + user.id]
        # Check if the updated attribute is reflected
        self.assertEqual(user_obj.first_name, "James")

    def test_deleted_instance(self):
        """Test reload() and save() methods after deleting an instance
        """
        # Create an instance
        time = datetime.isoformat(datetime.now())
        place = Place(id="12k34", created_at=time, updated_at=time,
                      first_name="John")
        # Call place()
        self.test_storage.new(place)
        # Save the place instance
        self.test_storage.save()
        # Delete the place instance and save()
        del self.test_storage._FileStorage__objects["Place." + place.id]
        self.test_storage.save()
        # Reload and check if the removed instance is still absent
        self.test_storage.reload()
        self.assertNotIn("Place." + place.id, self.test_storage.all())


if __name__ == "__main__":
    unittest.main()
