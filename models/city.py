#!/usr/bin/python3
"""City class, a child of the BaseModel class
"""


from models.base_model import BaseModel


class City(BaseModel):
    """Handles City information and inherits from the
    BaseModel class

    Args:
        BaseModel (class): Parent class
    """
    state_id = ""
    name = ""
