#!/usr/bin/python3
"""State class, a child of the BaseModel class
"""


from models.base_model import BaseModel


class State(BaseModel):
    """Handles State information and inherits from the
    BaseModel class

    Args:
        BaseModel (class): Parent class
    """
    name = ""
