'''user.py
'''

from models import BaseModel


class User(BaseModel):
    '''Class User
    '''

    email = ""
    password = ""
    first_name = ""
    last_name = ""
