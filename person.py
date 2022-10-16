import logging
from typing import Union, List

from idMappings import ids

# logger = logging.getLogger(__name__)

class Person:
    """Main class for managing the tree"""
    
    def __init__(self, id: int, firstName: str, lastName: str, sex: 'bool', middleNames: Union[str,List[str]] = []) -> None:
        """Setup Instances of classes and data"""

        self.id = id
        self.firstName = firstName.strip().lower()
        self.lastName = lastName.strip().lower()

        if isinstance(middleNames, str):
            middleNames = [middleNames]
        self.middleNames = middleNames

        self._sex = sex #biological sex stored as an 'isFemale' (True = f, False = m)

        self._mother: 'Person' = None
        self._father: 'Person' = None
        self.children: set[Person] = set()

    def __str__(self) -> str:
        return f"Person <name: {self.fullName}, id: {self.id}>"


    def getDirectSiblings(self) -> set['Person']:
        if self.mother is None or self.father is None:
            return set()
        motherChilderen = self.mother.children
        fatherChilderen = self.father.children

        sharedChilderen = motherChilderen.intersection(fatherChilderen)
        sharedChilderen.remove(self)

        return sharedChilderen

    def getAllSiblings(self) -> set['Person']:
        motherChilderen = set()
        fatherChilderen = set()
        if self.mother is not None:
            motherChilderen = self.mother.children
        if self.father is not None:
            fatherChilderen = self.father.children

        sharedChilderen = motherChilderen.union(fatherChilderen)
        sharedChilderen.remove(self)

        return sharedChilderen

    @property
    def sex(self) -> bool:
        """The bioligical sex of this person"""
        return self._sex

    @property
    def fullName(self) -> str:
        """The person's full name"""
        fullName = f"{self.firstName} "
        for name in self.middleNames:
            fullName += f"{name} "
        fullName += self.lastName
        return fullName.title()

    @property
    def mother(self) -> 'Person':
        """The person's biological mother"""
        return self._mother

    @property
    def father(self) -> 'Person':
        """The person's biological father"""
        return self._father

    @mother.setter
    def mother(self, mother: 'Person', force: 'bool' = False) -> None:
        """Change person's biological mother to the given Person"""
        if mother is None:
            if self._mother is not None:
                self._mother.children.remove(self)
            self._mother = mother
        else:
            if mother.sex is ids.FEMALE or force:
                if self._mother is not None:
                    self._mother.children.remove(self)
                mother.children.add(self)
                self._mother = mother
            else:
                raise ValueError("""The Biological Mother provided isn't female. 
                If you want to set this anyway, run with force set to True.""")

    @father.setter
    def father(self, father: 'Person', force: 'bool' = False) -> None:
        """Change person's biological father to the given Person"""
        if father is None:
            if self._father is not None:
                self._father.children.remove(self)
            self._father = father
        else:
            if father.sex is ids.MALE or force:
                if self._father is not None:
                    self._father.children.remove(self)
                father.children.add(self)
                self._father = father
            else:
                raise ValueError("""The Biological Father provided isn't male. 
                If you want to set this anyway, run with force set to True.""")
