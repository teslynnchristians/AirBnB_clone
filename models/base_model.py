#!/usr/bin/python3

'''Base Class for all models
'''
import models

from datetime import datetime
from uuid import uuid4


class BaseModel:
    '''Base Model class
    '''
    def __init__(self, *args, **kwargs):
        '''Initializes attributes of BaseModel instance
        '''

        if kwargs:
            for name, attr in kwargs.items():
                if name != '__class__':
                    if name not in ['created_at', 'updated_at']:
                        self.__setattr__(name, attr)
                    else:
                        self.__setattr__(name, datetime.fromisoformat(attr))
        else:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)

    def __str__(self):
        '''returns information about BaseModel instance.
        '''

        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        '''updates the public instance attribute updated_at
        with the current datetime
        '''

        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        '''
        returns a dictionary containing all keys/values
        of __dict__ of the instance
        '''

        to_dict = {}
        for key, value in self.__dict__.items():
            to_dict[key] = value

        to_dict['__class__'] = self.__class__.__name__

        to_dict['created_at'] = self.created_at.\
            strftime("%Y-%m-%dT%H:%M:%S.%f")

        to_dict['updated_at'] = self.updated_at.\
            strftime("%Y-%m-%dT%H:%M:%S.%f")

        return to_dict
