'''review.py
'''

from models import BaseModel


class Review(BaseModel):
    '''Class Review
    '''

    place_id = ""
    user_id = ""
    text = ""
