"""
This module contains Patch class.
"""
import os
from copy import deepcopy


class Patch:

    def __init__(self, program):
        self.program = program
        self.edit_list = []

    def __str__(self):
        return ' | '.join(list(map(str, self.edit_list)))

    def __len__(self):
        return len(self.edit_list)

    def __eq__(self, other):
        return self.edit_list == other.edit_list

    def clone(self):
        """
        Create a new patch which has the same sequence of edits with the current one.

        :return: The created Patch
        :rtype: :py:class:`.Patch`
        """
        clone_patch = Patch(self.program)
        clone_patch.edit_list = deepcopy(self.edit_list)
        return clone_patch

    @property
    def diff(self):
        return self.program.diff(self)

    def add(self, edit):
        """
        Add an edit to the edit list
        """
        self.edit_list.append(edit)

    def remove(self, index: int):
        """
        Remove an edit from the edit list
        """
        del self.edit_list[index]
