import pygame, sys
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from enum import Enum

sys.path.append('../familyTreeModel')
if TYPE_CHECKING:
	from personData.person import Person

from utils.personTileMappings import Mappings
from utils.settings import Settings


class LineDrawType(Enum):
	STRAIGHT = 0
	VERTICAL = 1
	HORIZONTAL = 2

class Relationship(ABC):
	def __init__(self, person1Id: int, person2Id: int, lineType: LineDrawType = LineDrawType.STRAIGHT) -> None:
		Mappings.addRelation(self)
		self.person1: int = person1Id
		self.person2: int = person2Id

		self.lineType: LineDrawType = lineType

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
		person1Rect: pygame.Rect = Mappings.getTileFromPersonId(self.person1).rect
		person2Rect: pygame.Rect = Mappings.getTileFromPersonId(self.person2).rect

		match self.lineType:
			case LineDrawType.VERTICAL:
				higher, lower = (person1Rect, person2Rect) if person1Rect.y < person2Rect.y else (person2Rect, person1Rect)

				heightDiff = lower.top - higher.bottom

				pygame.draw.line(screen, self.getRelationColor(), (higher.centerx, higher.bottom), (higher.centerx, higher.bottom+heightDiff//2), Settings.relationLineThickness)
				pygame.draw.line(screen, self.getRelationColor(), (higher.centerx, higher.bottom+heightDiff//2), (lower.centerx, higher.bottom+heightDiff//2), Settings.relationLineThickness)
				pygame.draw.line(screen, self.getRelationColor(), (lower.centerx, higher.bottom+heightDiff//2), (lower.centerx, lower.top), Settings.relationLineThickness)

			case LineDrawType.HORIZONTAL:
				left, right = (person1Rect, person2Rect) if person1Rect.x < person2Rect.x else (person2Rect, person1Rect)

				widthDiff = right.left - left.right

				pygame.draw.line(screen, self.getRelationColor(), (left.right, left.centery), (left.right+widthDiff//2, left.centery), Settings.relationLineThickness)
				pygame.draw.line(screen, self.getRelationColor(), (left.right+widthDiff//2, left.centery), (left.right+widthDiff//2, right.centery), Settings.relationLineThickness)
				pygame.draw.line(screen, self.getRelationColor(), (left.right+widthDiff//2, right.centery), (right.left, right.centery), Settings.relationLineThickness)
			
			case LineDrawType.STRAIGHT:
				pygame.draw.line(screen, self.getRelationColor(), person1Rect.center, person2Rect.center, Settings.relationLineThickness)
				

class ParentChildRelation(Relationship):

	def __init__(self, child: 'Person', parent: 'Person') -> None:
		super().__init__(child.id, parent.id, LineDrawType.VERTICAL)
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
		super().__init__(caller.id, other.id, LineDrawType.HORIZONTAL)
		other.partners.add(self)

	def onRemove(self) -> None:
		Mappings.getPersonFromId(self.person2).partners.remove(self)
		Mappings.getPersonFromId(self.person1).partners.remove(self)

		exShip = ExPartnerRelation(Mappings.getPersonFromId(self.person1), Mappings.getPersonFromId(self.person2))
		Mappings.getPersonFromId(self.person1).exPartners.add(exShip)
		Mappings.getPersonFromId(self.person2).exPartners.add(exShip)

	def isAPartner(self, partner: 'Person') -> bool:
		return partner == self.person1 or partner == self.person2

	def getDefaultColor(self) -> tuple[int, int, int]:
		return Settings.partnerRelationColor

class ExPartnerRelation(Relationship):

	def __init__(self, caller: 'Person', other: 'Person') -> None:
		super().__init__(caller.id, other.id, LineDrawType.HORIZONTAL)

	def onRemove(self) -> None:
		# assuming that if they are no longer an ex then they got back together
		Mappings.getPersonFromId(self.person2).exPartners.remove(self)
		Mappings.getPersonFromId(self.person1).exPartners.remove(self)

		newShip = PartneredRelation(Mappings.getPersonFromId(self.person1), Mappings.getPersonFromId(self.person2))
		Mappings.getPersonFromId(self.person1).partners.add(newShip)
		Mappings.getPersonFromId(self.person2).partners.add(newShip)

	def getDefaultColor(self) -> tuple[int, int, int]:
		return Settings.exPartnerRelationColor
