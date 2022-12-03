import unittest

from utils.idMappings import Ids
from utils.personTileMappings import Mappings
from personData.person import Person
from renderer.personTile import Tile
from renderer.treeRenderer import TreeRenderer


class personTests(unittest.TestCase):
    """Tests for Person class."""

    def setUp(self) -> None:
        self.rendererInstance = TreeRenderer()

        self.mainPerson = Person(0, "main", "mcTest", Ids.MALE)
        self.mainTile = Tile(self.rendererInstance, self.mainPerson)

        self.mother = Person(1, "mother", "mcTest", Ids.FEMALE)
        self.motherTile = Tile(self.rendererInstance, self.mother)
        self.mainPerson.mother = self.mother

    
    def testCorrectPerson(self) -> None:
        self.assertEqual(self.mainTile.person, self.mainPerson)

    def testMappingReturns(self) -> None:
        self.assertEqual(Mappings.person2TileMapping.get(self.mainPerson), self.mainTile)
        self.assertEqual(Mappings.tile2PersonMapping.get(self.mainTile), self.mainPerson)

    def testRelationTileRetevial(self) -> None:
        self.assertEqual(Mappings.person2TileMapping.get(self.mainPerson.mother), self.motherTile)
