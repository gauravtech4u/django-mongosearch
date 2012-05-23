#!/usr/bin/env python
from django.conf import settings

def adminpath( context ):
    # return the value you want as a dictionnary. you may add multiple values in there.
    return {'ADMIN_PATH': settings.ADMIN_PATH}
    
