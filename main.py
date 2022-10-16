
from idMappings import ids
from person import Person
from util import flatMap

john = Person(0, "john", "smith", ids.MALE)
daisy = Person(1, "daisy", "smith", ids.FEMALE)
bob = Person(0, "bob", "smith", ids.MALE)
dylan = Person(0, "dylan", "smith", ids.MALE)
anne = Person(0, "anne", "smith", ids.FEMALE)
children = {john, bob, dylan, anne}

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
