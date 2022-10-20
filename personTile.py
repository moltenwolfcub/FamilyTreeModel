import pygame
from typing import TYPE_CHECKING
from idMappings import Ids

from person import Person
from settings import Settings

if TYPE_CHECKING:
    from treeRenderer import TreeRenderer

class Tile:
    def __init__(self, renderer: 'TreeRenderer', person: Person) -> None:
        """Setup assets and variables for a tile"""
        self.nameFont = pygame.font.SysFont(Settings.fontFamily, Settings.fontSize)
        self.sexFont = pygame.font.SysFont(Settings.fontFamily, Settings.fontSexSize)

        self.renderer: 'TreeRenderer' = renderer
        self.person: Person = person
        self.rect: pygame.Rect = pygame.Rect(0, 0, Settings.tileWidth, Settings.tileHeight)

        self.updateInfo()


    def draw(self):
        """Draw the tile at its current location."""
        self.updateDrawPos()

        #mid
        self.renderer.screen.fill(Settings.tileMidBorderColor, self.rect)

        #light
        drawRect: pygame.Rect = pygame.Rect(
            self.rect.x, self.rect.y,
            self.rect.width- Settings.tileBorderThickness, self.rect.height - Settings.tileBorderThickness
        )
        self.renderer.screen.fill(Settings.tileLightBorderColor, drawRect)

        #dark
        drawRect: pygame.Rect = pygame.Rect(
            self.rect.x+Settings.tileBorderThickness, self.rect.y+Settings.tileBorderThickness,
            self.rect.width- Settings.tileBorderThickness, self.rect.height - Settings.tileBorderThickness
        )
        self.renderer.screen.fill(Settings.tileDarkBorderColor, drawRect)


        #main
        drawRect: pygame.Rect = pygame.Rect(
            self.rect.x+Settings.tileBorderThickness, self.rect.y+Settings.tileBorderThickness,
            self.rect.width- 2*Settings.tileBorderThickness, self.rect.height - 2*Settings.tileBorderThickness
        )
        self.renderer.screen.fill(Settings.tileMainColor, drawRect)

        #name
        self.renderer.screen.blit(self.name_image, self.name_rect)

        #sex
        drawRect: pygame.Rect = pygame.Rect(
            self.rect.x+self.rect.width-Settings.tileBorderThickness-Settings.tileSexBorderOffset-Settings.tileSexSize, 
            self.rect.y+Settings.tileBorderThickness+Settings.tileSexBorderOffset,
            Settings.tileSexSize, Settings.tileSexSize
        )
        self.renderer.screen.fill(self.sexColor, drawRect)

        sexLetterWidth = self.sexLetterImage.get_width()
        sexLetterHeight = self.sexLetterImage.get_height()
        sexTextOffsetX = (Settings.tileSexSize - sexLetterWidth)/2
        sexTextOffsetY = (Settings.tileSexSize - sexLetterHeight)/2
        drawRect.x += sexTextOffsetX
        drawRect.y += sexTextOffsetY
        drawRect.width = sexLetterWidth
        drawRect.height = sexLetterHeight
        self.renderer.screen.blit(self.sexLetterImage, drawRect)


    def updateInfo(self):
        """Update drawable objects based on self.person data"""
        name: str = self.person.fullName
        self.name_image = self.nameFont.render(name, True, Settings.tileFontColor, None)
        self.name_rect = self.name_image.get_rect()

        if self.person.sex is Ids.FEMALE:
            self.sexColor: int = Settings.tileFemaleColor
            sexLetter: str = "F"

        elif self.person.sex is Ids.MALE:
            self.sexColor: int = Settings.tileMaleColor
            sexLetter: str = "M"
        else:
            raise ValueError("This tile's person doesn't have a proper sex")

        self.sexLetterImage = self.sexFont.render(sexLetter, True, Settings.tileFontColor, None)

        self.updateDrawPos()

    def updateDrawPos(self):
        """Update draw location of objects"""
        self.name_rect.topleft = (self.rect.left + Settings.tileBorderThickness*2, self.rect.top + Settings.tileBorderThickness*2)

    def centre(self):
        """Centre the tile"""
        self.rect.center = self.renderer.screen.get_rect().center
