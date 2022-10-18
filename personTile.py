import pygame
from typing import TYPE_CHECKING

from person import Person
from settings import Settings

if TYPE_CHECKING:
    from treeRenderer import TreeRenderer

class Tile:
    def __init__(self, renderer: 'TreeRenderer', person: Person) -> None:
        """Setup assets and variables for a tile"""
        self.renderer: 'TreeRenderer' = renderer

        self.person: Person = person

        self.rect: pygame.Rect = pygame.Rect(0, 0, Settings.tileWidth, Settings.tileHeight)


    def draw(self):
        """Draw the tile at its current location."""

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

    def centre(self):
        """Centre the tile"""
        self.rect.center = self.renderer.screen.get_rect().center
