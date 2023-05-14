'''
This module defines the Controll class.
'''

# Imports.
import copy
import json
from model_hypgeo import Model_Hypgeo
from view import View

# Classes.
class Controller:
    '''
    Controlls the interaction from the user with the View and Model class.
    '''
    def __init__(self):
        self.model = copy.deepcopy(Model_Hypgeo())  # Model of the system, contains logic aspects.
        self.view = View(self.model, self)          # View of the system, contians visual aspects.

    def on_deck_size(self, value):
        if value == "":
            self.model.set_deck_size(0)
        else:
            self.model.set_deck_size(int(value))

    def on_sample_size(self, value):
        if value == "":
            self.model.set_deck_size(0)
        else:
            self.model.set_sample_size(int(value))

    def on_calculate(self):
        '''
        Calculate the probability of drawing the hand the user set up.
        '''
        self.model.calculate()

    def on_add_group(self):
        '''
        Adds a new group.
        '''
        self.model.add_defined_group()

    def on_del_group(self, key):
        '''
        Deletes a group.
        '''
        self.model.del_defined_group(key)

    def on_group_size(self, key, value):
        '''
        Changes a groups size.
        '''
        if value == "":
            self.model.set_defined_group_size(key, 0)
        else:
            self.model.set_defined_group_size(key, int(value))

    def on_group_min(self, key, value):
        '''
        Changes a groups min in sample.
        '''
        if value == "":
            self.model.set_defined_group_size(key, 0)
        else:
            self.model.set_defined_group_min(key, int(value))

    def on_group_max(self, key, value):
        '''
        Changes a groups max in sample.
        '''
        if value == "":
            self.model.set_defined_group_size(key, 0)
        else:
            self.model.set_defined_group_max(key, int(value))
