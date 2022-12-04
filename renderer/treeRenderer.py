import sys, pygame

sys.path.append('../familyTreeModel')

from utils.idMappings import Ids
from personData.person import Person
from renderer.personTile import Tile

from utils.settings import Settings

class TreeRenderer:
    """A class responsible for rendering a family tree"""

    def __init__(self) -> None:
        pygame.init()

        self.screen:pygame.Surface = pygame.display.set_mode((Settings.screenWidth, Settings.screenHeight), pygame.RESIZABLE)
        pygame.display.set_caption("Family Tree")
        self.screenSize = pygame.display.get_window_size()
        self.mouse_pos = pygame.mouse.get_pos()


        self.mouseHasBeenDown: bool = False

        self.initializeTiles()

    def initializeTiles(self) -> None:
        self.tiles: list[Tile] = []


        self.tmpPerson: Person = Person(0, "Testy", "McTest", Ids.MALE, "Test")
        self.tmpMother: Person = Person(1, "Tesa", "McTest", Ids.FEMALE)
        self.tmpFather: Person = Person(2, "Testo", "McTest", Ids.MALE)

        self.tmpPerson.setFather(self.tmpFather)
        self.tmpPerson.setMother(self.tmpMother)

        self.tmpTile: Tile = Tile(self, self.tmpPerson)
        self.tmpFatherTile: Tile = Tile(self, self.tmpFather)
        self.tmpMotherTile: Tile = Tile(self, self.tmpMother)

        self.tmpTile.centre()
        self.tmpMotherTile.centre()
        self.tmpFatherTile.centre()
        

        self.tiles.append(self.tmpTile)
        self.tiles.append(self.tmpMotherTile)
        self.tiles.append(self.tmpFatherTile)



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
        self.mouse_pos = pygame.mouse.get_pos()

        if pygame.mouse.get_pressed()[0]: #mouse left click
            if (self.mouseHasBeenDown): #check that mouse has just been pressed
                return
            self.mouseHasBeenDown: bool = True

            
            for tile in reversed(self.tiles):

                if (tile.rect.collidepoint(self.mouse_pos)):
                    tile.setLockedToMouse(True, self.mouse_pos[0]-tile.rect.x, self.mouse_pos[1]-tile.rect.y) #lock to mouse
                    self.tiles.remove(tile)
                    self.tiles.append(tile) #move to top of being drawn
                    break

        else:
            if (self.mouseHasBeenDown == True): #checks if mouse has just been released
                self.mouseHasBeenDown: bool = False
                for tile in self.tiles:
                    tile.setLockedToMouse(False, 0, 0)


    def update(self) -> None:
        self.screen.fill(Settings.backgroundColor)

        for tile in self.tiles:
            tile.drawRelations()
        for tile in self.tiles:
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
