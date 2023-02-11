import logging, sys
from typing import Union, List, Callable, Optional

sys.path.append('../familyTreeModel')

from personData.relationships import *
from utils.idMappings import Ids
from utils.settings import Settings
from utils.personTileMappings import Mappings

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

		self._partners: set[PartneredRelation] = set()
		self._exPartners: set[ExPartnerRelation] = set()

		self._mothers: set[MotherChildRelation] = set()
		self._fathers: set[FatherChildRelation] = set()
		self.children: set[ParentChildRelation] = set()

		Mappings.addPerson(self)

	def __str__(self) -> str:
		return f"Person <name: {self.fullName}, id: {self.id}, sex: {Ids.convertSexBool(self.sex)}>"


	def _setParent(self, relationType: str, otherPerson: 'Person', newRelationClass: type[Relationship], expectedSex: int = None) -> 'Person':
		if relationType not in ["mother", "father"]:
			raise ValueError("Invalid relation type provided. Please provide either 'mother' or 'father'.")
		
		if otherPerson is self:
			raise ValueError(f"Can't set yourself as your own {relationType}!")
		
		if expectedSex is not None and otherPerson and otherPerson.sex != expectedSex and not Settings.ignoreSex:
			raise ValueError(f"The {relationType} provided isn't {'male' if expectedSex == Ids.MALE else 'female'}. If you want to set this anyway, change ignoreSex to True.")

		relations: set[Relationship] = getattr(self, f"_{relationType}s")

		if not Settings.allowMoreParents or otherPerson is None:
			[remove.removeRelation() for remove in list(relations)]

		if otherPerson is not None:
			relations.add(newRelationClass(self, otherPerson))

		return self

	def setMother(self, mother: 'Person') -> 'Person':
		return self._setParent("mother", mother, MotherChildRelation, Ids.FEMALE)

	def setFather(self, father: 'Person') -> 'Person':
		return self._setParent("father", father, FatherChildRelation, Ids.MALE)

	def setPartner(self, partner: 'Person') -> 'Person':
		if partner is self:
			raise ValueError("""Can't set yourself as your own partner!""")

		exExs = [ex for ex in self._exPartners if ex.getOtherPerson(self) is partner]
		if (len(exExs)>0):
			[remove.removeRelation() for remove in list(self._exPartners)]
		else:
			if (not Settings.allowPolyShips or partner is None):
				[remove.removeRelation() for remove in list(self._partners)]
			if partner is not None:
				self._partners.add(PartneredRelation(self, partner))

		return self


	def getMothers(self) -> set[MotherChildRelation]:
		return self._mothers

	def getFathers(self) -> set[FatherChildRelation]:
		return self._fathers

	def getPartners(self) -> set[ParentChildRelation]:
		return self._partners

	def getExPartners(self) -> set[ExPartnerRelation]:
		return self._exPartners
	
	def getDirectSiblings(self) -> set['Person']:
		if len(self.getMothers()) <1 or len(self.getFathers()) <1:
			return set()

		parents: set['Person'] = set()
		for motherShips in self.getMothers():
			parents.add(motherShips.getParent())
		for fatherShips in self.getFathers():
			parents.add(fatherShips.getParent())

		siblings: list[set['Person']] = list()
		for parent in parents:
			children: set['Person'] = set()
			for childShip in parent.children:
				children.add(childShip.getChild())
			siblings.append(children)
		
		sharedChilderen: set['Person'] = set.intersection(*siblings)
		sharedChilderen.remove(self)

		return sharedChilderen

	def getAllSiblings(self) -> set['Person']:
		parents: set['Person'] = set()
		for motherShips in self.getMothers():
			parents.add(motherShips.getParent())
		for fatherShips in self.getFathers():
			parents.add(fatherShips.getParent())

		siblings: list[set['Person']] = list()
		for parent in parents:
			children: set['Person'] = set()
			for childShip in parent.children:
				children.add(childShip.getChild())
			siblings.append(children)
		
		sharedChilderen: set['Person'] = set.union(*siblings)
		sharedChilderen.remove(self)

		return sharedChilderen
	
	def getParentSiblings(self) -> set['Person']:
		parents: set['Person'] = set()
		for motherShips in self.getMothers():
			parents.add(motherShips.getParent())
		for fatherShips in self.getFathers():
			parents.add(fatherShips.getParent())
		
		allParentSiblings: set['Person'] = set()
		for parent in parents:
			allParentSiblings = allParentSiblings.union(parent.getAllSiblings())

		return allParentSiblings

	def getAunts(self) -> set['Person']:
		return filter(lambda person: person if person.sex is Ids.FEMALE else None, self.getParentSiblings())

	def getUncles(self) -> set['Person']:
		return filter(lambda person: person if person.sex is Ids.MALE else None, self.getParentSiblings())

	def getCousins(self) -> set['Person']:
		cousins: set['Person'] = set()
		for parentSib in self.getParentSiblings():
			for childShip in parentSib.children:
				child: 'Person' = childShip.getChild()
				cousins.add(child)
		
		return cousins

	def getAllPartners(self) -> set[Relationship]:
		exShips: set['ExPartnerRelation'] = self.getExPartners()
		exShips.union(self.getPartners())
		return exShips


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
