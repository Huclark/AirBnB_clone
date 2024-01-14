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
from uuid import UUID
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
        self.clear_stringio()

    def clear_stringio(self):
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

    def test_do_quit(self):
        """Tests the quit command
        """
        # Simulate inputting quit
        self.assertTrue(self.console.onecmd("quit"))
        # Check if anything is printed to stdout
        self.assertEqual("", self.out.getvalue())
        # Simulate inputting quit with improper syntax
        self.assertFalse(self.console.onecmd("QUIT"))
        # Get the expected output
        error_message = "*** Unknown syntax: QUIT\n"
        # Assert the output
        self.assertEqual(error_message, self.out.getvalue())
        # Check if quit command was handled successfully
        self.assertTrue(self.console.onecmd("quit kaks ka kascadk"))

    def test_eof(self):
        """Test EOF(Ctrl + D)
        """
        # Simulate an "EOF" input
        self.assertTrue(self.console.onecmd("EOF"))
        # Ascertain it prints a new line as output before exiting console
        self.assertEqual(self.out.getvalue(), "\n")

    def test_help(self):
        """Test help command
        """
        self.assertIsNone(self.console.onecmd("help"))

    def test_create(self):
        """Test the create command
        """
        # Test no argument
        self.assertFalse(self.console.onecmd("create"))
        # Check error message
        self.assertEqual(self.out.getvalue(), "** class name missing **\n")
        # Clear StringIO object
        self.clear_stringio()
        # Test invalid class
        self.assertFalse(self.console.onecmd("create John"))
        # Check error message
        self.assertEqual(self.out.getvalue(), "** class doesn't exist **\n")

        # Test if an instance is created successfully
        # Clear StringIO object
        self.clear_stringio()
        # Simulate the creation of a User instance
        self.assertIsNone(self.console.onecmd("create User"))
        # Extract the id string form stdout and strip the \n character
        str_id = self.out.getvalue()[:-1]
        try:
            # Check if the id string matches the string representation
            # of the UUID object
            result = str(UUID(str_id)) == str_id
        except (ValueError, TypeError):
            result = False
        self.assertTrue(result)
        


if __name__ == "__main__":
    unittest.main()
