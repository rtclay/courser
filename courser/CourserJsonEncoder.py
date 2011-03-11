'''
Created on Mar 9, 2011

@author: richard
'''
import json

class CourserJsonEncoder(json.JSONEncoder):
    '''
    Allows Objects in the Courser package to be encoded in JSON
    '''
    def default(self, obj):
        if hasattr(obj, "to_json"):
            return obj.to_json()
        raise TypeError(repr(obj) + " is not JSON serializable")