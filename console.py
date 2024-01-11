#!/usr/bin/python3
"""Entry point of the command interpreter
"""


import cmd
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
    # custom prompt for program
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
        # Retrieve command arguments
        argv = shlex.split(arg)

        # Check if user provided command arguments
        if not argv:
            print("** class name missing **")
        # Check if class matches an available class
        elif argv[0] not in self.__all_classes:
            print("** class doesn't exist **")

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
        elif argv[0] not in self.__all_classes:
            print("** class doesn't exist **")
            return False

        # Handle missing id argument
        elif len(argv) < 2:
            print("** instance id missing **")
            return False

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

        if self.validate_argv(argv):
            # Construct the key
            key = "{}.{}".format(argv[0], argv[1])
            # Retrieve all objects from storage
            obj_data = models.storage.all()
            obj = obj_data.get(key)
            # Check if object exists
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

        if self.validate_argv(argv):
            # Construct the key
            key = "{}.{}".format(argv[0], argv[1])
            # Retrieve all objects from storage
            obj_data = models.storage.all()
            # Check if object exists
            if key in obj_data:
                del obj_data[key]
                models.storage.save()
            else:
                print("** no instance found **")

    def do_all(self, arg):
        """Prints all the string representation of all instances based
        or not on the class name

        Args:
            arg (str): Command arguments

        Usage Example: $ all BaseModel or $ all
        """
        argv = shlex.split(arg)

        # print all instances if no argument exists
        if not arg:
            print([str(value) for _, value in models.storage.all().items()])
        else:
            # Validate argument
            if arg not in self.__all_classes:
                print("** class doesn't exist **")
                return

            # Retrieve all instances
            new_list = []

            # put all the target class' values in new_list
            for _, value in models.storage.all().items():
                # class_name = key.split(".")
                # if class_name[0] == argv[0]:
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
                        "<attribute value>"
        """
        argv = shlex.split(arg)

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
        print(count)
        return count
            

    def default(self, arg):
        # Split command line into words
        line = arg.split(".", 1)

        if len(line) < 2:
            print("*** Unknown syntax: {}".format(line[0]))
            return False
        
        if line[0] not in list(self.__all_classes.keys()):
            print("*** Unknown syntax: {}".format(arg))
            return False

        # class_name, command_all = line[0], line[1]
        command = line[1].split("(", 1)

        if len(command) < 2:
            print("*** Unknown syntax: {}".format(arg))
            return False

        if command[0] not in ["all", "create", "show", "destroy", "update", "count"]:
            print("*** Unknown syntax: {}".format(arg))
            return False

        if command[0] == "all":
            self.do_all(line[0])
            return

        if command[0] == "count":
            print(self.number_of_instances(line[0]))
            return

        object_id = command[1].split(")", 1)
        
        if command[0] == "show":
            self.do_show(line[0] + " " + object_id[0])
            return

        if command[0] == "destroy":
            self.do_destroy(line[0] + " " + object_id[0])
            return

        

if __name__ == "__main__":
    HBNBCommand().cmdloop()
