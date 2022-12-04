import unittest
from utils.idMappings import Ids

from personData.person import Person
from utils.settings import Settings

class personTests(unittest.TestCase):
    """Tests for Person class."""

    def setUp(self) -> None:
        self.person = Person(0, "testy", "mcTest", Ids.FEMALE)
        self.mother = Person(1, "Mother", "mcTest", Ids.FEMALE)
        self.father = Person(2, "Father", "mcTest", Ids.MALE)
        self.sibling = Person(3, "Testa", "mcTest", Ids.MALE)
        self.grandma = Person(6, "GrandTest", "mctest", Ids.FEMALE)
        self.cousin = Person(11, "CousinTest", "mctest", Ids.MALE)

        self.partner = Person(4, "Testo", "testalon", Ids.MALE)
    

    def testId(self):
        self.assertEqual(self.person.id, 0)


    def testFullName(self):
        self.assertEqual(self.person.fullName, 'Testy Mctest')

    def testFullNameWithMiddle(self):
        middleNames = ["kevin", "bob", "jones"]
        person = Person(16, "john", "smith", Ids.MALE, middleNames)
        self.assertEqual(person.fullName, 'John Kevin Bob Jones Smith')

    def testSimpleName(self):
        self.assertEqual(self.person.simpleName, 'Testy Mctest')

    def testSimpleNameWithMiddle(self):
        middleNames = ["kevin", "bob", "jones"]
        person = Person(16, "john", "smith", Ids.MALE, middleNames)
        self.assertEqual(person.simpleName, 'John Smith')


    def testEmptyMiddleName(self):
        self.assertEqual(self.person.middleNames, [])

    def testEmptyMiddleNameString(self):
        testPerson = Person(16, "john", "smith", Ids.MALE, "kevin")
        self.assertEqual(testPerson.middleNames, ['kevin'])

    def testMiddleName(self):
        testPerson = Person(16, "john", "smith", Ids.MALE, ["kevin", "jones"])
        self.assertEqual(testPerson.middleNames, ['kevin', 'jones'])

    
    def testMotherHasChild(self):
        self.person.setMother(self.mother)
        hasChild = False

        for ship in self.mother.children:
            if (ship.isChild(self.person)):
                hasChild = True

        self.assertTrue(hasChild)

    def testMotherWillLoseChildOnReplace(self):
        self.person.setMother(self.mother)
        mother = Person(18, "Mother", "mcTest", Ids.FEMALE, "beta")
        self.person.setMother(mother)

        hasChild = False

        for ship in self.mother.children:
            if (ship.isChild(self.person)):
                hasChild = True

        self.assertFalse(hasChild)

    def testMotherRemoval(self):
        self.person.setMother(self.mother)
        self.person.setMother(None)

        hasChild = False

        for ship in self.mother.children:
            if (ship.isChild(self.person)):
                hasChild = True

        self.assertFalse(hasChild)

    def testMotherSettingIncorrectSex(self):
        mother = Person(15, "boyMother", "mcTest", Ids.MALE)
        if Settings.ignoreSex:
            self.assertTrue(True)
        else:
            with self.assertRaises(ValueError):
                self.person.setMother(mother)


    def testFatherHasChild(self):
        self.person.setFather(self.father)

        hasChild = False
        for ship in self.father.children:
            if (ship.isChild(self.person)):
                hasChild = True

        self.assertTrue(hasChild)

    def testFatherWillLoseChildOnReplace(self):
        self.person.setFather(self.father)
        father = Person(18, "Father", "mcTest", Ids.MALE, "beta")
        self.person.father = father

        self.assertFalse(self.person in self.father.children)

    def testFatherRemoval(self):
        self.person.setFather(self.father)
        self.person.father = None

        self.assertFalse(self.person in self.father.children)

    def testFatherSettingIncorrectSex(self):
        father = Person(15, "girlFather", "mcTest", Ids.FEMALE)
        if Settings.ignoreSex:
            self.assertTrue(True)
        else:
            with self.assertRaises(ValueError):
                self.person.setFather(father)
    

    def testOneSiblings(self):
        self.person.setFather(self.father)
        self.person.setMother(self.mother)
        self.sibling.setMother(self.mother)
        self.sibling.setFather(self.father)

        self.assertIn(self.sibling, self.person.getDirectSiblings())

    def testMultipleSiblings(self):
        self.person.setFather(self.father)
        self.person.setMother(self.mother)

        self.sibling.setMother(self.mother)
        self.sibling.setFather(self.father)
        sibling = Person(32, "OtherSibling", "mctest", Ids.FEMALE)
        sibling.setMother(self.mother)
        sibling.setFather(self.father)

        self.assertTrue(self.sibling in self.person.getDirectSiblings())
        self.assertTrue(sibling in self.person.getDirectSiblings())

    def testNotOwnSiblings(self):
        self.person.setFather(self.father)
        self.person.setMother(self.mother)

        self.assertNotIn(self.person, self.person.getDirectSiblings())

    def testIncompleteParentsSiblingCheck(self):
        self.person.setFather(self.father)

        self.assertEqual(self.person.getDirectSiblings(), set())

    def testOneHalfSibling(self):
        self.person.setFather(self.father)
        self.person.setMother(self.mother)
        self.sibling.setMother(self.mother)

        self.assertIn(self.sibling, self.person.getAllSiblings())

    def testMultipleHalfSiblings(self):
        self.person.setFather(self.father)
        self.person.setMother(self.mother)

        self.sibling.setMother(self.mother)

        sibling2 = Person(40, "siblingPerson", "mcTest", Ids.MALE, "beta")
        sibling2.setFather(self.father)

        sibling3 = Person(42, "siblingPerson", "mcTest", Ids.FEMALE)
        sibling3.setFather(self.father)
        sibling3.setMother(self.mother)


        self.assertTrue(self.sibling in self.person.getAllSiblings())
        self.assertTrue(sibling2 in self.person.getAllSiblings())
        self.assertTrue(sibling3 in self.person.getAllSiblings())

    def testNotOwnAllSiblings(self):
        self.person.setFather(self.father)
        self.person.setMother(self.mother)

        self.assertNotIn(self.person, self.person.getAllSiblings())


    def testPartner(self):
        self.person.setPartner(self.partner)

        self.assertEqual(self.person.partner.getOtherPerson(self.person), self.partner)
        self.assertEqual(self.partner.partner.getOtherPerson(self.partner), self.person)
    
    def testPartnerChange(self):
        partner2 = Person(5, "John", "testFace", Ids.MALE)

        self.person.setPartner(self.partner)
        self.person.setPartner(partner2)

        self.assertEqual(self.person.partner.getOtherPerson(self.person), partner2)
        self.assertEqual(self.partner.partner, None)
        self.assertEqual(partner2.partner.getOtherPerson(partner2), self.person)

    def testPartnerNoneSetter(self):
        self.person.partner = self.partner
        self.person.partner = None

        self.assertTrue(
            self.person.partner == None and
            self.partner.partner == None
        )

    def testPartnerChangeExAddition(self):
        partner2 = Person(5, "John", "testFace", Ids.MALE)

        self.person.setPartner(self.partner)
        self.person.setPartner(partner2)

        hasEx = False
        for ship in self.person.exPartners:
            if (ship.contains(self.partner)):
                hasEx = True
        self.assertTrue(hasEx)

        hasEx = False
        for ship in self.partner.exPartners:
            if (ship.contains(self.person)):
                hasEx = True
        self.assertTrue(hasEx)

    def testPartnerRemovalExCreation(self):
        self.person.setPartner(self.partner)
        self.person.setPartner(None)

        hasEx = False
        for ship in self.person.exPartners:
            if (ship.contains(self.partner)):
                hasEx = True
        self.assertTrue(hasEx)

        hasEx = False
        for ship in self.partner.exPartners:
            if (ship.contains(self.person)):
                hasEx = True
        self.assertTrue(hasEx)

    
    def testOneParentSibling(self):
        self.mother.setMother(self.grandma)
        self.sibling.setMother(self.grandma)

        self.person.setMother(self.mother)

        self.assertTrue(self.sibling in self.person.getParentSiblings())

    def testMultipleParentSibling(self):
        self.mother.setMother(self.grandma)
        self.sibling.setMother(self.grandma)

        sibling2 = Person(7, "SiblingBro", "mcTest", Ids.MALE)
        sibling2.setMother(self.grandma)
        sibling3 = Person(8, "SiblingSis", "mcTest", Ids.FEMALE)
        sibling3.setMother(self.grandma)

        self.person.setMother(self.mother)

        self.assertIn(self.sibling, self.person.getParentSiblings())
        self.assertIn(sibling2, self.person.getParentSiblings())
        self.assertIn(sibling3, self.person.getParentSiblings())
    
    def testAunts(self):
        self.mother.setMother(self.grandma)
        self.sibling.setMother(self.grandma)

        sibling2 = Person(7, "SiblingSis", "mcTest", Ids.FEMALE, "the second")
        sibling2.setMother(self.grandma)
        sibling3 = Person(8, "SiblingSis", "mcTest", Ids.FEMALE)
        sibling3.setMother(self.grandma)

        self.person.setMother(self.mother)

        grandad = Person(89, "grandad", "mcTest2", Ids.MALE)
        self.father.setFather(grandad)

        sibling4 = Person(9, "SiblingSis", "mcTest", Ids.FEMALE, "the second")
        sibling4.setFather(grandad)
        sibling5 = Person(10, "SiblingSis", "mcTest", Ids.FEMALE)
        sibling5.setFather(grandad)

        self.person.setFather(self.father)

        self.assertNotIn(self.sibling, self.person.getAunts())
        self.assertIn(sibling2, self.person.getParentSiblings())
        self.assertIn(sibling3, self.person.getParentSiblings())
        self.assertIn(sibling4, self.person.getParentSiblings())
        self.assertIn(sibling5, self.person.getParentSiblings())

    def testUncles(self):
        self.mother.setMother(self.grandma)
        self.sibling.setMother(self.grandma)

        sibling2 = Person(7, "SiblingBro", "mcTest", Ids.MALE)
        sibling2.setMother(self.grandma)
        sibling3 = Person(8, "SiblingSis", "mcTest", Ids.FEMALE)
        sibling3.setMother(self.grandma)

        self.person.setMother(self.mother)

        grandad = Person(89, "grandad", "mcTest2", Ids.MALE)
        self.father.setFather(grandad)

        sibling4 = Person(9, "SiblingSis", "mcTest", Ids.MALE, "the second")
        sibling4.setFather(grandad)
        sibling5 = Person(10, "SiblingSis", "mcTest", Ids.MALE)
        sibling5.setFather(grandad)

        self.person.setFather(self.father)

        self.assertTrue(
            self.sibling in self.person.getUncles() and
            sibling2 in self.person.getUncles() and
            sibling3 not in self.person.getUncles() and
            sibling4 in self.person.getUncles() and
            sibling5 in self.person.getUncles()
        )


    def testOneCousins(self):
        self.person.setMother(self.mother)
        self.mother.setMother(self.grandma)
        self.sibling.setMother(self.grandma)
        self.cousin.setFather(self.sibling)
        self.assertIn(self.cousin, self.person.getCousins())


if __name__ == '__main__':
    unittest.main()
