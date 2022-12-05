import pygame, sys
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

sys.path.append('../familyTreeModel')
if TYPE_CHECKING:
	from personData.person import Person

from utils.personTileMappings import Mappings
from utils.settings import Settings


class Relationship(ABC):
	def __init__(self, person1Id: int, person2Id: int) -> None:
		Mappings.addRelation(self)
		self.person1: int = person1Id
		self.person2: int = person2Id

	def __str__(self) -> str:
		return f"A relationship between {Mappings.getPersonFromId(self.person1)} and {Mappings.getPersonFromId(self.person2)}."

	def removeRelation(self) -> None:
		self.onRemove()

	@abstractmethod
	def onRemove(self) -> None:
		pass

	def getOtherPerson(self, person: 'Person') -> 'Person':
		if (self.person1 == person.id):
			return Mappings.getPersonFromId(self.person2)
		elif (self.person2 == person.id):
			return Mappings.getPersonFromId(self.person1)
		else:
			raise ValueError("""The person parsed isn't in the relationship so the 'other' person 
				cannot be obtained.""")

	def contains(self, person: 'Person') -> bool:
		return person.id == self.person1 or person.id == self.person2

	def getRelationColor(self) -> tuple[int, int, int]:
		if (self.getDefaultColor() is None):
			return Settings.defaultRelationColor
		else:
			return self.getDefaultColor()

	@abstractmethod
	def getDefaultColor(self) -> tuple[int, int, int]:
		pass

	def drawRelation(self, screen: pygame.Surface) -> None:
		pygame.draw.line(screen, self.getRelationColor(), Mappings.getTileFromPersonId(self.person1).rect.center, 
			Mappings.getTileFromPersonId(self.person2).rect.center, Settings.relationLineThickness)

class ParentChildRelation(Relationship):

	def __init__(self, child: 'Person', parent: 'Person') -> None:
		super().__init__(child.id, parent.id)
		parent.children.add(self)

	def onRemove(self) -> None:
		Mappings.getPersonFromId(self.person2).children.remove(self)

	def isChild(self, child: 'Person') -> bool:
		return self.person1 == child.id

	def isMother(self, parent: 'Person') -> bool:
		return self.person2 == parent.id

	def getParent(self) -> 'Person':
		return Mappings.getPersonFromId(self.person2)

	def getChild(self) -> 'Person':
		return Mappings.getPersonFromId(self.person1)

	def getDefaultColor(self) -> tuple[int, int, int]:
		return super().getDefaultColor()

class MotherChildRelation(ParentChildRelation):
	def __init__(self, child: 'Person', mother: 'Person') -> None:
		super().__init__(child, mother)

	def getDefaultColor(self) -> tuple[int, int, int]:
		return Settings.motherRelationColor

class FatherChildRelation(ParentChildRelation):
	def __init__(self, child: 'Person', father: 'Person') -> None:
		super().__init__(child, father)

	def getDefaultColor(self) -> tuple[int, int, int]:
		return Settings.fatherRelationColor

class PartneredRelation(Relationship):

	def __init__(self, caller: 'Person', other: 'Person') -> None:
		super().__init__(caller.id, other.id)
		other.partner = self

	def onRemove(self) -> None:
		Mappings.getPersonFromId(self.person2).partner = None
		Mappings.getPersonFromId(self.person1).partner = None

		exShip = ExPartnerRelation(Mappings.getPersonFromId(self.person1), Mappings.getPersonFromId(self.person2))
		Mappings.getPersonFromId(self.person1).exPartners.add(exShip)
		Mappings.getPersonFromId(self.person2).exPartners.add(exShip)

	def isAPartner(self, partner: 'Person') -> bool:
		return partner == self.person1 or partner == self.person2

	def getDefaultColor(self) -> tuple[int, int, int]:
		return Settings.partnerRelationColor

class ExPartnerRelation(Relationship):

	def __init__(self, caller: 'Person', other: 'Person') -> None:
		super().__init__(caller.id, other.id)
		# other.partner = self

	def onRemove(self) -> None:
		raise ValueError("""Shouldn't be removing an ex from a person. If they were together once, then they are
			now ex together.""")

	def getDefaultColor(self) -> tuple[int, int, int]:
		return Settings.exPartnerRelationColor
