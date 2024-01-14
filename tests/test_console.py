#!/usr/bin/python3
"""Unit tests for the Console
"""


from console import HBNBCommand
import io
from io import StringIO
from os import remove
import sys
import unittest
from unittest.mock import patch, create_autospec
import models
from models.base_model import BaseModel


class TestHBNBCommand(unittest.TestCase):
    """HBNBCommand class test cases for the console

    Args:
        unittest (module): Module for unit tests
    """
    def setUp(self):
        """Set up resources and  configurations needed for the
        test cases
        """
        # Create an instance of the HBNBCommand class
        self.console = HBNBCommand()
        # Create a mock stdin and stdout
        self.mock_stdin = create_autospec(sys.stdin)
        self.mock_stdout = create_autospec(sys.stdout)
        # Redirect sys.stdout to StringIO()
        self.out = StringIO()
        sys.stdout = self.out
        # Clear the __objects dictionary in FileStorage
        models.storage._FileStorage__objects.clear()

    def tearDown(self):
        """Clean up any resources or configurations to prepare for
        new tests.
        """
        # Restore sys.stdout to its original value
        sys.stdout = sys.__stdout__
        # Remove the JSON file if it exists
        try:
            remove("file.json")
        except FileNotFoundError:
            pass
        # Clear the __objects dictionary in FileStorage
        models.storage._FileStorage__objects.clear()
        # Clear the content of the StringIO object
        self.clear_StringIO()

    def clear_StringIO(self):
        """Clears the content of the StringIO object
        """
        # Truncate the content of the StringIO object to 0 bytes
        self.out.truncate(0)
        # Set tje position of the StringIO object to the beginning
        self.out.seek(0)

    def test_do_create(self, mock_stdout, mock_stdin):
        """Test the do_Create() method

        Args:
            mock_stdout (StringIO): Captures and inspect printed output
        """


if __name__ == "__main__":
    unittest.main()
