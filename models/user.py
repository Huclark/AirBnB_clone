#!/usr/bin/python3
"""User class, a child of the BaseModel class
"""


from models.base_model import BaseModel


class User(BaseModel):
    """Handles user information and inherits from the
    BaseModel class

    Args:
        BaseModel (class): Parent class
    """
    email = ""
    password = ""
    first_name = ""
    last_name = ""
