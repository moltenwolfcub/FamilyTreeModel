import unittest
from idMappings import ids

from person import Person

class personTests(unittest.TestCase):
    """Tests for Person class."""

    def setUp(self) -> None:
        self.person = Person(0, "testy", "mcTest", ids.FEMALE)
        self.mother = Person(1, "Mother", "mcTest", ids.FEMALE)
        self.father = Person(2, "Father", "mcTest", ids.MALE)
        self.sibling = Person(3, "Testa", "mcTest", ids.MALE)
        self.grandma = Person(6, "GrandTest", "mctest", ids.FEMALE)
        self.cousin = Person(11, "CousinTest", "mctest", ids.MALE)

        self.partner = Person(4, "Testo", "testalon", ids.MALE)
    

    def testId(self):
        self.assertEqual(self.person.id, 0)


    def testFullName(self):
        self.assertEqual(self.person.fullName, 'Testy Mctest')

    def testFullNameWithMiddle(self):
        middleNames = ["kevin", "bob", "jones"]
        person = Person(16, "john", "smith", ids.MALE, middleNames)
        self.assertEqual(person.fullName, 'John Kevin Bob Jones Smith')


    def testEmptyMiddleName(self):
        self.assertEqual(self.person.middleNames, [])

    def testEmptyMiddleNameString(self):
        testPerson = Person(16, "john", "smith", ids.MALE, "kevin")
        self.assertEqual(testPerson.middleNames, ['kevin'])

    def testMiddleName(self):
        testPerson = Person(16, "john", "smith", ids.MALE, ["kevin", "jones"])
        self.assertEqual(testPerson.middleNames, ['kevin', 'jones'])

    
    def testMotherHasChild(self):
        self.person.mother = self.mother

        self.assertTrue(self.person in self.mother.children)

    def testMotherWillLoseChildOnReplace(self):
        self.person.mother = self.mother
        mother = Person(18, "Mother", "mcTest", ids.FEMALE, "beta")
        self.person.mother = mother

        self.assertFalse(self.person in self.mother.children)

    def testMotherRemoval(self):
        self.person.mother = self.mother
        self.person.mother = None

        self.assertFalse(self.person in self.mother.children)

    def testMotherSettingIncorrectSex(self):
        mother = Person(15, "boyMother", "mcTest", ids.MALE)
        with self.assertRaises(ValueError):
            self.person.mother = mother


    def testFatherHasChild(self):
        self.person.father = self.father

        self.assertTrue(self.person in self.father.children)

    def testFatherWillLoseChildOnReplace(self):
        self.person.father = self.father
        father = Person(18, "Father", "mcTest", ids.MALE, "beta")
        self.person.father = father

        self.assertFalse(self.person in self.father.children)

    def testFatherRemoval(self):
        self.person.father = self.father
        self.person.father = None

        self.assertFalse(self.person in self.father.children)

    def testFatherSettingIncorrectSex(self):
        father = Person(15, "girlFather", "mcTest", ids.FEMALE)
        with self.assertRaises(ValueError):
            self.person.father = father
    

    def testOneSiblings(self):
        self.person.father = self.father
        self.person.mother = self.mother
        self.sibling.mother = self.mother
        self.sibling.father = self.father

        self.assertIn(self.sibling, self.person.getDirectSiblings())

    def testMultipleSiblings(self):
        self.person.father = self.father
        self.person.mother = self.mother

        self.sibling.mother = self.mother
        self.sibling.father = self.father
        sibling = Person(32, "OtherSibling", "mctest", ids.FEMALE)
        sibling.mother = self.mother
        sibling.father = self.father

        self.assertTrue(self.sibling in self.person.getDirectSiblings() and sibling in self.person.getDirectSiblings())

    def testNotOwnSiblings(self):
        self.person.father = self.father
        self.person.mother = self.mother

        self.assertNotIn(self.person, self.person.getDirectSiblings())

    def testIncompleteParentsSiblingCheck(self):
        self.person.father = self.father

        self.assertEqual(self.person.getDirectSiblings(), set())

    def testOneHalfSibling(self):
        self.person.father = self.father
        self.person.mother = self.mother
        self.sibling.mother = self.mother

        self.assertIn(self.sibling, self.person.getAllSiblings())

    def testMultipleHalfSiblings(self):
        self.person.father = self.father
        self.person.mother = self.mother

        self.sibling.mother = self.mother

        sibling2 = Person(40, "siblingPerson", "mcTest", ids.MALE, "beta")
        sibling2.father = self.father

        sibling3 = Person(42, "siblingPerson", "mcTest", ids.FEMALE)
        sibling3.father = self.father
        sibling3.mother = self.mother


        self.assertTrue(
            self.sibling in self.person.getAllSiblings() and 
            sibling2 in self.person.getAllSiblings() and
            sibling3 in self.person.getAllSiblings()
            )

    def testNotOwnAllSiblings(self):
        self.person.father = self.father
        self.person.mother = self.mother

        self.assertNotIn(self.person, self.person.getAllSiblings())


    def testPartner(self):
        self.person.partner = self.partner

        self.assertTrue(
            self.person.partner == self.partner and
            self.partner.partner == self.person
        )
    
    def testPartnerChange(self):
        partner2 = Person(5, "John", "testFace", ids.MALE)

        self.person.partner = self.partner
        self.person.partner = partner2

        self.assertTrue(
            self.person.partner == partner2 and
            self.partner.partner == None and
            partner2.partner == self.person
        )

    def testPartnerNoneSetter(self):
        self.person.partner = self.partner
        self.person.partner = None

        self.assertTrue(
            self.person.partner == None and
            self.partner.partner == None
        )

    
    def testOneParentSibling(self):
        self.mother.mother = self.grandma
        self.sibling.mother = self.grandma

        self.person.mother = self.mother

        self.assertTrue(
            self.sibling in self.person.getParentSiblings()
        )

    def testMultipleParentSibling(self):
        self.mother.mother = self.grandma
        self.sibling.mother = self.grandma

        sibling2 = Person(7, "SiblingBro", "mcTest", ids.MALE)
        sibling2.mother = self.grandma
        sibling3 = Person(8, "SiblingSis", "mcTest", ids.FEMALE)
        sibling3.mother = self.grandma

        self.person.mother = self.mother

        self.assertTrue(
            self.sibling in self.person.getParentSiblings() and
            sibling2 in self.person.getParentSiblings() and
            sibling3 in self.person.getParentSiblings()
        )
    
    def testAunts(self):
        self.mother.mother = self.grandma
        self.sibling.mother = self.grandma

        sibling2 = Person(7, "SiblingSis", "mcTest", ids.FEMALE, "the second")
        sibling2.mother = self.grandma
        sibling3 = Person(8, "SiblingSis", "mcTest", ids.FEMALE)
        sibling3.mother = self.grandma

        self.person.mother = self.mother

        grandad = Person(89, "grandad", "mcTest2", ids.MALE)
        self.father.father = grandad

        sibling4 = Person(7, "SiblingSis", "mcTest", ids.FEMALE, "the second")
        sibling4.father = grandad
        sibling5 = Person(8, "SiblingSis", "mcTest", ids.FEMALE)
        sibling5.father = grandad

        self.person.father = self.father

        self.assertTrue(
            self.sibling not in self.person.getAunts() and
            sibling2 in self.person.getAunts() and
            sibling3 in self.person.getAunts() and
            sibling4 in self.person.getAunts() and
            sibling5 in self.person.getAunts()
        )

    def testUncles(self):
        self.mother.mother = self.grandma
        self.sibling.mother = self.grandma

        sibling2 = Person(7, "SiblingBro", "mcTest", ids.MALE)
        sibling2.mother = self.grandma
        sibling3 = Person(8, "SiblingSis", "mcTest", ids.FEMALE)
        sibling3.mother = self.grandma

        self.person.mother = self.mother

        grandad = Person(89, "grandad", "mcTest2", ids.MALE)
        self.father.father = grandad

        sibling4 = Person(7, "SiblingSis", "mcTest", ids.MALE, "the second")
        sibling4.father = grandad
        sibling5 = Person(8, "SiblingSis", "mcTest", ids.MALE)
        sibling5.father = grandad

        self.person.father = self.father

        self.assertTrue(
            self.sibling in self.person.getUncles() and
            sibling2 in self.person.getUncles() and
            sibling3 not in self.person.getUncles() and
            sibling4 in self.person.getUncles() and
            sibling5 in self.person.getUncles()
        )


    def testOneCousins(self):
        self.person.mother = self.mother #make mum
        self.mother.mother = self.grandma #make grandma
        self.sibling.mother = self.grandma #make uncle
        self.cousin.father = self.sibling #make cousin
        self.assertTrue(self.cousin in self.person.getCousins())


if __name__ == '__main__':
    unittest.main()
