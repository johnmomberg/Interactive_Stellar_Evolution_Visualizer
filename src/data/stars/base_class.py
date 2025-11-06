from dataclasses import dataclass 





# Base class that gives ParentStage, SubStage, and Model classes a __str__ and __repr__ function (so they print their ID's)
@dataclass
class BaseEntity:
    def __str__(self):
        return getattr(self, 'id', f"{self.__class__.__name__}()")

    def __repr__(self):
        return self.__str__()



