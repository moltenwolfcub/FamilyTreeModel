
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from renderer.personTile import Tile
    from personData.person import Person

class Mappings:
    """A class to map tiles and people together"""

    people: list['Person'] = []
    tiles: list['Tile'] = []
    ids: list[int] = []

    _Id2TileMapping: dict[int, 'Tile'] = dict()
    _tile2IdMapping: dict['Tile', int] = dict()
    _Id2PersonMapping: dict[int, 'Person'] = dict()

    def addTile(person: 'Person', tile: 'Tile') -> None:
        Mappings._Id2TileMapping[person.id] = tile
        Mappings._tile2IdMapping[tile] = person.id
        Mappings.tiles.append(tile)

    def addPerson(person: 'Person') -> None:
        Mappings._Id2PersonMapping[person.id] = person
        Mappings.people.append(person)
        Mappings.ids.append(person.id)

    def getPersonIdFromTile(tile: 'Tile') -> int:
        return Mappings._tile2IdMapping.get(tile)

    def getTileFromPersonId(personId: int) -> 'Tile':
        return Mappings._Id2TileMapping.get(personId)


    def getPersonFromId(id: 'int') -> 'Person':
        return Mappings._Id2PersonMapping.get(id)

    def getPersonFromTile(tile: 'Tile') -> 'Person':
        return Mappings._Id2PersonMapping.get(Mappings.getPersonIdFromTile(tile))

    def getTileFromPerson(person: 'Person') -> 'Tile':
        return Mappings._Id2TileMapping.get(person.id)
