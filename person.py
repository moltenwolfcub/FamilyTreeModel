import logging
from typing import Union, List

from idMappings import ids
from settings import settings
from util import flatMap

# logger = logging.getLogger(__name__)

class Person:
    """Main class for managing a person in the tree"""
    
    def __init__(self, id: int, firstName: str, lastName: str, sex: bool, middleNames: Union[str,List[str]] = []) -> None:
        """Setup Instances of classes and data"""

        self.id = id
        self.firstName = firstName.strip().lower()
        self.lastName = lastName.strip().lower()

        if isinstance(middleNames, str):
            middleNames = [middleNames]
        self.middleNames = middleNames

        self._sex = sex #biological sex stored as an 'isFemale' (True = f, False = m)

        self._partner: 'Person' = None
        self.exPartners: set[Person] = set()

        self._mother: 'Person' = None
        self._father: 'Person' = None
        self.children: set[Person] = set()

    def __str__(self) -> str:
        return f"Person <name: {self.fullName}, id: {self.id}, sex: {self.sex}>"


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
    
    def getParentSiblings(self) -> set['Person']:
        motherSiblings = set()
        fatherSiblings = set()
        if self.mother is not None:
            motherSiblings = self.mother.getAllSiblings()
        if self.father is not None:
            fatherSiblings = self.father.getAllSiblings()

        allParentSiblings = motherSiblings.union(fatherSiblings)
        return allParentSiblings

    def getAunts(self) -> set['Person']:
        return flatMap(self.getParentSiblings(), lambda person: person if person.sex is ids.FEMALE else None)

    def getUncles(self) -> set['Person']:
        return flatMap(self.getParentSiblings(), lambda person: person if person.sex is ids.MALE else None)

    def getCousins(self) -> set['Person']:
        cousins = set()
        for parentSib in self.getParentSiblings():
            for child in parentSib.children:
                cousins.add(child)
        
        return cousins
    
    def getExPartners(self) -> set['Person']:
        pass


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

    @property
    def partner(self) -> 'Person':
        """The person's partner of a relationship"""
        return self._partner

    @mother.setter
    def mother(self, mother: 'Person') -> None:
        """Change person's biological mother to the given Person"""
        if mother is None:
            if self._mother is not None:
                self._mother.children.remove(self)
            self._mother = mother
        else:
            if mother.sex is ids.FEMALE or settings.ignoreSex:
                if self._mother is not None:
                    self._mother.children.remove(self)
                mother.children.add(self)
                self._mother = mother
            else:
                raise ValueError("""The Biological Mother provided isn't female. 
                If you want to set this anyway, chagne ignoreSex to True in settings.""")

    @father.setter
    def father(self, father: 'Person') -> None:
        """Change person's biological father to the given Person"""
        if father is None:
            if self._father is not None:
                self._father.children.remove(self)
            self._father = father
        else:
            if father.sex is ids.MALE or settings.ignoreSex:
                if self._father is not None:
                    self._father.children.remove(self)
                father.children.add(self)
                self._father = father
            else:
                raise ValueError("""The Biological Father provided isn't male. 
                If you want to set this anyway, chagne ignoreSex to True in settings.""")
    
    @partner.setter
    def partner(self, partner: 'Person'):
        if partner is None:
            if self._partner is not None:
                self.exPartners.add(self._partner)
                self._partner.exPartners.add(self)
                self._partner._partner = None
            self._partner = partner
        else:
            if self._partner is not None:
                self._partner.exPartners.add(self)
                self.exPartners.add(self._partner)
                self._partner.partner = None

            self._partner = partner
            partner._partner = self
