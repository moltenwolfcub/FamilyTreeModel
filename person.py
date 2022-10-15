import logging
from typing import Union, List

# logger = logging.getLogger(__name__)

class Person:
    """Main class for managing the tree"""
    
    def __init__(self, id: int, firstName: str, lastName: str, middleNames: Union[str,List[str]] = []) -> None:
        """Setup Instances of classes and data"""

        self.id = id
        self.firstName = firstName.strip().lower()
        self.lastName = lastName.strip().lower()

        if isinstance(middleNames, str):
            middleNames = [middleNames]
        self.middleNames = middleNames

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
    def fullName(self) -> str:
        fullName = f"{self.firstName} "
        for name in self.middleNames:
            fullName += f"{name} "
        fullName += self.lastName
        return fullName.title()

    @property
    def mother(self) -> 'Person':
        return self._mother

    @property
    def father(self) -> 'Person':
        return self._father

    @mother.setter
    def mother(self, mother: 'Person'):
        if self._mother is not None:
            self._mother.children.remove(self)
        self._mother = mother
        if self._mother is not None:
            mother.children.add(self)

    @father.setter
    def father(self, father: 'Person'):
        if self._father is not None:
            self._father.children.remove(self)
        self._father = father
        if self._father is not None:
            father.children.add(self)
