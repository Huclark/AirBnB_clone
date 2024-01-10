#!/usr/bin/python3
"""Amenity class, a child of the BaseModel class
"""


from models.base_model import BaseModel


class Amenity(BaseModel):
    """Handles Amenity information and inherits from the
    BaseModel class

    Args:
        BaseModel (class): Parent class
    """
    name = ""
