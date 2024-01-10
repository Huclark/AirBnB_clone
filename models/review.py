#!/usr/bin/python3
"""Review class, a child of the BaseModel class
"""


from models.base_model import BaseModel


class Review(BaseModel):
    """Review State information and inherits from the
    BaseModel class

    Args:
        BaseModel (class): Parent class
    """
    place_id = ""
    user_id = ""
    text = ""
