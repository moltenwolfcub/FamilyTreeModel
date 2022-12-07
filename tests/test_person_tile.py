import unittest

from utils.idMappings import Ids
from utils.personTileMappings import Mappings
from personData.person import Person
from renderer.personTile import Tile
from renderer.treeRenderer import TreeRenderer


class personTests(unittest.TestCase):
    """Tests for Person class."""

    def setUp(self) -> None:
        self.rendererInstance: TreeRenderer = TreeRenderer()

        self.mainPerson: Person = Person(0, "main", "mcTest", Ids.MALE)
        self.mainTile = Tile(self.rendererInstance, self.mainPerson)

        self.mother: Person = Person(1, "mother", "mcTest", Ids.FEMALE)
        self.motherTile = Tile(self.rendererInstance, self.mother)
        self.mainPerson.mother = self.mother

    
    def testCorrectPerson(self) -> None:
        self.assertEqual(self.mainTile.person, self.mainPerson)


    def testTileRetrievalFromId(self) -> None:
        self.assertEqual(Mappings.getTileFromPersonId(self.mainPerson.id), self.mainTile)

    def testPersonIdRetrievalFromTile(self) -> None:
        self.assertEqual(Mappings.getPersonIdFromTile(self.mainTile), self.mainPerson.id)

    def testPersonRetrievalFromTile(self) -> None:
        self.assertEqual(Mappings.getPersonFromTile(self.mainTile), self.mainPerson)

    def testTileRetrievalFromPerson(self) -> None:
        self.assertEqual(Mappings.getTileFromPerson(self.mainPerson), self.mainTile)


    def testRelationTileRetevial(self) -> None:
        self.assertEqual(Mappings.getTileFromPersonId(self.mainPerson.mother.id), self.motherTile)
