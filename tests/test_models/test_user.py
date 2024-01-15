#!/usr/bin/python4
""" unitest for State Class
"""


from datetime import datetime
import unittest
import models
from models.user import User


class TestState(unittest.TestCase):
    """state class test cases

    Args:
        unittest (module): Module for unit tests
    """
    @classmethod
    def setUp(cls) -> None:
        """set up class instance to use for test
        """
        cls.instance = User()
        
    @classmethod
    def tearDownClass(cls) -> None:
        """Destroy instance of class state
        """
        del cls.instance
    
     
    def test_User_attribute(self):
        """
        test if the instance.id of type str
        test if the instance.name of type string
        """
        self.assertIsInstance(self.instance.id, str)
        self.assertIsInstance(self.instance.email, str)
        self.assertIsInstance(self.instance.password, str)
        self.assertIsInstance(self.instance.first_name, str)
        self.assertIsInstance(self.instance.last_name, str)
        # check updated_at and created_at are datetime obj
        self.assertIsInstance(self.instance.updated_at, datetime)
        self.assertIsInstance(self.instance.created_at, datetime)
        # check if base_model is an instance of BaseModel
        self.assertIsInstance(self.instance, State)
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
        base_model = User(**object_data)
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
        instance2 = User()
        self.assertLess(self.instance.created_at, instance2.created_at)
        
    def test_updated_time(self) -> None:
        """
        check if updated time of two instance created at different time
        """
        instance2 = User()
        self.assertLess(self.instance.updated_at, instance2.updated_at)
        
    def test_new_attribute_exist(self):
        """if name attribute exist
        """
        self.instance.email = "HuclarkSolomon@ghng.com"
        self.instance.password = "alxhardthing"
        self.instance.first_name = "Huclark"
        self.instance.last_name = "Solomon"
        obj_dct = self.instance.to_dict()
        self.assertIn("email", obj_dct)
        self.assertIn("passowrd", obj_dct)
        self.assertIn("first_name", obj_dct)
        self.assertIn("last_name", obj_dct)

    def test_save_method_updated_time(self) -> None:
        """test if save method updated the updated_at attribute
        """
        instance2 = User()
        updated_time = instance2.updated_at
        instance2.save()
        self.assertNotEqual(updated_time, instance2.updated_at)
        self.assertLess(updated_time, instance2.updated_at)
    
    def test_str(self) -> None:
        """test if str representation is overide"""
        dict_str = f"[User] ({self.instance.id}) {self.instance.__dict__}"
        self.assertEqual(dict_str, str(self.instance))
        
    def test_to_method(self) -> None:
        """test to_dict method
        """
        obj_dict = self.instance.to_dict()
        self.assertEqual(obj_dict["__class__"], "State")
        self.assertIsInstance(obj_dict["created_at"], str)
        self.assertIsInstance(obj_dict["updated_at"], str)
    
    def test_updated_file(self) -> None:
        """test if the file is updated
        """
        self.instance.save()
        with open("file.json", "r") as f:
            self.assertIn("State." + self.instance.id, f.read())
            


if "__name__" == "__main__":
     unittest.main()