#!/usr/bin/python3
"""find a description
"""


from models.engine.file_storage import FileStorage


# Create an instance of FileStorage
storage = FileStorage()

# Call reload() method on storage
storage.reload()
