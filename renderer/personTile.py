import pygame, sys
sys.path.append('../familyTreeModel')

from typing import TYPE_CHECKING
from utils.idMappings import Ids

from personData.person import Person
from utils.settings import Settings
from utils.personTileMappings import Mappings

if TYPE_CHECKING:
	from renderer.treeRenderer import TreeRenderer

class Tile:
	def __init__(self, renderer: 'TreeRenderer', person: Person) -> None:
		"""Setup assets and variables for a tile"""
		self.nameFont: pygame.font.Font = pygame.font.SysFont(Settings.fontFamily, Settings.fontNameSize)
		self.smallNameFont: pygame.font.Font = pygame.font.SysFont(Settings.fontFamily, Settings.fontSmallNameSize)
		self.sexFont: pygame.font.Font = pygame.font.SysFont(Settings.fontFamily, Settings.fontSexSize)

		self.renderer: 'TreeRenderer' = renderer
		self.person: Person = person
		self.rect: pygame.Rect = pygame.Rect(0, 0, Settings.tileWidth, Settings.tileHeight)

		self.locked: bool = False
		self.lockedX: int = 0
		self.lockedY: int = 0

		Mappings.addTile(self.person, self)

		self.updateInfo()


	def draw(self):
		"""Draw the tile at its current location."""
		self.updateDrawPos()

		#mid
		pygame.draw.rect(self.renderer.screen, Settings.tileMidBorderColor, self.rect)

		#light
		drawRect: pygame.Rect = pygame.Rect(
			self.rect.x, self.rect.y,
			self.rect.width- Settings.tileBorderThickness, self.rect.height - Settings.tileBorderThickness
		)
		pygame.draw.rect(self.renderer.screen, Settings.tileLightBorderColor, drawRect)

		#dark
		drawRect: pygame.Rect = pygame.Rect(
			self.rect.x+Settings.tileBorderThickness, self.rect.y+Settings.tileBorderThickness,
			self.rect.width- Settings.tileBorderThickness, self.rect.height - Settings.tileBorderThickness
		)
		pygame.draw.rect(self.renderer.screen, Settings.tileDarkBorderColor, drawRect)


		#main
		drawRect: pygame.Rect = pygame.Rect(
			self.rect.x+Settings.tileBorderThickness, self.rect.y+Settings.tileBorderThickness,
			self.rect.width- 2*Settings.tileBorderThickness, self.rect.height - 2*Settings.tileBorderThickness
		)
		pygame.draw.rect(self.renderer.screen, Settings.tileMainColor, drawRect)

		#name
		self.renderer.screen.blit(self.nameImage, self.nameRect)
		self.renderer.screen.blit(self.fullnameImage, self.fullnameRect)

		#id
		self.renderer.screen.blit(self.idImage, self.idRect)

		#sex
		drawRect: pygame.Rect = pygame.Rect(
			self.rect.x+self.rect.width-Settings.tileBorderThickness-Settings.tileSexBorderOffset-Settings.tileSexSize, 
			self.rect.y+Settings.tileBorderThickness+Settings.tileSexBorderOffset,
			Settings.tileSexSize, Settings.tileSexSize
		)
		pygame.draw.rect(self.renderer.screen, self.sexColor, drawRect)

		sexLetterWidth: int = self.sexLetterImage.get_width()
		sexLetterHeight: int = self.sexLetterImage.get_height()
		sexTextOffsetX: float = (Settings.tileSexSize - sexLetterWidth)/2
		sexTextOffsetY: float = (Settings.tileSexSize - sexLetterHeight)/2
		drawRect.x += sexTextOffsetX
		drawRect.y += sexTextOffsetY
		drawRect.width = sexLetterWidth
		drawRect.height = sexLetterHeight
		self.renderer.screen.blit(self.sexLetterImage, drawRect)

	def updateInfo(self):
		"""Update drawable objects based on self.person data"""
		name: str = self.person.simpleName
		self.nameImage: pygame.Surface = self.nameFont.render(name, True, Settings.tileFontColor, None)
		self.nameRect: pygame.Rect = self.nameImage.get_rect()

		fullName: str = self.person.fullName
		self.fullnameImage: pygame.Surface = self.smallNameFont.render(fullName, True, Settings.tileSmallNameFontColor, None)
		self.fullnameRect: pygame.Rect = self.fullnameImage.get_rect()

		id: str = self.person.id
		self.idImage: pygame.Surface = self.smallNameFont.render(str(id), True, Settings.tileSmallNameFontColor, None)
		self.idRect: pygame.Rect = self.idImage.get_rect()

		if self.person.sex is Ids.FEMALE:
			self.sexColor: int = Settings.tileFemaleColor
			sexLetter: str = "F"

		elif self.person.sex is Ids.MALE:
			self.sexColor: int = Settings.tileMaleColor
			sexLetter: str = "M"
		else:
			raise ValueError("This tile's person doesn't have a proper sex")
		self.sexLetterImage: pygame.Surface = self.sexFont.render(sexLetter, True, Settings.tileFontColor, None)

		self.updateDrawPos()

	def updateDrawPos(self):
		"""Update draw location of objects"""
		if (self.locked):
			self.rect.x = self.renderer.mouse_pos[0]-self.lockedX
			self.rect.y = self.renderer.mouse_pos[1]-self.lockedY


		self.nameRect.topleft = (self.rect.left + Settings.tileBorderThickness*2, self.rect.top + Settings.tileBorderThickness*2)
		self.fullnameRect.topleft = (self.rect.left + Settings.tileBorderThickness*2, self.rect.top + Settings.tileBorderThickness*2 + Settings.fontSmallNameSize)
		self.idRect.bottomright = (self.rect.right - Settings.tileBorderThickness-2, self.rect.bottom - Settings.tileBorderThickness)

	def centre(self):
		"""Centre the tile"""
		self.rect.center = self.renderer.screen.get_rect().center

	def setLockedToMouse(self, isLocked: bool, xOffset: int, yOffset: int):
		self.locked: bool = isLocked
		if isLocked:
			self.lockedX: int = xOffset
			self.lockedY: int = yOffset
		else:
			self.lockedX, self.lockedY = 0, 0
