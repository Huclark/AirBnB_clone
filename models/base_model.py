#!/usr/bin/python3
"""Base Model for all classes
"""


from uuid import uuid4
from datetime import datetime
import models


class BaseModel:
    """The super class
    """
    def __init__(self, *args, **kwargs):
        """Initializes a BaseModel instance
        """
        if kwargs:
            for key, value in kwargs.items():
                if key == "__class__":
                    continue
                if key in ["created_at", "updated_at"]:
                    value = datetime.fromisoformat(value)
                setattr(self, key, value)
        else:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)

    def __str__(self):
        """String representation of instance object

        Returns:
            str: string representation of instance object
        """
        return "[{}] ({}) {}".format(self.__class__.__name__,
                                     self.id, self.__dict__)

    def save(self):
        """Updates the public instance attribute, `updated at`
        with the current datetime
        """
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """A dictionary containing all keys/values of __dict__
        of the instance.

        Returns:
            dict: A dictionary of the instance
        """
        instance_dict = self.__dict__.copy()
        instance_dict["__class__"] = self.__class__.__name__
        instance_dict["created_at"] = self.created_at.isoformat()
        instance_dict["updated_at"] = self.updated_at.isoformat()
        return instance_dict
