from .dependencies import create_tables

# Initialize the database tables
create_tables()

# You can add any other initialization code here

# Optionally, you can define __all__ to control what gets imported with "from app import *"
__all__ = ['models', 'schemas', 'crud', 'dependencies']