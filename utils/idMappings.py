import sys
from typing import TYPE_CHECKING

sys.path.append('../familyTreeModel')

if TYPE_CHECKING:
    from personData.person import Person


class Ids:
    """A class to store Ids of hard-coded data for readability"""
    #person sex
    FEMALE: bool = True
    MALE: bool = False
    def convertSexBool(sex: bool) -> str:
        return "FEMALE" if sex else "MALE"

    def getNextFreePersonId(people: list['Person']) -> int:
        usedIds: set[int] = set()
        for person in people:
            usedIds.add(person.id)

        testID = 0
        while True:
            if (testID not in usedIds):
                break
            testID+=1
        return testID
