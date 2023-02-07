import sys

import pygame

sys.path.append('../familyTreeModel')

from personData.person import Person
from renderer.personTile import Tile
from utils.idMappings import Ids
from utils.personTileMappings import Mappings
from utils.settings import Settings


class TreeRenderer:
    """A class responsible for rendering a family tree"""

    def __init__(self) -> None:
        pygame.init()

        self.screen:pygame.Surface = pygame.display.set_mode((Settings.screenWidth, Settings.screenHeight), pygame.RESIZABLE)
        pygame.display.set_caption("Family Tree")
        self.screenSize: tuple[int, int] = pygame.display.get_window_size()
        self.mouse_pos: tuple[int, int] = pygame.mouse.get_pos()


        self.mouseHasBeenDown: bool = False

        self.initializeTiles()

    def initializeTiles(self) -> None:
        test = Person(Ids.getNextFreePersonId(Mappings.people), "Test", "Something", Ids.FEMALE)
        test2 = Person(Ids.getNextFreePersonId(Mappings.people), "Test2", "Something", Ids.MALE)
        test3 = Person(Ids.getNextFreePersonId(Mappings.people), "Test3", "Something", Ids.FEMALE)
        test4 = Person(Ids.getNextFreePersonId(Mappings.people), "Test4", "Something", Ids.FEMALE)

        test3.setMother(test).setFather(test2)
        test.setPartner(test2)
        test.setPartner(test4)

        for person in Mappings.people:
            Tile(self, person)



    def input(self) -> None:
        for inputEvent in pygame.event.get():
            if inputEvent.type == pygame.QUIT:
                exit()
            elif inputEvent.type == pygame.KEYDOWN:
                self._keydownInput(inputEvent)

        self._mouseInput()

    def _keydownInput(self, keydownEvent: pygame.event) -> None:
        if keydownEvent.key == pygame.K_ESCAPE:
            exit()

    def _mouseInput(self):
        self.mouse_pos: tuple[int, int] = pygame.mouse.get_pos()

        if pygame.mouse.get_pressed()[0]: #mouse left click
            if (self.mouseHasBeenDown): #check that mouse has just been pressed
                return
            self.mouseHasBeenDown: bool = True

            
            for tile in reversed(Mappings.tiles):

                if (tile.rect.collidepoint(self.mouse_pos)):
                    tile.setLockedToMouse(True, self.mouse_pos[0]-tile.rect.x, self.mouse_pos[1]-tile.rect.y) #lock to mouse
                    Mappings.tiles.remove(tile)
                    Mappings.tiles.append(tile) #move to top of being drawn
                    break

        else:
            if (self.mouseHasBeenDown == True): #checks if mouse has just been released
                self.mouseHasBeenDown: bool = False
                for tile in Mappings.tiles:
                    tile.setLockedToMouse(False, 0, 0)


    def update(self) -> None:
        self.screen.fill(Settings.backgroundColor)

        for relation in Mappings.relations:
            relation.drawRelation(self.screen)
        for tile in Mappings.tiles:
            tile.draw()

        self.screenSize = pygame.display.get_window_size()
        pygame.display.update()


    def main(self) -> None:
        while True:
            self.input()
            self.update()

    def exit(self) -> None:
        sys.exit()


if __name__ == '__main__':
    instance = TreeRenderer()
    instance.main()
