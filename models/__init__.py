from .base_model import BaseModel
from .engine.file_storage import FileStorage
from .user import User
from .state import State
from .city import City
from .amenity import Amenity
from .place import Place
from .review import Review

storage = FileStorage()
storage.reload()
