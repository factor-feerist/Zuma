import abc
from PyQt6.QtGui import QVector2D


class Trait(abc.ABC):
    @property
    @abc.abstractmethod
    def name(self):
        pass

    @classmethod
    def get_instance(cls, holder):
        return holder.get_value(cls.name)