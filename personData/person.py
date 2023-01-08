import logging, sys
from typing import Union, List, Callable, Optional

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

        self.id: int = id
        self.firstName: str = firstName.strip().lower()
        self.lastName: str = lastName.strip().lower()

        if isinstance(middleNames, str):
            middleNames = [middleNames]
        self.middleNames: list[str] = middleNames

        self._sex = sex #biological sex stored as an 'isFemale' (True = f, False = m)

        self.partner: PartneredRelation = None
        self.exPartners: set[ExPartnerRelation] = set()

        self.mother: MotherChildRelation = None
        self.father: FatherChildRelation = None
        self.children: set[ParentChildRelation] = set()

        Mappings.addPerson(self)

    def __str__(self) -> str:
        return f"Person <name: {self.fullName}, id: {self.id}, sex: {Ids.convertSexBool(self.sex)}>"


    def setMother(self, mother: 'Person') -> 'Person':
        self.mother = self.setShip(mother, self.mother, lambda m: MotherChildRelation(self, m), 
            None, lambda sex: sex == Ids.FEMALE)
        return self

    def setFather(self, father: 'Person') -> 'Person':
        self.father = self.setShip(father, self.father, lambda p: FatherChildRelation(self, p), 
            None, lambda sex: sex == Ids.MALE)
        return self

    def setPartner(self, partner: 'Person') -> 'Person':
        self.partner = self.setShip(partner, self.partner, lambda p: PartneredRelation(self, p), 
            partner.partner if partner is not None else None, lambda _: True)
        return self

    def setShip(
        self,
        newPerson: 'Person',
        currentShip: 'Relationship',
        createNewShip: Callable[['Person'], 'Relationship'],
        newPersonsOldShip: 'Relationship',
        sexIsApplicable: Callable[[bool], bool],
        ignoreSex: Optional[bool] = Settings.ignoreSex,
    ) -> Relationship:
        if newPerson is None:
            if currentShip is not None:
                currentShip.removeRelation()
            currentShip = None
        else:
            if sexIsApplicable(newPerson.sex) or ignoreSex:
                if currentShip is not None:
                    currentShip.removeRelation()
                if newPersonsOldShip is not None:
                    newPersonsOldShip.removeRelation()
                currentShip = createNewShip(newPerson)
            else:
                raise ValueError("""The Person provided isn't the correct sex.  
                If you want to set this anyway, chagne ignoreSex to True.""")
        return currentShip


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
        motherSiblings: set['Person'] = set()
        fatherSiblings: set['Person'] = set()
        if self.mother is not None:
            motherSiblings = self.mother.getParent().getAllSiblings()
        if self.father is not None:
            fatherSiblings = self.father.getParent().getAllSiblings()

        allParentSiblings: set['Person'] = motherSiblings.union(fatherSiblings)
        return allParentSiblings

    def getAunts(self) -> set['Person']:
        return flatMap(self.getParentSiblings(), lambda person: person if person.sex is Ids.FEMALE else None)

    def getUncles(self) -> set['Person']:
        return flatMap(self.getParentSiblings(), lambda person: person if person.sex is Ids.MALE else None)

    def getCousins(self) -> set['Person']:
        cousins: set['Person'] = set()
        for parentSib in self.getParentSiblings():
            for childShip in parentSib.children:
                child: 'Person' = childShip.getChild()
                cousins.add(child)
        
        return cousins
    
    def getExPartners(self) -> set['Person']:
        return self.exPartners
    
    def getAllPartners(self) -> set['Person']:
        exShips: set['ExPartnerRelation'] = self.exPartners
        exs: set['Person'] = set()
        for ship in exShips:
            exShips.add(ship.getOtherPerson(self))
        exs.add(self.partner)
        return exs


    @property
    def sex(self) -> bool:
        """The bioligical sex of this person"""
        return self._sex

    @property
    def fullName(self) -> str:
        """The person's full name"""
        fullName: str = f"{self.firstName} "
        for name in self.middleNames:
            fullName += f"{name} "
        fullName += self.lastName
        return fullName.title()

    @property
    def simpleName(self) -> str:
        """The person's first and last name formatted"""
        fullName: str = f"{self.firstName} {self.lastName}"
        return fullName.title()
