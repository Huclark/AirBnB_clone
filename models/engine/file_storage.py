#!/usr/bin/python3
"""FileStorage class
"""


from models.base_model import BaseModel
import json


class FileStorage:
    """This class serializes instances to a JSON file
    and deserializes JSON files to instances
    """
    __file_path = "file.json"
    __objects = {}

    # __objects = { class.id : "[{} ({}) {}]"}

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
                for key, value in load_obj.items():
                    class_name, obj_id = key.split(".")
                    self.__objects[key] = globals()[class_name](**value)
        except FileNotFoundError:
            pass
