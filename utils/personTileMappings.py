
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from personData.person import Person
    from renderer.personTile import Tile

class Mappings:
    """A class to map tiles and people together"""

    person2TileMapping: dict = dict()
    tile2PersonMapping: dict = dict()

    def addTile(person: 'Person', tile: 'Tile'):
        Mappings.person2TileMapping[person] = tile
        Mappings.tile2PersonMapping[tile] = person
