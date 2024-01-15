#!/usr/bin/python4
""" unitest for Place Class
"""


from datetime import datetime
import unittest
import models
from models.place import Place


class TestPlace(unittest.TestCase):
    """Place class test cases

    Args:
        unittest (module): Module for unit tests
    """
    def setUp(self):
        """set up class instance to use for test
        """
        self.instance = Place()

    def tearDown(self):
        """Destroy instance of class Place
        """
        del self.instance

    def test_place_attribute(self):
        """
        Test Place class attributes
        """
        self.assertIsInstance(self.instance.id, str)
        self.assertIsInstance(self.instance.city_id, str)
        self.assertIsInstance(self.instance.user_id, str)
        self.assertIsInstance(self.instance.name, str)
        self.assertIsInstance(self.instance.description, str)
        self.assertIsInstance(self.instance.number_bathrooms, int)
        self.assertIsInstance(self.instance.number_rooms, int)
        self.assertIsInstance(self.instance.max_guest, int)
        self.assertIsInstance(self.instance.price_by_night, int)
        self.assertIsInstance(self.instance.latitude, float)
        self.assertIsInstance(self.instance.longitude, float)
        self.assertIsInstance(self.instance.amenity_ids, list)
        # check updated_at and created_at are datetime obj
        self.assertIsInstance(self.instance.updated_at, datetime)
        self.assertIsInstance(self.instance.created_at, datetime)
        # check if base_model is an instance of BaseModel
        self.assertIsInstance(self.instance, Place)
        # check if base_model is a valid object __class__
        self.assertTrue(hasattr(self.instance, "__class__"))
        # check if calling new() was successful
        self.assertIn(self.instance, models.storage.all().values())

    def test_place_kwargs(self):
        """Test initialization of BaseModel with kwargs
        """
        object_data = {
            "id": "1234-1234-1234-123a",
            "created_at": datetime.isoformat(datetime.now()),
            "updated_at": datetime.isoformat(datetime.now()),
            "__class__": "BaseModel",
            "Country": "Ghana"
        }
        base_model = Place(**object_data)
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
        instance2 = Place()
        self.assertLess(self.instance.created_at, instance2.created_at)

    def test_updated_time(self) -> None:
        """
        check if updated time of two instance created at different time
        """
        instance2 = Place()
        self.assertLess(self.instance.updated_at, instance2.updated_at)

    def test_new_attribute_exist(self):
        """if name attribute exist
        """
        self.instance.city_id = "Lagos"
        self.instance.user_id = "H739282"
        self.instance.name = "Huclark Solomon"
        self.instance.description = "Tall"
        self.instance.number_rooms = 3
        self.instance.number_bathrooms = 3
        self.instance.max_guest = 6
        self.instance.price_by_night = 100000
        self.instance.latitude = 1.1
        self.instance.longitude = 2.1
        self.instance.amenity_ids = ["Huclark", "Solomon"]
        obj_dct = self.instance.to_dict()
        self.assertIn("city_id", obj_dct)
        self.assertIn("user_id", obj_dct)
        self.assertIn("name", obj_dct)
        self.assertIn("description", obj_dct)
        self.assertIn("number_rooms", obj_dct)
        self.assertIn("number_bathrooms", obj_dct)
        self.assertIn("max_guest", obj_dct)
        self.assertIn("price_by_night", obj_dct)
        self.assertIn("latitude", obj_dct)
        self.assertIn("longitude", obj_dct)
        self.assertIn("amenity_ids", obj_dct)

    def test_save_method_updated_time(self) -> None:
        """test if save method updated the updated_at attribute
        """
        instance2 = Place()
        updated_time = instance2.updated_at
        instance2.save()
        self.assertNotEqual(updated_time, instance2.updated_at)
        self.assertLess(updated_time, instance2.updated_at)

    def test_str(self) -> None:
        """test if str representation is overide"""
        dict_str = f"[Place] ({self.instance.id}) {self.instance.__dict__}"
        self.assertEqual(dict_str, str(self.instance))

    def test_to_method(self) -> None:
        """test to_dict method
        """
        obj_dict = self.instance.to_dict()
        self.assertEqual(obj_dict["__class__"], "Place")
        self.assertIsInstance(obj_dict["created_at"], str)
        self.assertIsInstance(obj_dict["updated_at"], str)

    def test_updated_file(self) -> None:
        """test if the file is updated
        """
        self.instance.save()
        with open("file.json", "r", encoding="utf-8") as f:
            self.assertIn("Place." + self.instance.id, f.read())


if __name__ == "__main__":
    unittest.main()
