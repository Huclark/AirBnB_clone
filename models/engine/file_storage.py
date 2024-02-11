#!/usr/bin/python3
"""FileStorage class
"""

import json
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class FileStorage:
    """This class serializes instances to a JSON file
    and deserializes JSON files to instances
    """
    __file_path = "file.json"

    # Eg: __objects = {class.id: "address of BaseModel Instance"}
    __objects = {}

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

    def all(self):
        """Returns the dictionary `__objects`

        Returns:
            dict: A dictionary of all objects
        """
        return self.__objects

    def new(self, obj):
        """Updates the dictionary objects with a new object

        Args:
            obj: The new object to be added
        """
        # Construct key
        key = "{}.{}".format(obj.__class__.__name__, obj.id)

        # Assign Value to key
        self.__objects[key] = obj

    def save(self):
        """Serializes `__objects` to a JSON file(__file_path)
        """
        new_dict = {}
        for key, obj in self.__objects.items():
            new_dict[key] = obj.to_dict()
        with open(self.__file_path, "w", encoding="utf-8") as file:
            json.dump(new_dict, file)

    def reload(self):
        """Deserializes the JSON file (__file_path) to update the objects.
        If the JSON file (__file_path) doesn't exist, it does nothing
        """
        try:
            with open(self.__file_path, "r", encoding="utf-8") as file:
                load_obj = json.load(file)
                for key, obj in load_obj.items():
                    clsname = key.split(".")
                    self.__objects[key] = self.__all_classes[clsname[0]](**obj)
        except (FileNotFoundError, PermissionError, TypeError):
            pass
