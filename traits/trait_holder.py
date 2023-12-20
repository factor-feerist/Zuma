import abc
from PyQt6.QtGui import QVector2D


class TraitHolder:
    def __init__(self):
        self.p_values = dict()

    def get_value(self, name):
        if name in self.p_values:
            return self.p_values[name]
        return None

    def set_trait(self, trait):
        name = trait.name
        self.p_values[name] = trait
    pass
