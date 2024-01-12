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
        the case where emptyline + ENTER key is used"""
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
        # Create a new instance and print its id.
        else:
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
            print([str(value) for _, value in models.storage.all().items()])
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
            for _, value in models.storage.all().items():
                # If an instance is found, append to new_list
                if argv[0] == type(value).__name__:
                    new_list.append(str(value))
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
        if self.__flag:
            argv = shlex.split(arg)

        else:
            line = arg.split(", ")
            class_name, str_id = line[0].split()
            argv = []
            argv.append(class_name)
            argv.append(str_id.strip('"'))
            argv.append(line[1].strip('"'))
            argv.append(line[2].strip('"'))

        if self.validate_argv(argv):
            # Construct the key
            key = "{}.{}".format(argv[0], argv[1])
            # Retrieve all objects from storage
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
            all_instances[key].save()

    @staticmethod
    def number_of_instances(class_name):
        count = 0
        for _, value in models.storage.all().items():
            if type(value).__name__ == class_name:
                count += 1
        return count

    def default(self, arg):
        # Split command line into words
        line = arg.split(".", 1)
        # [classname, "comman(xxx)"]

        if len(line) < 2:
            print("*** Unknown syntax: {}".format(line[0]))
            return False

        if line[0] not in list(self.__all_classes.keys()):
            print("*** Unknown syntax: {}".format(arg))
            return False

        # class_name, command_all = line[0], line[1]
        command = line[1].split("(", 1)
        # command = ["command", xxxxx)]
        if len(command) < 2:
            print("*** Unknown syntax: {}".format(arg))
            return False

        if command[0] not in ["all", "create", "show", "destroy", "update", "count"]:
            print("*** Unknown syntax: {}".format(arg))
            return False

        if command[0] in ["all", "count"] and not command[1].startswith(")"):
            print("*** Unknown syntax: {}".format(arg))
            return False

        if command[0] == "all":
            self.do_all(line[0])
            return

        if command[0] == "count":
            print(self.number_of_instances(line[0]))
            return

        if command[0] in ["show", "destroy", "update"] and not command[1].endswith(")"):
            print("*** Unknown syntax: {}".format(arg))
            return False

        object_id = command[1].split(")", 1)

        if command[0] == "show":
            self.do_show(line[0] + " " + object_id[0])
            return

        if command[0] == "destroy":
            self.do_destroy(line[0] + " " + object_id[0])
            return

        if command[0] == "update":
            args = command[1].rstrip(")")
            first_match = re.match(r'^(.*)\s*,\s*({.*})\s*(\S+)', args)
            if not first_match:
                matchdata = re.match(r'^(.*)\s*,\s*({.*})', args)
                if matchdata:
                    obj_id = matchdata.group(1)
                    attribute_dict = ast.literal_eval(matchdata.group(2))
                    for attribute_name, attribute_value in attribute_dict.items():
                        ag = line[0] + " " + obj_id + " " + attribute_name + " " + attribute_value
                        self.do_update(ag)

            if first_match or not matchdata:
                match_a = re.match(r'^(.*)\s*,\s*(.*)\s*,\s*(.*)\s*,\s*(\S+)', args)
                if match_a or len(args.split(", ")) < 3:
                    print("*** Unknown syntax: {}".format(arg))
                    return False
                arguments = line[0] + " " + args
                self.__flag = False
                self.do_update(arguments)

            return


if __name__ == "__main__":
    HBNBCommand().cmdloop()
