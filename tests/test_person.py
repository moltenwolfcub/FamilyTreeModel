import unittest
from utils.idMappings import Ids

from personData.person import Person
from utils.settings import Settings

class personTests(unittest.TestCase):
    """Tests for Person class."""

    def setUp(self) -> None:
        self.person: Person = Person(0, "testy", "mcTest", Ids.FEMALE)
        self.mother: Person = Person(1, "Mother", "mcTest", Ids.FEMALE)
        self.father: Person = Person(2, "Father", "mcTest", Ids.MALE)
        self.sibling: Person = Person(3, "Testa", "mcTest", Ids.MALE)
        self.grandma: Person = Person(6, "GrandTest", "mctest", Ids.FEMALE)
        self.cousin: Person = Person(11, "CousinTest", "mctest", Ids.MALE)

        self.partner: Person = Person(4, "Testo", "testalon", Ids.MALE)
    
    #region personInfo
    def testId(self):
        self.assertEqual(self.person.id, 0)


    def testFullName(self):
        self.assertEqual(self.person.fullName, 'Testy Mctest')

    def testFullNameWithMiddle(self):
        middleNames: list[str] = ["kevin", "bob", "jones"]
        person: Person = Person(16, "john", "smith", Ids.MALE, middleNames)
        self.assertEqual(person.fullName, 'John Kevin Bob Jones Smith')

    def testSimpleName(self):
        self.assertEqual(self.person.simpleName, 'Testy Mctest')

    def testSimpleNameWithMiddle(self):
        middleNames = ["kevin", "bob", "jones"]
        person: Person = Person(16, "john", "smith", Ids.MALE, middleNames)
        self.assertEqual(person.simpleName, 'John Smith')


    def testEmptyMiddleName(self):
        self.assertEqual(self.person.middleNames, [])

    def testEmptyMiddleNameString(self):
        testPerson: Person = Person(16, "john", "smith", Ids.MALE, "kevin")
        self.assertEqual(testPerson.middleNames, ['kevin'])

    def testMiddleName(self):
        testPerson: Person = Person(16, "john", "smith", Ids.MALE, ["kevin", "jones"])
        self.assertEqual(testPerson.middleNames, ['kevin', 'jones'])
    #endregion personInfo
    
    #region mother
    def testMotherHasChild(self):
        self.person.setMother(self.mother)

        self.assertTrue(any(ship.isChild(self.person) for ship in self.mother.children))

    def testMotherWillLoseChildOnReplace(self):
        Settings.allowMoreParents = False
        mother = Person(18, "Mother", "mcTest", Ids.FEMALE, "beta")

        self.person.setMother(self.mother)
        self.person.setMother(mother)

        self.assertFalse(any(ship.isChild(self.person) for ship in self.mother.children))

    def testMotherRemoval(self):
        Settings.allowMoreParents = False
        self.person.setMother(self.mother)
        self.person.setMother(None)

        self.assertFalse(any(ship.isChild(self.person) for ship in self.mother.children))

    def testMotherChanging(self):
        Settings.allowMoreParents = False
        mother = Person(18, "Mother", "mcTest", Ids.FEMALE, "beta")

        self.person.setMother(self.mother)
        self.person.setMother(mother)

        self.assertTrue(any(ship.isChild(self.person) for ship in mother.children))

    def testMotherSettingIncorrectSex(self):
        Settings.ignoreSex = False
        mother: Person = Person(15, "boyMother", "mcTest", Ids.MALE)
        with self.assertRaises(ValueError):
            self.person.setMother(mother)

    def testMoreMothers(self):
        Settings.allowMoreParents = True
        mother = Person(18, "Mother", "mcTest", Ids.FEMALE, "beta")

        self.person.setMother(self.mother)
        self.person.setMother(mother)

        self.assertTrue(any(ship.isParent(self.mother) for ship in self.person.getMothers()))
        self.assertTrue(any(ship.isParent(mother) for ship in self.person.getMothers()))
        self.assertTrue(any(ship.isChild(self.person) for ship in mother.children))
        self.assertTrue(any(ship.isChild(self.person) for ship in self.mother.children))

    def testMotherSelf(self):
        with self.assertRaises(ValueError):
            self.person.setMother(self.person)
    #endregion mother

    #region father
    def testFatherHasChild(self):
        Settings.allowMoreParents = False
        self.person.setFather(self.father)

        self.assertTrue(any(ship.isChild(self.person) for ship in self.father.children))

    def testFatherWillLoseChildOnReplace(self):
        Settings.allowMoreParents = False
        father: Person = Person(18, "Father", "mcTest", Ids.MALE, "beta")
        self.person.setFather(self.father)
        self.person.setFather(father)

        self.assertFalse(any(ship.isChild(self.person) for ship in self.father.children))

    def testFatherRemoval(self):
        Settings.allowMoreParents = False
        self.person.setFather(self.father)
        self.person.setFather(None)

        self.assertFalse(any(ship.isChild(self.person) for ship in self.father.children))

    def testFatherChanging(self):
        Settings.allowMoreParents = False
        father: Person = Person(18, "Father", "mcTest", Ids.MALE, "beta")

        self.person.setFather(self.father)
        self.person.setFather(father)

        self.assertTrue(any(ship.isChild(self.person) for ship in father.children))

    def testFatherSettingIncorrectSex(self):
        Settings.ignoreSex = False
        father: Person = Person(15, "girlFather", "mcTest", Ids.FEMALE)
        with self.assertRaises(ValueError):
            self.person.setFather(father)

    def testMoreFathers(self):
        Settings.allowMoreParents = True
        father: Person = Person(18, "Father", "mcTest", Ids.MALE, "beta")

        self.person.setFather(self.father)
        self.person.setFather(father)

        self.assertTrue(any(ship.isParent(self.father) for ship in self.person.getFathers()))
        self.assertTrue(any(ship.isParent(father) for ship in self.person.getFathers()))
        self.assertTrue(any(ship.isChild(self.person) for ship in father.children))
        self.assertTrue(any(ship.isChild(self.person) for ship in self.father.children))

    def testFatherSelf(self):
        with self.assertRaises(ValueError):
            self.person.setFather(self.person)
    #endregion father

    #region siblings
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
        sibling: Person = Person(32, "OtherSibling", "mctest", Ids.FEMALE)
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

        sibling2: Person = Person(40, "siblingPerson", "mcTest", Ids.MALE, "beta")
        sibling2.setFather(self.father)

        sibling3: Person = Person(42, "siblingPerson", "mcTest", Ids.FEMALE)
        sibling3.setFather(self.father)
        sibling3.setMother(self.mother)


        self.assertTrue(self.sibling in self.person.getAllSiblings())
        self.assertTrue(sibling2 in self.person.getAllSiblings())
        self.assertTrue(sibling3 in self.person.getAllSiblings())

    def testNotOwnAllSiblings(self):
        self.person.setFather(self.father)
        self.person.setMother(self.mother)

        self.assertNotIn(self.person, self.person.getAllSiblings())
    #endregion siblings

    #region partners
    def testPartner(self):
        self.person.setPartner(self.partner)
        self.assertTrue(any(ship.getOtherPerson(self.person) == self.partner for ship in self.person.getPartners()))
        self.assertTrue(any(ship.getOtherPerson(self.partner) == self.person for ship in self.partner.getPartners()))
    
    def testPartnerChange(self):
        Settings.allowPolyShips = False
        partner2: Person = Person(5, "John", "testFace", Ids.MALE)

        self.person.setPartner(self.partner)
        self.person.setPartner(partner2)

        self.assertTrue(any(ship.getOtherPerson(self.person) == partner2 for ship in self.person.getPartners()))
        self.assertEqual(len(self.partner.getPartners()), 0)
        self.assertTrue(any(ship.getOtherPerson(partner2) == self.person for ship in partner2.getPartners()))

    def testPartnerNoneSetter(self):
        self.person.setPartner(self.partner)
        self.person.setPartner(None)

        self.assertTrue(not self.person.getPartners() and not self.partner.getPartners())

    def testPartnerSelf(self):
        with self.assertRaises(ValueError):
            self.person.setPartner(self.person)

    def testPartnerChangeExAddition(self):
        Settings.allowPolyShips = False
        partner2: Person = Person(5, "John", "testFace", Ids.MALE)

        self.person.setPartner(self.partner)
        self.person.setPartner(partner2)

        self.assertTrue(any(ship.contains(self.partner) for ship in self.person.getExPartners()))
        self.assertTrue(any(ship.contains(self.person) for ship in self.partner.getExPartners()))

    def testMultipleExs(self):
        Settings.allowPolyShips = False
        partner2: Person = Person(5, "Partner2", "testFace", Ids.MALE)

        self.person.setPartner(self.partner)
        self.person.setPartner(partner2)
        self.person.setPartner(None)

        self.assertTrue(any(ship.contains(self.partner) for ship in self.person.getExPartners()))
        self.assertTrue(any(ship.contains(partner2) for ship in self.person.getExPartners()))
        self.assertTrue(any(ship.contains(self.person) for ship in self.partner.getExPartners()))
        self.assertTrue(any(ship.contains(self.person) for ship in partner2.getExPartners()))

    def testPartnerRemovalExCreation(self):
        self.person.setPartner(self.partner)
        self.person.setPartner(None)

        self.assertTrue(any(ship.contains(self.partner) for ship in self.person.getExPartners()))
        self.assertTrue(any(ship.contains(self.person) for ship in self.partner.getExPartners()))

    def testExRemoval(self):
        Settings.allowPolyShips = False
        self.person.setPartner(self.partner)
        self.person.setPartner(None)
        self.person.setPartner(self.partner)

        self.assertTrue(any(ship.getOtherPerson(self.person) is not self.partner for ship in self.person.getExPartners()) or len(self.person.getExPartners()) < 1)
        self.assertTrue(any(ship.getOtherPerson(self.partner) is not self.person for ship in self.partner.getExPartners()) or len(self.partner.getExPartners()) < 1)

    def testExAndNewRetainment(self):
        Settings.allowPolyShips = False
        partner2: Person = Person(5, "Partner2", "testFace", Ids.MALE)

        self.person.setPartner(self.partner)
        self.person.setPartner(partner2)

        self.assertTrue(any(ship.contains(self.partner) for ship in self.person.getExPartners()))
        self.assertTrue(any(ship.contains(partner2) for ship in self.person.getPartners()))
        self.assertTrue(any(ship.contains(self.person) for ship in self.partner.getExPartners()))
        self.assertTrue(any(ship.contains(self.person) for ship in partner2.getPartners()))

    def testPolyPartners(self):
        Settings.allowPolyShips = True
        partner2: Person = Person(5, "John", "testFace", Ids.MALE)
        self.person.setPartner(self.partner)
        self.person.setPartner(partner2)
        self.assertTrue(any(ship.getOtherPerson(self.person) == self.partner for ship in self.person.getPartners()))
        self.assertTrue(any(ship.getOtherPerson(self.person) == partner2 for ship in self.person.getPartners()))
        self.assertTrue(any(ship.getOtherPerson(self.partner) == self.person for ship in self.partner.getPartners()))
        self.assertTrue(any(ship.getOtherPerson(partner2) == self.person for ship in partner2.getPartners()))

    def testPolyPartnerNoneSetter(self):
        Settings.allowPolyShips = True
        partner2: Person = Person(5, "John", "testFace", Ids.MALE)
        self.person.setPartner(self.partner)
        self.person.setPartner(partner2)
        self.person.setPartner(None)

        self.assertTrue(not self.person.getPartners() and not self.partner.getPartners() and not partner2.getPartners())
    #endregion partners
    
    #region extendedFamily
    def testOneParentSibling(self):
        self.mother.setMother(self.grandma)
        self.sibling.setMother(self.grandma)

        self.person.setMother(self.mother)

        self.assertTrue(self.sibling in self.person.getParentSiblings())

    def testMultipleParentSibling(self):
        self.mother.setMother(self.grandma)
        self.sibling.setMother(self.grandma)

        sibling2: Person = Person(7, "SiblingBro", "mcTest", Ids.MALE)
        sibling2.setMother(self.grandma)
        sibling3: Person = Person(8, "SiblingSis", "mcTest", Ids.FEMALE)
        sibling3.setMother(self.grandma)

        self.person.setMother(self.mother)

        self.assertIn(self.sibling, self.person.getParentSiblings())
        self.assertIn(sibling2, self.person.getParentSiblings())
        self.assertIn(sibling3, self.person.getParentSiblings())
    
    def testAunts(self):
        self.mother.setMother(self.grandma)
        self.sibling.setMother(self.grandma)

        sibling2: Person = Person(7, "SiblingSis", "mcTest", Ids.FEMALE, "the second")
        sibling2.setMother(self.grandma)
        sibling3: Person = Person(8, "SiblingSis", "mcTest", Ids.FEMALE)
        sibling3.setMother(self.grandma)

        self.person.setMother(self.mother)

        grandad: Person = Person(89, "grandad", "mcTest2", Ids.MALE)
        self.father.setFather(grandad)

        sibling4: Person = Person(9, "SiblingSis", "mcTest", Ids.FEMALE, "the second")
        sibling4.setFather(grandad)
        sibling5: Person = Person(10, "SiblingSis", "mcTest", Ids.FEMALE)
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

        sibling2: Person = Person(7, "SiblingBro", "mcTest", Ids.MALE)
        sibling2.setMother(self.grandma)
        sibling3: Person = Person(8, "SiblingSis", "mcTest", Ids.FEMALE)
        sibling3.setMother(self.grandma)

        self.person.setMother(self.mother)

        grandad: Person = Person(89, "grandad", "mcTest2", Ids.MALE)
        self.father.setFather(grandad)

        sibling4: Person = Person(9, "SiblingSis", "mcTest", Ids.MALE, "the second")
        sibling4.setFather(grandad)
        sibling5: Person = Person(10, "SiblingSis", "mcTest", Ids.MALE)
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
    #endregion extendedFamily

if __name__ == '__main__':
    unittest.main()
