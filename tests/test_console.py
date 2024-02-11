#!/usr/bin/python3
"""Unit tests for the Console
"""


from io import StringIO
import json
from os import remove
import sys
import unittest
from unittest.mock import create_autospec
from uuid import UUID
from console import HBNBCommand
import models


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
        self.console =\
            HBNBCommand(stdin=self.mock_stdin, stdout=self.mock_stdout)
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
        # Set the position of the StringIO object to the beginning
        self.out.seek(0)

    def test_enter_with_noinput(self):
        """Tests for an empty command (empty string or newline character)

        Note: onecmd() returns True for successful handling and False otherwise
              In this case, an empty command should not be handled
              successfully, so the expectation is False
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
        # Check if the id is of a UUID type
        self.assertIsInstance(UUID(str_id), UUID)

    def test_all(self):
        """Test the all command
        """
        # Create two instances
        self.assertFalse(self.console.onecmd("create City"))
        self.assertFalse(self.console.onecmd("create User"))
        # Clear StringIO
        self.clear_stringio()
        # Simulate the all method with no argument
        self.assertFalse(self.console.onecmd("all"))
        # all() prints the string representation of a list of
        # all instances to stdout
        # Hence, deserialise the string representation of the list
        all_output = json.loads(self.out.getvalue())
        # Confirm if the output is a list
        self.assertIsInstance(all_output, list)
        # Confirm length of list
        self.assertEqual(len(all_output), 2)
        # Check if each object in the list is a string
        for obj in all_output:
            self.assertIsInstance(obj, str)
        # Create two more City instances to test all with arguments
        self.assertFalse(self.console.onecmd("create City"))
        self.assertFalse(self.console.onecmd("create City"))
        # Clear StringIO
        self.clear_stringio()
        # Simulate the all method with argument
        self.assertFalse(self.console.onecmd("all City"))
        # Deserialise the string representation of the list
        all_output = json.loads(self.out.getvalue())
        # Confirm if the output is a list
        self.assertIsInstance(all_output, list)
        # Confirm length of list
        self.assertEqual(len(all_output), 3)
        # Check if each object in the list is a string
        for obj in all_output:
            self.assertIsInstance(obj, str)

    def test_update(self):
        """Test the update() method
        """
        # Test no argument
        self.assertFalse(self.console.onecmd("update"))
        # Check error message
        self.assertEqual(self.out.getvalue(), "** class name missing **\n")
        # Clear StringIO object
        self.clear_stringio()
        # Test invalid class
        self.assertFalse(self.console.onecmd("update John"))
        # Check error message
        self.assertEqual(self.out.getvalue(), "** class doesn't exist **\n")
        # Clear StringIO object
        self.clear_stringio()
        # Create a City instance
        self.assertFalse(self.console.onecmd("create City"))
        # Extract the id string form stdout and strip the \n character
        str_id = self.out.getvalue()[:-1]
        # Clear StringIO object
        self.clear_stringio()
        # Test missing id
        self.assertFalse(self.console.onecmd("update City"))
        # Check error message
        self.assertEqual(self.out.getvalue(), "** instance id missing **\n")
        # Clear StringIO object
        self.clear_stringio()
        # Test if instance exists
        self.assertFalse(self.console.onecmd("update City 1234-24442323"))
        # Check error message
        self.assertEqual(self.out.getvalue(), "** no instance found **\n")
        # Clear StringIO object
        self.clear_stringio()
        # Test if attribute name exists
        self.assertFalse(self.console.onecmd("update City " + str_id))
        # Check error message
        self.assertEqual(self.out.getvalue(), "** attribute name missing **\n")
        # Clear StringIO object
        self.clear_stringio()
        # Test if attribute value exists
        self.assertFalse(self.console.onecmd("update City " + str_id + " red"))
        # Check error message
        self.assertEqual(self.out.getvalue(), "** value missing **\n")
        # Clear StringIO object
        self.clear_stringio()
        # Test if instance data is updated
        input_ = "update City " + str_id + " 'first_name' 'John'"
        self.assertFalse(self.console.onecmd(input_))
        # Clear StringIO object
        self.clear_stringio()
        # Simulate the all method with City as argument
        self.assertFalse(self.console.onecmd("all City"))
        # Check for the update
        self.assertTrue("'first_name': 'John'" in self.out.getvalue())

    def test_update_alt_syntax(self):
        """Test the alternative syntax for update command
        """
        # Create a City instance
        self.assertFalse(self.console.onecmd("create City"))
        # Extract the id string form stdout and strip the \n character
        str_id = self.out.getvalue()[:-1]
        # Clear String_IO object
        self.clear_stringio()
        # Test improper syntax for dictionary argument
        user_input = "City.update(" + str_id + " {'name': 'John')"
        self.assertIsNone(self.console.onecmd(user_input))
        error_msg = "*** Unknown syntax: " + user_input + "\n"
        self.assertEqual(self.out.getvalue(), error_msg)
        # Clear String_IO object
        self.clear_stringio()
        # Test too many arguments (dictionary method)
        # Construct user input
        user_input =\
            "City.update(" + str_id + " {'name': 'John'} " + "JohnDoe)"
        # Simulate command
        self.assertIsNone(self.console.onecmd(user_input))
        # Print out all City instances
        self.assertIsNone(self.console.onecmd("all City"))
        # Check if attribute name is in output
        self.assertTrue("{'name': 'John'}" in self.out.getvalue())
        self.clear_stringio()
        # Construct user input
        user_input = "City.update(" + str_id +\
            " {'name': 'John', 1: 'ball'} " + "JohnDoe"
        # Simulate command
        self.assertIsNone(self.console.onecmd(user_input))
        # Check output
        error_msg = "*** Unknown syntax: " + user_input + "\n"
        self.assertEqual(self.out.getvalue(), error_msg)

    def test_count(self):
        """Tests the count command
        """
        # Create the instances
        self.assertFalse(self.console.onecmd("create City"))
        self.assertFalse(self.console.onecmd("create City"))
        self.assertFalse(self.console.onecmd("create City"))
        self.assertFalse(self.console.onecmd("create Amenity"))
        self.assertFalse(self.console.onecmd("create Place"))
        # Clear String_IO object
        self.clear_stringio()
        # Print number of instances
        self.assertIsNone(self.console.onecmd("City.count()"))
        # Deserialize the string representation of number
        no_of_instances = json.loads(self.out.getvalue())
        # Ascertain number of City instances
        self.assertEqual(no_of_instances, 3)

    def test_show(self):
        """Test show command
        """
        # Test no argument
        self.assertFalse(self.console.onecmd("show"))
        # Check error message
        self.assertEqual(self.out.getvalue(), "** class name missing **\n")
        # Clear StringIO object
        self.clear_stringio()
        # Test invalid class
        self.assertFalse(self.console.onecmd("show John"))
        # Check error message
        self.assertEqual(self.out.getvalue(), "** class doesn't exist **\n")
        # Clear StringIO object
        self.clear_stringio()
        # Create a City instance
        self.assertFalse(self.console.onecmd("create City"))
        # Extract the id string form stdout and strip the \n character
        str_id = self.out.getvalue()[:-1]
        # Clear StringIO object
        self.clear_stringio()
        # Test missing id
        self.assertFalse(self.console.onecmd("show City"))
        # Check error message
        self.assertEqual(self.out.getvalue(), "** instance id missing **\n")
        # Clear StringIO object
        self.clear_stringio()
        # Test if instance exists
        self.assertFalse(self.console.onecmd("show City 1234-2444-2323-2323"))
        # Check error message
        self.assertEqual(self.out.getvalue(), "** no instance found **\n")
        # Clear StringIO object
        self.clear_stringio()
        # Clear StringIO
        self.clear_stringio()
        # Simulate the show method with argument
        self.assertIsNone(self.console.onecmd("show City " + str_id))
        # Confirm if the output contains the City id
        self.assertTrue(str_id in self.out.getvalue())
        # Clear String_IO object
        self.clear_stringio()
        # Construct user input
        user_input = "City.show(" + str_id + ")"
        # Simulate command
        self.assertIsNone(self.console.onecmd(user_input))
        # Confirm if the output contains the City id
        self.assertTrue(str_id in self.out.getvalue())

    def test_destroy(self):
        """Test destroy method
        """
        # Test no argument
        self.assertFalse(self.console.onecmd("destroy"))
        # Check error message
        self.assertEqual(self.out.getvalue(), "** class name missing **\n")
        # Clear StringIO object
        self.clear_stringio()
        # Test invalid class
        self.assertFalse(self.console.onecmd("destroy John"))
        # Check error message
        self.assertEqual(self.out.getvalue(), "** class doesn't exist **\n")
        # Clear StringIO object
        self.clear_stringio()
        # Create a City instance
        self.assertFalse(self.console.onecmd("create City"))
        # Extract the id string form stdout and strip the \n character
        str_id = self.out.getvalue()[:-1]
        # Clear StringIO object
        self.clear_stringio()
        # Test missing id
        self.assertFalse(self.console.onecmd("destroy City"))
        # Check error message
        self.assertEqual(self.out.getvalue(), "** instance id missing **\n")
        # Clear StringIO object
        self.clear_stringio()
        # Test if instance exists
        self.assertFalse(self.console.onecmd("destroy City 1234-244-2323"))
        # Check error message
        self.assertEqual(self.out.getvalue(), "** no instance found **\n")
        # Clear StringIO object
        self.clear_stringio()
        # Clear StringIO
        self.clear_stringio()
        # Simulate the show method with argument
        self.assertIsNone(self.console.onecmd("destroy City " + str_id))
        # Confirm if the output contains the City id
        self.assertTrue(str_id not in self.out.getvalue())
        # Clear String_IO object
        self.clear_stringio()
        # Construct user input
        user_input = "City.destroy(" + str_id + ")"
        # Simulate command
        self.assertIsNone(self.console.onecmd(user_input))
        # Confirm if the output contains the City id
        self.assertTrue(str_id not in self.out.getvalue())


if __name__ == "__main__":
    unittest.main()
