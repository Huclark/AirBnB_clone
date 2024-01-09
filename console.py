#!/usr/bin/python3
"""Entry point of the command interpreter
"""


import cmd
import models
from models.base_model import BaseModel


class HBNBCommand(cmd.Cmd):
    """The HBNBCommand class
    """
    # custom prompt for program
    prompt = "(hbnb) "

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
        if not arg:
            print("** class name missing **")
        elif arg not in globals() or not isinstance(globals()[arg], type):
            print("** class doesn't exist **")
        else:
            new_instance = globals()[arg]()
            new_instance.save()
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
        elif argv[0] not in globals() or\
                not isinstance(globals()[argv[0]], type):
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
            arg: Command arguments

        Usage example: $ show BaseModel 1234-1234-1234
        """
        # Store various command arguments in a list
        argv = arg.split()
        
        # argv = ["BaseModel", "1234"]

        if self.validate_argv(argv):
            # Construct the key
            key = "{}.{}".format(argv[0], argv[1])
            # Retrieve all objects from storage
            obj_data = models.storage.all()
            # Check if object exists
            if key in obj_data:
                print(obj_data[key])
            else:
                print("** no instance found **")

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id
        and then updates the JSON file with the changes made

        Args:
            arg: The command arguments

        Usage example: $ destroy BaseModel 1234-1234-1234
        """
        # Store various command arguments in a list
        argv = arg.split()

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

    # def do_update(self, arg):
    #     argv = arg.split()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
