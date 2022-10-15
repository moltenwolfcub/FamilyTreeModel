import unittest

from person import Person

class personTests(unittest.TestCase):
    """Tests for Person class."""

    def setUp(self) -> None:
        self.person = Person(14, "testy", "mcTest")
        self.mother = Person(20, "Mother", "mcTest")
        self.father = Person(24, "Father", "mcTest")
        self.sibling = Person(28, "Testa", "mcTest")
    

    def testId(self):
        self.assertEqual(self.person.id, 14)


    def testFullName(self):
        self.assertEqual(self.person.fullName, 'Testy Mctest')

    def testFullNameWithMiddle(self):
        middleNames = ["kevin", "bob", "jones"]
        person = Person(16, "john", "smith", middleNames)
        self.assertEqual(person.fullName, 'John Kevin Bob Jones Smith')


    def testEmptyMiddleName(self):
        self.assertEqual(self.person.middleNames, [])

    def testEmptyMiddleNameString(self):
        testPerson = Person(16, "john", "smith", "kevin")
        self.assertEqual(testPerson.middleNames, ['kevin'])

    def testMiddleName(self):
        testPerson = Person(16, "john", "smith", ["kevin", "jones"])
        self.assertEqual(testPerson.middleNames, ['kevin', 'jones'])

    
    def testMotherHasChild(self):
        self.person.mother = self.mother

        self.assertTrue(self.person in self.mother.children)

    def testMotherWillLoseChildOnReplace(self):
        self.person.mother = self.mother
        mother = Person(18, "Mother", "mcTest", "beta")
        self.person.mother = mother

        self.assertFalse(self.person in self.mother.children)

    def testMotherRemoval(self):
        self.person.mother = self.mother
        self.person.mother = None

        self.assertFalse(self.person in self.mother.children)


    def testFatherHasChild(self):
        self.person.father = self.father

        self.assertTrue(self.person in self.father.children)

    def testFatherWillLoseChildOnReplace(self):
        self.person.father = self.father
        father = Person(18, "Father", "mcTest", "beta")
        self.person.father = father

        self.assertFalse(self.person in self.father.children)

    def testFatherRemoval(self):
        self.person.father = self.father
        self.person.father = None

        self.assertFalse(self.person in self.father.children)

    
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
        sibling = Person(32, "OtherSibling", "mctest")
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

        sibling2 = Person(40, "siblingPerson", "mcTest", "beta")
        sibling2.father = self.father

        sibling3 = Person(42, "siblingPerson", "mcTest")
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

if __name__ == '__main__':
    unittest.main()
