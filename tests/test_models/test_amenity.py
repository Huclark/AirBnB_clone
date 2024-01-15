#!/usr/bin/python3
""" unitest for Amenity Class
"""


from datetime import datetime
import unittest
import models
from models.amenity import Amenity


class TestAmenity(unittest.TestCase):
    """Amenity class test cases

    Args:
        unittest (module): Module for unit tests
    """
    @classmethod
    def setUp(cls) -> None:
        """set up class instance to use for test
        """
        cls.instance = Amenity()
        
    @classmethod
    def tearDownClass(cls) -> None:
        """Destroy instance of class Amenity
        """
        del cls.instance
    
     
    def test_Amenity_attribute(self):
        """
        test if the instance.id of type str
        test if the instance.name of type string
        """
        self.assertIsInstance(self.instance.id, str)
        self.assertIsInstance(self.instance.name, str)
        # check updated_at and created_at are datetime obj
        self.assertIsInstance(self.instance.updated_at, datetime)
        self.assertIsInstance(self.instance.created_at, datetime)
        # check if base_model is an instance of BaseModel
        self.assertIsInstance(self.instance, Amenity)
        # check if base_model is a valid object __class__
        self.assertTrue(hasattr(self.instance, "__class__"))
        # check if calling new() was successful
        self.assertIn(self.instance, models.storage.all().values())

    def test_amenity_kwargs(self):
        """Test initialization of BaseModel with kwargs
        """
        object_data = {
            "id": "1234-1234-1234-123a",
            "created_at": datetime.isoformat(datetime.now()),
            "updated_at": datetime.isoformat(datetime.now()),
            "__class__": "BaseModel",
            "Country": "Ghana"
        }
        base_model = Amenity(**object_data)
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
        
    def test_unused_args(self) -> None:
       """
       check if args is unused
       """ 
       self.assertNotEqual(None, self.instance.__dict__.values())
       
    def test_created_time(self) -> None:
        """
        check if created at used datetime class to generate
        and the created time are different
        """
        instance2 = Amenity()
        self.assertLess(self.instance.created_at, instance2.created_at)
        
    def test_updated_time(self) -> None:
        """
        check if updated time of two instance created at different time
        """
        instance2 = Amenity()
        self.assertLess(self.instance.updated_at, instance2.updated_at)
        
    
    if "__name__" == "__main__":
        unittest.main()