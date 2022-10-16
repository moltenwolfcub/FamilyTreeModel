
from idMappings import ids
from person import Person
from util import flatMap

john = Person(0, "john", "smith", ids.MALE)
daisy = Person(1, "daisy", "smith", ids.FEMALE)
bob = Person(0, "bob", "smith", ids.MALE)
dylan = Person(0, "dylan", "smith", ids.MALE)
anne = Person(0, "anne", "smith", ids.FEMALE)
childeren = [john, bob, dylan, anne]

def addDaisyMother(child: Person):
    child.mother = daisy
childeren = flatMap(childeren, addDaisyMother)

def isFemale(person: Person):
    if person.sex is ids.FEMALE:
        return person
    return None
def isMale(person: Person):
    if person.sex is ids.MALE:
        return person
    return None

for i in flatMap(john.getAllSiblings(), (lambda person: person if person.sex is ids.MALE else None)):
    print(i)
