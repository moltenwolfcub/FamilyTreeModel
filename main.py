
from utils.idMappings import Ids
from personData.person import Person
from utils.util import flatMap

john: Person = Person(0, "john", "smith", Ids.MALE)
daisy: Person = Person(1, "daisy", "smith", Ids.FEMALE)
bob: Person = Person(0, "bob", "smith", Ids.MALE)
dylan: Person = Person(0, "dylan", "smith", Ids.MALE)
anne: Person = Person(0, "anne", "smith", Ids.FEMALE)
children: set[Person] = {john, bob, dylan, anne}

# def addDaisyMother(child: Person):
#     child.mother = daisy
# children = flatMap(children, addDaisyMother)

# def isFemale(person: Person):
#     if person.sex is ids.FEMALE:
#         return person
#     return None
# def isMale(person: Person):
#     if person.sex is ids.MALE:
#         return person
#     return None

# for i in flatMap(john.getAllSiblings(), (lambda person: person if person.sex is ids.MALE else None)):
#     print(i)

john.partner = daisy
john.partner = None

for partner in john.exPartners:
    print(partner)
print("\n")
for partner in daisy.exPartners:
    print(partner)
