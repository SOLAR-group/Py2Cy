import ast
import inspect
from abc import ABC, abstractmethod
import random

import utilities.cython_tree as cy


class TreeEdit(ABC):
    @abstractmethod
    def apply(self, program, new_contents, modification_points):
        """"
        Apply the operator to the contents of program
        :param program: The original program instance
        :type program: :py:class:`.Program`
        :param new_contents: The new contents of program to which the edit will be applied
        :type new_contents: dict(str, list(?))
        :param modification_points: The original modification points
        :type modification_points: list(?)
        :return: success or not
        :rtype: bool
        """
        pass

    @classmethod
    @abstractmethod
    def create(cls):
        """
        :return: The operator instance with randomly-selected properties.
        """
        pass


class TypeInsertion(TreeEdit):
    def __init__(self, target, c_type):
        self.target = target
        self.c_type = c_type

    def apply(self, new_contents, modification_points):
        return cy.insert_type(self.target, new_contents, modification_points, self.c_type)

    @classmethod
    def create(cls, program, target=None, c_type=None):
        types = ['char', 'short', 'int', 'long', 'long long',
                 'float', 'double', 'long double', 'bool']

        target_file = "output/test.pyx"

        if target == None:
            return cls(program.random_target(), random.choice(types))
        else:
            return cls(target, c_type)
