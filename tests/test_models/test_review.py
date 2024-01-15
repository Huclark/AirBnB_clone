#!/usr/bin/python4
""" unitest for Review Class
"""


from datetime import datetime
import unittest
import models
from models.review import Review


class TestReview(unittest.TestCase):
    """Review class test cases

    Args:
        unittest (module): Module for unit tests
    """
    def setUp(self):
        """set up class instance to use for test
        """
        self.instance = Review()

    def tearDown(self):
        """Destroy instance of class Review
        """
        del self.instance

    def test_review_attribute(self):
        """
        Test the Review class attributes
        """
        self.assertIsInstance(self.instance.place_id, str)
        self.assertIsInstance(self.instance.user_id, str)
        self.assertIsInstance(self.instance.text, str)
        # check updated_at and created_at are datetime obj
        self.assertIsInstance(self.instance.updated_at, datetime)
        self.assertIsInstance(self.instance.created_at, datetime)
        # check if review is an instance of Review
        self.assertIsInstance(self.instance, Review)
        # check if review is a valid object __class__
        self.assertTrue(hasattr(self.instance, "__class__"))
        # check if calling new() was successful
        self.assertIn(self.instance, models.storage.all().values())

    def test_review_kwargs(self):
        """Test initialization of Review with kwargs
        """
        object_data = {
            "id": "1234-1234-1234-123a",
            "created_at": datetime.isoformat(datetime.now()),
            "updated_at": datetime.isoformat(datetime.now()),
            "__class__": "Review",
            "Country": "Ghana"
        }
        review = Review(**object_data)
        # check if review is a valid object __class__
        self.assertTrue(hasattr(review, "__class__"))
        # Validate object id
        self.assertEqual(object_data["id"], review.id)
        # Validate created_at and updated_at
        created_at = datetime.fromisoformat(object_data["created_at"])
        updated_at = datetime.fromisoformat(object_data["updated_at"])
        self.assertEqual(created_at, review.created_at)
        self.assertEqual(updated_at, review.updated_at)
        # Validate additional attributes
        self.assertEqual(object_data["Country"], review.Country)

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
        instance2 = Review()
        self.assertLess(self.instance.created_at, instance2.created_at)

    def test_updated_time(self) -> None:
        """
        check if updated time of two instance created at different time
        """
        instance2 = Review()
        self.assertLess(self.instance.updated_at, instance2.updated_at)

    def test_new_attribute_exist(self):
        """if name attribute exist
        """
        self.instance.place_id = "Accra233"
        self.instance.user_id = "1234"
        self.instance.text = "Settings"
        obj_dct = self.instance.to_dict()
        self.assertIn("place_id", obj_dct)
        self.assertIn("user_id", obj_dct)
        self.assertIn("text", obj_dct)

    def test_save_method_updated_time(self) -> None:
        """test if save method updated the updated_at attribute
        """
        instance2 = Review()
        updated_time = instance2.updated_at
        instance2.save()
        self.assertNotEqual(updated_time, instance2.updated_at)
        self.assertLess(updated_time, instance2.updated_at)

    def test_str(self) -> None:
        """test if str representation is overide"""
        dict_str = f"[Review] ({self.instance.id}) {self.instance.__dict__}"
        self.assertEqual(dict_str, str(self.instance))

    def test_to_method(self) -> None:
        """test to_dict method
        """
        obj_dict = self.instance.to_dict()
        self.assertEqual(obj_dict["__class__"], "Review")
        self.assertIsInstance(obj_dict["created_at"], str)
        self.assertIsInstance(obj_dict["updated_at"], str)

    def test_updated_file(self) -> None:
        """test if the file is updated
        """
        self.instance.save()
        with open("file.json", "r", encoding="utf-8") as f:
            self.assertIn("Review." + self.instance.id, f.read())


if __name__ == "__main__":
    unittest.main()
