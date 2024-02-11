#!/usr/bin/python3
"""Entry point of the command interpreter
"""


import ast
import cmd
import re
import shlex
import models
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class HBNBCommand(cmd.Cmd):
    """The HBNBCommand class
    """
    # Custom prompt for program
    prompt = "(hbnb) "

    # Create all available classes
    __all_classes = {
        "Amenity": Amenity,
        "BaseModel": BaseModel,
        "City": City,
        "Place": Place,
        "Review": Review,
        "State": State,
        "User": User,
    }

    # Boolean flag for update command
    __flag = True

    def do_quit(self, arg):
        """Quit command to exit the program
        """
        return True

    def do_EOF(self, arg):
        """Use ctrl+D as keyboard shortcut to exit program
        """
        print()
        return True

    def do_help(self, arg):
        """Shows help message"""
        super().do_help(arg)

    def emptyline(self):
        """Does nothing on an empty line so as to handle
        the case where emptyline + ENTER key is used
        """
        pass

    def do_create(self, arg):
        """Creates a new instance of BaseModel, saves it (to the JSON file)
        and prints the id.

        Args:
            arg (str): The argument passed to create command

        Usage example: $ create BaseModel
        """
        # Check if user provided command arguments
        if not arg:
            print("** class name missing **")
            return False
        # Retrieve command arguments
        argv = shlex.split(arg)
        # Print an error if class does not match the available classes
        if argv[0] not in self.__all_classes:
            print("** class doesn't exist **")
            return False
        # Create a new instance of the specified class
        new_instance = self.__all_classes[argv[0]]()
        # Save the new instance
        new_instance.save()
        # Print the the instance id
        print(new_instance.id)

    def validate_argv(self, argv):
        """Validates the command arguments and print error messages
        if needed.

        Args:
            argv (list): A list of the command arguments

        Returns:
            bool: True if validation passes. False if otherwise.
        """
        # Handle no argument
        if not argv:
            print("** class name missing **")
            return False
        # Handle invalid class
        if argv[0] not in self.__all_classes:
            print("** class doesn't exist **")
            return False
        # Handle missing id argument
        if len(argv) < 2:
            print("** instance id missing **")
            return False
        # Argument is valid
        return True

    def do_show(self, arg):
        """Prints the string representation of an instance based on the
        class name and id.

        Args:
            arg(str): Command arguments

        Usage example: $ show BaseModel 1234-1234-1234
        """
        # Store various command arguments in a list
        argv = shlex.split(arg)
        # Validate the command arguments
        if self.validate_argv(argv):
            # Construct the key
            key = "{}.{}".format(argv[0], argv[1])
            # Retrieve all objects from storage
            obj_data = models.storage.all()
            # Retrieve the object using its key
            obj = obj_data.get(key)
            # Check if object exists and print
            print(obj if obj else "** no instance found **")

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id
        and then updates the JSON file with the changes made

        Args:
            arg(str): The command arguments

        Usage example: $ destroy BaseModel 1234-1234-1234
        """
        # Store various command arguments in a list
        argv = shlex.split(arg)
        # Validate the command arguments
        if self.validate_argv(argv):
            # Construct the key
            key = "{}.{}".format(argv[0], argv[1])
            # Retrieve all objects from storage
            obj_data = models.storage.all()
            # Check if object exists
            if key in obj_data:
                # Delete the object
                del obj_data[key]
                # Save the changes onto the JSON file
                models.storage.save()
            else:
                # Print error message if object does not exist
                print("** no instance found **")

    def do_all(self, arg):
        """Prints all the string representation of all instances based
        or not on the class name

        Args:
            arg (str): Command arguments

        Usage Example: $ all BaseModel or $ all
        """
        # Print all instances if no argument exists
        if not arg:
            print([str(value) for value in models.storage.all().values()])
        else:
            # Store various command arguments in a list
            argv = shlex.split(arg)
            # Validate argument
            if argv[0] not in self.__all_classes:
                print("** class doesn't exist **")
                return
            # Create a list to contain all instances of the class
            new_list = []
            # Iterate over the instances dictionary
            for obj in models.storage.all().values():
                # If an instance is found, append to new_list
                if argv[0] == type(obj).__name__:
                    new_list.append(str(obj))
            # print list
            print(new_list)

    def do_update(self, arg):
        """Updates an instance based on the class name and id
        by adding or updating attribute and then saves the changes to
        the file.json file

        Args:
            arg (str): Command arguments

        Usage example: update <class name> <id> <attribute name>
                        <attribute value>
        """
        # True means use shlex to split command arguments
        if self.__flag:
            argv = shlex.split(arg)
        # False means construct list of arguments without shlex
        else:
            # Get rid of commas
            line = arg.split(", ")
            # line = ['<class_name> <"id">', '"attr_name"', '"attr_value"']
            # Retrieve the class name and id
            class_name, obj_id = line[0].split()
            # Create a list to contain all command arguments
            argv = []
            # Append the class name to list
            argv.append(class_name)
            # Strip the quotes off id and append to list
            argv.append(obj_id.strip('"'))
            # Strip the quotes off attribute name and append to list
            argv.append(line[1].strip('"'))
            # Strip the quotes off attribute value and append to list
            argv.append(line[2].strip('"'))
            # argv = [class_name, id, attribute name, attribute value]
        # Validate the command arguments
        if self.validate_argv(argv):
            # Construct the key
            key = "{}.{}".format(argv[0], argv[1])
            # Retrieve all instances from storage
            all_instances = models.storage.all()
            # Check if instance exists
            if key not in all_instances:
                print("** no instance found **")
                return
            # Check if attribute name is provided
            if len(argv) < 3:
                print("** attribute name missing **")
                return
            # Check for missing attribute value
            if len(argv) < 4:
                print("** value missing **")
                return
            # Set the new attribute in the right instance
            setattr(all_instances[key], argv[2], argv[3])
            # Save the changes into JSON file
            all_instances[key].save()

    @staticmethod
    def number_of_instances(class_name):
        """Counts the number of instances of a specific class

        Args:
            class_name (str): Name of class

        Returns:
            int: Number of instances of the specified class
        """
        # Intialise count variable to 0
        count = 0
        # Iterate over storage dictionary
        for _, value in models.storage.all().items():
            # If the specified class is encountered increment count
            if type(value).__name__ == class_name:
                count += 1
        # Return number of instances found
        return count

    def default(self, line):
        """Handles the default behaviour of the command-line interpreter

        Args:
            line (str): Command and arguments from the command-line

        Returns:
            bool: False if the syntax is unknown or the command is invalid;
                  otherwise, no return value

        Description:
            This method parses and executes commands related to managing
            instances of different classes. The syntax for each command
            is validated, and appropriate actions are taken based on the input.

        Usage Examples:
            $ <class name>.all()
            $ <class name>.count()
            $ <class name>.show(<id>)
            $ <class name>.destroy(<id>)
            $ <class name>.update(<id>, <attribute name>, <attribute value>)
            $ <class name>.update(<id>, <dictionary representation>)
        """
        # Split command line into a list of class name and command
        arg = line.split(".", 1)
        # arg = [classname, "command(arguments)"]
        # Validate class name and command syntax
        if len(arg) < 2:
            print("*** Unknown syntax: {}".format(arg[0]))
            return
        if arg[0] not in list(self.__all_classes.keys()):
            print("** class doesn't exist **")
            return
        # Put command and arguments into a list
        command = arg[1].split("(", 1)
        # command = ["command", "argument"]
        # Validate command
        if not self.all_count_helper(command):
            print("*** Unknown syntax: {}".format(line))
            return
        # Execute do_all if command is "all"
        if command[0] == "all":
            self.do_all(arg[0])
            return
        # Print number of instances if command is "count"
        if command[0] == "count":
            print(self.number_of_instances(arg[0]))
            return
        # Check if command is show, destroy or update
        # and has the correct syntax
        if command[0] in ["show", "destroy", "update"] and\
                not command[1].endswith(")"):
            print("*** Unknown syntax: {}".format(line))
            return
        # Obtain the object id
        object_id = command[1].split(")", 1)
        # Execute do_show if command is "show"
        if command[0] == "show":
            # if len(object_id) > 1:
            #     print("*** Unknown syntax: {}".format(line))
            #     return
            self.do_show(arg[0] + " " + object_id[0])
            return
        # Execute do_destroy if command is "destroy"
        if command[0] == "destroy":
            # if len(object_id) > 1:
            #     print("*** Unknown syntax: {}".format(line))
            #     return
            self.do_destroy(arg[0] + " " + object_id[0])
            return
        # Execute do_update if command is "update"
        if command[0] == "update":
            # Strip ")" off the arguments string
            args = command[1].rstrip(")")
            # args = "id and other arguments"
            # Check if args matches the pattern,
            # "id, {} and any non-whitespace character"
            first_match = re.match(r'^(.*)\s*,\s*({.*})\s*(\S+)', args)
            # Check if args maatches the pattern,"id, {}"
            matchdata = re.match(r'^(.*)\s*,\s*({.*})', args)
            # True if args matches the exact pattern, "id, {}"
            if not first_match and matchdata:
                try:
                    # Retrieve string representation of id
                    obj_id = str(matchdata.group(1))
                    # Convert string representation of dictionary to a dict
                    attribute_dict = ast.literal_eval(matchdata.group(2))
                    # Iterate over dictionary of attribute names and values
                    for attribute_name, attribute_value in\
                            attribute_dict.items():
                        # Construct class_name and cmd arguments as a string
                        arguments = arg[0] + " " + obj_id + " " +\
                            str(attribute_name) + " " + str(attribute_value)
                        # arguments = "class_name id attr_name attr_value"
                        self.do_update(arguments)
                except (ValueError, SyntaxError):
                    # If literal_eval fails, print syntax error
                    print("*** Unknown syntax: {}".format(line))
            # True if args does not match the exact pattern, "id, {}"
            else:
                # Check if arguments > 4 or arguments < 3
                match_a =\
                    re.match(r'^(.*)\s*,\s*(.*)\s*,\s*(.*)\s*,\s*(\S+)', args)
                if match_a or len(args.split(", ")) < 3:
                    print("*** Unknown syntax: {}".format(line))
                    return
                # Construct argument for do_update
                arguments = arg[0] + " " + args
                # Set flag to False so do_update does not use shlex.split()
                self.__flag = False
                self.do_update(arguments)
            return

    @staticmethod
    def all_count_helper(command):
        """Helper function for validating arguments for calling
        do_all() and do_count methods

        Args:
            command (list): List of command and arguments
            line (str): Commands and arguments from the command-line

        Returns:
            bool: False if command or arguments are invalid; otherwise, it
                  returns True
        """
        if len(command) < 2:
            return False

        if command[0] not in\
                ["all", "create", "show", "destroy", "update", "count"]:
            return False

        if command[0] in ["all", "count"] and not command[1].startswith(")"):
            return False
        return True


if __name__ == "__main__":
    HBNBCommand().cmdloop()
