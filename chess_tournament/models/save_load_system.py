from abc import ABC, abstractmethod
from dataclasses import dataclass
import weakref
import json


class Register(object):
    """Keep track of all Register instances."""
    tracked_instances = {}

    def __new__(cls, *args, **kwargs):
        instance = object.__new__(cls)
        cls.tracked_instances.setdefault(instance.__class__.__name__, []).append(weakref.ref(instance))
        return instance

    @classmethod
    def get_instances(cls):
        return cls.tracked_instances


class BackupManager:
    """Save and load system."""
    def __init__(self, path=""):
        self.path = path

    def save(self):
        for class_name, obj_list in Serializable.get_instances().items():
            print(class_name, obj_list)
            with open(class_name + ".json", 'w') as jsonfile:
                json.dump(, jsonfile, default=obj.encoder)
            for object in obj_list:
                print(json.dumps(object.encode(), cls=object.Encoder, sort_keys=True, indent=4)))

    def load(self):
        pass