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
        """
        if not arg:
            print("** class name missing **")
        elif arg not in globals() or not isinstance(globals()[arg], type):
            print("** class doesn't exist **")
        else:
            newInstance = globals()[arg]()
            newInstance.save()
            print(newInstance.id)


if __name__ == "__main__":
    HBNBCommand().cmdloop()
