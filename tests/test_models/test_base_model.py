#!/usr/bin/python3
"""Unit tests for the BaseModel class
"""


from datetime import datetime
import unittest
import models
from models.base_model import BaseModel


class TestBaseModel(unittest.TestCase):
    """BaseModel class test cases

    Args:
        unittest (module): Module for unit tests
    """
    def test_init(self):
        """Test initialization of a BaseModel instance with no
        arguments passed
        """
        base_model = BaseModel()
        # check if id is a str
        self.assertIsInstance(base_model.id, str)
        # check updated_at and created_at are datetime obj
        self.assertIsInstance(base_model.updated_at, datetime)
        self.assertIsInstance(base_model.created_at, datetime)
        # check if base_model is an instance of BaseModel
        self.assertIsInstance(base_model, BaseModel)
        # check if base_model is a valid object __class__
        self.assertTrue(hasattr(base_model, "__class__"))
        # check if calling new() was successful
        self.assertIn(base_model, models.storage.all().values())

    def test_base_model_with_kwargs(self):
        """Test initialization of BaseModel with kwargs
        """
        object_data = {
            "id": "1234-1234-1234-123a",
            "created_at": datetime.isoformat(datetime.now()),
            "updated_at": datetime.isoformat(datetime.now()),
            "__class__": "BaseModel",
            "Country": "Ghana"
        }
        base_model = BaseModel(**object_data)
        # check if base_model is a valid object __class__
        self.assertTrue(hasattr(base_model, "__class__"))
        # Validate object id
        self.assertEqual(object_data["id"], base_model.id)
        # Validate created_at and updated_at
        created_at = datetime.fromisoformat(object_data["created_at"])
        updated_at = datetime.fromisoformat(object_data["updated_at"])
        self.assertEqual(created_at, base_model.created_at)
        self.assertEqual(updated_at, base_model.updated_at)
        # Validate additional attributes)
        self.assertEqual(object_data["Country"], base_model.Country)

    def test_str(self):
        """Test the string representation of the BaseModel
        """
        base_model = BaseModel()
        # Construct the string representation
        basemodel_str =\
            "[BaseModel] ({}) {}".format(base_model.id, base_model.__dict__)
        self.assertEqual(basemodel_str, str(base_model))

    def test_save(self):
        """Test the save method of the BaseModel class
        """
        # Create a BaseModel instance
        base_model = BaseModel()
        # Retrieve original updated_at
        prev_updated_at = base_model.updated_at
        # Save the object
        base_model.save()
        # Compare orignal updated_at with new time
        self.assertNotEqual(prev_updated_at, base_model.updated_at)

    def test_to_dict(self):
        """Test the to_dict() method of BaseModel class
        """
        # Create a new instance
        base_model = BaseModel()
        # Create the expected dictionary
        basemodel_dict = {
            "id": base_model.id,
            "created_at": base_model.created_at.isoformat(),
            "updated_at": base_model.updated_at.isoformat(),
            "__class__": "BaseModel",
        }
        # Assert the to_dict return value
        self.assertEqual(basemodel_dict, base_model.to_dict())


if __name__ == "__main__":
    unittest.main()
