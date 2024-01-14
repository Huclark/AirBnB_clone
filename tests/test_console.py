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
        # Create a mock stdin and stdout
        self.mock_stdin = create_autospec(sys.stdin)
        self.mock_stdout = create_autospec(sys.stdout)
        # Create an instance of the HBNBCommand class
        self.console = HBNBCommand(stdin=self.mock_stdin, stdout=self.mock_stdout)
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

    # def _last_write(self, nr=None):
    #     """:return: last `n` output lines"""
    #     if nr is None:
    #         return self.mock_stdout.write.call_args[0][0]
    #     return "".join(map(lambda c: c[0][0],
    #                        self.mock_stdout.write.call_args_list[-nr:]))

    def test_enter_with_noinput(self):
        """Tests for an empty command (empty string or newline character)

        Note: onecmd() returns True for successful handling and False otherwise
              In this case, an empty command should not be handled successfully,
              so the expectation is False
        """
        # Simulate pressing the enter key with no input
        self.assertFalse(self.console.onecmd("\n"))
        # Check if the standard output is an empty string
        self.assertEqual(self.out.getvalue(), "")
        


if __name__ == "__main__":
    unittest.main()
