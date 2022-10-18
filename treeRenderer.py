import sys, pygame
from idMappings import Ids
from person import Person
from personTile import Tile

from settings import Settings

class TreeRenderer:
    """A class responsible for rendering a family tree"""

    def __init__(self) -> None:
        pygame.init()

        self.screen:pygame.Surface = pygame.display.set_mode((Settings.screenWidth, Settings.screenHeight), pygame.RESIZABLE)
        pygame.display.set_caption("Family Tree")
        self.screenSize = pygame.display.get_window_size()

        self.tmpPerson: Person = Person(0, "Temp", "McTemporary", Ids.MALE)
        self.tmpTile: 'Tile' = Tile(self, self.tmpPerson)
        self.tmpTile.centre()

        self.mouse_pos = pygame.mouse.get_pos()


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
        if pygame.mouse.get_pressed()[0]:
            self.tmpTile.rect.center = self.mouse_pos



    def update(self) -> None:
        self.screen.fill(Settings.backgroundColor)
        self.tmpTile.draw()

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
