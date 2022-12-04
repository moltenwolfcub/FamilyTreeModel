import logging, sys
from typing import Union, List

sys.path.append('../familyTreeModel')

from personData.relationships import *
from utils.idMappings import Ids
from utils.settings import Settings
from utils.personTileMappings import Mappings
from utils.util import flatMap

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

        self.partner: PartneredRelation = None
        self.exPartners: set[ExPartnerRelation] = set()

        self.mother: ParentChildRelation = None
        self.father: ParentChildRelation = None
        self.children: set[ParentChildRelation] = set()

        Mappings.addPerson(self)

    def __str__(self) -> str:
        return f"Person <name: {self.fullName}, id: {self.id}, sex: {Ids.convertSexBool(self.sex)}>"


    def setMother(self, mother: 'Person') -> None:
        if mother is None:
            if self.mother is not None:
                self.mother.removeRelation()
            self.mother = None
        else:
            if mother.sex is Ids.FEMALE or Settings.ignoreSex:
                if self.mother is not None:
                    self.mother.removeRelation()
                self.mother = ParentChildRelation(self, mother)
            else:
                raise ValueError("""The Biological Mother provided isn't female.  
                If you want to set this anyway, chagne ignoreSex to True in settings.""")

    def setFather(self, father: 'Person') -> None:
        if father is None:
            if self.father is not None:
                self.father.removeRelation()
            self.father = None
        else:
            if father.sex is Ids.MALE or Settings.ignoreSex:
                if self.father is not None:
                    self.father.removeRelation()
                self.father = ParentChildRelation(self, father)
            else:
                raise ValueError("""The Biological Father provided isn't male.  
                If you want to set this anyway, chagne ignoreSex to True in settings.""")

    def setPartner(self, partner: 'Person') -> None:
        if partner is None:
            if self.partner is not None:
                self.partner.removeRelation()
            self.partner = None
        else:
            if self.partner is not None:
                self.partner.removeRelation()
            self.partner = PartneredRelation(self, partner)


    def getDirectSiblings(self) -> set['Person']:
        if self.mother is None or self.father is None:
            return set()
        motherChildrenShips: set[ParentChildRelation] = self.mother.getParent().children
        fatherChildrenShips: set[ParentChildRelation] = self.father.getParent().children
        motherChildren: set['Person'] = set()
        fatherChildren: set['Person'] = set()
        for ship in motherChildrenShips:
            motherChildren.add(ship.getChild())
        for ship in fatherChildrenShips:
            fatherChildren.add(ship.getChild())

        sharedChildren: set['Person'] = motherChildren.intersection(fatherChildren)
        sharedChildren.remove(self)

        return sharedChildren

    def getAllSiblings(self) -> set['Person']:
        motherChildren: set['Person'] = set()
        fatherChildren: set['Person'] = set()
        if self.mother is not None:
            motherChildrenShips: set[ParentChildRelation] = self.mother.getParent().children
            for ship in motherChildrenShips:
                motherChildren.add(ship.getChild())

        if self.father is not None:
            fatherChildrenShips: set[ParentChildRelation] = self.father.getParent().children
            for ship in fatherChildrenShips:
                fatherChildren.add(ship.getChild())

        sharedChilderen = motherChildren.union(fatherChildren)
        sharedChilderen.remove(self)

        return sharedChilderen
    
    def getParentSiblings(self) -> set['Person']:
        motherSiblings = set()
        fatherSiblings = set()
        if self.mother is not None:
            motherSiblings = self.mother.getParent().getAllSiblings()
        if self.father is not None:
            fatherSiblings = self.father.getParent().getAllSiblings()

        allParentSiblings = motherSiblings.union(fatherSiblings)
        return allParentSiblings

    def getAunts(self) -> set['Person']:
        return flatMap(self.getParentSiblings(), lambda person: person if person.sex is Ids.FEMALE else None)

    def getUncles(self) -> set['Person']:
        return flatMap(self.getParentSiblings(), lambda person: person if person.sex is Ids.MALE else None)

    def getCousins(self) -> set['Person']:
        cousins = set()
        for parentSib in self.getParentSiblings():
            for childShip in parentSib.children:
                child: 'Person' = childShip.getChild()
                cousins.add(child)
        
        return cousins
    
    def getExPartners(self) -> set['Person']:
        return self.exPartners
    
    def getAllPartners(self) -> set['Person']:
        exs = self.exPartners
        exs.add(self.partner)
        return exs


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
    def simpleName(self) -> str:
        """The person's first and last name formatted"""
        fullName = f"{self.firstName} {self.lastName}"
        return fullName.title()
