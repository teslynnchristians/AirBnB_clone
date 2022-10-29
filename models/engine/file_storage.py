'''file_storage.py
'''
import json

from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    '''FileStorage class:
    that serializes instances to a JSON file and
    deserializes JSON file to instances
    __file_path:
        string - path to the JSON file (ex: file.json)
    __objects:
        dictionary - empty but will store all objects by <class name>.id
    '''
    __file_path = "file.json"
    __objects = {}

    def all(self):
        '''returns the dictionary __objects
        '''

        return FileStorage.__objects

    def new(self, obj):
        '''sets in __objects the obj with key <obj class name>.id
        '''

        key = f"{obj.__class__.__name__}.{obj.id}"
        FileStorage.__objects.setdefault(key, obj)

    def save(self):
        '''serializes __objects to the JSON file (path: __file_path)
        '''

        to_save = {}
        for key, obj in FileStorage.__objects.items():
            key = f"{obj.__class__.__name__}.{obj.id}"
            to_save.setdefault(key, obj.to_dict())

        with open(self.__file_path, 'w') as f_obj:
            json.dump(to_save, f_obj, indent=4)

    def reload(self):
        ''' deserializes the JSON file to __objects
        (only if the JSON file (__file_path) exists
        '''

        try:
            with open(self.__file_path, 'r') as f_obj:
                data = json.load(f_obj)

            for obj_dict in data.values():
                key = f"{obj_dict['__class__']}.{obj_dict['id']}"
                FileStorage.__objects.\
                    setdefault(key, eval(obj_dict['__class__'])(**obj_dict))

        except FileNotFoundError as e:
            pass

    def delete(self, obj):
        name = obj.__class__.__name__
        id = obj.id
        key = ".".join([name, id])
        if key in FileStorage.__objects:
            del FileStorage.__objects[key]
            self.save()
            return True

        return False
